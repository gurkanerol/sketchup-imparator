"""SketchUp (.skp) import backend built on the bundled OpenSKP parser.

This module converts a parsed SketchUp model into Blender data.  It needs no
proprietary SketchUp SDK: ``openskp`` is a clean-room reader, imported from
``_vendor/`` as part of this package (never through ``sys.path``).  Its
third-party needs are met outside the vendor: ``defusedxml`` and
``mapbox_earcut`` as extension wheels, ``shapely`` by
:mod:`shapely_fallback`.

Design notes
------------
* Components are imported once per *definition* and placed with per-node
  object matrices.  Object transforms therefore keep SketchUp's own component
  origins, rotation and scale instead of being baked into world-space
  vertices.
* Face UVs arrive already baked from SketchUp's per-face ``uv_transform`` and
  the material's tile size, so no Mapping-node scaling is applied.  One tile
  equals one image repetition, exactly as in SketchUp.
* One SketchUp tag (layer) becomes one Blender collection, with the tag's
  hidden state carried over.
"""

from __future__ import annotations

import os
import tempfile

import bpy
import numpy as np
from mathutils import Matrix, Vector

from ._vendor.openskp import SkpFile
from ._vendor.openskp.instanced_scene import build_instanced_scene
from .shapely_fallback import install as _install_shapely_fallback

_install_shapely_fallback()

INCH_TO_METER = 0.0254
DEFAULT_MATERIAL = "DefaultMaterial"

# glTF is Y-up/metres, Blender is Z-up/metres: (x, y, z) -> (x, -z, y).
YUP_TO_ZUP = Matrix(((1.0, 0.0, 0.0, 0.0),
                     (0.0, 0.0, -1.0, 0.0),
                     (0.0, 1.0, 0.0, 0.0),
                     (0.0, 0.0, 0.0, 1.0)))
YUP_TO_ZUP_INV = YUP_TO_ZUP.inverted()


def _log(*args):
    print("SketchUp Imparator |", *args)


def _texture_key(texture):
    """Stable identity for a texture's bytes (same rule OpenSKP dedupes by)."""
    if texture is None or getattr(texture, "data", None) is None:
        return None
    data = texture.data
    return (len(data), data[:16])


def _axis_swap(points):
    """(N, 3) glTF Y-up metres -> Blender Z-up metres."""
    out = np.empty_like(points)
    out[:, 0] = points[:, 0]
    out[:, 1] = -points[:, 2]
    out[:, 2] = points[:, 1]
    return out


def _matrix_from_gltf(values):
    """16 column-major glTF floats -> Blender Matrix (Y-up -> Z-up)."""
    m = Matrix(((values[0], values[4], values[8], values[12]),
                (values[1], values[5], values[9], values[13]),
                (values[2], values[6], values[10], values[14]),
                (values[3], values[7], values[11], values[15])))
    return YUP_TO_ZUP @ m @ YUP_TO_ZUP_INV


def _as_numpy(array, dtype):
    return np.frombuffer(array, dtype=dtype) if len(array) else np.empty(0, dtype=dtype)


def _set_input(node, names, value):
    """Set the first existing socket from *names* (input names move between
    Blender versions)."""
    if isinstance(names, str):
        names = (names,)
    for name in names:
        socket = node.inputs.get(name)
        if socket is not None:
            socket.default_value = value
            return True
    return False


def _srgb_to_linear(value):
    return pow(max(value, 0.0), 2.2)


class SkpSceneImporter:
    """Builds Blender objects, meshes, curves and materials from a .skp file."""

    def __init__(self, owner, context, options):
        self.owner = owner
        self.context = context
        self.filepath = owner.filepath
        self.prefix = owner.filename_prefix
        self.options = options

        # On reload, rebuild materials/images so source changes (textures,
        # colors) are picked up.
        self.reuse_material = options.get("reuse_material", True) and not options.get("is_update", False)
        self.smart_pbr = options.get("smart_pbr", True)
        self.import_edges = options.get("import_standalone_edges", True)
        self.import_cameras = options.get("import_scene", True)
        self.scene_filter = (options.get("import_scene_filter") or "").strip()

        self.model = None
        self.scene = None
        self.root_coll = None
        self.layer_colls = {}
        self._edges_coll = None
        self.materials = {}
        self.materials_by_gltf = {}
        self.materials_by_index = []
        self.images = {}
        self.mesh_data = {}
        self.curve_data = {}
        self._progress = 0
        self._progress_max = 100
        self._wm = getattr(context, "window_manager", None)

        # Material naming lookup: exact (colour, alpha, texture) -> name, then
        # colour-only fallback for SketchUp materials whose image is missing.
        self._names_exact = {}
        self._names_color = {}
        self._colorized_exact = {}
        # (rgb, texture) -> [(name, opacity, colorized)] for recovering info
        # when OpenSKP's glTF loses names/alpha (e.g. transparent glass).
        self._names_rgbtex = {}

    # ── progress ──────────────────────────────────────────────────────────
    def _begin_progress(self, maximum):
        self._progress = 0
        self._progress_max = max(int(maximum), 1)
        if self._wm is not None:
            try:
                self._wm.progress_begin(0, self._progress_max)
            except Exception:
                self._wm = None

    def _step(self, percent):
        """Report an absolute progress percentage."""
        self._progress = percent
        if self._wm is not None:
            try:
                self._wm.progress_update(min(int(percent), self._progress_max))
            except Exception:
                self._wm = None

    def _end_progress(self):
        if self._wm is not None:
            try:
                self._wm.progress_end()
            except Exception:
                pass

    # ── pipeline ──────────────────────────────────────────────────────────
    def run(self):
        self._begin_progress(100)
        try:
            self._parse()
            self._step(35)
            self._init_collections()
            self._build_material_names()
            self._build_materials()
            self._step(45)
            self._build_mesh_resources()
            self._build_curve_resources()
            self._step(70)
            self._build_objects()
            self._step(92)
            self._build_cameras()
            self._apply_layer_visibility()
            self._step(100)
        finally:
            self._end_progress()

    def _parse(self):
        skp = SkpFile.open(self.filepath)
        self.model = skp.parse()
        parsed = getattr(skp, "_parsed", None)
        if parsed is not None:
            self.scene = build_instanced_scene(parsed)
        else:  # pragma: no cover - OpenSKP caches the parse, but be safe
            self.scene = skp.build_instanced_scene()
        self.owner.skp_model = self.model
        _log(f"Parsed {len(self.model.definitions)} definitions, "
             f"{len(self.model.materials)} materials, "
             f"{len(self.model.layers)} tags")

    # ── collections ───────────────────────────────────────────────────────
    def _init_collections(self):
        base = os.path.basename(self.filepath)
        root_name = f"SKP: {base}"
        root = bpy.data.collections.get(root_name) or bpy.data.collections.new(root_name)
        if root.name not in bpy.context.scene.collection.children:
            bpy.context.scene.collection.children.link(root)
        root["skp_filepath"] = self.filepath
        root["skp_version"] = self.owner.version_string
        root["skp_import_edges"] = bool(self.import_edges)
        try:
            root["skp_mtime"] = os.path.getmtime(self.filepath)
        except OSError:
            root["skp_mtime"] = 0.0
        self.root_coll = root

        if self.options.get("is_update"):
            for ob in list(root.all_objects):
                data = ob.data
                bpy.data.objects.remove(ob, do_unlink=True)
                if data is not None and getattr(data, "users", 1) == 0:
                    if isinstance(data, bpy.types.Mesh):
                        bpy.data.meshes.remove(data)
                    elif isinstance(data, bpy.types.Curve):
                        bpy.data.curves.remove(data)

    def _layer_collection(self, layer_name):
        name = layer_name or "Untagged"
        coll = self.layer_colls.get(name)
        if coll is not None:
            return coll
        coll_name = f"{self.prefix}{name}"
        coll = bpy.data.collections.get(coll_name) or bpy.data.collections.new(coll_name)
        if coll.name not in self.root_coll.children:
            self.root_coll.children.link(coll)
        coll["skp_layer"] = name
        self.layer_colls[name] = coll
        return coll

    def _edges_collection(self):
        if self._edges_coll is not None:
            return self._edges_coll
        coll_name = f"{self.prefix}Edges"
        coll = bpy.data.collections.get(coll_name) or bpy.data.collections.new(coll_name)
        if coll.name not in self.root_coll.children:
            self.root_coll.children.link(coll)
        coll["skp_edges"] = True
        self._edges_coll = coll
        return coll

    def _apply_layer_visibility(self):
        hidden = self.scene.layer_hidden or {}
        for name, coll in self.layer_colls.items():
            coll.hide_viewport = bool(hidden.get(name, False))
            coll.hide_render = bool(hidden.get(name, False))

    # ── materials ─────────────────────────────────────────────────────────
    def _build_material_names(self):
        for mat in self.model.materials:
            name = (mat.name or "").strip()
            if not name:
                continue
            rgb = tuple(round(c) for c in mat.color[:3])
            alpha = round(float(mat.transparency), 4)
            texture = _texture_key(mat.texture)
            key = (rgb, alpha, texture)
            self._names_exact.setdefault(key, name)
            self._colorized_exact.setdefault(key, bool(mat.colorized))
            # Colour alone only identifies a material when it has no image:
            # two textured materials can share a colour and still be distinct.
            if texture is None:
                self._names_color.setdefault((rgb, alpha), name)
            rt_key = (rgb, texture)
            self._names_rgbtex.setdefault(rt_key, []).append(
                (name, alpha, bool(mat.colorized))
            )

    def _material_identity(self, gltf_mat):
        pbr = gltf_mat.get("pbrMetallicRoughness", {})
        factor = pbr.get("baseColorFactor", (0.8, 0.8, 0.8, 1.0))
        rgb = tuple(round(c * 255) for c in factor[:3])
        alpha = round(float(factor[3]), 4)
        tex = pbr.get("baseColorTexture", {}).get("index")
        key = (rgb, alpha, tex)
        if key in self.materials_by_gltf:
            return None, key, None, None

        texture = self._scene_texture_key(tex)
        exact = (rgb, alpha, texture)
        name = self._names_exact.get(exact)
        colorized = False
        resolved_alpha = alpha
        if name is not None:
            colorized = self._colorized_exact.get(exact, False)
        else:
            name = self._names_color.get((rgb, alpha))

        # OpenSKP can lose names and alpha (glass becomes opaque, name empty).
        # Try (rgb, texture) candidates ignoring alpha to recover.
        if not name or (alpha >= 0.999):
            cands = self._names_rgbtex.get((rgb, texture), [])
            if cands:
                picked = None
                glass_kw = ("glass", "cam", "transluc", "lente", "window", "şeffaf", "seffaf")
                has_opaque = any(c[1] >= 0.999 for c in cands)
                has_transp = any(c[1] < 0.999 for c in cands)
                if len(cands) == 1:
                    picked = cands[0]
                elif alpha >= 0.999 and has_opaque and has_transp:
                    # Ambiguous (e.g. opaque Material5 vs transparent glass at
                    # same color): do NOT force transparency. Keep glTF opaque.
                    picked = None
                else:
                    glass_cands = [
                        c for c in cands
                        if c[1] < 0.999 or any(k in (c[0] or "").lower() for k in glass_kw)
                    ]
                    if alpha >= 0.999 and len(glass_cands) == 1:
                        picked = glass_cands[0]
                if picked and (not name or alpha >= 0.999):
                    name = name or picked[0]
                    if alpha >= 0.999 and picked[1] < 0.999 and not (has_opaque and has_transp):
                        resolved_alpha = picked[1]
                    elif alpha >= 0.999 and picked[1] < 0.999 and not has_opaque:
                        resolved_alpha = picked[1]
                    colorized = picked[2]

        if not name:
            base = f"Material_{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"
            name = f"{base}_tex{tex}" if tex is not None else base

        # Two different SketchUp materials can still resolve to the same name
        # (for example after a colour-only match); keep them separate.
        if name in self.materials:
            suffix = 2
            while f"{name}.{suffix:03d}" in self.materials:
                suffix += 1
            name = f"{name}.{suffix:03d}"
        return name, key, colorized, resolved_alpha

    def _scene_texture_key(self, index):
        if index is None:
            return None
        data = self.scene.textures[index].data
        return (len(data), data[:16])

    def _build_materials(self):
        # SketchUp's own "DefaultMaterial" always exists for unpainted faces.
        default = self._new_default_material()
        self.materials[DEFAULT_MATERIAL] = default
        self.owner.materials[DEFAULT_MATERIAL] = default

        for gltf_mat in self.scene.gltf_materials:
            name, key, colorized, resolved_alpha = self._material_identity(gltf_mat)
            if name is None:  # already built (duplicate identity)
                self.materials_by_index.append(self.materials_by_gltf[key])
                continue
            if (name or "").strip().lower() == "<auto>":
                self.materials_by_gltf[key] = default
                self.materials_by_index.append(default)
                continue
            mat = self._build_material(gltf_mat, key, name, colorized, resolved_alpha)
            self.materials[name] = mat
            self.materials_by_gltf[key] = mat
            self.materials_by_index.append(mat)
            self.owner.materials[name] = mat

    def _new_default_material(self):
        full_name = self.prefix + DEFAULT_MATERIAL
        mat = bpy.data.materials.get(full_name)
        if mat is not None and self.reuse_material:
            return mat
        if mat is None:
            mat = bpy.data.materials.new(full_name)
        mat.use_nodes = True
        nodes, links = mat.node_tree.nodes, mat.node_tree.links
        nodes.clear()
        out = nodes.new("ShaderNodeOutputMaterial")
        bsdf = nodes.new("ShaderNodeBsdfPrincipled")
        links.new(bsdf.outputs[0], out.inputs[0])
        _set_input(bsdf, "Base Color", (0.8, 0.8, 0.8, 1.0))
        mat["skp_imported"] = True
        mat["skp_name"] = DEFAULT_MATERIAL
        return mat

    def _build_material(self, gltf_mat, key, name, colorized, resolved_alpha=None):
        full_name = self.prefix + name
        existing = bpy.data.materials.get(full_name)
        if existing is not None and self.reuse_material:
            existing["skp_name"] = name
            return existing

        mat = existing or bpy.data.materials.new(full_name)
        mat.use_nodes = True
        mat["skp_imported"] = True
        mat["skp_name"] = name
        nodes, links = mat.node_tree.nodes, mat.node_tree.links
        nodes.clear()

        rgb, alpha, tex_index = key
        if resolved_alpha is not None:
            alpha = resolved_alpha
        alpha_f = max(0.0, min(1.0, float(alpha)))

        tex_node = None
        image = self._image_for_texture(tex_index)
        if image is not None:
            tex_node = nodes.new("ShaderNodeTexImage")
            tex_node.image = image
            tex_node.extension = "REPEAT"
            tex_node.location = (-500, 0)
            uv_node = nodes.new("ShaderNodeTexCoord")
            uv_node.location = (-750, 0)
            links.new(uv_node.outputs["UV"], tex_node.inputs["Vector"])

        bsdf = nodes.new("ShaderNodeBsdfPrincipled")
        bsdf.location = (0, 0)
        out = nodes.new("ShaderNodeOutputMaterial")
        out.location = (350, 0)
        links.new(bsdf.outputs[0], out.inputs[0])

        base = (_srgb_to_linear(rgb[0] / 255.0),
                _srgb_to_linear(rgb[1] / 255.0),
                _srgb_to_linear(rgb[2] / 255.0), 1.0)

        if tex_node is not None:
            if colorized:
                # SketchUp colourized material: greyscale image tinted by the
                # material colour.  Multiply reproduces that on the texture.
                mix = nodes.new("ShaderNodeMixRGB")
                mix.blend_type = "MULTIPLY"
                mix.inputs["Fac"].default_value = 1.0
                mix.location = (-220, 0)
                mix.inputs["Color2"].default_value = base
                links.new(tex_node.outputs["Color"], mix.inputs["Color1"])
                links.new(mix.outputs["Color"], bsdf.inputs["Base Color"])
            else:
                links.new(tex_node.outputs["Color"], bsdf.inputs["Base Color"])
            if alpha_f < 1.0 or getattr(image, "depth", 24) == 32:
                links.new(tex_node.outputs["Alpha"], bsdf.inputs["Alpha"])
                self._set_transparent(mat)
        else:
            _set_input(bsdf, "Base Color", base)

        _set_input(bsdf, "Alpha", alpha_f)
        if alpha_f < 0.999:
            self._set_transparent(mat)

        mat.use_backface_culling = False

        if self.smart_pbr:
            self._apply_smart_pbr(mat, name)
        return mat

    @staticmethod
    def _set_transparent(mat):
        for method in ("HASHED", "BLEND"):
            try:
                mat.blend_method = method
                break
            except (TypeError, ValueError):
                continue
        try:
            mat.surface_render_method = "BLENDED"
        except (AttributeError, TypeError, ValueError):
            pass

    def _image_for_texture(self, tex_index):
        if tex_index is None:
            return None
        cached = self.images.get(tex_index)
        if cached is not None:
            return cached
        if tex_index < 0 or tex_index >= len(self.scene.textures):
            return None
        texture = self.scene.textures[tex_index]
        filename = os.path.basename((texture.filename or "").replace("\\", "/"))
        suffix = os.path.splitext(filename)[1].lower()
        if suffix not in {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".webp"}:
            suffix = ".png" if "png" in (texture.mime_type or "") else ".jpg"
        fd, temp_path = tempfile.mkstemp(prefix=self.prefix, suffix=suffix)
        image = None
        try:
            with os.fdopen(fd, "wb") as handle:
                handle.write(texture.data)
            image = bpy.data.images.load(temp_path, check_existing=False)
            image.name = filename or os.path.basename(temp_path)
            try:
                image.pack()
            except Exception:
                pass
        except Exception as exc:
            _log(f"Texture '{filename}' could not be loaded: {exc}")
        finally:
            try:
                os.unlink(temp_path)
            except OSError:
                pass
        if image is not None:
            self.images[tex_index] = image
        return image

    def _apply_smart_pbr(self, mat, name):
        bsdf = next((n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
        if bsdf is None:
            return
        key = (name or "").lower()
        if "glass" in key or "cam" in key:
            _set_input(bsdf, ("Transmission Weight", "Transmission"), 1.0)
            _set_input(bsdf, "Roughness", 0.02)
            _set_input(bsdf, "IOR", 1.45)
            self._set_transparent(mat)
        elif any(word in key for word in ("metal", "steel", "celik", "gold")):
            _set_input(bsdf, "Metallic", 1.0)
            _set_input(bsdf, "Roughness", 0.15)
        elif "mirror" in key or "ayna" in key:
            _set_input(bsdf, "Metallic", 1.0)
            _set_input(bsdf, "Roughness", 0.0)
            _set_input(bsdf, "Base Color", (1.0, 1.0, 1.0, 1.0))
        elif "water" in key or key == "su":
            _set_input(bsdf, ("Transmission Weight", "Transmission"), 1.0)
            _set_input(bsdf, "Roughness", 0.01)
            _set_input(bsdf, "IOR", 1.33)
            self._set_transparent(mat)

    # ── meshes ────────────────────────────────────────────────────────────
    def _build_mesh_resources(self):
        total = len(self.scene.mesh_resources)
        for index, resource in enumerate(self.scene.mesh_resources, 1):
            try:
                self.mesh_data[resource.id] = self._build_mesh(resource)
            except Exception as exc:  # one broken definition must not abort
                _log(f"Mesh '{resource.definition_name}' failed: {exc}")
            if total and index % max(total // 20, 1) == 0:
                self._step(45 + int(25 * index / total))
                _log(f"Meshes {index}/{total}")

    def _ngon_faces_from_tris(self, pts, tris, tri_mats=None):
        """Merge coplanar adjacent triangles (same material) into ngons.

        Returns (ngons, ngon_mats).
        """
        from collections import defaultdict

        tris = np.asarray(tris)
        n_tri = len(tris)
        if n_tri == 0:
            return [], []
        if tri_mats is None:
            tri_mats = [None] * n_tri

        tri_norms = []
        for t in tris:
            a, b, c = pts[t[0]], pts[t[1]], pts[t[2]]
            n = np.cross(b - a, c - a)
            ln = np.linalg.norm(n)
            n = n / ln if ln > 1e-12 else np.array([0.0, 0.0, 1.0], dtype=np.float32)
            tri_norms.append(n)
        tri_norms = np.array(tri_norms)

        edge_map = defaultdict(list)
        for ti, t in enumerate(tris):
            for i in range(3):
                e = tuple(sorted((int(t[i]), int(t[(i + 1) % 3]))))
                edge_map[e].append(ti)

        parent = list(range(n_tri))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[rb] = ra

        for _e, tri_idxs in edge_map.items():
            if len(tri_idxs) == 2:
                a, b = tri_idxs
                if tri_mats[a] == tri_mats[b] and float(np.dot(tri_norms[a], tri_norms[b])) > 0.9999:
                    union(a, b)

        groups = defaultdict(list)
        for ti in range(n_tri):
            groups[find(ti)].append(ti)

        ngons = []
        ngon_mats = []
        for g in groups.values():
            mat = tri_mats[g[0]]
            verts_set = set()
            edge_count = defaultdict(int)
            for ti in g:
                t = tris[ti]
                for v in t:
                    verts_set.add(int(v))
                for i in range(3):
                    e = tuple(sorted((int(t[i]), int(t[(i + 1) % 3]))))
                    edge_count[e] += 1

            boundary_edges = [e for e, c in edge_count.items() if c == 1]
            if not boundary_edges:
                ngons.append(sorted(verts_set))
                ngon_mats.append(mat)
                continue

            v_to_edges = defaultdict(list)
            for e in boundary_edges:
                v_to_edges[e[0]].append(e)
                v_to_edges[e[1]].append(e)

            used_edges = set()
            loops = []
            for start_e in boundary_edges:
                if start_e in used_edges:
                    continue
                loop = [start_e[0], start_e[1]]
                used_edges.add(start_e)
                prev, curr = start_e[0], start_e[1]
                for _ in range(10000):
                    nexts = [
                        e
                        for e in v_to_edges[curr]
                        if e != (prev, curr)
                        and e != (curr, prev)
                        and e not in used_edges
                    ]
                    if not nexts:
                        break
                    next_e = nexts[0]
                    used_edges.add(next_e)
                    nxt = next_e[0] if next_e[1] == curr else next_e[1]
                    if nxt == loop[0]:
                        break
                    loop.append(nxt)
                    prev, curr = curr, nxt
                if len(loop) >= 3:
                    loops.append(loop)

            if len(loops) == 1:
                ngons.append(loops[0])
                ngon_mats.append(mat)
            elif len(loops) > 1:
                for ti in g:
                    t = tris[ti]
                    ngons.append([int(t[0]), int(t[1]), int(t[2])])
                    ngon_mats.append(mat)
            else:
                ngons.append(sorted(verts_set))
                ngon_mats.append(mat)

        return ngons, ngon_mats

    @staticmethod
    def _weld_vertices(
        verts, faces, face_corner_uvs, face_materials=None, pos_eps=1e-5
    ):
        """Merge vertices by position (topological connectivity); keep per-loop UVs."""
        if len(verts) == 0 or len(faces) == 0:
            if face_materials is None:
                return verts, faces, face_corner_uvs
            return verts, faces, face_corner_uvs, face_materials
        verts = np.asarray(verts, dtype=np.float32).reshape(-1, 3)
        pq = np.round(verts / pos_eps).astype(np.int64)
        keys = {}
        remap = np.empty(len(verts), dtype=np.int32)
        new_verts = []
        for i in range(len(verts)):
            k = (int(pq[i, 0]), int(pq[i, 1]), int(pq[i, 2]))
            j = keys.get(k)
            if j is None:
                j = len(new_verts)
                keys[k] = j
                new_verts.append(verts[i])
            remap[i] = j
        new_verts = np.array(new_verts, dtype=np.float32)
        new_faces = []
        new_corner_uvs = []
        new_mats = [] if face_materials is not None else None
        for fi, f in enumerate(faces):
            cuv = face_corner_uvs[fi]
            rf = [int(remap[v]) for v in f]
            if len(rf) < 2:
                continue
            cleaned_f = [rf[0]]
            cleaned_uv = [cuv[0]]
            for vi, v in enumerate(rf[1:], 1):
                if v != cleaned_f[-1]:
                    cleaned_f.append(v)
                    cleaned_uv.append(cuv[vi])
            if len(cleaned_f) >= 2 and cleaned_f[0] == cleaned_f[-1]:
                cleaned_f.pop()
                cleaned_uv.pop()
            if len(cleaned_f) >= 3:
                new_faces.append(cleaned_f)
                new_corner_uvs.append(cleaned_uv)
                if new_mats is not None:
                    new_mats.append(face_materials[fi])
        if face_materials is None:
            return new_verts, new_faces, new_corner_uvs
        return new_verts, new_faces, new_corner_uvs, new_mats

    def _filter_coincident_back_prims(self, resource):
        prims = list(resource.primitives)
        if len(prims) < 2:
            return prims

        gltf_mats = getattr(self.scene, "gltf_materials", []) or []
        infos = []
        for p in prims:
            if len(p.positions) == 0 or len(p.indices) == 0:
                infos.append(None)
                continue
            pos = _as_numpy(p.positions, np.float32).reshape(-1, 3)
            idx = _as_numpy(p.indices, np.uint32).reshape(-1, 3)
            tris = pos[idx]
            v0, v1, v2 = tris[:, 0], tris[:, 1], tris[:, 2]
            n = np.cross(v1 - v0, v2 - v0)
            nl = np.linalg.norm(n, axis=1, keepdims=True)
            n = n / np.where(nl > 1e-12, nl, 1.0)
            centers = tris.mean(axis=1)
            infos.append((centers, n, len(idx)))

        drop = [False] * len(prims)
        for i in range(len(prims)):
            if drop[i] or infos[i] is None:
                continue
            ci, ni, ti = infos[i]
            for j in range(i + 1, len(prims)):
                if drop[j] or infos[j] is None:
                    continue
                cj, nj, tj = infos[j]
                if ti != tj or ti == 0:
                    continue
                # check coincident+opposite (sample if large)
                sample = min(ti, 200)
                step = max(1, ti // sample)
                ai = np.arange(0, ti, step)[:sample]
                matches = 0
                for k in ai:
                    d = np.sum((cj - ci[k]) ** 2, axis=1)
                    m = int(np.argmin(d))
                    if d[m] < 1e-8 and float(np.dot(ni[k], nj[m])) < -0.9:
                        matches += 1
                if matches >= int(0.9 * len(ai)):
                    # duplicate front/back pair: prefer textured material
                    def has_tex(pi):
                        mi = prims[pi].material_index
                        if mi is None or mi < 0 or mi >= len(gltf_mats):
                            return False
                        return "baseColorTexture" in gltf_mats[mi].get("pbrMetallicRoughness", {})
                    if has_tex(i) and not has_tex(j):
                        drop[j] = True
                    elif has_tex(j) and not has_tex(i):
                        drop[i] = True
                        break
                    else:
                        drop[j] = True
        return [p for p, d in zip(prims, drop) if not d]

    def _build_mesh(self, resource):
        primitives = self._filter_coincident_back_prims(resource)

        verts, uvs, tris, tri_materials = [], [], [], []
        offset = 0
        for prim in primitives:
            if len(prim.positions) == 0 or len(prim.indices) == 0:
                continue
            points = _as_numpy(prim.positions, np.float32).reshape(-1, 3)
            points = _axis_swap(points)
            count = len(points)
            verts.append(points)
            if len(prim.uvs):
                uvs.append(_as_numpy(prim.uvs, np.float32).reshape(-1, 2))
            else:
                uvs.append(np.zeros((count, 2), dtype=np.float32))
            indices = _as_numpy(prim.indices, np.uint32).reshape(-1, 3)
            tris.append(indices + offset)
            tri_materials.append((prim.material_index, len(indices)))
            offset += count

        if not verts:
            return None

        all_verts = np.concatenate(verts)
        all_uvs = np.concatenate(uvs)
        all_tris_arr = np.concatenate(tris)

        tri_mats = []
        for gltf_index, count in tri_materials:
            tri_mats.extend([gltf_index] * count)

        # Merge coplanar adjacent triangles (same material) globally into ngons
        pts = all_verts.reshape(-1, 3)
        all_ngons, all_ngon_materials = self._ngon_faces_from_tris(
            pts, all_tris_arr, tri_mats
        )
        all_corner_uvs = [[all_uvs[vi].tolist() for vi in _ngon] for _ngon in all_ngons]

        # Weld by position for topological connectivity; preserve per-loop UVs.
        all_verts, all_ngons, all_corner_uvs, all_ngon_materials = self._weld_vertices(
            all_verts, all_ngons, all_corner_uvs, all_ngon_materials
        )

        default_mat = self.materials.get(DEFAULT_MATERIAL)
        used = []
        for mat in all_ngon_materials:
            if mat not in used:
                used.append(mat)
        slot_of = {gltf_index: slot for slot, gltf_index in enumerate(used)}

        name = f"{self.prefix}{resource.definition_name or 'Mesh'}"
        if resource.variant_key:
            name = f"{name}_{resource.variant_key}"
        mesh = bpy.data.meshes.new(name)

        mesh.from_pydata(all_verts.tolist(), [], all_ngons)
        mesh.update()

        # UVs per loop (preserves seams while vertices are topologically welded)
        uv_layer = mesh.uv_layers.new(name="UVMap")
        if len(mesh.loops) and all_corner_uvs:
            loop_uvs = np.empty((len(mesh.loops), 2), dtype=np.float32)
            for pi, poly in enumerate(mesh.polygons):
                cuv = all_corner_uvs[pi]
                ls = poly.loop_start
                for li in range(poly.loop_total):
                    loop_uvs[ls + li] = cuv[li]
            uv_layer.data.foreach_set("uv", loop_uvs.ravel())

        material_indices = np.empty(len(all_ngons), dtype=np.int32)
        for i, gltf_index in enumerate(all_ngon_materials):
            material_indices[i] = slot_of[gltf_index]
        mesh.polygons.foreach_set("material_index", material_indices)

        for gltf_index in used:
            if gltf_index is None or gltf_index < 0 or gltf_index >= len(self.materials_by_index):
                mat = default_mat
            else:
                mat = self.materials_by_index[gltf_index]
            if mat is None:
                mat = default_mat
            mesh.materials.append(mat)

        mesh.polygons.foreach_set("use_smooth", np.zeros(len(mesh.polygons), dtype=bool))
        mesh.update()

        # Dissolve coplanar faces (removes diagonal triangulation on flat areas)
        # while respecting material boundaries and UVs.
        if len(mesh.polygons):
            import math

            import bmesh

            bm = bmesh.new()
            bm.from_mesh(mesh)
            bmesh.ops.dissolve_limit(
                bm,
                angle_limit=math.radians(1.0),
                verts=bm.verts,
                edges=bm.edges,
                use_dissolve_boundaries=False,
                delimit={"MATERIAL", "SEAM", "SHARP"},
            )
            bm.to_mesh(mesh)
            bm.free()
            mesh.update()

        mesh["skp_imported"] = True
        return mesh

    @staticmethod
    def _resource_normals(resource):
        """Per-vertex normals for a definition, or None if unusable."""
        if not resource.primitives or not len(resource.primitives[0].normals):
            return None
        chunks = []
        for prim in resource.primitives:
            if len(prim.positions) == 0 or len(prim.indices) == 0:
                continue
            count = len(prim.positions) // 3
            if len(prim.normals) != count * 3:
                return None
            chunks.append(_axis_swap(_as_numpy(prim.normals, np.float32).reshape(-1, 3)))
        if not chunks:
            return None
        normals = np.concatenate(chunks)
        return normals if np.isfinite(normals).all() else None

    # ── curves ────────────────────────────────────────────────────────────
    def _build_curve_resources(self):
        if not self.import_edges:
            return
        for resource in self.scene.curve_resources:
            points = []
            closed_flags = []
            for local in resource.curves:
                if len(local.points_m) < 2:
                    continue
                points.append(_axis_swap(np.asarray(local.points_m, dtype=np.float32)))
                closed_flags.append(local.closed)
            if not points:
                continue
            name = f"{self.prefix}{resource.definition_name or 'Edges'}"
            curve = bpy.data.curves.new(name, "CURVE")
            curve.dimensions = "3D"
            curve.bevel_depth = 0.0
            for pts, closed in zip(points, closed_flags):
                spline = curve.splines.new("POLY")
                spline.points.add(len(pts) - 1)
                flat = np.empty((len(pts), 4), dtype=np.float32)
                flat[:, :3] = pts
                flat[:, 3] = 1.0
                spline.points.foreach_set("co", flat.ravel())
                spline.use_cyclic_u = bool(closed)
            curve["skp_imported"] = True
            self.curve_data[resource.id] = curve

    # ── objects ───────────────────────────────────────────────────────────
    def _build_objects(self):
        root_node = self.scene.scene_hierarchy
        self._created = 0
        # The scene root can carry loose edges of its own (SketchUp's model
        # root is itself a definition), and it is never visited as a child.
        if root_node.curve_resource_id in self.curve_data:
            root_obj = bpy.data.objects.new(
                self._node_name(root_node, "RootEdges"),
                self.curve_data[root_node.curve_resource_id],
            )
            self._setup_object(root_obj, root_node, None, None, edges=True)
        for child in root_node.children:
            self._create_node(child, None)
        _log(f"Created {self._created} objects")

    @staticmethod
    def _node_name(node, fallback):
        return node.name or node.definition_name or fallback

    def _create_node(self, node, parent, local_override=None):
        local = local_override if local_override is not None else _matrix_from_gltf(node.matrix)
        mesh = self.mesh_data.get(node.mesh_resource_id) if node.mesh_resource_id else None
        has_curve = node.curve_resource_id in self.curve_data

        # Collapse anonymous structural container with exactly 1 child:
        # skip the empty and merge its transform into the child.
        if mesh is None and not has_curve and len(node.children) == 1:
            if not (node.guid or (node.name or "").strip() or (node.definition_name or "").strip()):
                child = node.children[0]
                child_local = _matrix_from_gltf(child.matrix)
                combined = local @ child_local if local is not None else child_local
                self._create_node(child, parent, combined)
                return

        obj = None
        is_edge_obj = False
        if mesh is not None:
            obj = bpy.data.objects.new(self._node_name(node, "Mesh"), mesh)
        elif has_curve:
            obj = bpy.data.objects.new(
                self._node_name(node, "Edges"),
                self.curve_data[node.curve_resource_id],
            )
            is_edge_obj = True
        elif node.children:
            obj = bpy.data.objects.new(self._node_name(node, "Group"), None)
            obj.empty_display_type = "PLAIN_AXES"
            obj.empty_display_size = 0.15

        if obj is not None:
            self._setup_object(obj, node, parent, local, edges=is_edge_obj)
            # A definition can hold both faces and loose edges; the mesh
            # resource only carries the faces, so the edges ride along as a
            # child object of the same placement.
            if mesh is not None and has_curve:
                edges = bpy.data.objects.new(
                    f"{obj.name} (Edges)",
                    self.curve_data[node.curve_resource_id],
                )
                self._setup_object(edges, node, obj, Matrix.Identity(4), edges=True)

        next_parent = obj if obj is not None else parent
        for child in node.children:
            self._create_node(child, next_parent)

    def _setup_object(self, obj, node, parent, local, edges=False):
        obj["skp_imported"] = True
        obj["skp_layer"] = node.layer or ""
        if node.guid:
            obj["skp_guid"] = node.guid
        if node.definition_name:
            obj["skp_definition"] = node.definition_name
        if node.properties:
            obj["skp_properties"] = {k: str(v) for k, v in node.properties.items()}
        if edges:
            self._edges_collection().objects.link(obj)
        else:
            self._layer_collection(node.layer).objects.link(obj)
        if parent is not None:
            obj.parent = parent
        if local is not None:
            obj.matrix_basis = local

        self._created += 1
        if self._created % 2000 == 0:
            self._step(min(70 + self._created // 1000, 92))

    # ── cameras ───────────────────────────────────────────────────────────
    def _build_cameras(self):
        if not self.import_cameras:
            return
        pages = [
            p for p in self.model.pages
            if p.eye is not None and p.target is not None
            and (not self.scene_filter or p.name == self.scene_filter)
        ]
        if not pages:
            if self.scene_filter:
                _log(f"SketchUp scene '{self.scene_filter}' not found in this file.")
            return
        clip_end = 250.0
        try:
            addon = self.context.preferences.addons.get("sketchup_imparator")
            if addon and addon.preferences:
                clip_end = addon.preferences.camera_far_plane
        except Exception:
            pass
        for page in pages:
            data = bpy.data.cameras.new(f"{self.prefix}{page.name}")
            data.clip_start = 0.01
            data.clip_end = max(clip_end, 1.0)
            data.sensor_fit = "VERTICAL"
            data.angle = np.radians(page.fov if page.fov else 35.0)
            if page.parallel and page.ortho_height > 0:
                data.type = "ORTHO"
                data.ortho_scale = page.ortho_height * INCH_TO_METER
            obj = bpy.data.objects.new(f"{self.prefix}{page.name}", data)
            eye = Vector(page.eye) * INCH_TO_METER
            target = Vector(page.target) * INCH_TO_METER
            obj.location = eye
            obj.matrix_world = self._look_at(eye, target, page.up)
            obj["skp_imported"] = True
            obj["skp_scene"] = page.name
            self.root_coll.objects.link(obj)
            if page.hidden_layers:
                for layer in page.hidden_layers:
                    coll = self.layer_colls.get(layer)
                    if coll is not None:
                        coll.hide_viewport = True
                        coll.hide_render = True

    @staticmethod
    def _look_at(eye, target, up):
        direction = (target - eye)
        if direction.length < 1e-9:
            direction = Vector((0.0, 0.0, -1.0))
        forward = (-direction).normalized()  # camera looks down its -Z
        up_vector = Vector(up) if up else Vector((0.0, 0.0, 1.0))
        right = up_vector.cross(forward)
        if right.length < 1e-6:
            right = Vector((1.0, 0.0, 0.0)).cross(forward)
            if right.length < 1e-6:
                right = Vector((0.0, 1.0, 0.0)).cross(forward)
        right.normalize()
        true_up = forward.cross(right).normalized()
        rotation = Matrix((right, true_up, forward)).transposed()
        result = rotation.to_4x4()
        result.translation = eye
        return result


def import_skp(owner, context, options):
    """Entry point used by :class:`SceneImporter`."""
    importer = SkpSceneImporter(owner, context, options)
    importer.run()
    owner.mesh_data = importer.mesh_data
    owner.curve_data = importer.curve_data
    owner.images = importer.images
    return {"FINISHED"}

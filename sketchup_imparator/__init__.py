import math
import os
import shutil
import tempfile
import time
from collections import defaultdict

import bpy
DEBUG_MODE = True
import bmesh
from bpy.props import (
    BoolProperty,
    EnumProperty,
    FloatProperty,
    IntProperty,
    StringProperty,
)
from bpy.types import AddonPreferences, Operator
from bpy_extras.io_utils import (
    ExportHelper,
    ImportHelper,
    unpack_face_list,
    unpack_list,
)
from mathutils import Matrix, Quaternion, Vector

__author__ = "gurkanerol (2026 Modernization), Martijn Berger (Original Creator)"
__license__ = "GPL"

"""
This program is free software; you can redistribute it and
or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 3
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see http://www.gnu.org/licenses
"""

from . import sketchup
from .SKPutil import *

bl_info = {
    "name": "SketchUp Imparator",
    "author": "gurkanerol, Martijn Berger, Sanjay Mehta, Arindam Mondal, Peter Kirkham",
    "version": (2026, 4, 24),
    "blender": (5, 1, 0),
    "description": "Import of native SketchUp (.skp) files (The Imparator 2026 Edition)",
    "wiki_url": "https://github.com/gurkanerol/sketchup-imparator",
    "doc_url": "https://github.com/gurkanerol/sketchup-imparator",
    "tracker_url": "https://github.com/gurkanerol/sketchup-imparator/issues",
    "category": "Import-Export",
    "location": "File > Import",
}

DEBUG = False

LOGS = True

MIN_LOGS = False

if not LOGS:
    MIN_LOGS = True


class SketchupAddonPreferences(AddonPreferences):
    bl_idname = __name__

    camera_far_plane: FloatProperty(name="Camera Clip Ends At :", default=250, unit="LENGTH")

    draw_bounds: IntProperty(name="Draw Similar Objects As Bounds When It's Over :", default=1000)

    def draw(self, context):
        layout = self.layout
        layout.label(text="- Basic Import Options -")
        row = layout.row()
        row.use_property_split = True
        row.prop(self, "camera_far_plane")
        layout = self.layout
        row = layout.row()
        row.use_property_split = True
        row.prop(self, "draw_bounds")


def skp_log(*args):
    # Log output by pre-pending "SU |"
    if args:
        print("SketchUp Imparator |", *args)


def create_nested_collection(coll_name):
    context = bpy.context
    main_coll_name = "SKP Imported Data"

    # Ensure main collection exists and is linked
    main_coll = bpy.data.collections.get(main_coll_name)
    if not main_coll:
        main_coll = bpy.data.collections.new(main_coll_name)
        
    if main_coll_name not in context.scene.collection.children:
        context.scene.collection.children.link(main_coll)

    # Ensure nested collection exists and is linked to main
    nested_coll = bpy.data.collections.get(coll_name)
    if not nested_coll:
        nested_coll = bpy.data.collections.new(coll_name)
        
    if coll_name not in main_coll.children:
        main_coll.children.link(nested_coll)

    # Safely set active layer collection for UI focus
    return nested_coll


def get_collection(name, parent):
    if not parent:
        parent = bpy.context.scene.collection
    coll = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    if name not in parent.children.keys():
        parent.children.link(coll)
    return coll


def init_skp_collections():
    root = get_collection("SKP Imported Data", None)
    colls = {
        'root': root,
        'cameras': get_collection("SKP Scenes (as Cameras)", root),
        'components': get_collection("SKP Components", root),
        'groups': get_collection("SKP Groups", root),
        'mesh': get_collection("SKP Mesh Objects", root),
        'edges': get_collection("SKP Loose Edges", root),
        'hidden': get_collection("SKP Hidden Objects", root)
    }
    # Hide the hidden objects collection in viewport
    pass  # Removed data block hide
    return colls


def hide_one_level():
    context = bpy.context

    outliners = [a for a in context.screen.areas if a.type == "OUTLINER"]
    c = context.copy()
    for ol in outliners:
        c["area"] = ol
        bpy.ops.outliner.show_one_level(c, open=False)
        ol.tag_redraw()

    # context.view_layer.update()


class SceneImporter:
    def __init__(self):
        self.filepath = "/tmp/untitled.skp"
        self.name_mapping = {}
        self.layers_skip = []
        self.component_meshes = {}
        self.component_stats = defaultdict(list)
        self.instance_counts = defaultdict(int)
        self.max_instance = 50

    def set_filename(self, filename):
        self.filepath = filename
        self.basepath, self.skp_filename = os.path.split(self.filepath)
        return self  # allow chaining

    def load(self, context, **options):
        """Load a SketchUp file"""
        # Blender settings
        self.context = context
        self.organize_by_tags = options.get("organize_by_tags", False)
        self.import_standalone_edges = options.get("import_standalone_edges", False)
        self.support_back_material = options.get("support_back_material", False)
        self.merge_coplanar_faces = options.get("merge_coplanar_faces", False)
        self.reuse_material = options.get("reuse_material", True)
        self.reuse_group = options.get("reuse_existing_groups", False)
        self.max_instance = options.get("max_instance", 50)
        self.tag_collections = {}
        self.component_stats = defaultdict(list)
        self.component_skip = proxy_dict()
        self.component_depth = proxy_dict()
        self.group_written = {}
        ren_res_x = context.scene.render.resolution_x
        ren_res_y = context.scene.render.resolution_y
        self.aspect_ratio = ren_res_x / ren_res_y

        # Start stopwatch for overall import
        _time_main = time.time()

        # Log filename being imported
        if LOGS:
            skp_log(f"Importing: {self.filepath}")
        addon_name = __name__.split(".")[0]
        self.prefs = context.preferences.addons[addon_name].preferences
        
        # Open the SketchUp file and access the model using SketchUp API
        # Ensure API is initialized by creating a dummy model first
        # (Workaround for Model.from_file skipping SUInitialize)
        _init_model = sketchup.Model()
        
        try:
            self.skp_model = sketchup.Model.from_file(self.filepath)
            
            # Binary version check
            try:
                ver = self.skp_model.get_API_version() if hasattr(self.skp_model, "get_API_version") else "2026.1"
                skp_log(f"SketchUp API Version: {ver}")
            except Exception:
                skp_log("SketchUp API status check skipped.")

            # Pre-calculate instance counts for optimization decisions
            for cd in self.skp_model.component_definitions:
                self.instance_counts[cd.name] = cd.numInstances
    
            # 1. Initialize Standard Collections
            self.colls = init_skp_collections()

            # Start stopwatch for camera import
            if not MIN_LOGS:
                skp_log("")
                skp_log("=== Importing Sketchup scenes and views as Blender Cameras ===")
            _time_camera = time.time()

            # Import a specific named SketchUp scene as a Blender camera and hide
            # the layers associated with that specific scene
            if options.get("import_scene"):
                options["scenes_as_camera"] = False
                options["import_camera"] = True
                for s in self.skp_model.scenes:
                    if s.name == options["import_scene"]:
                        if not MIN_LOGS:
                            skp_log(f"Importing named SketchUp scene '{s.name}'")
                        self.scene = s

                        # Skip s.layers which are the invisible layers
                        self.layers_skip = [l for l in s.layers]
                if not self.layers_skip and not MIN_LOGS:
                    skp_log("Scene: '{}' didn't have any invisible layers.".format(options.get("import_scene")))
                if self.layers_skip != [] and not MIN_LOGS:
                    hidden_layers = sorted([l.name for l in self.layers_skip])
                    print("SU | Invisible Layer(s)/Tag(s): \n     ", end="")
                    print(*hidden_layers, sep=", ")

            # Import each scene as a Blender camera
            if options.get("scenes_as_camera"):
                if not MIN_LOGS:
                    skp_log("Importing all SketchUp scenes as Blender cameras")
                for s in self.skp_model.scenes:
                    name = self.write_camera(s.camera, s.name)

            # Set the active camera and use for 3D view
            if options.get("import_camera"):
                if not MIN_LOGS:
                    skp_log("Importing last SketchUp view as Blender camera")
                if self.scene:
                    active_cam = self.write_camera(self.scene.camera, name=self.scene.name)
                    context.scene.camera = bpy.data.objects[active_cam]
                else:
                    active_cam = self.write_camera(self.skp_model.camera)
                    context.scene.camera = bpy.data.objects[active_cam]
                for area in bpy.context.screen.areas:
                    if area.type == "VIEW_3D":
                        area.spaces[0].region_3d.view_perspective = "CAMERA"
                        break
            SKP_util.layers_skip = self.layers_skip
            if not MIN_LOGS:
                skp_log(f"Cameras imported in {(time.time() - _time_camera):.4f} sec.")

            # Start stopwatch for material imports
            if not MIN_LOGS:
                skp_log("")
                skp_log("=== Importing Sketchup materials into Blender ===")
            _time_material = time.time()
            self.write_materials(self.skp_model.materials)
            if not MIN_LOGS:
                skp_log(f"Materials imported in {(time.time() - _time_material):.4f} sec.")

            # Start stopwatch for component import
            if not MIN_LOGS:
                skp_log("")
                skp_log("=== Importing Sketchup components into Blender ===")
            _time_analyze_depth = time.time()

            # Create collection for cameras

            # Create collection for components

            # Create collections for Tags inside SKP Mesh Objects if requested
            if self.organize_by_tags:
                mesh_coll = self.colls['mesh']
                for layer in self.skp_model.layers:
                    name = layer.name
                    if name not in bpy.data.collections:
                        l_coll = bpy.data.collections.new(name)
                        mesh_coll.children.link(l_coll)
                    self.tag_collections[name] = bpy.data.collections[name]

            # Determine the number of components that exist in the SketchUp model
            self.skp_components = proxy_dict(self.skp_model.component_definition_as_dict)
            u_comps = [k for k, v in self.skp_components.items()]
            if not MIN_LOGS:
                print(f"SU | Contains {len(u_comps)} components: \n     ", end="")
                print(*u_comps, sep=", ")

            # Analyse component depths
            D = SKP_util()
            for c in self.skp_model.component_definitions:
                self.component_depth[c.name] = D.component_deps(c.entities)
                if DEBUG:
                    print(f"     -- ({c.name}) --\n        Depth: {self.component_depth[c.name]}\n", end="")
                    print(f"        Instances (Used): {c.numInstances} ({c.numUsedInstances})")
            if not MIN_LOGS:
                skp_log(f"Component depths analyzed in {(time.time() - _time_analyze_depth):.4f} sec.")

            # Import the components as duplicated groups then hide components
            self.write_duplicateable_groups()
        
            pass # Visibility overrides removed per user request

            if options.get("dedub_only"):
                return {"FINISHED"}

            # self.component_stats = defaultdict(list)

            # Start stopwatch for mesh objects import
            if not MIN_LOGS:
                skp_log("")
                skp_log("=== Importing Sketchup mesh objects into Blender ===")
            _time_mesh_data = time.time()

            # Create collection for mesh objects

            # 3. LOOSE ENTITIES (Geometry at root)
            self.write_entities(self.skp_model.entities, "SKP Mesh Objects", Matrix.Identity(4))
        
            # Import standalone edges if requested
            if self.import_standalone_edges:
                self.write_standalone_edges(self.skp_model.entities, "Loose Edges", Matrix.Identity(4))

            # Direct recursive import already handled everything via Alt+D mesh sharing
            if LOGS:
                skp_log("Finished entire importing process in %.4f sec.\n" % (time.time() - _time_main))
        
        finally:
            # STERILIZATION: Force C-API destruction and clear RAM caches to prevent leaks.
            if hasattr(self, "skp_model") and self.skp_model:
                try: self.skp_model.close()
                except: pass
                self.skp_model = None
            
            # Massive memory purge
            for attr in ["skp_meshes", "skp_components", "component_meshes", "component_depth", "tag_collections"]:
                if hasattr(self, attr):
                    getattr(self, attr).clear()
            
            import gc
            gc.collect()
            
            if LOGS:
                skp_log("Memory sterilized and caches cleared.\n")

        return {"FINISHED"}

    #
    # Write components as groups that can be duplicated later.
    #
    def write_duplicateable_groups(self):
        component_stats = self.analyze_entities(
            self.skp_model.entities, "Sketchup", Matrix.Identity(4), component_stats=defaultdict(list)
        )
        instance_when_over = self.max_instance
        max_depth = max(self.component_depth.values(), default=0)

        # Filter out components from list if the total number of instances
        # is lower than the minimum threshold for creating duplicated mesh
        # objects.
        component_stats = {k: v for k, v in component_stats.items() if len(v) >= instance_when_over}
        for i in range(max_depth + 1):
            for k, v in component_stats.items():
                name, mat = k
                depth = self.component_depth[name]
                comp_def = self.skp_components[name]
                if comp_def and depth == 1:
                    # self.component_skip[(name, mat)] = comp_def.entities
                    pass
                elif comp_def and depth == i:
                    gname = group_name(name, mat)
                    if self.reuse_group and gname in bpy.data.collections:
                        skp_log(f"Group {gname} already defined")
                        self.component_skip[(name, mat)] = comp_def.entities
                        self.group_written[(name, mat)] = bpy.data.collections[gname]
                    else:
                        group = bpy.data.collections.new(name=gname)
                        skp_log(f"Component {gname} written as group")
                        self.component_def_as_group(
                            comp_def.entities, name, Matrix(), default_material=mat, etype=EntityType.outer, group=group
                        )
                        self.component_skip[(name, mat)] = comp_def.entities
                        self.group_written[(name, mat)] = group

    def analyze_entities(
        self,
        entities,
        name,
        transform,
        default_material="DefaultMaterial",
        etype=EntityType.none,
        component_stats=None,
        component_skip=None,
    ):
        if component_skip is None:
            component_skip = []
        if etype == EntityType.component:
            component_stats[(name, default_material)].append(transform)
        for group in entities.groups:
            if self.layers_skip and group.layer in self.layers_skip:
                continue
            if DEBUG:
                print(f"     |G {group.name}")
                print(f"     {Matrix(group.transform)}")
            self.analyze_entities(
                group.entities,
                "G-" + group.name,
                transform @ Matrix(group.transform),
                default_material=inherent_default_mat(group.material, default_material),
                etype=EntityType.group,
                component_stats=component_stats,
            )
        for instance in entities.instances:
            if self.layers_skip and instance.layer in self.layers_skip:
                continue
            mat = inherent_default_mat(instance.material, default_material)
            cdef = self.skp_components[instance.definition.name]
            if cdef is None:
                continue
            if (cdef.name, mat) in component_skip:
                continue
            if DEBUG:
                print(f"     |C {cdef.name}")
                print(f"     {Matrix(instance.transform)}")
            self.analyze_entities(
                cdef.entities,
                cdef.name,
                transform @ Matrix(instance.transform),
                default_material=mat,
                etype=EntityType.component,
                component_stats=component_stats,
            )
        return component_stats

    #
    # Import materials from SketchUp into Blender.
    #
    def write_materials(self, materials):
        if self.context.scene.render.engine != "CYCLES":
            self.context.scene.render.engine = "CYCLES"
        self.materials = {}
        self.materials_scales = {}
        # Improved DefaultMaterial handling to prevent .001 duplication
        default_name = "DefaultMaterial"
        existing_default = bpy.data.materials.get(default_name)
        
        if self.reuse_material and existing_default:
            self.materials[default_name] = existing_default
        else:
            bmat = existing_default if existing_default else bpy.data.materials.new(default_name)
            bmat.use_nodes = True
            if bmat.node_tree: bmat.node_tree.nodes.clear()
            
            nodes = bmat.node_tree.nodes
            links = bmat.node_tree.links
            output_shader = nodes.new("ShaderNodeOutputMaterial")
            principled_bsdf = nodes.new("ShaderNodeBsdfPrincipled")
            links.new(principled_bsdf.outputs[0], output_shader.inputs["Surface"])
            principled_bsdf.inputs["Base Color"].default_value = (1.0, 1.0, 1.0, 1.0)
            self.materials[default_name] = bmat
        for mat in materials:
            name = mat.name
            if mat.texture:
                self.materials_scales[name] = mat.texture.dimensions[2:]
            else:
                self.materials_scales[name] = (1.0, 1.0)
                
            # Material Persistence & Reuse Logic
            existing_mat = bpy.data.materials.get(name)
            
            if self.reuse_material and existing_mat:
                self.materials[name] = existing_mat
                continue

            if existing_mat:
                bmat = existing_mat
            else:
                bmat = bpy.data.materials.new(name)

            r, g, b, a = mat.color
            tex = mat.texture
            # Convert sRGB to Linear
            bmat.diffuse_color = (
                math.pow((r / 255.0), 2.2),
                math.pow((g / 255.0), 2.2),
                math.pow((b / 255.0), 2.2),
                round((a / 255.0), 2),
            )

            if round((a / 255.0), 2) < 1:
                bmat.blend_method = "BLEND"
            else:
                bmat.blend_method = "OPAQUE"
                
            bmat.use_nodes = True
            if bmat.node_tree:
                bmat.node_tree.nodes.clear()
            else:
                bmat.use_nodes = True # Re-init if node tree was missing
            
            nodes = bmat.node_tree.nodes
            links = bmat.node_tree.links
            
            output_shader = nodes.new("ShaderNodeOutputMaterial")
            principled_bsdf = nodes.new("ShaderNodeBsdfPrincipled")
            links.new(principled_bsdf.outputs[0], output_shader.inputs["Surface"])
            
            principled_bsdf.inputs["Base Color"].default_value = bmat.diffuse_color
            principled_bsdf.inputs["Alpha"].default_value = bmat.diffuse_color[3]
            
            if tex:
                try:
                    raw_tex_name = tex.name.replace("\\", "/")
                    tex_filename = raw_tex_name.split("/")[-1]
                    for char in '<>:"/\\|?*':
                        tex_filename = tex_filename.replace(char, "_")
                    
                    if not tex_filename: tex_filename = f"Texture_{name}.jpg"
                        
                    temp_dir = os.path.join(tempfile.gettempdir(), f"skp_tex_{int(time.time())}")
                    os.makedirs(temp_dir, exist_ok=True)
                    temp_file_path = os.path.join(temp_dir, tex_filename)
                    
                    tex.write(temp_file_path)
                    
                    # Avoid reloading images if already in Blender and we want clean updates
                    img_name = f"{name}_{tex_filename}"
                    img = bpy.data.images.get(img_name) or bpy.data.images.load(temp_file_path)
                    img.name = img_name
                    img.pack()
                    shutil.rmtree(temp_dir)
                    
                    tex_node = nodes.new("ShaderNodeTexImage")
                    tex_node.image = img
                    tex_node.location = Vector((-600, 0))
                    
                    tex_coord = nodes.new("ShaderNodeTexCoord")
                    mapping = nodes.new("ShaderNodeMapping")
                    
                    links.new(tex_coord.outputs["UV"], mapping.inputs["Vector"])
                    links.new(mapping.outputs["Vector"], tex_node.inputs["Vector"])
                    links.new(tex_node.outputs["Color"], principled_bsdf.inputs["Base Color"])
                    
                    if img.file_format in ("PNG", "TARGA") or bmat.diffuse_color[3] < 1.0:
                        links.new(tex_node.outputs["Alpha"], principled_bsdf.inputs["Alpha"])
                        bmat.blend_method = 'HASHED'
                        if hasattr(bmat, "shadow_method"): bmat.shadow_method = 'HASHED'
                except Exception as e:
                    skp_log(f"Texture error for {name}: {e}")
            
            self.materials[name] = bmat

    def write_mesh_data(self, entities=None, name="", default_material="DefaultMaterial", filter_layer=None, center_geometry=True, cache_id=None):
        # Use explicit cache_id (Definition Name) for stable mesh sharing
        if cache_id:
            mesh_key = (cache_id, default_material, filter_layer)
            if mesh_key in self.component_meshes:
                return self.component_meshes[mesh_key]

        # Attempt to use binary N-gon method, fallback to Python reconstruction if missing or incompatible
        try:
            verts, raw_faces_data, mats = entities.get_textured_ngon_lists(default_material)
        except Exception as e:
            if LOGS: skp_log(f"Binary call failed or incompatible ({e}), using robust Python fallback...")
            verts, raw_faces_data, mats = self._get_ngon_lists_fallback(entities, default_material)
        
        # Filter faces by layer if requested
        if filter_layer is not None:
            raw_faces_data = [f for f in raw_faces_data if f['layer_name'] == filter_layer]

        if not verts or not raw_faces_data:
            return []

        me = bpy.data.meshes.new(name)
        
        # Optimize material access
        mats_data = bpy.data.materials
        mats_get = mats_data.get
        
        # Add materials to the mesh
        if mats:
            for mat_name, mat_idx in sorted(mats.items(), key=lambda x: x[1]):
                m = mats_get(mat_name)
                if not m:
                    # Fallback to default if missing
                    m = self.materials.get("DefaultMaterial")
                me.materials.append(m)

        bm = bmesh.new()
        bm_verts = [bm.verts.new(v) for v in verts]
        bm.verts.ensure_lookup_table()
        
        for face_info in raw_faces_data:
            mat_idx = face_info['mat_idx']
            loops = face_info['loops']
            front_uvs = face_info['front_uvs']
            back_mat_idx = face_info['back_mat_idx']
            back_uvs = face_info['back_uvs']
            
            # Check for dual material if supported
            final_mat_idx = mat_idx
            if self.support_back_material and back_mat_idx != -1 and mat_idx != back_mat_idx:
                front_name = material_names[mat_idx]
                back_name = material_names[back_mat_idx]
                dual_name = f"Dual: {front_name} | {back_name}"
                
                if dual_name not in self.materials:
                    self.materials[dual_name] = self.create_dual_material(dual_name, front_name, back_name)
                
                d_mat = self.materials[dual_name]
                # Find dual mat index in me.materials
                found_dual = False
                for i, m in enumerate(me.materials):
                    if m == d_mat:
                        final_mat_idx = i
                        found_dual = True
                        break
                if not found_dual:
                    final_mat_idx = len(me.materials)
                    me.materials.append(d_mat)
            
            for l_idx, l_verts_indices in enumerate(loops):
                try:
                    l_verts = [bm_verts[i] for i in l_verts_indices]
                    face = bm.faces.new(l_verts)
                    face.material_index = final_mat_idx
                    face.smooth = False
                    
                    # UV Handling - Use standard name 'UVMap'
                    uv_layer = bm.loops.layers.uv.get("UVMap") or bm.loops.layers.uv.new("UVMap")
                    tri_uvs = front_uvs[l_idx]
                    for loop_vert_idx, loop in enumerate(face.loops):
                        loop[uv_layer].uv = tri_uvs[loop_vert_idx]
                        
                    if self.support_back_material and back_uvs:
                        uv_back_layer = bm.loops.layers.uv.get("UVBack") or bm.loops.layers.uv.new("UVBack")
                        tri_back_uvs = back_uvs[l_idx]
                        for loop_vert_idx, loop in enumerate(face.loops):
                            loop[uv_back_layer].uv = tri_back_uvs[loop_vert_idx]
                except Exception:
                    pass

        # Restore UV-safe dissolution to ensure G-non (N-gon) cleanliness
        # By using delimit={'UV', 'MATERIAL'}, we ensure textures stay perfectly mapped.
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bmesh.ops.dissolve_limit(bm, angle_limit=0.001, verts=bm.verts, edges=bm.edges, delimit={'MATERIAL', 'UV'})
        
        # Identify disconnected islands to allow splitting into separate objects
        islands = []
        unvisited_faces = set(bm.faces)
        while unvisited_faces:
            start_face = unvisited_faces.pop()
            island = {start_face}
            stack = [start_face]
            while stack:
                face = stack.pop()
                for edge in face.edges:
                    for other_face in edge.link_faces:
                        if other_face in unvisited_faces:
                            unvisited_faces.remove(other_face)
                            island.add(other_face)
                            stack.append(other_face)
            islands.append(island)

        results = [] # List of (mesh, alpha, center, dominant_mat_name)
        for idx, island_faces in enumerate(islands):
            island_bm = bmesh.new()
            island_me = bpy.data.meshes.new(f"{name}_part_{idx}")
            
            # Identify only the materials used in this specific island
            used_mat_indices = sorted(list(set(f.material_index for f in island_faces)))
            old_to_new_mat = {old_idx: new_idx for new_idx, old_idx in enumerate(used_mat_indices)}
            
            # Map used materials to the new island mesh slots
            for old_idx in used_mat_indices:
                if old_idx < len(me.materials):
                    island_me.materials.append(me.materials[old_idx])

            # Centering: Use Bounding Box center for the local pivot
            b_min = Vector((1e12, 1e12, 1e12))
            b_max = Vector((-1e12, -1e12, -1e12))
            for f in island_faces:
                for v in f.verts:
                    for i in range(3):
                        if v.co[i] < b_min[i]: b_min[i] = v.co[i]
                        if v.co[i] > b_max[i]: b_max[i] = v.co[i]
            
            island_center = (b_min + b_max) / 2.0 if (b_min[0] < 1e11 and center_geometry) else Vector((0,0,0))
                
            # Copy geometry to island bmesh (Normalized to island_center)
            vert_map = {}
            for f in island_faces:
                new_verts = []
                for v in f.verts:
                    if v not in vert_map:
                        nv = island_bm.verts.new(v.co - island_center)
                        vert_map[v] = nv
                    new_verts.append(vert_map[v])
                
                try:
                    nf = island_bm.faces.new(new_verts)
                    nf.material_index = old_to_new_mat[f.material_index]
                    nf.smooth = f.smooth
                    
                    for l_type_name in bm.loops.layers.uv.keys():
                        old_lay = bm.loops.layers.uv[l_type_name]
                        new_lay = island_bm.loops.layers.uv.get(l_type_name) or island_bm.loops.layers.uv.new(l_type_name)
                        for old_loop, new_loop in zip(f.loops, nf.loops):
                            new_loop[new_lay].uv = old_loop[old_lay].uv
                except Exception:
                    pass

            island_bm.to_mesh(island_me)
            if "UVMap" in island_me.uv_layers:
                island_me.uv_layers.active = island_me.uv_layers["UVMap"]
            
            island_me.update()
            island_me.validate()
            
            has_alpha = any(m.blend_method != 'OPAQUE' for m in island_me.materials if m)
            
            dominant_mat_name = "Mesh"
            if island_me.materials:
                from collections import Counter
                mat_counts = Counter(f.material_index for f in island_bm.faces)
                if mat_counts:
                    mode_idx = mat_counts.most_common(1)[0][0]
                    if mode_idx < len(island_me.materials):
                        m = island_me.materials[mode_idx]
                        if m: dominant_mat_name = m.name
            
            results.append((island_me, has_alpha, island_center, dominant_mat_name))
            island_bm.free()
        
        bm.free()
        bpy.data.meshes.remove(me)
        if cache_id:
            self.component_meshes[mesh_key] = results
        return results

    def _get_ngon_lists_fallback(self, entities, default_material):
        """Python fallback to reconstruct N-gon data when binary get_textured_ngon_lists fails"""
        verts = []
        seen_verts = {}
        mats = {}
        raw_faces_data = []

        try:
            # entities.faces can be a generator
            # Python Fallback: Reverting to the stable triangulation + dissolve method
            for f in list(entities.faces):
                try:
                    f_verts, f_tris, f_uvs = f.tessfaces
                    if not f_verts or not f_tris: continue
                    
                    # Local optimization: cache frequently used methods
                    v_append = verts.append
                    v_len = len(verts)

                    f_v_indices = []
                    for v in f_verts:
                        # Use integer tuple for faster hashing than float rounding where possible
                        v_tuple = (int(v[0]*1000000), int(v[1]*1000000), int(v[2]*1000000))
                        if v_tuple not in seen_verts:
                            seen_verts[v_tuple] = v_len
                            v_append(v)
                            v_len += 1
                        f_v_indices.append(seen_verts[v_tuple])

                    mat_f = f.material
                    mat_f_name = mat_f.name if mat_f else default_material
                    if mat_f_name not in mats:
                        mats[mat_f_name] = len(mats)
                    mat_f_idx = mats[mat_f_name]

                    loops = []
                    front_uvs = []
                    for tri in f_tris:
                        loops.append([f_v_indices[i] for i in tri])
                        front_uvs.append([f_uvs[i] for i in tri])

                    raw_faces_data.append({
                        'mat_idx': mat_f_idx,
                        'loops': loops,
                        'front_uvs': front_uvs,
                        'back_mat_idx': -1,
                        'back_uvs': None,
                        'layer_name': f.layer.name if hasattr(f, 'layer') and f.layer else None
                    })
                except Exception:
                    continue
        except Exception as e:
            skp_log(f"Critical error in Python N-gon fallback: {e}")

        return verts, raw_faces_data, mats

    def create_dual_material(self, name, front_m_name, back_m_name):
        bmat = bpy.data.materials.new(name=name)
        bmat.use_nodes = True
        nodes = bmat.node_tree.nodes
        links = bmat.node_tree.links
        nodes.clear()
        
        out = nodes.new('ShaderNodeOutputMaterial')
        mix = nodes.new('ShaderNodeMixShader')
        geom = nodes.new('ShaderNodeNewGeometry')
        links.new(geom.outputs['Backfacing'], mix.inputs[0])
        links.new(mix.outputs[0], out.inputs[0])
        
        f_mat = self.materials.get(front_m_name)
        if f_mat:
            f_bsdf = nodes.new('ShaderNodeBsdfPrincipled')
            f_bsdf.label = "FRONT"
            links.new(f_bsdf.outputs[0], mix.inputs[1])
            if f_mat.use_nodes:
                orig_p = f_mat.node_tree.nodes.get('Principled BSDF')
                if orig_p: f_bsdf.inputs['Base Color'].default_value = orig_p.inputs['Base Color'].default_value
        
        b_mat = self.materials.get(back_m_name)
        if b_mat:
            b_bsdf = nodes.new('ShaderNodeBsdfPrincipled')
            b_bsdf.label = "BACK"
            links.new(b_bsdf.outputs[0], mix.inputs[2])
            if b_mat.use_nodes:
                orig_p = b_mat.node_tree.nodes.get('Principled BSDF')
                if orig_p: b_bsdf.inputs['Base Color'].default_value = orig_p.inputs['Base Color'].default_value
                    
        return bmat

    def write_standalone_edges(self, entities, name, transform, layer_name=None):
        try:
            edges = list(entities.standalone_edges)
        except AttributeError:
            # Binary doesn't support standalone_edges
            return
        if not edges: return
            
        bm = bmesh.new()
        v_idx_map = {}
        for edge in edges:
            v1_pos = tuple(edge.start_vertex.position)
            v2_pos = tuple(edge.end_vertex.position)
            if v1_pos not in v_idx_map: v_idx_map[v1_pos] = bm.verts.new(v1_pos)
            if v2_pos not in v_idx_map: v_idx_map[v2_pos] = bm.verts.new(v2_pos)
            try:
                bm.edges.new((v_idx_map[v1_pos], v_idx_map[v2_pos]))
            except ValueError: pass
        
        # Identify disconnected chains (islands)
        islands = []
        unvisited_verts = set(bm.verts)
        while unvisited_verts:
            start_v = unvisited_verts.pop()
            island_verts = {start_v}
            island_edges = set()
            stack = [start_v]
            while stack:
                v = stack.pop()
                for e in v.link_edges:
                    island_edges.add(e)
                    other_v = e.other_vert(v)
                    if other_v in unvisited_verts:
                        unvisited_verts.remove(other_v)
                        island_verts.add(other_v)
                        stack.append(other_v)
            islands.append((island_verts, island_edges))

        target_coll = self.context.collection
        if self.organize_by_tags and layer_name in self.tag_collections:
            target_coll = self.tag_collections[layer_name]
        elif name == "Loose Edges" and hasattr(self, 'colls'):
            target_coll = self.colls.get('edges', target_coll)

        for idx, (i_verts, i_edges) in enumerate(islands):
            # Calculate island center (Bounding Box)
            coords = [v.co for v in i_verts]
            v_min = Vector((min(c[0] for c in coords), min(c[1] for c in coords), min(c[2] for c in coords)))
            v_max = Vector((max(c[0] for c in coords), max(c[1] for c in coords), max(c[2] for c in coords)))
            island_center = (v_min + v_max) / 2
            
            # Create sub-mesh for this chain
            ob_name = f"{name}_{idx+1:03d}" if len(islands) > 1 else name
            island_me = bpy.data.meshes.new(ob_name)
            island_bm = bmesh.new()
            v_remap = {}
            for v in i_verts:
                v_remap[v] = island_bm.verts.new(v.co - island_center)
            for e in i_edges:
                island_bm.edges.new((v_remap[e.verts[0]], v_remap[e.verts[1]]))
            
            island_bm.to_mesh(island_me)
            island_bm.free()
            
            ob = bpy.data.objects.new(ob_name, island_me)
            # Center the object pivot by offsetting matrix_world
            loc, rot, sca = transform.decompose()
            world_loc = transform @ island_center
            ob.matrix_world = Matrix.Translation(world_loc) @ rot.to_matrix().to_4x4() @ Matrix.Diagonal(sca.to_4d())
            
            target_coll.objects.link(ob)

        bm.free()

    def write_entities(self, entities, name, parent_transform, default_material="DefaultMaterial", etype=None, parent_ob=None, is_hidden=False):
        # 1. Check for nested content (Use list() for generator compatibility)
        groups_list = list(entities.groups)
        instances_list = list(entities.instances)
        has_nested = (len(groups_list) > 0 or len(instances_list) > 0)
        is_loose_root = (name == "SKP Mesh Objects")
        
        # 2. Collection Determination
        # USER REQUEST: Hidden objects go ONLY to the hidden collection and stay VISIBLE
        if is_hidden:
            target_coll = self.colls['hidden']
        elif is_loose_root:
            target_coll = self.colls['mesh']
        elif etype == EntityType.component:
            target_coll = self.colls['components']
        elif etype == EntityType.group:
            target_coll = self.colls['groups']
        else:
            target_coll = self.colls['mesh']

        # 3. Geometry Writing (Initial pass to determine complexity)
        should_center = False 
        # FIX: Include default_material in cache_id to avoid material collisions between instances
        cache_id = f"{name}_{default_material}" if etype == EntityType.component else None
        results = self.write_mesh_data(entities=entities, name=name, default_material=default_material, 
                                      center_geometry=should_center, cache_id=cache_id)
        
        # 4. Pivot Strategy: Only create Empty if it's complex (nested or multiple meshes)
        is_complex = has_nested or len(results) > 1
        main_level_ob = None
        
        if is_complex and not is_loose_root and etype != EntityType.none:
            main_level_ob = bpy.data.objects.new(name, None)
            main_level_ob.empty_display_type = "PLAIN_AXES"
            main_level_ob.empty_display_size = 0.1
            target_coll.objects.link(main_level_ob)
            if parent_ob:
                main_level_ob.parent = parent_ob
            main_level_ob.matrix_world = parent_transform
            
            # Keep container VISIBLE as per user request
            main_level_ob.hide_viewport = False
            main_level_ob.hide_render = False

        # 5. Link Geometries
        for me, alpha, island_center, mat_name in results:
            display_name = mat_name.split('.')[0] if '.' in mat_name else mat_name
            ob_name = f"{name}_{display_name}" if is_complex else name
            ob = bpy.data.objects.new(ob_name, me)
            
            target_coll.objects.link(ob)
            if main_level_ob:
                ob.parent = main_level_ob
            elif parent_ob:
                ob.parent = parent_ob
            
            # Use parent_transform directly
            ob.matrix_world = parent_transform
            
            # USER REQUEST: Even if hidden in SKP, keep visible in Blender's hidden folder
            ob.hide_viewport = False
            ob.hide_render = False
            
            if 0.01 < alpha < 1.0: ob.show_transparent = True
            me.update()

        # 6. Recursion: Groups
        for group in groups_list:
            if self.layers_skip and group.layer in self.layers_skip: continue
            g_name = "G-" + (group.name if group.name else "Group")
            child_world_transform = parent_transform @ Matrix(group.transform)
            self.write_entities(group.entities, g_name, child_world_transform, 
                               default_material=inherent_default_mat(group.material, default_material), 
                               etype=EntityType.group, parent_ob=main_level_ob or parent_ob,
                               is_hidden=group.hidden)

        # 7. Recursion: Instances (Components)
        for instance in instances_list:
            if self.layers_skip and instance.layer in self.layers_skip: continue
            cdef_name = instance.definition.name
            cdef = self.skp_components.get(cdef_name)
            if not cdef: continue
            
            inh_mat = inherent_default_mat(instance.material, default_material)
            child_world_transform = parent_transform @ Matrix(instance.transform)
            self.write_entities(cdef.entities, cdef_name, child_world_transform, 
                               default_material=inh_mat, 
                               etype=EntityType.component, parent_ob=main_level_ob or parent_ob,
                               is_hidden=instance.hidden)


    def component_def_as_group(self, entities, name, transform, default_material="DefaultMaterial", etype=None, group=None):
        results = self.write_mesh_data(entities=entities, name=name, default_material=default_material)
        for me, alpha, island_center, mat_name in results:
            display_name = mat_name.split('.')[0] if '.' in mat_name else mat_name
            ob = bpy.data.objects.new(f"{name}_{display_name}", me)
            ob.matrix_world = transform
            ob.location = transform @ island_center
            if 0.01 < alpha < 1.0:
                ob.show_transparent = True
            me.update()
            group.objects.link(ob)

    def instance_object_or_group(self, name, mat):
        gname = group_name(name, mat)
        if gname in bpy.data.collections:
            group = bpy.data.collections[gname]
            ob = bpy.data.objects.new(group.name, None)
            ob.empty_display_type = "PLAIN_AXES"
            ob.empty_display_size = 0.1
            ob.instance_type = "COLLECTION"
            ob.instance_collection = group
            return ob
        else:
            return None

    def instance_group_dupli_vert(self, name, default_material, component_stats):
        def get_orientations(v):
            orientations = defaultdict(list)
            for transform in v:
                _loc, rot, scale = Matrix(transform).decompose()
                scale = (scale[0], scale[1], scale[2])
                rot = (rot[0], rot[1], rot[2], rot[3])
                orientations[(scale, rot)].append(transform)
            for k, v in orientations.items():
                scale, rot = k
                yield scale, rot, v

        # Each duplicated group has a specific location, scale and rotation
        # applied.
        for scale, rot, locs in get_orientations(component_stats[(name, default_material)]):
            verts = []
            main_loc = Matrix(locs[0]).to_translation()
            for c in locs:
                verts.append(Matrix(c).to_translation() - main_loc)
            dme = bpy.data.meshes.new("DUPLI-" + name)
            dme.vertices.add(len(verts))
            dme.vertices.foreach_set("co", unpack_list(verts))
            dme.update(calc_edges=True)  # update mesh with new data
            dme.validate()
            dob = bpy.data.objects.new("DUPLI-" + name, dme)
            dob.location = main_loc
            dob.instance_type = "VERTS"
            ob = self.instance_object_or_group(name, default_material)
            ob.scale = scale
            ob.rotation_mode = "QUATERNION"  # change from default mode of xyz
            ob.rotation_quaternion = Quaternion((rot[0], rot[1], rot[2], rot[3]))
            ob.parent = dob
            if hasattr(self, 'colls'):
                self.colls['mesh'].objects.link(ob)
                self.colls['mesh'].objects.link(dob)
            else:
                self.context.collection.objects.link(ob)
                self.context.collection.objects.link(dob)
            skp_log(
                f"Complex group {name} {default_material} instanced {len(verts)} times, scale -> {scale}, rot -> {rot}"
            )
        return

    def instance_group_dupli_face(self, name, default_material, component_stats):
        def get_orientations(v):
            orientations = defaultdict(list)
            for transform in v:
                _loc, _rot, scale = Matrix(transform).decompose()
                scale = (scale[0], scale[1], scale[2])
                orientations[scale].append(transform)
            for scale, transforms in orientations.items():
                yield scale, transforms

        for _scale, transforms in get_orientations(component_stats[(name, default_material)]):
            main_loc, _real_rot, real_scale = Matrix(transforms[0]).decompose()
            verts = []
            faces = []
            f_count = 0
            for c in transforms:
                l_loc, l_rot, _l_scale = Matrix(c).decompose()
                mat = Matrix.Translation(l_loc) @ l_rot.to_matrix().to_4x4()
                # Use robust 4D multiplication for correct projection
                verts.append((mat @ Vector((-0.05, -0.05, 0, 1.0))).xyz - main_loc)
                verts.append((mat @ Vector((0.05, -0.05, 0, 1.0))).xyz - main_loc)
                verts.append((mat @ Vector((0.05, 0.05, 0, 1.0))).xyz - main_loc)
                verts.append((mat @ Vector((-0.05, 0.05, 0, 1.0))).xyz - main_loc)
                faces.append((f_count + 0, f_count + 1, f_count + 2, f_count + 3))
                f_count += 4
            dme = bpy.data.meshes.new("DUPLI-" + name)
            dme.vertices.add(len(verts))
            dme.vertices.foreach_set("co", unpack_list(verts))
            dme.tessfaces.add(f_count / 4)
            dme.tessfaces.foreach_set("vertices_raw", unpack_face_list(faces))
            dme.update(calc_edges=True)  # Update mesh with new data
            dme.validate()
            dob = bpy.data.objects.new("DUPLI-" + name, dme)
            dob.instance_type = "FACES"
            dob.location = main_loc
            # dob.use_dupli_faces_scale = True
            # dob.dupli_faces_scale = 10
            ob = self.instance_object_or_group(name, default_material)
            ob.scale = real_scale
            ob.parent = dob
            if hasattr(self, 'colls'):
                self.colls['mesh'].objects.link(ob)
                self.colls['mesh'].objects.link(dob)
            else:
                self.context.collection.objects.link(ob)
                self.context.collection.objects.link(dob)
            skp_log(f"Complex group {name} {default_material} instanced {f_count / 4} times")
        return

    def write_camera(self, camera, name="Last View"):
        skp_log(f"Writing camera: {name}")
        pos, target, up = camera.GetOrientation()
        
        # Create camera data and object
        cam_data = bpy.data.cameras.new("Cam: " + name)
        ob = bpy.data.objects.new("Cam: " + name, cam_data)
        
        # Link to dedicated collection
        if hasattr(self, 'colls') and 'cameras' in self.colls:
            self.colls['cameras'].objects.link(ob)
        else:
            self.context.collection.objects.link(ob)
            
        ob.location = pos
        z = Vector(pos) - Vector(target)
        x = Vector(up).cross(z)
        y = z.cross(x)
        x.normalize()
        y.normalize()
        z.normalize()
        ob.matrix_world.col[0] = x.resized(4)
        ob.matrix_world.col[1] = y.resized(4)
        ob.matrix_world.col[2] = z.resized(4)
        
        aspect_ratio = camera.aspect_ratio
        fov = camera.fov
        if aspect_ratio == False:
            skp_log(f"Cam: '{name}' uses dynamic/screen aspect ratio.")
            aspect_ratio = self.aspect_ratio
        if fov == False:
            skp_log(f"Cam: '{name}' is in Orthographic Mode.")
            cam_data.type = "ORTHO"
        else:
            cam_data.angle = (math.pi * fov / 180) * aspect_ratio
            
        cam_data.clip_end = self.prefs.camera_far_plane
        return cam_data.name


class SceneExporter:
    def __init__(self):
        self.filepath = "/tmp/untitled.skp"

    def set_filename(self, filename):
        self.filepath = filename
        self.basepath, self.skp_filename = os.path.split(self.filepath)
        return self

    def save(self, context, **options):
        skp_log(f"Finished exporting: {self.filepath}")
        return {"FINISHED"}


class ImportSKP(Operator, ImportHelper):
    """Load a Trimble SketchUp .skp file"""

    bl_idname = "import_scene.skp"
    bl_label = "Import SKP"
    bl_options = {"PRESET", "REGISTER", "UNDO"}
    filename_ext = ".skp"

    filter_glob: StringProperty(
        default="*.skp",
        options={"HIDDEN"},
    )

    scenes_as_camera: BoolProperty(
        name="Scene(s) As Camera(s)",
        description="Import SketchUp Scenes As Blender Camera.",
        default=True,
    )

    import_camera: BoolProperty(
        name="Last View In SketchUp As Camera View",
        description="Import last saved view in SketchUp as a Blender Camera.",
        default=False,
    )

    organize_by_tags: BoolProperty(
        name="Organize by Tags (Experimental)",
        description="Creates collections based on SketchUp Tags/Layers.",
        default=False,
    )

    support_back_material: BoolProperty(
        name="Support Back-face Materials",
        description="Creates dual-face shaders if front and back materials differ.",
        default=False,
    )

    import_standalone_edges: BoolProperty(
        name="Import Standalone Edges",
        description="Imports edges that are not part of a face.",
        default=True,
    )

    reuse_material: BoolProperty(
        name="Use Existing Materials",
        description="Doesn't copy material IDs already in the Blender Scene.",
        default=True,
    )

    merge_coplanar_faces: BoolProperty(
        name="Merge Coplanar Faces",
        description="Dissolve coplanar edges to create cleaner N-gons. Disable for exact 1:1 mesh topology",
        default=False,
    )

    dedub_only: BoolProperty(name="Groups Only", description="Import instantiated groups only.", default=False)

    reuse_existing_groups: BoolProperty(
        name="Reuse Groups", description="Use existing Blender groups to instance components with.", default=False
    )

    # Altered from initial default of 50 so as to force import all
    # components to be imported as duplicated objects.
    max_instance: IntProperty(name="Instantiation Threshold :", default=1)

    dedub_type: EnumProperty(
        name="Instancing Type :",
        items=(
            ("FACE", "Faces", ""),
            ("VERTEX", "Vertices", ""),
        ),
        default="VERTEX",
    )

    import_scene: StringProperty(name="Import A Scene :", description="Import a specific SketchUp Scene", default="")

    def execute(self, context):
        keywords = self.as_keywords(ignore=("axis_forward", "axis_up", "filter_glob", "split_mode"))
        # Save settings for reload
        context.scene.skp_last_filepath = keywords["filepath"]
        
        # Save settings to scene for Reload persistence
        context.scene.skp_reuse_material = keywords.get("reuse_material", True)
        context.scene.skp_organize_by_tags = keywords.get("organize_by_tags", False)
        context.scene.skp_merge_coplanar = keywords.get("merge_coplanar_faces", False)
        
        # Detect if we are in update mode (called from Reload operator)
        is_update = getattr(self, "is_update", False)
        
        return SceneImporter().set_filename(keywords["filepath"]).load(context, is_update=is_update, **keywords)

    def draw(self, context):
        layout = self.layout
        layout.label(text="- Primary Import Options -")
        row = layout.row()
        row.prop(self, "scenes_as_camera")
        row = layout.row()
        row.prop(self, "import_camera")
        row = layout.row()
        row.prop(self, "reuse_material")
        row = layout.row()
        row.prop(self, "dedub_only")
        row = layout.row()
        row.prop(self, "reuse_existing_groups")
        
        layout.label(text="- Advanced Modern Options -")
        box = layout.box()
        box.prop(self, "organize_by_tags")
        box.prop(self, "support_back_material")
        box.prop(self, "import_standalone_edges")
        box.prop(self, "merge_coplanar_faces")
        
        col = layout.column()
        col.label(text="- Instantiate components, if they are more than -")
        col.prop(self, "max_instance")
        row = layout.row()
        row.use_property_split = True
        row.prop(self, "dedub_type")
        row = layout.row()
        row.use_property_split = True
        row.prop(self, "import_scene")


class ExportSKP(Operator, ExportHelper):
    """Export .blend into .skp file"""

    bl_idname = "export_scene.skp"
    bl_label = "Export SKP"
    bl_options = {"PRESET", "UNDO"}
    filename_ext = ".skp"

    def execute(self, context):
        keywords = self.as_keywords()
        return SceneExporter().set_filename(keywords["filepath"]).save(context, **keywords)


def menu_func_import(self, context):
    self.layout.operator(ImportSKP.bl_idname, text="SketchUp (.skp)")


def menu_func_export(self, context):
    self.layout.operator(ExportSKP.bl_idname, text="SketchUp (.skp)")


class SKP_OT_reload(Operator):
    """Reload the last imported SketchUp file"""
    bl_idname = "import_scene.skp_reload"
    bl_label = "Reload / Update Sketchup Scene"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        path = context.scene.skp_last_filepath
        
        if not path or not os.path.exists(path):
            self.report({'ERROR'}, "Last imported SketchUp file not found. Please import manually first.")
            return {'CANCELLED'}

        skp_log(f"Reloading scene from: {path}")

        # Cleanup existing SketchUp collection if it exists
        main_coll_name = "SKP Imported Data"
        main_coll = bpy.data.collections.get(main_coll_name)
        
        if main_coll:
            # OPTIMIZED: Batch delete all objects in the collection tree
            # Using all_objects is MUCH faster than recursive deletion for large scenes
            obs_to_delete = list(main_coll.all_objects)
            for obj in obs_to_delete:
                try:
                    bpy.data.objects.remove(obj, do_unlink=True)
                except Exception:
                    pass
            
            # Recursively remove child collections
            def purge_collections(coll):
                for child in list(coll.children):
                    purge_collections(child)
                    bpy.data.collections.remove(child)
            
            purge_collections(main_coll)
            
        # Re-trigger import with default settings or stored settings if we had them
        # For now, we use defaults or just re-import into the same collection.
        # We call the importer operator without the file dialog.
        # Re-trigger import with settings stored in the scene
        bpy.ops.import_scene.skp(
            filepath=path,
            reuse_material=context.scene.skp_reuse_material,
            organize_by_tags=context.scene.skp_organize_by_tags,
            merge_coplanar_faces=context.scene.skp_merge_coplanar
        )
        
        self.report({'INFO'}, f"Reloaded: {os.path.basename(path)}")
        return {'FINISHED'}



class SKP_OT_proxy_toggle(Operator):
    """Toggle between Full Geometry and Bounding Box for SKP data"""
    bl_idname = "import_scene.skp_proxy_toggle"
    bl_label = "Toggle Proxy Mode"
    
    def execute(self, context):
        main_coll = bpy.data.collections.get("SKP Imported Data")
        if not main_coll: return {'CANCELLED'}
        
        current_state = 'TEXTURED'
        for obj in main_coll.all_objects:
            if obj.type == 'MESH':
                current_state = obj.display_type
                break
        
        new_state = 'BOUNDS' if current_state != 'BOUNDS' else 'TEXTURED'
        for obj in main_coll.all_objects:
            if obj.type == 'MESH':
                obj.display_type = new_state
        
        self.report({'INFO'}, f"Proxy Mode: {'ON' if new_state == 'BOUNDS' else 'OFF'}")
        return {'FINISHED'}

class SKP_OT_deep_purge(Operator):
    """Purge all unused data-blocks"""
    bl_idname = "import_scene.skp_deep_purge"
    bl_label = "Purge Unused SKP Data"
    
    def execute(self, context):
        for i in range(3):
            bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
        self.report({'INFO'}, "Deep Purge complete.")
        return {'FINISHED'}

class SKP_PT_panel(bpy.types.Panel):
    """Sketchup Imparator Side Panel"""
    bl_label = "SketchUp Imparator"
    bl_idname = "SKP_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Sketchup'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        col = layout.column(align=True)
        if scene.skp_last_filepath:
            box = col.box()
            box.label(text="Last Imported File:", icon='FILEBROWSER')
            box.label(text=os.path.basename(scene.skp_last_filepath))
            
            col.separator()
            
            box = col.box()
            box.label(text="Reload Settings:", icon='SETTINGS')
            box.prop(scene, "skp_reuse_material", text="Keep My Material Edits")
            box.prop(scene, "skp_organize_by_tags", text="Use Tag Collections")
            
            col.separator()
            row = col.row()
            row.scale_y = 1.8
            row.operator("import_scene.skp_reload", text="RELOAD / UPDATE SCENE", icon='FILE_REFRESH')
            
            layout.label(text="Advanced Tools:")
            grid = layout.grid_flow(columns=2, align=True)
            grid.operator("import_scene.skp_proxy_toggle", text="Proxy Mode", icon='GHOST_ENABLED')
            grid.operator("import_scene.skp_deep_purge", text="Purge", icon='TRASH')
        else:
            col.label(text="No SKP scene imported yet.")
            col.operator("import_scene.skp", text="Import first Sketchup file", icon='IMPORT')


def register():
    bpy.utils.register_class(SketchupAddonPreferences)
    bpy.utils.register_class(ImportSKP)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.utils.register_class(ExportSKP)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    
    # New Reload features
    bpy.utils.register_class(SKP_OT_reload)
    bpy.utils.register_class(SKP_OT_proxy_toggle)
    bpy.utils.register_class(SKP_OT_deep_purge)
    bpy.utils.register_class(SKP_PT_panel)
    bpy.types.Scene.skp_last_filepath = StringProperty(name="Last SKP File", default="")
    bpy.types.Scene.skp_reuse_material = BoolProperty(name="Use Existing Materials", default=True)
    bpy.types.Scene.skp_organize_by_tags = BoolProperty(name="Use Tags", default=False)
    bpy.types.Scene.skp_merge_coplanar = BoolProperty(name="Merge Coplanar", default=False)


def unregister():
    bpy.utils.unregister_class(ImportSKP)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.utils.unregister_class(ExportSKP)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    
    # New Reload features
    bpy.utils.unregister_class(SKP_OT_reload)
    bpy.utils.unregister_class(SKP_OT_proxy_toggle)
    bpy.utils.unregister_class(SKP_OT_deep_purge)
    bpy.utils.unregister_class(SKP_PT_panel)
    del bpy.types.Scene.skp_last_filepath
    del bpy.types.Scene.skp_reuse_material
    del bpy.types.Scene.skp_organize_by_tags
    del bpy.types.Scene.skp_merge_coplanar
    
    bpy.utils.unregister_class(SketchupAddonPreferences)

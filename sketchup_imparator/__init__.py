import math
import os
import shutil
import tempfile
import time
import gc
from collections import defaultdict
try:
    import numpy as np
except ImportError:
    np = None
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
    "version": (2026, 6, 0, 0),
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
    
    skp_keep_smoothing: BoolProperty(
        name="Keep Smoothing After Reload",
        description="Automatically restore 'Smooth by Angle' modifiers during scene updates",
        default=True
    )

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
        
        layout.label(text="- Preservation Options -")
        row = layout.row()
        row.prop(self, "skp_keep_smoothing")


def skp_log(*args):
    # Log output by pre-pending "SU |"
    if args:
        print("SketchUp Imparator |", *args)





def get_collection(name, parent):
    if not parent:
        parent = bpy.context.scene.collection
    coll = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    if name not in parent.children.keys():
        parent.children.link(coll)
    return coll


def init_skp_collections(filepath):
    import os
    base_name = os.path.basename(filepath)
    root_name = f"SKP: {base_name}"
    prefix = base_name.split('.')[0] + "_"
    
    # 1. Create a single Root Collection for easy visibility toggle
    root_coll = get_collection(root_name, None)
    root_coll["skp_filepath"] = filepath
    root_coll["skp_version"] = "2026.6.0.0"

    # FIX: ROOT Empty removed entirely (no leftover dot at origin).
    root_empty = None

    # FIX: Collections for outliner bulk grouping (no parent lines).
    # Groups/components separated in outliner, objects not parented to ROOT.
    def get_subcoll(name, parent_coll):
        coll = bpy.data.collections.get(name) or bpy.data.collections.new(name)
        if name not in parent_coll.children.keys():
            parent_coll.children.link(coll)
        return coll

    groups_coll = get_subcoll(prefix + "GROUPS", root_coll)
    components_coll = get_subcoll(prefix + "COMPONENTS", root_coll)
    mesh_coll = get_subcoll(prefix + "MESH", root_coll)
    edges_coll = get_subcoll(prefix + "EDGES", root_coll)

    colls = {
        'root_coll': root_coll,
        'root_empty': root_empty,
        'components_node': components_coll,
        'groups_node': groups_coll,
        'mesh_node': mesh_coll,
        'edges_node': edges_coll,
        'hidden_node': root_empty  # alias, hidden stays in own type collection
    }
    return colls


    # Hide the hidden objects collection in viewport
    pass  # Removed data block hide
    return colls


def hide_one_level():
    context = bpy.context
    if not context.screen:
        return

    outliners = [a for a in context.screen.areas if a.type == "OUTLINER"]
    for ol in outliners:
        try:
            with context.temp_override(area=ol):
                bpy.ops.outliner.show_one_level(open=False)
            ol.tag_redraw()
        except Exception:
            pass

    # context.view_layer.update()




class SceneImporter:
    def __init__(self):
        self.skp_model = None
        self.filepath = ""
        self.filename_prefix = ""  # Used to isolate data between multiple imports
        self.materials = {}
        self.materials_scales = {}
        self.texture_scales = {}
        self.component_meshes = {}
        self.group_written = {}
        self.component_stats = defaultdict(list)
        self.instance_counts = defaultdict(int)
        self.max_instance = 50

    def set_filename(self, filename):
        self.filepath = filename
        self.basepath, self.skp_filename = os.path.split(self.filepath)
        return self  # allow chaining

    def load(self, context, is_update=False, **options):
        """Load a SketchUp file"""
        # 0. Unit Sync: Ensure Blender is in Metric Meters for correct scale
        context.scene.unit_settings.system = 'METRIC'
        context.scene.unit_settings.scale_length = 1.0
        context.scene.unit_settings.length_unit = 'METERS'
        
        # Blender settings
        self.context = context
        self.import_standalone_edges = options.get("import_standalone_edges", False)
        self.support_back_material = options.get("support_back_material", False)
        self.merge_coplanar_faces = options.get("merge_coplanar_faces", False)
        self.reuse_material = options.get("reuse_material", True)
        self.smart_pbr = options.get("smart_pbr", True)
        self.reuse_group = options.get("reuse_existing_groups", False)
        self.max_instance = options.get("max_instance", 50)
        self.component_stats = defaultdict(list)
        self.component_skip = proxy_dict()
        self.component_depth = proxy_dict()
        self.group_written = {}
        ren_res_x = context.scene.render.resolution_x
        ren_res_y = context.scene.render.resolution_y
        self.aspect_ratio = ren_res_x / ren_res_y
        self.scene = None
        self.layers_skip = []
        self.mesh_cache = {} # Cache for component definition meshes (reuse data)

        # Start stopwatch for overall import
        _time_main = time.time()

        # Log filename being imported
        if LOGS:
            skp_log(f"Importing: {self.filepath}")
        
        # Set unique prefix for this import session
        import os
        self.filename_prefix = os.path.basename(self.filepath).split('.')[0] + "_"
        
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

            # 1. Initialize Progress Bar and window manager
            wm = context.window_manager
            # Convert generator to list to get length for progress bar
            skp_defs = list(self.skp_model.component_definitions)
            # Total steps: defs analysis + duplicateable groups + root entities + instancing
            total_elements = len(skp_defs) * 2 + 5 
            wm.progress_begin(0, total_elements)
            self.progress_count = 0
            
            # Pre-calculate instance counts for optimization decisions
            for i, cd in enumerate(skp_defs):
                self.progress_count += 1
                wm.progress_update(self.progress_count)
                self.instance_counts[cd.name] = cd.numInstances
    
            # 2. Initialize Standard Collections (now unique per file)
            self.colls = init_skp_collections(self.filepath)

            # CLEANUP: If this is an update/reload, remove old objects to prevent duplication
            if is_update:
                if not MIN_LOGS:
                    skp_log("Reload detected: Cleaning up old objects...")
                
                # List of category nodes to clean
                categories = ['mesh_node', 'components_node', 'groups_node', 'edges_node', 'hidden_node']
                for cat_key in categories:
                    cat_node = self.colls.get(cat_key)
                    if cat_node:
                        # Recursively find and delete all child objects
                        # We do this before the main import loop
                        children = [obj for obj in bpy.data.objects if obj.parent == cat_node]
                        for child in children:
                            # If it's an empty (folder), it might have its own children
                            # For simplicity and safety, we delete everything parented to category nodes
                            # In Blender, deleting the object doesn't delete the data-block (mesh), 
                            # but we'll let Blender's garbage collection handle that.
                            try:
                                # Delete recursively (optional but safer for nested empties)
                                def delete_recursive(ob):
                                    for c in ob.children:
                                        delete_recursive(c)
                                    # Unlink and delete
                                    for coll in ob.users_collection:
                                        coll.objects.unlink(ob)
                                    bpy.data.objects.remove(ob, do_unlink=True)
                                
                                delete_recursive(child)
                            except:
                                pass

            # Start stopwatch for camera import
            if not MIN_LOGS:
                skp_log("")
                skp_log("=== Importing Sketchup scenes and views as Blender Cameras ===")
            _time_camera = time.time()

            # Import a specific named SketchUp scene as a Blender camera and hide
            # the layers associated with that specific scene
            scene_filter = options.get("import_scene_filter")
            if scene_filter:
                options["import_scene"] = False # Disable bulk import if specific filter is set
                options["import_camera"] = True
                for s in self.skp_model.scenes:
                    if s.name == scene_filter:
                        if not MIN_LOGS:
                            skp_log(f"Importing named SketchUp scene '{s.name}'")
                        self.scene = s

                        # Skip s.layers which are the invisible layers
                        self.layers_skip = [l for l in s.layers]
                if not self.layers_skip and not MIN_LOGS:
                    skp_log("Scene: '{}' didn't have any invisible layers.".format(scene_filter))
                if self.layers_skip != [] and not MIN_LOGS:
                    hidden_layers = sorted([l.name for l in self.layers_skip])
                    print("SU | Invisible Layer(s)/Tag(s): \n     ", end="")
                    print(*hidden_layers, sep=", ")

            # Camera and Scene import disabled per user request to preserve Blender camera settings
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

            # Final pass: Ensure everything is parented correctly and visibility is set
            # (Visibility overrides removed per user request)
            pass



        
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

            # 4. INSTANCING: Process analyzed component statistics
            inst_len = len(self.component_stats)
            for i, (k, _v) in enumerate(self.component_stats.items()):
                self.progress_count += 1
                wm.progress_update(self.progress_count)
                name, mat = k
                if options.get("dedub_type") == "VERTEX":
                    self.instance_group_dupli_vert(name, mat, self.component_stats)
                else:
                    self.instance_group_dupli_face(name, mat, self.component_stats)

            if LOGS:
                duration = time.time() - _time_main
                summary = f"Import Finished: {len(self.materials)} Mats, {len(self.component_meshes)} Components in {duration:.2f}s"
                skp_log(summary)
                self.context.workspace.status_text_set(summary)
            
            # End Progress Bar
            wm.progress_end()
            
            # 5. AUTO FOCUS: Zoom to the imported model
            if not options.get("is_update"):
                try:
                    for area in context.screen.areas:
                        if area.type == 'VIEW_3D' and area.regions:
                            with context.temp_override(
                                window=context.window,
                                area=area,
                                region=area.regions[-1],
                            ):
                                bpy.ops.view3d.view_all(center=True)
                except: pass
        
        finally:
            # STERILIZATION: Force C-API destruction to prevent RAM leaks.
            if hasattr(self, "skp_model") and self.skp_model:
                try:
                    self.skp_model.close()
                except Exception:
                    pass
                self.skp_model = None
            
            # Purge massive memory caches and trigger garbage collection
            clear_import_state(self)
            
            import gc
            gc.collect()
            try:
                bpy.data.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
            except Exception:
                pass
            
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
    def _find_existing_material(self, original_name):
        if not original_name: return None
        
        # 1. Clean the name (SketchUp often has trailing spaces)
        search_name = original_name.strip()
        search_lower = search_name.lower()
        
        # 2. Search by custom property (The most reliable way)
        for m in bpy.data.materials:
            if m.get("skp_name") == search_name:
                return m
        
        # 3. Case-insensitive name search (Handles "Bamboo" vs "bamboo")
        for m in bpy.data.materials:
            if m.name.lower() == search_lower:
                m["skp_name"] = search_name # Tag it for next time
                return m
        
        # 4. Handle sanitized colons (Blender replaces : with _)
        if ":" in search_name:
            sanitized = search_name.replace(":", "_").lower()
            for m in bpy.data.materials:
                if m.name.lower() == sanitized:
                    m["skp_name"] = search_name
                    return m
                    
        return None

    def write_image(self, tex):
        import tempfile
        try:
            # Sanitize filename (basename only, no path traversal)
            tex_filename = os.path.basename(tex.name.replace("\\", "/"))
            if not tex_filename: tex_filename = "texture.png"
            suffix = os.path.splitext(tex_filename)[1] or ".png"

            # Secure unique temp file (no predictable-path symlink race)
            fd, temp_path = tempfile.mkstemp(prefix=self.filename_prefix, suffix=suffix)
            os.close(fd)

            # Write SketchUp texture to disk
            tex.write(temp_path)

            # Load into Blender
            img = bpy.data.images.load(temp_path, check_existing=True)
            img.name = os.path.basename(temp_path)
            return img
        except Exception as e:
            skp_log(f"Failed to write texture {tex.name}: {e}")
            return None

    def write_materials(self, materials):
        self.materials = {}
        self.materials_scales = {}
        if not hasattr(self, "texture_scales"):
            self.texture_scales = {}
        prefix = self.filename_prefix
        
        # 1. Helper for color conversion
        def srgb_to_line(c):
            return pow(c / 255.0, 2.2)

        # 2. Default Material (Essential for SketchUp)
        def_mat_name = "DefaultMaterial"
        full_def_name = prefix + def_mat_name
        bmat_def = bpy.data.materials.get(full_def_name)
        if not bmat_def:
            bmat_def = bpy.data.materials.new(full_def_name)
            bmat_def.use_nodes = True
            bmat_def.node_tree.nodes.clear()
            out = bmat_def.node_tree.nodes.new("ShaderNodeOutputMaterial")
            bsdf = bmat_def.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
            bmat_def.node_tree.links.new(bsdf.outputs[0], out.inputs[0])
            bsdf.inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1.0)
        
        self.materials[def_mat_name] = bmat_def
        self.materials_scales[def_mat_name] = (1.0, 1.0)

        # 3. Process all other materials
        for m in materials:
            name = m.name
            full_name = prefix + name

            # Record SketchUp texture scale for inherited UV fix
            # (sketchup.pyx only multiplies inherited faces by this).
            try:
                _t = m.texture
                if _t and not isinstance(_t, bool):
                    _d = _t.dimensions
                    self.texture_scales[name] = (float(_d[2]), float(_d[3]))
            except Exception:
                pass

            # Use existing if found
            bmat = bpy.data.materials.get(full_name)
            if bmat and self.reuse_material:
                self.materials[name] = bmat
                # Skip recreation of nodes if user already has this material
                continue 

            if not bmat:
                bmat = bpy.data.materials.new(full_name)
                bmat.use_nodes = True
            
            bmat["skp_imported"] = True # Stability tag
            self.materials[name] = bmat
            # 3. Shader Node Construction (Organized Layout)
            nodes = bmat.node_tree.nodes
            links = bmat.node_tree.links
            nodes.clear()
            
            # Position variables for a clean UI
            x_pos = -800
            
            # 3. Shader Node Construction
            node_tex = None
            tex = m.texture
            if tex:
                img = self.write_image(tex)
                if img:
                    # Create Tiling Nodes only if there is a texture
                    node_tex_coord = nodes.new("ShaderNodeTexCoord")
                    node_tex_coord.location = (x_pos, 0)
                    x_pos += 250
                    
                    node_mapping = nodes.new("ShaderNodeMapping")
                    node_mapping.location = (x_pos, 0)
                    x_pos += 300
                    
                    node_tex = nodes.new("ShaderNodeTexImage")
                    node_tex.image = img
                    node_tex.location = (x_pos, 0)
                    x_pos += 300
                    
                    # FIX: STQ/Q already contains tile counts. Mapping must be
                    # identity (1,1,1). Previously s_scale/0.0254 double-scaled
                    # UVs -> textures 10-1000x too big or too small.
                    node_mapping.inputs["Scale"].default_value[0] = 1.0
                    node_mapping.inputs["Scale"].default_value[1] = 1.0
                    node_mapping.inputs["Scale"].default_value[2] = 1.0
                    node_mapping.inputs["Location"].default_value[0] = 0.0
                    node_mapping.inputs["Location"].default_value[1] = 0.0
                    node_mapping.inputs["Location"].default_value[2] = 0.0







                    
                    # Link Tiling Nodes
                    links.new(node_tex_coord.outputs["UV"], node_mapping.inputs["Vector"])
                    links.new(node_mapping.outputs["Vector"], node_tex.inputs["Vector"])

            node_bsdf = nodes.new("ShaderNodeBsdfPrincipled")
            node_bsdf.location = (x_pos, 0)
            x_pos += 350
            
            node_output = nodes.new("ShaderNodeOutputMaterial")
            node_output.location = (x_pos, 0)
            
            # 4. Final Linking and Color Logic
            try:
                c = m.color
                r, g, b, a = c[0], c[1], c[2], c[3]
                alpha = a / 255.0
                base_color = (srgb_to_line(r), srgb_to_line(g), srgb_to_line(b), 1.0)
                
                if node_tex:
                    links.new(node_tex.outputs["Color"], node_bsdf.inputs["Base Color"])
                    if alpha < 0.99 or node_tex.image.depth == 32:
                        links.new(node_tex.outputs["Alpha"], node_bsdf.inputs["Alpha"])
                        bmat.blend_method = 'HASHED'
                else:
                    node_bsdf.inputs["Base Color"].default_value = base_color
                    node_bsdf.inputs["Alpha"].default_value = alpha
                    bmat.blend_method = 'HASHED' if alpha < 0.99 else 'OPAQUE'
            except:
                node_bsdf.inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1.0)
            
            links.new(node_bsdf.outputs[0], node_output.inputs[0])

            
            # 5. Smart PBR Heuristics
            if self.smart_pbr:
                self._apply_smart_pbr(bmat, name)


    def _apply_smart_pbr(self, bmat, name):
        """Helper to apply Smart PBR heuristics to a Blender material based on SketchUp names"""
        if not bmat or not bmat.use_nodes: return
        nodes = bmat.node_tree.nodes
        bsdf = next((n for n in nodes if n.type == 'BSDF_PRINCIPLED'), None)
        if not bsdf: return
        
        mat_lower = name.lower()
        
        # 1. Glass / Cam Heuristics
        if "glass" in mat_lower or "cam" in mat_lower:
            bsdf.inputs["Transmission Weight"].default_value = 1.0
            bsdf.inputs["Roughness"].default_value = 0.02
            bsdf.inputs["IOR"].default_value = 1.45 # Standard Glass
            bmat.blend_method = 'BLEND' # Better for architectural glass
            
        # 2. Metal / Steel / Celik
        elif "metal" in mat_lower or "steel" in mat_lower or "celik" in mat_lower or "gold" in mat_lower:
            bsdf.inputs["Metallic"].default_value = 1.0
            bsdf.inputs["Roughness"].default_value = 0.15
            
        # 3. Mirror / Ayna
        elif "mirror" in mat_lower or "ayna" in mat_lower:
            bsdf.inputs["Metallic"].default_value = 1.0
            bsdf.inputs["Roughness"].default_value = 0.0
            bsdf.inputs["Base Color"].default_value = (1.0, 1.0, 1.0, 1.0)
            
        # 4. Water / Su
        elif "water" in mat_lower or "su" in mat_lower:
            bsdf.inputs["Transmission Weight"].default_value = 1.0
            bsdf.inputs["Roughness"].default_value = 0.01
            bsdf.inputs["IOR"].default_value = 1.33 # Water
            bmat.blend_method = 'BLEND'
        
        # Default fallback for others
        else:
            if bsdf.inputs["Alpha"].default_value < 1.0:
                bmat.blend_method = 'HASHED'


    def write_mesh_data(self, entities=None, name="", default_material="DefaultMaterial", filter_layer=None, center_geometry=True, cache_id=None, parent_node=None, **kwargs):
        # Prefix mesh name with filename to prevent global collision
        full_name = self.filename_prefix + name
        
        # Use explicit cache_id (Definition Name) for stable mesh sharing
        if cache_id:
            mesh_key = (self.filename_prefix + cache_id, default_material, filter_layer)
            if mesh_key in self.component_meshes:
                return self.component_meshes[mesh_key]

        # Use binary N-gon method for maximum performance, fallback to Python if needed
        # Pass inherited texture scales so Cython scales only inherited faces.
        _scales = getattr(self, "texture_scales", None)
        try:
            try:
                verts, raw_faces_data, mats = entities.get_textured_ngon_lists(default_material, _scales)
            except TypeError:
                verts, raw_faces_data, mats = entities.get_textured_ngon_lists(default_material)
        except Exception as e:
            if LOGS: skp_log(f"Binary call failed or incompatible ({e}), using robust Python fallback...")
            verts, raw_faces_data, mats = self._get_ngon_lists_fallback(entities, default_material)
        
        # Filter faces by layer if requested
        if filter_layer is not None:
            raw_faces_data = [f for f in raw_faces_data if f['layer_name'] == filter_layer]

        if not verts or not raw_faces_data:
            return []

        # FIX: Keep SketchUp local coordinates. Previous bbox-centering moved
        # every mesh origin to its bbox center (often the import center).
        # SketchUp origin = group/component origin (= parent_transform).
        island_center = Vector((0,0,0))

        me = bpy.data.meshes.new(full_name)
        
        # Add materials to the mesh using a pre-calculated mapping
        slot_map = {}
        if mats:
            # Sort materials by their index to ensure slot order matches binary data
            sorted_mats = sorted(mats.items(), key=lambda x: x[1])
            for mat_name, mat_idx in sorted_mats:
                m = self.materials.get(mat_name) or self._find_existing_material(mat_name)
                
                if not m:
                    skp_log(f"Recovering missing material: {mat_name}")
                    m = bpy.data.materials.new(name=self.filename_prefix + mat_name if mat_name else "Safe_Material")
                    m["skp_name"] = mat_name
                    m["skp_imported"] = True
                    m.use_nodes = True
                    # Initialize basic nodes for the recovered material
                    m.node_tree.nodes.clear()
                    out = m.node_tree.nodes.new("ShaderNodeOutputMaterial")
                    bsdf = m.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
                    m.node_tree.links.new(bsdf.outputs[0], out.inputs[0])
                    self.materials[mat_name] = m
                    
                me.materials.append(m)
                slot_map[mat_name] = len(me.materials) - 1
        
        # Default material fallback index
        def_mat = self.materials.get("DefaultMaterial")
        def_mat_idx = -1
        if def_mat:
            if def_mat.name not in [m.name for m in me.materials if m]:
                me.materials.append(def_mat)
            for i, m in enumerate(me.materials):
                if m == def_mat:
                    def_mat_idx = i
                    break


        bm = bmesh.new()
        try:
            bm_verts = [bm.verts.new(v) for v in verts]
            bm.verts.ensure_lookup_table()
            
            # Create a lookup list for material names by index
            material_names = [None] * len(mats)
            for m_name, m_idx in mats.items():
                material_names[m_idx] = m_name
            
            for face_info in raw_faces_data:
                mat_idx = face_info['mat_idx']
                loops = face_info['loops']
                front_uvs = face_info['front_uvs']
                back_mat_idx = face_info['back_mat_idx']
                back_uvs = face_info['back_uvs']
                
                # Front-Face Only Strategy:
                # We ignore back-face materials to keep the material list clean and slots independent.
                # If a user wants different colors on two sides of a wall, they should model with thickness.
                
                # Get pre-calculated material index
                m_name = material_names[mat_idx] if mat_idx != -1 else "DefaultMaterial"
                f_me_idx = slot_map.get(m_name, def_mat_idx)

                for l_idx, l_verts_indices in enumerate(loops):
                    try:
                        if len(l_verts_indices) < 3: continue
                        
                        unique_indices = []
                        seen_idx = set()
                        for i in l_verts_indices:
                            if i not in seen_idx:
                                unique_indices.append(i)
                                seen_idx.add(i)
                        if len(unique_indices) < 3: continue
                        
                        l_verts = [bm_verts[i] for i in unique_indices]
                        
                        # Create only the front face
                        face = bm.faces.new(l_verts)
                        face.material_index = f_me_idx
                        face.smooth = False
                        
                        uv_layer = bm.loops.layers.uv.get("UVMap") or bm.loops.layers.uv.new("UVMap")
                        tri_uvs = front_uvs[l_idx]
                        for loop_vert_idx, loop in enumerate(face.loops):
                            if loop_vert_idx < len(tri_uvs):
                                loop[uv_layer].uv = tri_uvs[loop_vert_idx]
                    except Exception:
                        pass

            # Restore UV-safe dissolution to ensure G-non (N-gon) cleanliness
            # By using delimit={'UV', 'MATERIAL'}, we ensure textures stay perfectly mapped.
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
            bmesh.ops.dissolve_limit(bm, angle_limit=0.001, verts=bm.verts, edges=bm.edges, delimit={'MATERIAL', 'UV'})

            # Consolidate all geometry into a single mesh for maximum performance
            # Use the mesh 'me' already created and populated with materials at the start of write_mesh_data
            bm.to_mesh(me)
        finally:
            bm.free()
        
        # Ensure UV layers are active
        if "UVMap" in me.uv_layers:
            me.uv_layers.active = me.uv_layers["UVMap"]
            
        me.update()
        
        # Determine if the mesh has any transparent materials
        has_alpha = any(m.blend_method != 'OPAQUE' for m in me.materials if m)
        
        # Get dominant material name for object naming
        dominant_mat_name = "Mesh"
        if me.materials:
            from collections import Counter
            mat_counts = Counter(f.material_index for f in me.polygons)
            if mat_counts:
                mode_idx = mat_counts.most_common(1)[0][0]
                if mode_idx < len(me.materials):
                    m = me.materials[mode_idx]
                    if m: dominant_mat_name = m.name
        
        results = [(me, has_alpha, island_center, dominant_mat_name)]
        
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
            for f in entities.faces:
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

                    # FIX: tessfaces returns S/Q. Apply scale only for inherited faces.
                    _s, _t = 1.0, 1.0
                    if mat_f is None:
                        _sc = getattr(self, "texture_scales", {}).get(default_material)
                        if _sc:
                            try:
                                _s, _t = float(_sc[0]), float(_sc[1])
                                if abs(_s) < 1e-4: _s = 1.0
                                if abs(_t) < 1e-4: _t = 1.0
                            except Exception:
                                _s, _t = 1.0, 1.0

                    loops = []
                    front_uvs = []
                    for tri, tri_uvs in zip(f_tris, f_uvs):
                        loops.append([f_v_indices[i] for i in tri])
                        front_uvs.append([(u * _s, v * _t) for (u, v) in tri_uvs])

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
        
        # Diagnostic report for silent failures
        if len(entities.faces) > 0 and len(raw_faces_data) == 0:
            skp_log(f"WARNING: Fallback failed to extract any faces from {len(entities.faces)} potential candidates.")
        elif len(raw_faces_data) < len(entities.faces) * 0.5:
             skp_log(f"WARNING: High failure rate in Python fallback. Only {len(raw_faces_data)}/{len(entities.faces)} faces recovered.")

        return verts, raw_faces_data, mats

        
    def write_standalone_edges(self, entities, name, transform, layer_name=None):
        if not self.import_standalone_edges: return
        skp_log(f"Writing standalone edges for: {name}")
        
        # Binary access to edge lists
        try:
            edges = list(entities.standalone_edges)
        except AttributeError:
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
        if name == "Loose Edges" and hasattr(self, 'colls'):
            target_coll = self.colls.get('edges_node', self.colls.get('root_coll', target_coll))

        for idx, (i_verts, i_edges) in enumerate(islands):
            # FIX: Keep SketchUp local coords, origin = transform origin.
            # (Previously centered to island bbox -> scene center.)
            ob_name = f"{name}_{idx+1:03d}" if len(islands) > 1 else name
            island_me = bpy.data.meshes.new(ob_name)
            island_bm = bmesh.new()
            v_remap = {}
            for v in i_verts:
                v_remap[v] = island_bm.verts.new(v.co)
            for e in i_edges:
                try: island_bm.edges.new((v_remap[e.verts[0]], v_remap[e.verts[1]]))
                except: pass
            
            island_bm.to_mesh(island_me)
            island_bm.free()
            
            ob = bpy.data.objects.new(ob_name, island_me)
            ob.matrix_world = transform
            
            target_coll.objects.link(ob)
            ob["skp_imported"] = True # Stability tag

            # No ROOT parent (no lines). EDGES collection only for outliner.

        bm.free()


    def write_entities(self, entities, name, parent_transform, default_material="DefaultMaterial", etype=None, parent_ob=None, is_hidden=False):
        # 1. Check for nested content (Use list() for generator compatibility)
        groups_list = list(entities.groups)
        instances_list = list(entities.instances)
        has_nested = (len(groups_list) > 0 or len(instances_list) > 0)
        is_loose_root = (name == "SKP Mesh Objects")
        
        # 2. Category collections for outliner (GROUPS / COMPONENTS / MESH)
        # FIX: Collections (not empties) so outliner shows bulk groups
        # without parent lines. Top-level parent = None (no ROOT lines).
        if is_loose_root:
            category_coll = self.colls['mesh_node']
        elif etype == EntityType.component:
            category_coll = self.colls['components_node']
        elif etype == EntityType.group:
            category_coll = self.colls['groups_node']
        else:
            category_coll = self.colls['mesh_node']

        # Target collection for linking (type-specific sub-collection)
        target_coll = category_coll

        # 3. Geometry Writing... FIX: no centering, keep SketchUp local coords
        should_center = False
        cache_id = f"{name}_{default_material}" if etype == EntityType.component else None
        results = self.write_mesh_data(entities=entities, name=name, default_material=default_material, 
                                      center_geometry=should_center, cache_id=cache_id, parent_node=category_coll)
        
        # 4. Pivot Strategy (LEAN): Only container empties when needed.
        # Single-mesh groups/components use the mesh itself as pivot,
        # children parent to that mesh (no extra Empty, no extra line).
        # Empty only when: no direct mesh (pure container) or multiple meshes.
        is_complex = len(results) > 1
        need_empty = (not is_loose_root and etype != EntityType.none and (len(results) == 0 or is_complex))
        main_level_ob = None
        pivot_for_children = parent_ob  # default: fall through to parent
        if need_empty:
            main_level_ob = bpy.data.objects.new(name, None)
            main_level_ob.empty_display_type = "PLAIN_AXES"
            main_level_ob.empty_display_size = 0.1
            target_coll.objects.link(main_level_ob)
            main_level_ob["skp_imported"] = True

            # Top-level: parent None (no ROOT lines). Nested: parent_ob.
            main_level_ob.parent = parent_ob
            if main_level_ob.parent:
                main_level_ob.matrix_parent_inverse = Matrix.Identity(4)
            main_level_ob.matrix_world = parent_transform

            main_level_ob.hide_viewport = False
            main_level_ob.hide_render = False
            pivot_for_children = main_level_ob

        # 5. Link Geometries
        single_mesh_ob = None
        for me, alpha, island_center, mat_name in results:
            display_name = mat_name.split('.')[0] if '.' in mat_name else mat_name
            ob_name = f"{name}_{display_name}" if is_complex else name
            ob = bpy.data.objects.new(ob_name, me)

            target_coll = category_coll
            target_coll.objects.link(ob)
            ob["skp_imported"] = True # Stability tag

            # Top-level: parent None (no ROOT lines). Nested: mesh/empty pivot.
            if main_level_ob:
                ob.parent = main_level_ob
            else:
                ob.parent = parent_ob

            if ob.parent:
                ob.matrix_parent_inverse = Matrix.Identity(4)


            # FIX: Origin = SketchUp group/component origin (= parent_transform).
            # Previously parent_transform @ Translation(island_center) put the
            # origin at the bbox center (often the import scene center).
            ob.matrix_world = parent_transform

            # USER REQUEST: Even if hidden in SKP, keep visible in Blender's hidden folder
            ob.hide_viewport = False
            ob.hide_render = False

            if 0.01 < alpha < 1.0: ob.show_transparent = True
            me.update()
            single_mesh_ob = ob

        # If single mesh and group/component (not loose root), mesh is the pivot
        if single_mesh_ob and not main_level_ob and not is_loose_root and etype != EntityType.none:
            pivot_for_children = single_mesh_ob

        # 6. Recursion: Groups
        for group in groups_list:
            if self.layers_skip and group.layer in self.layers_skip: continue
            g_name = "G-" + (group.name if group.name else "Group")
            child_world_transform = parent_transform @ Matrix(group.transform)
            self.write_entities(group.entities, g_name, child_world_transform, 
                               default_material=inherent_default_mat(group.material, default_material), 
                               etype=EntityType.group, parent_ob=pivot_for_children,
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
                               etype=EntityType.component, parent_ob=pivot_for_children,
                               is_hidden=instance.hidden)


    def component_def_as_group(self, entities, name, transform, default_material="DefaultMaterial", etype=None, group=None):
        results = self.write_mesh_data(entities=entities, name=name, default_material=default_material)
        for me, alpha, island_center, mat_name in results:
            display_name = mat_name.split('.')[0] if '.' in mat_name else mat_name
            ob = bpy.data.objects.new(f"{name}_{display_name}", me)
            ob.matrix_world = transform
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
                self.colls['mesh_node'].objects.link(ob)
                self.colls['mesh_node'].objects.link(dob)
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
            # Blender 4+: polygons (tessfaces removed)
            dme.polygons.add(f_count // 4)
            dme.polygons.foreach_set("vertices", unpack_face_list(faces))
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
                self.colls['mesh_node'].objects.link(ob)
                self.colls['mesh_node'].objects.link(dob)
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
        
        # Link to root collection and parent to cameras node
        root_coll = self.colls.get('root_coll', self.context.collection)
        root_coll.objects.link(ob)
        
        if hasattr(self, 'colls') and 'cameras_node' in self.colls:
            ob.parent = self.colls['cameras_node']
            ob.matrix_parent_inverse = Matrix.Identity(4)
            
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
    """Import SketchUp Scene (.skp)"""
    bl_idname = "import_scene.skp"
    bl_label = "Import Sketchup Scene"
    bl_options = {'PRESET', 'UNDO'}

    filename_ext = ".skp"
    filter_glob: StringProperty(default="*.skp", options={'HIDDEN'})

    import_scene: BoolProperty(
        name="Import Scene",
        description="Imports SketchUp scenes as Blender cameras",
        default=True,
    )
    
    is_update: BoolProperty(
        name="Is Update",
        description="Internal flag to indicate if this is a reload operation",
        default=False,
        options={'HIDDEN', 'SKIP_SAVE'},
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

    smart_pbr: BoolProperty(
        name="Enable Smart PBR Materials",
        description="Automatically assigns physical properties (Glass, Metal, Water) based on material names.",
        default=True,
    )

    max_instance: IntProperty(
        name="Instantiation Threshold :", 
        description="Number of components before instancing starts",
        default=50
    )

    dedub_only: BoolProperty(name="Groups Only", description="Import instantiated groups only.", default=False)

    reuse_existing_groups: BoolProperty(
        name="Reuse Groups", description="Use existing Blender groups to instance components with.", default=False
    )

    dedub_type: EnumProperty(
        name="Instancing Type :",
        items=(
            ("FACE", "Faces", ""),
            ("VERTEX", "Vertices", ""),
        ),
        default="VERTEX",
    )

    import_scene_filter: StringProperty(name="Import A Scene :", description="Import a specific SketchUp Scene", default="")

    def invoke(self, context, event):
        if context.scene.skp_last_filepath:
            self.filepath = context.scene.skp_last_filepath
        return super().invoke(context, event)

    def execute(self, context):
        keywords = self.as_keywords()
        
        # SAVE STATE: This is required for the Reload menu to appear and function!
        scene = context.scene
        scene.skp_last_filepath = keywords.get("filepath", "")
        scene.skp_reuse_material = keywords.get("reuse_material", True)
        scene.skp_smart_pbr = keywords.get("smart_pbr", True)
        scene.skp_max_instance = keywords.get("max_instance", 50)
        
        # Hardcode internal defaults for stripped features
        keywords["support_back_material"] = True
        keywords["merge_coplanar_faces"] = False
        keywords["import_standalone_edges"] = False
        
        is_update = keywords.pop("is_update", False)
        return SceneImporter().set_filename(keywords["filepath"]).load(context, is_update=is_update, **keywords)

    def draw(self, context):
        layout = self.layout
        layout.label(text="- Primary Import Options -")
        row = layout.row()
        row.prop(self, "import_scene")
        row = layout.row()
        row.prop(self, "reuse_material")
        row = layout.row()
        row.prop(self, "smart_pbr")
        row = layout.row()
        row.prop(self, "dedub_only")
        row = layout.row()
        row.prop(self, "reuse_existing_groups")
        
        layout.label(text="- Advanced Modern Options -")
        box = layout.box()
        box.prop(self, "smart_pbr")
        
        col = layout.column()
        col.label(text="- Instantiate components, if they are more than -")
        col.prop(self, "max_instance")
        row = layout.row()
        row.use_property_split = True
        row.prop(self, "dedub_type")
        row = layout.row()
        row.use_property_split = True
        row.prop(self, "import_scene_filter")


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
    """Reload a specific SketchUp file"""
    bl_idname = "import_scene.skp_reload"
    bl_label = "Reload / Update Sketchup Scene"
    bl_options = {"REGISTER", "UNDO"}

    # Add property to target a specific collection
    target_collection: bpy.props.StringProperty(name="Target Collection", default="")

    def execute(self, context):
        # FIND THE TARGET FILE
        target_coll = None
        path = ""
        
        # 1. If a specific collection is provided, use it
        if self.target_collection:
            target_coll = bpy.data.collections.get(self.target_collection)
            if target_coll:
                path = target_coll.get("skp_filepath", "")
        
        # 2. Otherwise, try to find SKP root from active object (Context-aware)
        if not path:
            obj = context.active_object
            if obj:
                curr_coll = obj.users_collection[0] if obj.users_collection else None
                while curr_coll:
                    if "skp_filepath" in curr_coll:
                        target_coll = curr_coll
                        path = curr_coll["skp_filepath"]
                        break
                    # Go up hierarchy
                    parent = None
                    for c in bpy.data.collections:
                        if curr_coll.name in c.children:
                            parent = c
                            break
                    curr_coll = parent

        # 3. Fallback to global last path
        if not path:
            path = context.scene.skp_last_filepath
            for c in bpy.data.collections:
                if c.get("skp_filepath") == path:
                    target_coll = c
                    break

        if not path or not os.path.exists(path):
            self.report({'ERROR'}, "No SketchUp source found for selection. Please select an object from the SKP import or import manually.")
            return {'CANCELLED'}

        # 1. PRESERVATION: Backup material assignments by object name
        material_backup = {}
        modifier_backup = {}
        main_coll_name = ""
        transform_backup = None
        
        main_coll = target_coll
        if main_coll:
            main_coll_name = main_coll.name
            
            # BACKUP: Material assignments and Modifiers
            for obj in main_coll.all_objects:
                if obj.type == 'MESH':
                    # Backup Materials
                    mats = [slot.material.name if slot.material else None for slot in obj.material_slots]
                    material_backup[obj.name] = mats
                    
                    # Backup Modifiers (Architectural Set)
                    supported_types = {'BEVEL', 'SOLIDIFY', 'MIRROR', 'ARRAY', 'SUBSURF'}
                    target_mods = [m for m in obj.modifiers if m.type in supported_types]
                    
                    if target_mods:
                        mod_data = []
                        for m in target_mods:
                            data = {'name': m.name, 'type': m.type}
                            
                            if m.type == 'BEVEL':
                                data.update({
                                    'width': m.width, 'segments': m.segments,
                                    'limit_method': m.limit_method, 'angle_limit': m.angle_limit,
                                    'harden_normals': getattr(m, 'harden_normals', False),
                                    'miter_inner': getattr(m, 'miter_inner', 'OFFSET'),
                                    'miter_outer': getattr(m, 'miter_outer', 'SHARP')
                                })
                            elif m.type == 'SOLIDIFY':
                                data.update({'thickness': m.thickness, 'offset': m.offset})
                            elif m.type == 'MIRROR':
                                data.update({'use_axis': list(m.use_axis), 'mirror_object': m.mirror_object.name if m.mirror_object else None})
                            elif m.type == 'ARRAY':
                                data.update({'count': m.count, 'relative_offset_displace': list(m.relative_offset_displace)})
                            elif m.type == 'SUBSURF':
                                data.update({'levels': m.levels, 'render_levels': m.render_levels})
                                
                            mod_data.append(data)
                        modifier_backup[obj.name] = mod_data
            
            # BACKUP: Transformation if requested
            root_empty_name = f"ROOT: {os.path.basename(path)}"
            root_empty = bpy.data.objects.get(root_empty_name)
            transform_backup = None
            if context.scene.skp_keep_transform and root_empty:
                transform_backup = root_empty.matrix_world.copy()


            skp_log("Batch purging existing objects for fast reload...")
            
            # 2. CLEANUP: Remove everything linked to the root collection
            # except the root collection itself for UI stability
            obs_to_remove = list(main_coll.all_objects)
            # Remove objects, which includes our ROOT empty and sub-empties
            bpy.data.batch_remove(ids=obs_to_remove)
            
            # 3. MESH CLEANUP: Fast orphan removal
            bpy.data.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
            gc.collect()
            
        # 4. RE-IMPORT
        bpy.ops.import_scene.skp(
            filepath=path,
            is_update=True,
            reuse_material=context.scene.skp_reuse_material,
            smart_pbr=context.scene.skp_smart_pbr,
            max_instance=context.scene.skp_max_instance
        )
        
        if context.scene.skp_reuse_material and material_backup:
            new_main_coll = bpy.data.collections.get(main_coll_name)
            if new_main_coll:
                for obj in new_main_coll.all_objects:
                    if obj.type == 'MESH' and obj.name in material_backup:
                        saved_mats = material_backup[obj.name]
                        for i, mat_name in enumerate(saved_mats):
                            if i < len(obj.material_slots) and mat_name:
                                mat = bpy.data.materials.get(mat_name)
                                if mat:
                                    obj.material_slots[i].material = mat
                                    
        # 6. RESTORATION: Re-apply Modifiers
        if modifier_backup:
            new_main_coll = bpy.data.collections.get(main_coll_name)
            if new_main_coll:
                for obj in new_main_coll.all_objects:
                    if obj.type == 'MESH' and obj.name in modifier_backup:
                        for m_data in modifier_backup[obj.name]:
                            # Ensure we don't double-add
                            if m_data['name'] not in obj.modifiers:
                                try:
                                    m = obj.modifiers.new(name=m_data['name'], type=m_data['type'])
                                    if m_data['type'] == 'BEVEL':
                                        m.width = m_data['width']
                                        m.segments = m_data['segments']
                                        m.limit_method = m_data['limit_method']
                                        m.angle_limit = m_data['angle_limit']
                                        if hasattr(m, 'harden_normals'): m.harden_normals = m_data['harden_normals']
                                        m.miter_inner = m_data['miter_inner']
                                        m.miter_outer = m_data['miter_outer']
                                    elif m_data['type'] == 'SOLIDIFY':
                                        m.thickness = m_data['thickness']
                                        m.offset = m_data['offset']
                                    elif m_data['type'] == 'MIRROR':
                                        m.use_axis = m_data['use_axis']
                                        if m_data['mirror_object']:
                                            m.mirror_object = bpy.data.objects.get(m_data['mirror_object'])
                                    elif m_data['type'] == 'ARRAY':
                                        m.count = m_data['count']
                                        m.relative_offset_displace = m_data['relative_offset_displace']
                                    elif m_data['type'] == 'SUBSURF':
                                        m.levels = m_data['levels']
                                        m.render_levels = m_data['render_levels']
                                except Exception as e:
                                    skp_log(f"Failed to restore modifier {m_data['name']}: {e}")
                                    
        # 7. RESTORATION: Re-apply transformation
        if context.scene.skp_keep_transform and transform_backup:
            root_empty_name = f"ROOT: {os.path.basename(path)}"
            root_empty = bpy.data.objects.get(root_empty_name)
            if root_empty:
                root_empty.matrix_world = transform_backup

        
        self.report({'INFO'}, f"Reloaded: {os.path.basename(path)}")
        
        # 6. CLEANUP: Purge orphan data-blocks specifically from SKP
        # This keeps the file size small during repeated reloads
        for i in range(2):
            bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
            
        return {'FINISHED'}



class SKP_OT_proxy_toggle(Operator):
    """Toggle between Full Geometry and Bounding Box for SKP data"""
    bl_idname = "import_scene.skp_proxy_toggle"
    bl_label = "Toggle Proxy Mode"
    
    target_collection: bpy.props.StringProperty(name="Target Collection", default="")

    def execute(self, context):
        main_coll = None
        if self.target_collection:
            main_coll = bpy.data.collections.get(self.target_collection)
        
        # Fallback: find the first available SKP collection
        if not main_coll:
            for c in bpy.data.collections:
                if "skp_filepath" in c:
                    main_coll = c
                    break
        
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
                obj.show_all_edges = (new_state != 'BOUNDS')
        
        return {'FINISHED'}

class SKP_OT_delete(Operator):
    """Completely remove an imported SketchUp file and its data"""
    bl_idname = "import_scene.skp_delete"
    bl_label = "Delete SKP Import"
    bl_options = {"REGISTER", "UNDO"}
    
    target_collection: bpy.props.StringProperty(name="Target Collection", default="")

    def execute(self, context):
        if not self.target_collection: return {'CANCELLED'}
        target_coll = bpy.data.collections.get(self.target_collection)
        if target_coll:
            obs = list(target_coll.all_objects)
            # Collect meshes to ensure they are purged
            target_meshes = [o.data for o in obs if o.type == 'MESH' and o.data]
            
            bpy.data.batch_remove(ids=obs)
            bpy.data.collections.remove(target_coll)
            
            # Fast cleanup of orphaned data
            bpy.data.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
        
        self.report({'INFO'}, f"Deleted SketchUp import: {self.target_collection}")
        return {'FINISHED'}

class SKP_OT_deep_purge(Operator):
    """Deep clean all unused data-blocks, empty objects and collections"""
    bl_idname = "import_scene.skp_deep_purge"
    bl_label = "Deep Purge"
    
    def execute(self, context):
        # 1. Standard recursive purge of orphans
        bpy.data.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

        # Collect SKP descendant collections for scoped cleanup
        skp_descendants = set()
        for coll in bpy.data.collections:
            if "skp_filepath" in coll:
                stack = list(coll.children)
                while stack:
                    c = stack.pop()
                    if c.name in skp_descendants:
                        continue
                    skp_descendants.add(c.name)
                    stack.extend(c.children)

        # 2. Cleanup Empty Objects — SKP-tagged only (never generic empties)
        empties_removed = 0
        for obj in list(bpy.data.objects):
            if obj.type == 'EMPTY' and not obj.children:
                if obj.get("skp_imported"):
                    bpy.data.objects.remove(obj, do_unlink=True)
                    empties_removed += 1

        # 3. Cleanup Empty Collections — SKP hierarchy only
        colls_removed = 0
        for coll in list(bpy.data.collections):
            if coll.name not in skp_descendants:
                continue
            if not coll.all_objects and not coll.children:
                if coll.library is None and coll.asset_data is None:
                    bpy.data.collections.remove(coll)
                    colls_removed += 1
        
        # 4. Final recursive purge for any data-blocks freed by the above
        bpy.data.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
        
        self.report({'INFO'}, f"Deep Purge: Removed {empties_removed} pivots and {colls_removed} collections.")
        return {'FINISHED'}

class SKP_OT_purge_materials(Operator):
    """Clean unused materials and empty slots while respecting Fake User protection"""
    bl_idname = "import_scene.skp_purge_materials"
    bl_label = "Purge Materials"
    
    def execute(self, context):
        count = 0
        
        # Phase 1: Clean redundant material slots safely
        slots_removed = 0
        for obj in bpy.data.objects:
            if obj.type != 'MESH' or obj.data.library is not None:
                continue

            # Find which material indices are actually used on faces
            used_indices = {p.material_index for p in obj.data.polygons}

            # Remove unused slots, highest index first so lower ones stay valid
            for i in range(len(obj.material_slots) - 1, -1, -1):
                if i in used_indices:
                    continue
                mat = obj.material_slots[i].material

                # SAFETY CHECK: Only remove if it's safe
                if mat is None:
                    can_remove = True  # Empty slot
                elif mat.use_fake_user:
                    can_remove = False  # User explicitly wants to keep this!
                elif "DefaultMaterial" in mat.name:
                    can_remove = True  # Unused default is safe to remove
                else:
                    can_remove = bool(mat.get("skp_imported"))

                if can_remove:
                    # Direct mesh-data removal: no operator context needed
                    try:
                        obj.data.materials.pop(index=i)
                        slots_removed += 1
                    except (RuntimeError, TypeError):
                        pass

        # Phase 2: Force recursive orphan removal (RESPECTING FAKE USER)
        # We run multiple passes because removing a material might orphan a texture
        for i in range(3):
            for mat in list(bpy.data.materials):
                if mat.library is None and mat.asset_data is None:
                    # NEVER delete if it has a Fake User or active users
                    if mat.users == 0 and not mat.use_fake_user:
                        bpy.data.materials.remove(mat, do_unlink=True)
                        count += 1
            
            bpy.data.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
        
        self.report({'INFO'}, f"Material Purge: Removed {count} unused materials and {slots_removed} empty slots.")
        return {'FINISHED'}

class SKP_OT_apply_smooth(Operator):
    """Apply Smooth by Angle to selected objects"""
    bl_idname = "import_scene.skp_apply_smooth"
    bl_label = "Smooth Selected"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected = context.selected_objects
        count = 0
        
        if context.active_object and context.active_object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        for ob in selected:
            if ob.type == 'MESH':
                context.view_layer.objects.active = ob
                ob.select_set(True)
                
                # FORCE MODIFIER ADDITION (Explicitly from Essentials)
                try:
                    # 1. First ensure it's set to smooth shading
                    bpy.ops.object.shade_smooth()
                    
                    # 2. Call the operator that ADDS the modifier box
                    bpy.ops.object.shade_smooth_by_angle()
                    
                    # 3. Double check if it was added, if not, use the asset call
                    if not any("Smooth" in m.name for m in ob.modifiers):
                        bpy.ops.object.modifier_add_node_group(
                            asset_library_type='ESSENTIALS', 
                            asset_identifier='Smooth by Angle'
                        )
                    count += 1
                except Exception as e:
                    skp_log(f"Smoothing failed: {e}")

        self.report({'INFO'}, f"Added Smooth by Angle modifier to {count} objects.")
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
        
        # 1. PERMANENT IMPORT BUTTON
        row = layout.row()
        row.scale_y = 1.5
        row.operator("import_scene.skp", text="IMPORT NEW SKP", icon='IMPORT')
        
        layout.separator()

        # Tools Section
        box = layout.box()
        row = box.row(align=True)
        row.operator("import_scene.skp_apply_smooth", text="Smooth", icon='MOD_SMOOTH')
        row.operator("import_scene.skp_deep_purge", text="Purge", icon='TRASH')

        layout.separator()
        
        # 2. LIST ALL INDEPENDENT IMPORTS
        layout.label(text="Imported SketchUp Files:", icon='FILE_3D')
        
        skp_imports_found = False
        import os
        
        for coll in bpy.data.collections:
            if "skp_filepath" in coll:
                skp_imports_found = True
                path = coll["skp_filepath"]
                filename = os.path.basename(path)
                
                box = layout.box()
                row = box.row(align=True)
                row.label(text=filename, icon='COLLECTION_NEW')
                
                # RELOAD specific button
                r_op = row.operator("import_scene.skp_reload", text="", icon='FILE_REFRESH')
                r_op.target_collection = coll.name
                
                # PROXY specific button
                p_op = row.operator("import_scene.skp_proxy_toggle", text="", icon='GHOST_ENABLED')
                p_op.target_collection = coll.name
                
                # DELETE specific button
                d_op = row.operator("import_scene.skp_delete", text="", icon='REMOVE')
                d_op.target_collection = coll.name


        if not skp_imports_found:
            layout.label(text="No SKP files in scene.", icon='INFO')

        layout.separator()
        
        # 3. GENERAL SETTINGS AND TOOLS
        if skp_imports_found or scene.skp_last_filepath:
            col = layout.column(align=True)
            box = col.box()
            box.label(text="Global Settings:", icon='SETTINGS')
            box.prop(scene, "skp_reuse_material", text="Keep My Material Edits")
            box.prop(scene, "skp_keep_transform", text="Keep My Placement")
            box.prop(scene, "skp_smart_pbr", text="Convert to Smart PBR")
            
            col.separator()
            
            layout.label(text="Advanced Tools:")
            grid = layout.grid_flow(columns=2, align=True)
            grid.operator("import_scene.skp_proxy_toggle", text="Global Proxy", icon='GHOST_ENABLED')
            grid.operator("import_scene.skp_deep_purge", text="Deep Purge", icon='TRASH')
            grid.operator("import_scene.skp_purge_materials", text="Purge Mats", icon='MATERIAL')


def register():
    # Register Classes
    for cls in (SketchupAddonPreferences, ImportSKP, ExportSKP, 
                SKP_OT_reload, SKP_OT_proxy_toggle, SKP_OT_delete, SKP_OT_deep_purge, 
                SKP_OT_purge_materials, SKP_OT_apply_smooth, SKP_PT_panel):
        bpy.utils.register_class(cls)
    
    # Menus
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    
    # Scene Properties
    bpy.types.Scene.skp_last_filepath = StringProperty(name="Last SKP File", default="")
    bpy.types.Scene.skp_reuse_material = BoolProperty(name="Use Existing Materials", default=True)
    bpy.types.Scene.skp_keep_transform = BoolProperty(name="Keep Placement", default=True)
    bpy.types.Scene.skp_smart_pbr = BoolProperty(name="Smart PBR", default=True)
    bpy.types.Scene.skp_max_instance = IntProperty(name="Max Instance", default=50)


def unregister():
    # Remove menu functions
    try: bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    except: pass
    try: bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    except: pass
    
    # Remove Scene properties safely
    props = ["skp_last_filepath", "skp_reuse_material", "skp_keep_transform",
             "skp_smart_pbr", "skp_max_instance"]
    for p in props:
        if hasattr(bpy.types.Scene, p):
            delattr(bpy.types.Scene, p)
    
    # Unregister classes in reverse order
    for cls in reversed((SketchupAddonPreferences, ImportSKP, ExportSKP, 
                         SKP_OT_reload, SKP_OT_proxy_toggle, SKP_OT_deep_purge, 
                         SKP_OT_purge_materials, SKP_PT_panel)):
        try: bpy.utils.unregister_class(cls)
        except: pass

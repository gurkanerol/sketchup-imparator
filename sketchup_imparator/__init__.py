"""SketchUp Imparator - native .skp importer for Blender.

The parser is OpenSKP (vendored, MIT), so no proprietary SketchUp SDK and no
compiled SketchUp bindings are required.  Components are imported with
instancing preserved: one mesh per component definition, one object per
placement, keeping SketchUp's own origins, rotation and scale.
"""

import gc
import os
import time

import bpy
from bpy.props import BoolProperty, FloatProperty, IntProperty, StringProperty
from bpy.types import AddonPreferences, Operator
from bpy_extras.io_utils import ImportHelper

from . import skp_scene

__author__ = "gurkanerol (2026 Modernization), Martijn Berger (Original Creator)"
__license__ = "GPL-3.0-or-later"

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

ADDON_VERSION = "2026.7.0"

bl_info = {
    "name": "SketchUp Imparator",
    "author": "gurkanerol, Martijn Berger, Sanjay Mehta, Arindam Mondal, Peter Kirkham",
    "version": (2026, 7, 0),
    "blender": (4, 2, 0),
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
        default=True,
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


def clear_import_state(importer):
    """Drop the parsed model so a reload does not keep it alive."""
    importer.skp_model = None
    importer.materials = {}
    importer.mesh_data = {}
    importer.curve_data = {}
    importer.images = {}


class SceneImporter:
    """Thin facade over :mod:`skp_scene` (kept for operator compatibility)."""

    version_string = ADDON_VERSION

    def __init__(self):
        self.skp_model = None
        self.filepath = ""
        self.filename_prefix = ""
        self.materials = {}
        self.mesh_data = {}
        self.curve_data = {}
        self.images = {}

    def set_filename(self, filename):
        self.filepath = filename
        self.basepath, self.skp_filename = os.path.split(self.filepath)
        self.filename_prefix = os.path.splitext(self.skp_filename)[0] + "_"
        return self

    def load(self, context, is_update=False, **options):
        """Import the .skp file set by :meth:`set_filename`."""
        context.scene.unit_settings.system = "METRIC"
        context.scene.unit_settings.scale_length = 1.0
        context.scene.unit_settings.length_unit = "METERS"

        started = time.time()
        if LOGS:
            skp_log(f"Importing: {self.filepath}")

        options = dict(options)
        options["is_update"] = is_update

        try:
            result = skp_scene.import_skp(self, context, options)
        except Exception as exc:
            self.report_error(exc)
            raise

        duration = time.time() - started
        summary = (
            f"Import finished: {len(self.materials)} materials, "
            f"{len(self.mesh_data)} meshes in {duration:.2f}s"
        )
        if LOGS:
            skp_log(summary)
            try:
                context.workspace.status_text_set(summary)
            except Exception:
                pass

        if not is_update:
            self._focus_view(context)

        clear_import_state(self)
        gc.collect()
        try:
            bpy.data.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
        except Exception:
            pass
        return result if isinstance(result, set) else {"FINISHED"}

    @staticmethod
    def report_error(exc):
        skp_log(f"SketchUp import failed: {exc}")

    @staticmethod
    def _focus_view(context):
        try:
            for area in context.screen.areas:
                if area.type == "VIEW_3D" and area.regions:
                    with context.temp_override(
                        window=context.window,
                        area=area,
                        region=area.regions[-1],
                    ):
                        bpy.ops.view3d.view_all(center=True)
        except Exception:
            pass


class ImportSKP(Operator, ImportHelper):
    """Import SketchUp Scene (.skp)"""

    bl_idname = "import_scene.skp"
    bl_label = "Import Sketchup Scene"
    bl_options = {"PRESET", "UNDO"}

    filename_ext = ".skp"
    filter_glob: StringProperty(default="*.skp", options={"HIDDEN"})

    import_scene: BoolProperty(
        name="Import Scene",
        description="Imports SketchUp scenes as Blender cameras",
        default=True,
    )

    is_update: BoolProperty(
        name="Is Update",
        description="Internal flag to indicate if this is a reload operation",
        default=False,
        options={"HIDDEN", "SKIP_SAVE"},
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

    import_scene_filter: StringProperty(
        name="Import A Scene :", description="Import a specific SketchUp Scene", default=""
    )

    def invoke(self, context, event):
        if context.scene.skp_last_filepath:
            self.filepath = context.scene.skp_last_filepath
        return super().invoke(context, event)

    def execute(self, context):
        keywords = self.as_keywords()

        scene = context.scene
        scene.skp_last_filepath = keywords.get("filepath", "")
        scene.skp_reuse_material = keywords.get("reuse_material", True)
        scene.skp_smart_pbr = keywords.get("smart_pbr", True)

        is_update = keywords.pop("is_update", False)
        return SceneImporter().set_filename(keywords["filepath"]).load(
            context, is_update=is_update, **keywords
        )

    def draw(self, context):
        layout = self.layout
        layout.label(text="- Primary Import Options -")
        layout.prop(self, "import_scene")
        layout.prop(self, "reuse_material")
        layout.prop(self, "smart_pbr")
        layout.prop(self, "import_standalone_edges")

        layout.label(text="- SketchUp Scenes -")
        row = layout.row()
        row.use_property_split = True
        row.prop(self, "import_scene_filter")


def menu_func_import(self, context):
    self.layout.operator(ImportSKP.bl_idname, text="SketchUp (.skp)")


class SKP_OT_reload(Operator):
    """Reload a specific SketchUp file"""

    bl_idname = "import_scene.skp_reload"
    bl_label = "Reload / Update Sketchup Scene"
    bl_options = {"REGISTER", "UNDO"}

    target_collection: StringProperty(name="Target Collection", default="")

    def execute(self, context):
        target_coll = None
        path = ""

        if self.target_collection:
            target_coll = bpy.data.collections.get(self.target_collection)
            if target_coll:
                path = target_coll.get("skp_filepath", "")

        if not path:
            obj = context.active_object
            if obj:
                curr_coll = obj.users_collection[0] if obj.users_collection else None
                while curr_coll:
                    if "skp_filepath" in curr_coll:
                        target_coll = curr_coll
                        path = curr_coll["skp_filepath"]
                        break
                    parent = None
                    for c in bpy.data.collections:
                        if curr_coll.name in c.children:
                            parent = c
                            break
                    curr_coll = parent

        if not path:
            path = context.scene.skp_last_filepath
            for c in bpy.data.collections:
                if c.get("skp_filepath") == path:
                    target_coll = c
                    break

        if not path or not os.path.exists(path):
            self.report(
                {"ERROR"},
                "No SketchUp source found for selection. Select an object from the "
                "SKP import or import a file first.",
            )
            return {"CANCELLED"}

        material_backup = {}
        modifier_backup = {}
        transform_backup = {}
        smoothing_backup = set()
        main_coll_name = ""
        import_edges = True
        if target_coll is not None:
            import_edges = bool(target_coll.get("skp_import_edges", True))

        main_coll = target_coll
        if main_coll:
            main_coll_name = main_coll.name
            bpy.context.view_layer.update()

            for obj in main_coll.all_objects:
                if obj.type != "MESH":
                    continue
                material_backup[obj.name] = [
                    slot.material.name if slot.material else None for slot in obj.material_slots
                ]
                if context.scene.skp_keep_transform:
                    transform_backup[obj.name] = obj.matrix_world.copy()

                supported_types = {"BEVEL", "SOLIDIFY", "MIRROR", "ARRAY", "SUBSURF"}
                target_mods = [m for m in obj.modifiers if m.type in supported_types]
                if target_mods:
                    mod_data = []
                    for m in target_mods:
                        data = {"name": m.name, "type": m.type}
                        if m.type == "BEVEL":
                            data.update(
                                {
                                    "width": m.width,
                                    "segments": m.segments,
                                    "limit_method": m.limit_method,
                                    "angle_limit": m.angle_limit,
                                    "harden_normals": getattr(m, "harden_normals", False),
                                    "miter_inner": getattr(m, "miter_inner", "OFFSET"),
                                    "miter_outer": getattr(m, "miter_outer", "SHARP"),
                                }
                            )
                        elif m.type == "SOLIDIFY":
                            data.update({"thickness": m.thickness, "offset": m.offset})
                        elif m.type == "MIRROR":
                            data.update(
                                {
                                    "use_axis": list(m.use_axis),
                                    "mirror_object": m.mirror_object.name
                                    if m.mirror_object
                                    else None,
                                }
                            )
                        elif m.type == "ARRAY":
                            data.update(
                                {
                                    "count": m.count,
                                    "relative_offset_displace": list(m.relative_offset_displace),
                                }
                            )
                        elif m.type == "SUBSURF":
                            data.update({"levels": m.levels, "render_levels": m.render_levels})
                        mod_data.append(data)
                    modifier_backup[obj.name] = mod_data

                if any("Smooth" in m.name for m in obj.modifiers):
                    smoothing_backup.add(obj.name)

            skp_log("Batch purging existing objects for fast reload...")
            obs_to_remove = list(main_coll.all_objects)
            bpy.data.batch_remove(ids=obs_to_remove)
            bpy.data.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
            gc.collect()

        bpy.ops.import_scene.skp(
            filepath=path,
            is_update=True,
            reuse_material=context.scene.skp_reuse_material,
            smart_pbr=context.scene.skp_smart_pbr,
            import_standalone_edges=import_edges,
        )

        new_main_coll = bpy.data.collections.get(main_coll_name) if main_coll_name else None
        if new_main_coll:
            bpy.context.view_layer.update()
            for obj in new_main_coll.all_objects:
                if obj.name in transform_backup:
                    obj.matrix_world = transform_backup[obj.name]

                if obj.type == "MESH" and obj.name in material_backup:
                    for i, mat_name in enumerate(material_backup[obj.name]):
                        if i < len(obj.material_slots) and mat_name:
                            mat = bpy.data.materials.get(mat_name)
                            if mat:
                                obj.material_slots[i].material = mat

                if obj.type == "MESH" and obj.name in modifier_backup:
                    for m_data in modifier_backup[obj.name]:
                        if m_data["name"] in obj.modifiers:
                            continue
                        try:
                            m = obj.modifiers.new(name=m_data["name"], type=m_data["type"])
                            if m_data["type"] == "BEVEL":
                                m.width = m_data["width"]
                                m.segments = m_data["segments"]
                                m.limit_method = m_data["limit_method"]
                                m.angle_limit = m_data["angle_limit"]
                                if hasattr(m, "harden_normals"):
                                    m.harden_normals = m_data["harden_normals"]
                                m.miter_inner = m_data["miter_inner"]
                                m.miter_outer = m_data["miter_outer"]
                            elif m_data["type"] == "SOLIDIFY":
                                m.thickness = m_data["thickness"]
                                m.offset = m_data["offset"]
                            elif m_data["type"] == "MIRROR":
                                m.use_axis = m_data["use_axis"]
                                if m_data["mirror_object"]:
                                    m.mirror_object = bpy.data.objects.get(m_data["mirror_object"])
                            elif m_data["type"] == "ARRAY":
                                m.count = m_data["count"]
                                m.relative_offset_displace = m_data["relative_offset_displace"]
                            elif m_data["type"] == "SUBSURF":
                                m.levels = m_data["levels"]
                                m.render_levels = m_data["render_levels"]
                        except Exception as exc:
                            skp_log(f"Failed to restore modifier {m_data['name']}: {exc}")

        if smoothing_backup:
            prefs = context.preferences.addons.get(__name__.split(".")[0])
            if prefs and prefs.preferences.skp_keep_smoothing:
                objects = [
                    bpy.data.objects.get(name)
                    for name in smoothing_backup
                    if bpy.data.objects.get(name) is not None
                ]
                self._restore_smoothing(context, objects)

        self.report({"INFO"}, f"Reloaded: {os.path.basename(path)}")

        for _ in range(2):
            try:
                bpy.data.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
            except Exception:
                pass

        return {"FINISHED"}

    @staticmethod
    def _restore_smoothing(context, objects):
        if not objects:
            return
        try:
            bpy.ops.object.select_all(action="DESELECT")
            for obj in objects:
                obj.select_set(True)
            context.view_layer.objects.active = objects[0]
            bpy.ops.object.shade_smooth_by_angle()
            bpy.ops.object.select_all(action="DESELECT")
        except Exception as exc:
            skp_log(f"Smoothing restore failed: {exc}")


class SKP_OT_proxy_toggle(Operator):
    """Toggle between Full Geometry and Bounding Box for SKP data"""

    bl_idname = "import_scene.skp_proxy_toggle"
    bl_label = "Toggle Proxy Mode"

    target_collection: StringProperty(name="Target Collection", default="")

    def execute(self, context):
        main_coll = None
        if self.target_collection:
            main_coll = bpy.data.collections.get(self.target_collection)

        if not main_coll:
            for c in bpy.data.collections:
                if "skp_filepath" in c:
                    main_coll = c
                    break

        if not main_coll:
            return {"CANCELLED"}

        current_state = "TEXTURED"
        for obj in main_coll.all_objects:
            if obj.type == "MESH":
                current_state = obj.display_type
                break

        new_state = "BOUNDS" if current_state != "BOUNDS" else "TEXTURED"
        for obj in main_coll.all_objects:
            if obj.type == "MESH":
                obj.display_type = new_state
                obj.show_all_edges = new_state != "BOUNDS"

        return {"FINISHED"}


class SKP_OT_delete(Operator):
    """Completely remove an imported SketchUp file and its data"""

    bl_idname = "import_scene.skp_delete"
    bl_label = "Delete SKP Import"
    bl_options = {"REGISTER", "UNDO"}

    target_collection: StringProperty(name="Target Collection", default="")

    def execute(self, context):
        if not self.target_collection:
            return {"CANCELLED"}
        target_coll = bpy.data.collections.get(self.target_collection)
        if target_coll:
            obs = list(target_coll.all_objects)
            bpy.data.batch_remove(ids=obs)
            for child in list(target_coll.children_recursive):
                bpy.data.collections.remove(child)
            bpy.data.collections.remove(target_coll)
            bpy.data.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

        self.report({"INFO"}, f"Deleted SketchUp import: {self.target_collection}")
        return {"FINISHED"}


class SKP_OT_deep_purge(Operator):
    """Deep clean all unused data-blocks, empty objects and collections"""

    bl_idname = "import_scene.skp_deep_purge"
    bl_label = "Deep Purge"

    def execute(self, context):
        bpy.data.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

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

        empties_removed = 0
        for obj in list(bpy.data.objects):
            if obj.type == "EMPTY" and not obj.children:
                if obj.get("skp_imported"):
                    bpy.data.objects.remove(obj, do_unlink=True)
                    empties_removed += 1

        colls_removed = 0
        for coll in list(bpy.data.collections):
            if coll.name not in skp_descendants:
                continue
            if not coll.all_objects and not coll.children:
                if coll.library is None and coll.asset_data is None:
                    bpy.data.collections.remove(coll)
                    colls_removed += 1

        bpy.data.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

        self.report(
            {"INFO"}, f"Deep Purge: Removed {empties_removed} pivots and {colls_removed} collections."
        )
        return {"FINISHED"}


class SKP_OT_purge_materials(Operator):
    """Clean unused materials and empty slots while respecting Fake User protection"""

    bl_idname = "import_scene.skp_purge_materials"
    bl_label = "Purge Materials"

    def execute(self, context):
        count = 0

        slots_removed = 0
        for obj in bpy.data.objects:
            if obj.type != "MESH" or obj.data.library is not None:
                continue

            used_indices = {p.material_index for p in obj.data.polygons}

            for i in range(len(obj.material_slots) - 1, -1, -1):
                if i in used_indices:
                    continue
                mat = obj.material_slots[i].material

                if mat is None:
                    can_remove = True
                elif mat.use_fake_user:
                    can_remove = False
                elif "DefaultMaterial" in mat.name:
                    can_remove = True
                else:
                    can_remove = bool(mat.get("skp_imported"))

                if can_remove:
                    try:
                        obj.data.materials.pop(index=i)
                        slots_removed += 1
                    except (RuntimeError, TypeError):
                        pass

        for _ in range(3):
            for mat in list(bpy.data.materials):
                if mat.library is None and mat.asset_data is None:
                    if mat.users == 0 and not mat.use_fake_user:
                        bpy.data.materials.remove(mat, do_unlink=True)
                        count += 1

            bpy.data.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

        self.report(
            {"INFO"},
            f"Material Purge: Removed {count} unused materials and {slots_removed} empty slots.",
        )
        return {"FINISHED"}


class SKP_OT_apply_smooth(Operator):
    """Apply Smooth by Angle to selected objects"""

    bl_idname = "import_scene.skp_apply_smooth"
    bl_label = "Smooth Selected"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        selected = context.selected_objects
        count = 0

        if context.active_object and context.active_object.mode != "OBJECT":
            bpy.ops.object.mode_set(mode="OBJECT")

        for ob in selected:
            if ob.type == "MESH":
                context.view_layer.objects.active = ob
                ob.select_set(True)

                try:
                    bpy.ops.object.shade_smooth()

                    bpy.ops.object.shade_smooth_by_angle()

                    if not any("Smooth" in m.name for m in ob.modifiers):
                        bpy.ops.object.modifier_add_node_group(
                            asset_library_type="ESSENTIALS", asset_identifier="Smooth by Angle"
                        )
                    count += 1
                except Exception as exc:
                    skp_log(f"Smoothing failed: {exc}")

        self.report({"INFO"}, f"Added Smooth by Angle modifier to {count} objects.")
        return {"FINISHED"}


class SKP_PT_panel(bpy.types.Panel):
    """Sketchup Imparator Side Panel"""

    bl_label = "SketchUp Imparator"
    bl_idname = "SKP_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Sketchup"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.scale_y = 1.5
        row.operator("import_scene.skp", text="IMPORT NEW SKP", icon="IMPORT")

        layout.separator()

        box = layout.box()
        row = box.row(align=True)
        row.operator("import_scene.skp_apply_smooth", text="Smooth", icon="MOD_SMOOTH")
        row.operator("import_scene.skp_deep_purge", text="Purge", icon="TRASH")

        layout.separator()

        layout.label(text="Imported SketchUp Files:", icon="FILE_3D")

        skp_imports_found = False

        for coll in bpy.data.collections:
            if "skp_filepath" in coll:
                skp_imports_found = True
                path = coll["skp_filepath"]
                filename = os.path.basename(path)

                box = layout.box()
                row = box.row(align=True)
                row.label(text=filename, icon="COLLECTION_NEW")

                r_op = row.operator("import_scene.skp_reload", text="", icon="FILE_REFRESH")
                r_op.target_collection = coll.name

                p_op = row.operator("import_scene.skp_proxy_toggle", text="", icon="GHOST_ENABLED")
                p_op.target_collection = coll.name

                d_op = row.operator("import_scene.skp_delete", text="", icon="REMOVE")
                d_op.target_collection = coll.name

        if not skp_imports_found:
            layout.label(text="No SKP files in scene.", icon="INFO")

        layout.separator()

        if skp_imports_found or scene.skp_last_filepath:
            col = layout.column(align=True)
            box = col.box()
            box.label(text="Global Settings:", icon="SETTINGS")
            box.prop(scene, "skp_reuse_material", text="Keep My Material Edits")
            box.prop(scene, "skp_keep_transform", text="Keep My Placement")
            box.prop(scene, "skp_smart_pbr", text="Convert to Smart PBR")

            col.separator()

            layout.label(text="Advanced Tools:")
            grid = layout.grid_flow(columns=2, align=True)
            grid.operator("import_scene.skp_proxy_toggle", text="Global Proxy", icon="GHOST_ENABLED")
            grid.operator("import_scene.skp_deep_purge", text="Deep Purge", icon="TRASH")
            grid.operator("import_scene.skp_purge_materials", text="Purge Mats", icon="MATERIAL")


def register():
    for cls in (
        SketchupAddonPreferences,
        ImportSKP,
        SKP_OT_reload,
        SKP_OT_proxy_toggle,
        SKP_OT_delete,
        SKP_OT_deep_purge,
        SKP_OT_purge_materials,
        SKP_OT_apply_smooth,
        SKP_PT_panel,
    ):
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

    bpy.types.Scene.skp_last_filepath = StringProperty(name="Last SKP File", default="")
    bpy.types.Scene.skp_reuse_material = BoolProperty(name="Use Existing Materials", default=True)
    bpy.types.Scene.skp_keep_transform = BoolProperty(name="Keep Placement", default=True)
    bpy.types.Scene.skp_smart_pbr = BoolProperty(name="Smart PBR", default=True)


def unregister():
    try:
        bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    except Exception:
        pass

    props = [
        "skp_last_filepath",
        "skp_reuse_material",
        "skp_keep_transform",
        "skp_smart_pbr",
    ]
    for p in props:
        if hasattr(bpy.types.Scene, p):
            delattr(bpy.types.Scene, p)

    for cls in reversed(
        (
            SketchupAddonPreferences,
            ImportSKP,
            SKP_OT_reload,
            SKP_OT_proxy_toggle,
            SKP_OT_delete,
            SKP_OT_deep_purge,
            SKP_OT_purge_materials,
            SKP_OT_apply_smooth,
            SKP_PT_panel,
        )
    ):
        try:
            bpy.utils.unregister_class(cls)
        except Exception:
            pass

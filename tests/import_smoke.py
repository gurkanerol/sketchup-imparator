"""Headless smoke test for the importer.

Run it with a real .skp file:

    blender -b --factory-startup --python tests/import_smoke.py -- "/path/to/file.skp"

Exits non-zero (through an assertion) if the import, reload, proxy or delete
flow misbehaves.  It is deliberately free of framework dependencies so it can
run against an installed extension or the source tree.
"""

import sys
import time

import addon_utils
import bpy


def _enable_addon():
    """Prefer the installed extension, fall back to the source tree."""
    for name in ("bl_ext.user_default.sketchup_imparator", "sketchup_imparator"):
        try:
            addon_utils.enable(name, default_set=True, persistent=True)
        except Exception:
            continue
        module = sys.modules.get(name)
        if module is not None:
            print(f"enabled {name}")
            return module
    raise RuntimeError("sketchup_imparator is not installed")


def _strip_factory_scene():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    bpy.data.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)


def _counts():
    objects = list(bpy.data.objects)
    meshes = [o for o in objects if o.type == "MESH"]
    return {
        "objects": len(objects),
        "meshes": len(meshes),
        "curves": sum(1 for o in objects if o.type == "CURVE"),
        "empties": sum(1 for o in objects if o.type == "EMPTY"),
        "mesh_data": len(bpy.data.meshes),
        "materials": len(bpy.data.materials),
        "packed_images": sum(1 for i in bpy.data.images if i.packed_file),
        "no_uv": sum(1 for o in meshes if not o.data.uv_layers),
    }


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    if not argv:
        raise SystemExit("usage: blender -b --python tests/import_smoke.py -- file.skp")
    filepath = argv[0]

    _strip_factory_scene()
    module = _enable_addon()

    started = time.time()
    importer = module.SceneImporter().set_filename(filepath)
    importer.load(bpy.context)
    print(f"import took {time.time() - started:.2f}s")

    first = _counts()
    print("after import:", first)
    assert first["objects"] > 0, "nothing was imported"
    assert first["mesh_data"] > 0, "no mesh datablocks were created"
    assert first["no_uv"] == 0, f"{first['no_uv']} meshes have no UV map"

    roots = [c for c in bpy.data.collections if "skp_filepath" in c]
    assert roots, "the import collection was not tagged with skp_filepath"
    root = roots[0]

    # every object must live in a collection and be tagged
    orphans = [o for o in bpy.data.objects if not o.users_collection]
    assert not orphans, f"{len(orphans)} objects are not linked to a collection"
    untagged = [o for o in bpy.data.objects if not o.get("skp_imported")]
    assert not untagged, f"{len(untagged)} objects are missing the skp_imported tag"

    bpy.ops.import_scene.skp_proxy_toggle(target_collection=root.name)
    bounds = sum(1 for o in root.all_objects if o.display_type == "BOUNDS")
    bpy.ops.import_scene.skp_proxy_toggle(target_collection=root.name)
    print(f"proxy toggled {bounds} meshes to bounds and back")

    started = time.time()
    bpy.ops.import_scene.skp_reload(target_collection=root.name)
    print(f"reload took {time.time() - started:.2f}s")
    second = _counts()
    print("after reload:", second)
    assert second["meshes"] == first["meshes"], "reload changed the mesh count"
    assert second["curves"] == first["curves"], "reload changed the curve count"

    before_purge = len(bpy.data.materials)
    bpy.ops.import_scene.skp_purge_materials()
    used = sum(1 for m in bpy.data.materials if m.users)
    print(f"materials {before_purge} -> {len(bpy.data.materials)} ({used} in use)")
    assert used == len(bpy.data.materials), "material purge removed a material in use"

    bpy.ops.import_scene.skp_deep_purge()
    bpy.ops.import_scene.skp_delete(target_collection=root.name)
    remaining = [c for c in bpy.data.collections if "skp_filepath" in c]
    assert not remaining, "delete left the import collection behind"
    print("delete left", len(bpy.data.objects), "objects and", len(bpy.data.materials), "materials")
    print("SMOKE TEST PASSED")


if __name__ == "__main__":
    main()

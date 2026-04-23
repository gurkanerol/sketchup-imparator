# SketchUp Importer Handover Notes

## 1. Core State
- **Root Directory:** `/Volumes/SSD256/Sketchup_Importer-master`
- **Stable Version:** `v2026.1.53`
- **Author Signature:** `gurkanerol`

## 2. Technical Fixes (Permanent)
- **Memory Fix (sketchup.pyx):** Converted `SUEntityRef` addresses to hex-strings to prevent 64-bit `OverflowError`. Do NOT revert to `size_t` or integer-based handles.
- **Dependency Fixes:** `import math` and `empty_display_type = "PLAIN_AXES"` are correctly implemented in `__init__.py`.
- **Material Optimization:** Enabled safe `reuse_material` logic to skip node recreation for existing materials without affecting mesh geometry.

## 3. UI & Features
- **Reload Button:** Added a "Reload" operator that uses `context.scene.skp_last_filepath`.
- **Auto-Purge:** Reload triggers `bpy.ops.outliner.orphans_purge` with `do_linked_ids=True` to clear the cache and keep the scene running smoothly.

## 4. Maintenance
- Avoid "Smart Sync" (partial object updates) as it ruins the SketchUp hierarchy.
- Stick to "Sterilized Re-import" logic (delete old collection, re-import fresh) for 100% accuracy.
- Build command: `./uv run python3 build_addons.py` after cleaning `build/` and `dist/`.

**System Status: STABLE & CLEAN**

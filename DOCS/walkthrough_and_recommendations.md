# Walkthrough & Imparator Recommendations
## Usage Guide
1. **First Import:** Use File > Import > SketchUp (.skp). This sets the focus.
2. **Iterate:** After making changes in SketchUp, just hit **RELOAD** in the sidebar. The scene updates, old meshes are purged, and the model stays fresh.
3. **Performance:** If the viewport lags, click **Proxy Mode** to turn complex geometry into boxes. Click again to restore.
4. **Maintenance:** Use **Deep Purge** before major saves to keep file size small.
## Critical Recommendations
- **Units:** Never change the core scaling code (manual 0.0254 etc.) unless Blender scene units are strictly Meter-bound and drifting.
- **Origins:** The current aggressive flattening keeps outliner clean. If you need deep hierarchies, you must toggle the recursion logic in __init__.py.
- **Persistence:** Reload relies on skp_last_filepath scene property. Always save your Blender file to keep this metadata alive.

# SketchUp Imparator

Native SketchUp (`.skp`) importer for Blender. No proprietary SketchUp SDK, no
compiled bindings — parsing is done by the bundled [OpenSKP](https://github.com/iamahsanmehmood/openskp)
reader, so the add-on installs like any other Blender extension.

## Features

- **Real instancing.** Every component definition is imported once; every
  placement becomes an object that references that mesh. Origins, rotation and
  scale stay exactly as in SketchUp, and editing one definition updates all of
  its copies.
- **Clean geometry.** Faces are triangulated with `mapbox_earcut`, then
  coplanar triangles are merged into ngons (faces with holes keep their
  holes); flat shading is applied. Loose edges go to an `Edges` collection (you can hide/show it manually).
- **Small package.** The whole extension zip is ~461 KB: three wheels
  (`defusedxml`, plus `mapbox_earcut` at 66 KB per Python ABI) and
  pure-Python parsing. `shapely`
  is optional upstream and is not bundled — install it yourself only if you
  need the overlapping-hole union path.
- **Baked UVs.** Texture coordinates arrive per-vertex from SketchUp, so one
  image repetition equals one SketchUp tile without any Mapping-node scaling.
- **Materials.** SketchUp materials, colours, transparency and colourized
  textures are rebuilt as Principled BSDF node trees. Images are packed into the
  .blend, nothing is left behind on disk.
- **Tags.** Every SketchUp tag becomes a collection under `SKP: <file>`, with
  the tag's hidden state carried over to viewport and render visibility.
- **Scenes.** SketchUp scenes import as Blender cameras (perspective and
  orthographic), including per-scene hidden tags.
- **Loose edges.** Standalone edges are imported as curve objects, including
  edge sets that belong to a definition that also has faces.
- **Reload.** Re-import a file in place while keeping object transforms,
  material assignments, supported modifiers and Smooth-by-Angle. With
  **Reload When Saved in SketchUp** on, the add-on polls the file every two
  seconds and re-imports it a moment after you save it there.
- **Proxy, purge and delete.** One-click bounding-box mode for heavy scenes,
  Deep Purge for leftover empties/collections, and a material purge that
  respects Fake User.

## Installation

### Blender extensions platform
1. Download the latest `sketchup_imparator-<version>.zip` from the releases page.
2. **Edit > Preferences > Get Extensions**, open the menu in the top right and
   choose **Install from Disk…**.
3. Pick the zip and enable **SketchUp Imparator**.
4. The `mapbox_earcut` wheels bundled in the zip are installed
   into the extension's local site-packages on first enable.

### Manual
Unzip into your extensions folder (`.../Blender/<version>/extensions/user_default/`)
or drop the zip into **Install from Disk**. Do not unzip the wheels by hand —
Blender resolves them for the running Python version.

## Usage

1. **File > Import > SketchUp (.skp)**.
2. Pick the file and press **Import Sketchup Scene**.
   - *Import Scene* — import SketchUp scenes as cameras.
   - *Use Existing Materials* — keep your edits when re-importing.
   - *Enable Smart PBR Materials* — glass/metal/water presets by material name.
   - *Import Standalone Edges* — import loose edges as curves.
   - *Import A Scene* — restrict camera import to one SketchUp scene.
3. The 3D View sidebar tab **Sketchup** holds reload, proxy, purge, delete and
   the global settings.

## Compatibility

- Blender **4.2+** (verified on 4.2 and 5.2).
- macOS Apple Silicon (`macos-arm64`). The wheels are the only platform-bound
  part; adding Windows/Linux would mean adding their wheels to `wheels/` and to
  `platforms` in the manifest.
- SketchUp files up to and including 2025.x (whatever OpenSKP reads).

## How it works

```
.skp ── OpenSKP (_vendor/openskp) ──► InstancedScene
                                        ├── gltf_materials + textures
                                        ├── mesh_resources  (definition-local)
                                        ├── curve_resources (loose edges)
                                        └── node tree       (per-placement matrices)
                                             │
                                   skp_scene.py (Blender)
                                             │
                        meshes · curves · materials · collections · cameras
```

- OpenSKP converts the file to glTF conventions (Y-up, metres). The importer
  converts once with `(x, y, z) → (x, −z, y)` and maps node matrices with
  `B · M · B⁻¹`, so Blender stays Z-up and dimensions are real metres.
- One mesh datablock per definition variant; one object per placement.
- Empties are created only for nodes that have children and no geometry.

## Development

```bash
# build the extension zip (reads the version from blender_manifest.toml)
python3 build_addons.py            # -> dist/sketchup_imparator-<version>.zip

# validate the package
blender -b --command extension validate dist/sketchup_imparator-<version>.zip

# import smoke test (headless)
blender -b --factory-startup --python tests/import_smoke.py -- "/path/to/file.skp"
```

Layout:

| Path | Purpose |
| --- | --- |
| `sketchup_imparator/__init__.py` | add-on entry, operators, panels, reload |
| `sketchup_imparator/skp_scene.py` | SketchUp → Blender conversion |
| `sketchup_imparator/_vendor/openskp/` | vendored parser (MIT), unmodified upstream |
| `sketchup_imparator/shapely_fallback.py` | skips openskp's optional hole union |
| `sketchup_imparator/wheels/` | defusedxml + mapbox_earcut wheels |
| `blender_manifest.toml` | extension manifest, version source of truth |

## Licence

GPL-3.0-or-later. Bundled third-party components and their licences are listed
in [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).

## Credits

- **gurkanerol** — 2026 rewrite: OpenSKP backend, instancing, extension packaging.
- **Martijn Berger** — original `pyslapi` / importer.
- **Sanjay Mehta, Arindam Mondal, Peter Kirkham** — hierarchy, transform and
  C API contributions.
- **Ahsan Mehmood** — OpenSKP.

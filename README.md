# SketchUp Imparator
Python bindings for the official Sketchup API and an importer for blender based on them


## Installing the Addon in Blender

### Method 1: Direct Installation (Recommended)
1) Download the latest release from [the releases page](https://github.com/gurkanerol/sketchup-imparator/releases)
2) Start Blender
3) From the top menu, choose: **Edit > Preferences...**
4) Click on the **Add-ons** tab
5) Click on the **Install...** button
6) Browse to and select the downloaded zip file (e.g., `sketchup_imparator_v2026.1.0.zip`)
7) Click **Install Add-on**
8) In the add-ons list, search for "Sketchup"
9) Enable the add-on by clicking the checkbox next to **Import-Export: Sketchup importer**
10) Click **Save Preferences** to keep the add-on enabled for future Blender sessions

### Method 2: Manual Installation
1) Download the latest release zip file
2) Unpack the zip file into Blender's addons folder:
   - Windows: `%APPDATA%\Blender Foundation\Blender\[version]\scripts\addons`
   - macOS: `~/Library/Application Support/Blender/[version]/scripts/addons`
   - Linux: `~/.config/blender/[version]/scripts/addons`
3) Restart Blender and enable the add-on as described in steps 3-10 above

## Using the Addon
Once installed and enabled, you can import Sketchup files (.skp) by:
1) From Blender's top menu, choose: **File > Import > Import Sketchup Scene (.skp)**
2) Navigate to and select your .skp file
3) Adjust import settings if needed and click **Import Sketchup Scene**

## Compatibility
The latest version of the importer is compatible with:
- Blender 5.1
- Python 3.13
- Various versions of SketchUp files up to and including version 2025.1

## Version 2026.1 Modernization

This version introduces a major overhaul of the geometry and texture pipeline, modernized by **gurkanerol** for professional-grade Blender workflows:

- **Robust N-gon Pipeline**: Replaced ambiguous loop extraction with a failsafe "Triangulate + Dissolve" strategy. This ensures that all faces are imported as solid geometry with perfect support for complex holes and booleans.
- **Precision Texture Mapping**: Fixed a long-standing issue where textures appeared incorrectly scaled. The importer now correctly interprets SketchUp's STQ coordinates using material-specific scaling (`s_scale`, `t_scale`).
- **Blender 5.1 & Python 3.13 Support**: Built with the latest Python 3.13 stable ABI for future-proof compatibility with modern Blender releases.
- **Improved Portability**: Automated build script (`build_addons.py`) that handles complex internal framework dependencies, ensuring the addon works out-of-the-box on different macOS systems.

## Features Not Yet Implemented

### Platform Support
- **Linux/Windows Support**: Currently focused on macOS Apple Silicon. Windows support can be added by providing the corresponding DLLs in the framework structure.

### Import Options
- **Line-Only Import**: Future feature to import standalone edge geometry.

---

## Technical Credits
- **gurkanerol**: Lead Architect & 2026 Modernization (N-gons, UV Scaling, Mac Build Automation)
- **Martijn Berger**: Original `pyslapi` creator (Historical context)
- **Peter Kirkham**: Hierarchy and transformation fixes (v0.25)
- **Sanjay Mehta, Arindam Mondal**: C API binding contributions

---

## Build Instructions (Developers)

The project is now fully automated for easy maintenance.

### Prerequisites (macOS)
1. **Python 3.13** (via pyenv or python.org)
2. **uv** package manager: `curl -LsSf https://astral.sh/uv/install.sh | sh`
3. **SketchUp SDK**: Download and extract to the root.

### Build & Package
1. Copy `SketchUpAPI.framework` and `LayOutAPI.framework` to the root directory.
2. Run the automated build script:
   ```bash
   ./uv run python3 build_addons.py
   ```
3. The distributable addon will be generated in:
   `dist/sketchup_imparator_v2026.1.0.zip`

---
*Note: This project is licensed under the GPL-3.0 License.*

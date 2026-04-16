# Project Modernization Summary (2026)

This document summarizes the major technical improvements made to the SketchUp Importer project by **gurkanerol** during the April 2026 modernization cycle.

## 1. Geometry Pipeline Overhaul
- **Native N-gon Support**: Transitioned from basic triangle-only import to a sophisticated "Triangulate-then-Dissolve" strategy. This allows complex faces with holes to be imported as clean, Blender-native N-gons.
- **Fail-Safe Robustness**: Switched to a MeshHelper-based extraction that guarantees solid geometry even for non-convex or hollowed-out SketchUp objects.
- **Vertex Deduplication**: Implemented precision vertex merging at both the C++ and Python layers to ensure manifold meshes.

## 2. Texturing & UV Accuracy
- **UV Scaling Fix**: Resolved a persistent issue where imported textures appeared at incorrect scales. The importer now retrieves `s_scale` and `t_scale` metadata from SketchUp materials to properly normalize UV coordinates.
- **Precision STQ Mapping**: Optimized the conversion of SketchUp's internal STQ coordinates to Blender-compatible UV loops.

## 3. Platform & Build Automation
- **Blender 5.1 Ready**: Verified and optimized for Blender 5.1 and Python 3.13.
- **Automated Build System**: Created `build_addons.py`, a robust Python-based build tool that automates:
    - Cython compilation.
    - Framework bundling.
    - Internal library path fixing (`install_name_tool`).
    - ZIP packaging for distribution.
- **Framework Self-Containment**: Enhanced the packaging logic to include all internal dynamic libraries (`Frameworks/`, `Libraries/`), resolving missing dependency errors (`@rpath` issues) on clean macOS installations.

## 4. Contributor Recognition
- **gurkanerol** added to official contributor list in `bl_info` and documentation.
- Project structure reorganized for portability and GitHub readiness.

---
**Lead Architect for 2026 Update**: gurkanerol
**Base Project**: pyslapi by Martijn Berger

# SketchUp Imparator Implementation Plan
## Objectives
- Modernize SketchUp Importer for Blender 4.2+ (Python 3.11+ / 3.13 stability)
- Implement high-performance N-gon geometry processing.
- Establish a reliable Reload/Update workflow for architectural iterations.
## Done
- C-API Sterilization (Zero RAM leaks via try...finally blocks).
- Reload Operator with deep collection and data-block purging.
- Proxy Mode and Deep Purge utility tools.
- Identity-Scale preservation (1:1 with SketchUp units as per user preference).

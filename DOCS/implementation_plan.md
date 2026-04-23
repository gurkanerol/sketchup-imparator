# Refactor SketchUp Mesh Instancing to Shared Mesh Data (Alt+D)

Transition the SketchUp Importer from the complex "Dupli-Vert" / "Collection Instance" architecture to a native "Shared Mesh Data" system. This will enable direct, non-destructive editability of individual instances in Blender while maintaining memory efficiency through data-block sharing.

## User Review Required

> [!IMPORTANT]
> This change will remove the "Instancing Threshold" (max_instance) and "Instancing Type" (Vertex/Face) options from the import UI, as all components will now be imported as first-class Blender objects with shared data.

> [!NOTE]
> This approach makes the scene hierarchy much more "Blender-native", allowing users to move, rotate, and scale individual component instances without editing a parent "Dupli-mesh".

## Proposed Changes

### [sketchup_imparator](file:///Volumes/SSD256/Sketchup_Importer-master/sketchup_imparator)

Summary: Remove all Dupli-Vert/Collection Instance logic and refactor the main import pipeline to use a clean recursive approach with mesh data caching.

#### [MODIFY] [__init__.py](file:///Volumes/SSD256/Sketchup_Importer-master/sketchup_imparator/__init__.py)

- **New Property**: Add `use_shared_instances` (BoolProperty, default=True) to `ImportSKP`.
- **`SceneImporter.load`**:
    - If `use_shared_instances` is True:
        - Bypasses `write_duplicateable_groups` and instancing passes.
        - Directly calls `write_entities` for a one-pass recursive import.
    - If `use_shared_instances` is False:
        - Falls back to the existing legacy Dupli-Vert logic (stability mode).
- **`write_entities`**:
    - Naturally handles all instances when `component_skip` is empty (which it will be in Shared Instance mode).
    - Caching in `write_mesh_data` ensures mesh blocks are shared correctly.
- **UI Layout**:
    - Group legacy options (Instancing Threshold, Type) under a sub-box that only appears if "Shared Instances" is disabled.

## Open Questions

- Should we keep any "Performance Mode" that uses Dupli-Verts for extremely large scenes (e.g., 50,000+ tiny bushes)?
    - *Proposed Answer*: No, standard Shared Mesh Data (Alt+D) is very efficient in modern Blender Versions (4.x/5.x), and the workflow benefits of individual objects outweigh the minor speed gain of Dupli-Verts.

## Verification Plan

### Automated Tests
- Import a SketchUp file with multiple instances of the same component.
- Verify in Blender's Outliner (Data API view) that:
    1. Multiple Objects exist for the instances.
    2. Only ONE Mesh data-block exists for the component geometry.
    3. Modifying the mesh of one instance (in Edit Mode) updates all others.

### Manual Verification
- Test with "Organize by Tags" enabled and disabled.
- Verify "Reload" functionality still works correctly with the new architecture.
- Verify that hierarchy (parenting) is correctly preserved.

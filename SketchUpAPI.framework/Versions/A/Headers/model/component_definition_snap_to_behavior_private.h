/**
 * @file
 * @brief Definition for \ref SUSnapToBehavior. Don't include directly.
 *
 * @warning Do not include this header directly. This file is part of a
 *   compatibility shim. Instead include `SketchUpAPI/model/component_definition.h`.
 */

/**
@enum SUSnapToBehavior
@headerfile <SketchUpAPI/model/component_definition.h>
@brief Describes how the component instance can be placed when a user adds it to a model.

For example a window component instance should snap to a vertical plane.

@see SUComponentBehavior

@bug This enum was incorrectly defined inside the \ref SUComponentBehavior struct. This is
  not valid C. As of SketchUp 2025.0 (API 13.0), this enum is conditionally defined outside
  of the struct when the header is consumed by a C compiler.

@code
// Usage from a C compiler:
SUSnapToBehavior behavior;
SUComponentDefinitionSetBehavior(component_definition, &behavior);
if (behavior.component_snap == SUSnapToBehavior_Vertical) {
  // ...
}
@endcode

@code
// Usage from a C++ compiler:
SUSnapToBehavior behavior;
SUComponentDefinitionSetBehavior(component_definition, &behavior);
if (behavior.component_snap == SUComponentBehavior::SUSnapToBehavior_Vertical) {
  // ...
}
@endcode
*/
enum SUSnapToBehavior {
  SUSnapToBehavior_None = 0,
  SUSnapToBehavior_Any,
  SUSnapToBehavior_Horizontal,
  SUSnapToBehavior_Vertical,
  SUSnapToBehavior_Sloped
};

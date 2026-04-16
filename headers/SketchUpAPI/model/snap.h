// Copyright 2024 Trimble Inc. All Rights Reserved.

/**
 * @file
 * @brief Interfaces for SUSnapRef.
 */
#ifndef SKETCHUP_MODEL_SNAP_H_
#define SKETCHUP_MODEL_SNAP_H_

#include <SketchUpAPI/common.h>
#include <SketchUpAPI/geometry.h>
#include <SketchUpAPI/model/defs.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
@struct SUSnapRef
@extends SUDrawingElementRef
@brief  References a snap.
@since SketchUp 2025.0, API 13.0

A Snap is a custom grip used by SketchUp's Move tool. Snaps can be added at strategic places such
as connectors to help assembling objects.

\image html snaps.png

SUSnapGetDirection() is the direction a snap is "pointing". This can be thought of as the normal
direction of the snap. It can also be thought of as the direction you move an object when plugging
it into another object, e.g. inserting a power coord.

SUSnapGetUp() controls the rotation around the Snap's axis.

When two objects are snapped together, the Snaps have opposite SUSnapGetDirection() vectors but
matching SUSnapGetUp() vectors.
*/

/**
@brief Converts from an \ref SUSnapRef to an \ref SUEntityRef.
       This is essentially an upcast operation.
@since SketchUp 2025.0, API 13.0
@param[in] snap The given snap reference.
@related SUSnapRef
@return
- The converted SUEntityRef if \p snap is a valid snap.
- If not, the returned reference will be invalid.
*/
SU_EXPORT SUEntityRef SUSnapToEntity(SUSnapRef snap);

/**
@brief Converts from an \ref SUEntityRef to an \ref SUSnapRef.
       This is essentially a downcast operation so the given entity must be
       convertible to an \ref SUSnapRef.
@since SketchUp 2025.0, API 13.0
@param[in] entity The given entity reference.
@related SUSnapRef
@return
- The converted SUSnapRef if the downcast operation succeeds
- If not, the returned reference will be invalid
*/
SU_EXPORT SUSnapRef SUSnapFromEntity(SUEntityRef entity);

/**
@brief Converts from an \ref SUSnapRef to an \ref SUDrawingElementRef.
       This is essentially an upcast operation.
@since SketchUp 2025.0, API 13.0
@param[in] snap The given snap reference.
@related SUSnapRef
@return
- The converted \ref SUEntityRef if \p snap is a valid snap.
- If not, the returned reference will be invalid.
*/
SU_EXPORT SUDrawingElementRef SUSnapToDrawingElement(SUSnapRef snap);

/**
@brief Converts from an \ref SUDrawingElementRef to an \ref SUSnapRef.
       This is essentially a downcast operation so the given element must be
       convertible to an SUSnapRef.
@since SketchUp 2025.0, API 13.0
@param[in] drawing_elem The given element reference.
@related SUSnapRef
@return
- The converted \ref SUSnapRef if the downcast operation succeeds
- If not, the returned reference will be invalid
*/
SU_EXPORT SUSnapRef SUSnapFromDrawingElement(SUDrawingElementRef drawing_elem);

/**
@brief Creates a snap at the given position and orientation.
@since SketchUp 2025.0, API 13.0
@param[out] snap       The snap object created.
@param[in]  position   The position of the snap.
@param[in]  direction  The orientation of the snap. Pass `NULL` to use the default orientation.
@param[in]  up         The up vector controls the rotation around the \p orientation of the snap.
                       Pass `NULL` to use the default up vector.
@related SUSnapRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_ARGUMENT if \p direction an \p up are parallel.
- \ref SU_ERROR_NULL_POINTER_OUTPUT if \p snap is `NULL`
- \ref SU_ERROR_OVERWRITE_VALID if \p snap already refers to a valid object
*/
SU_RESULT SUSnapCreate(
    SUSnapRef* snap, const struct SUPoint3D position, const struct SUVector3D* direction,
    const struct SUVector3D* up);

/**
@brief Releases a snap object and its associated resources.
@since SketchUp 2025.0, API 13.0
@param[in] snap The snap object.
@related SUSnapRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_NULL_POINTER_INPUT if \p snap points to an `NULL`
- \ref SU_ERROR_INVALID_INPUT if the \p snap object is not a valid object.
*/
SU_RESULT SUSnapRelease(SUSnapRef* snap);

/**
@brief Retrieves the position of a snap.
@since SketchUp 2025.0, API 13.0
@param[in]  snap     The snap object.
@param[out] position The position retrieved.
@related SUSnapRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p snap point is an invalid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if position is `NULL`
*/
SU_RESULT SUSnapGetPosition(SUSnapRef snap, struct SUPoint3D* position);

/**
@brief Retrieves the orientation of a snap.
@since SketchUp 2025.0, API 13.0
@param[in]  snap      The snap object.
@param[out] direction The direction of the snap.
@related SUSnapRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p snap point is an invalid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if direction is `NULL`
*/
SU_RESULT SUSnapGetDirection(SUSnapRef snap, struct SUVector3D* direction);

/**
@brief Retrieves the up vector of a snap.
@since SketchUp 2025.0, API 13.0
@param[in]  snap The snap object.
@param[out] up   The up vector of the snap.
@related SUSnapRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p snap point is an invalid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if up is `NULL`
*/

SU_RESULT SUSnapGetUp(SUSnapRef snap, struct SUVector3D* up);
/**
@brief Sets the position, direction and up vector of the snap.

If only \p position is provided then \p direction and \p up remains unchanged.

@since SketchUp 2025.0, API 13.0
@param[in] snap      The snap object.
@param[in] position  The position of the snap.
@param[in] direction The orientation of the snap. Pass `NULL` to use the default orientation.
@param[in] up        The up vector of the snap. Pass `NULL` to use the default up vector.
@related SUSnapRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_ARGUMENT if \p direction an \p up are parallel.
- \ref SU_ERROR_NULL_POINTER_INPUT if \p snap is `NULL`
*/
SU_RESULT SUSnapSet(
    SUSnapRef snap, const struct SUPoint3D position, const struct SUVector3D* direction,
    const struct SUVector3D* up);

#ifdef __cplusplus
}
#endif

#endif  // SKETCHUP_MODEL_SNAP_H_

// Copyright 2024-2025 Trimble Inc. All Rights Reserved.

/**
 * @file
 * @brief Interfaces for SUEnvironmentRef.
 */
#ifndef SKETCHUP_MODEL_ENVIRONMENT_H_
#define SKETCHUP_MODEL_ENVIRONMENT_H_

#include <SketchUpAPI/common.h>
#include <SketchUpAPI/model/defs.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
@struct SUEnvironmentRef
@brief References an environment, which enables sky boxes and image-based lighting.
@since SketchUp 2025.0, API 13.0
*/

/**
@brief Converts from an \ref SUEnvironmentRef to an \ref SUEntityRef.
       This is essentially an upcast operation.
@since SketchUp 2025.0, API 13.0
@param[in] environment The given environment reference.
@related SUEnvironmentRef
@return
- The converted \ref SUEntityRef if \p environment is a valid object
- If not, the returned reference will be invalid
*/
SU_EXPORT SUEntityRef SUEnvironmentToEntity(SUEnvironmentRef environment);

/**
@brief Converts from an \ref SUEntityRef to an SUEnvironmentRef.
       This is essentially a downcast operation so the given \ref SUEntityRef
       must be convertible to an \ref SUEnvironmentRef.
@since SketchUp 2025.0, API 13.0
@param[in] entity The given entity reference.
@related SUEnvironmentRef
@return
- The converted \ref SUEnvironmentRef if the downcast operation succeeds
- If not, the returned reference will be invalid
*/
SU_EXPORT SUEnvironmentRef SUEnvironmentFromEntity(SUEntityRef entity);

/**
 * @brief Creates an environment object from an SKE, HDR, or EXR file.
 *   The image or SKE file will be loaded into the environment's skydome as a cubemap.
 * @since SketchUp 2025.0, API 13.0
 * @param[out] environment The created environment object.
 * @param[in] file_path    The path to the SKE, HDR, or EXR file.
 * @param[in] name         The name of the environment. If empty, the name will default to the name
 * stored in the SKE file (if available), or to the file name.
 * @related SUEnvironmentRef
 * @return
 * - \ref SU_ERROR_NONE on success
 * - \ref SU_ERROR_OVERWRITE_VALID if \p environment already references a valid object
 * - \ref SU_ERROR_NULL_POINTER_INPUT if \p file_path , \p name , or \p environment is `NULL`
 * - \ref SU_ERROR_INVALID_ARGUMENT if \p file_path is an empty string
 * - \ref SU_ERROR_SERIALIZATION if the \p environment could not be created from the file at \p
 * file_path
 *
 */
SU_RESULT SUEnvironmentCreateFromFile(
    SUEnvironmentRef* environment, const char* file_path, const char* name);

/**
 * @brief Writes an environment to an SKE file.
 * @since SketchUp 2025.0, API 13.0
 * @param[in] environment The environment object to write to file.
 * @param[in] file_path   The location to save the environment to. Assumed to be UTF-8 encoded.
 * @related SUEnvironmentRef
 * @return
 * - \ref SU_ERROR_NONE on success
 * - \ref SU_ERROR_INVALID_INPUT if \p environment is not a valid object
 * - \ref SU_ERROR_NULL_POINTER_INPUT if \p file_path , \p name , or \p environment is `NULL`
 * - \ref SU_ERROR_INVALID_ARGUMENT if \p file_path or \p name is an empty string
 * - \ref SU_ERROR_SERIALIZATION if the \p environment could not be written to \p file_path
 *
 */
SU_RESULT SUEnvironmentWriteToFile(SUEnvironmentRef environment, const char* file_path);

/**
@brief Releases an environment object and its associated objects.
@note An environment object retrieved through \p SUEnvironmentsRef methods should not be released as
  it is owned by the model.
@since SketchUp 2025.0, API 13.0
@param[in,out] environment The environment object.
@related SUEnvironmentRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_NULL_POINTER_INPUT if \p environment is `NULL`
- \ref SU_ERROR_INVALID_INPUT if \p environment does not reference a valid object
*/
SU_RESULT SUEnvironmentRelease(SUEnvironmentRef* environment);

/**
@brief Sets the name of a environment object.
@since SketchUp 2025.0, API 13.0
@param[in] environment The environment object.
@param[in] name  The name string to set the environment object.
                 Assumed to be UTF-8 encoded.
@related SUEnvironmentRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p environment is not a valid object
- \ref SU_ERROR_NULL_POINTER_INPUT if \p name is `NULL`
- \ref SU_ERROR_INVALID_ARGUMENT if \p name is an empty string or if no manager is associated with
the environment
- \ref SU_ERROR_DUPLICATE if \p name is a duplicate of another environment
*/
SU_RESULT SUEnvironmentSetName(SUEnvironmentRef environment, const char* name);

/**
@brief Retrieves the name of a environment object.
@since SketchUp 2025.0, API 13.0
@param[in]  environment The environment object.
@param[out] name The name retrieved.
@related SUEnvironmentRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p environment is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if \p name is `NULL`
- \ref SU_ERROR_INVALID_OUTPUT if \p name does not point to a valid \ref
  SUStringRef object
*/
SU_RESULT SUEnvironmentGetName(SUEnvironmentRef environment, SUStringRef* name);

/**
@brief Sets the description of a environment object.
@since SketchUp 2025, API 13.0
@param[in] environment The environment object.
@param[in] desc The description to be set.
Assumed to be UTF-8 encoded.
@related SUEnvironmentRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p environment is not a valid object
- \ref SU_ERROR_NULL_POINTER_INPUT if \p desc is `NULL`
*/
SU_RESULT SUEnvironmentSetDescription(SUEnvironmentRef environment, const char* desc);

/**
@brief Retrieves the description of a environment object.
@since SketchUp 2025.0, API 13.0
@param[in]  environment The environment object.
@param[out] desc  The description retrieved.
@related SUEnvironmentRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p environment is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if \p desc is `NULL`
- \ref SU_ERROR_INVALID_OUTPUT if \p desc does not point to a valid \ref SUStringRef object
*/
SU_RESULT SUEnvironmentGetDescription(SUEnvironmentRef environment, SUStringRef* desc);

/**
 * @brief Sets the the environment to be used as a skydome.
 * @since SketchUp 2025.0, API 13.0
 * @param[in] environment The environment object.
 * @param[in] skydome The flag to set on the environment object.
 * @related SUEnvironmentRef
 * @return
 * - \ref SU_ERROR_NONE on success
 * - \ref SU_ERROR_INVALID_INPUT if \p environment is not a valid object
 */
SU_RESULT SUEnvironmentSetUseAsSkydome(SUEnvironmentRef environment, bool skydome);

/**
 * @brief Retrieves whether the environment is used as a skydome.
 * @since SketchUp 2025.0, API 13.0
 * @param[in]  environment The environment object.
 * @param[out] skydome The flag retrieved.
 * @related SUEnvironmentRef
 * @return
 * - \ref SU_ERROR_NONE on success
 * - \ref SU_ERROR_INVALID_INPUT if \p environment is not a valid object
 * - \ref SU_ERROR_NULL_POINTER_OUTPUT if skydome is `NULL`
 */
SU_RESULT SUEnvironmentGetUseAsSkydome(SUEnvironmentRef environment, bool* skydome);

/**
 * @brief Sets the the environment to be used for reflections.
 * @since SketchUp 2025.0, API 13.0
 * @param[in] environment The environment object.
 * @param[in] reflections The flag to set the environment object.
 * @related SUEnvironmentRef
 * @return
 * - \ref SU_ERROR_NONE on success
 * - \ref SU_ERROR_INVALID_INPUT if \p environment is not a valid object
 */
SU_RESULT SUEnvironmentSetUseForReflections(SUEnvironmentRef environment, bool reflections);

/**
 * @brief Retrieves whether the environment is used for reflections.
 * @since SketchUp 2025.0, API 13.0
 * @param[in]  environment The environment object.
 * @param[out] reflections The flag retrieved.
 * @related SUEnvironmentRef
 * @return
 * - \ref SU_ERROR_NONE on success
 * - \ref SU_ERROR_INVALID_INPUT if \p environment is not a valid object
 * - \ref SU_ERROR_NULL_POINTER_OUTPUT if \p reflections is `NULL`
 */
SU_RESULT SUEnvironmentGetUseForReflections(SUEnvironmentRef environment, bool* reflections);

/**
 * @brief Sets the the environment image vertical rotation angle in degrees.
 * @since SketchUp 2025.0, API 13.0
 * @param[in] environment The environment object.
 * @param[in] angle The angle to set the environment object, within the range `[0.0, 360.0)`
 * @related SUEnvironmentRef
 * @return
 * - \ref SU_ERROR_NONE on success
 * - \ref SU_ERROR_INVALID_INPUT if \p environment is not a valid object
 * - \ref SU_ERROR_OUT_OF_RANGE if \p angle is not within the range `[0.0, 360.0)`
 */
SU_RESULT SUEnvironmentSetRotation(SUEnvironmentRef environment, double angle);

/**
 * @brief Retrieves the environment image rotation in degrees.
 * @since SketchUp 2025.0, API 13.0
 * @param[in]  environment The environment object.
 * @param[out] angle The angle retrieved.
 * @related SUEnvironmentRef
 * @return
 * - \ref SU_ERROR_NONE on success
 * - \ref SU_ERROR_INVALID_INPUT if \p environment is not a valid object
 * - \ref SU_ERROR_NULL_POINTER_OUTPUT if \p angle is `NULL`
 */
SU_RESULT SUEnvironmentGetRotation(SUEnvironmentRef environment, double* angle);

/**
 * @brief Sets the skydome exposure to compensate for variations in HDR image exposure.
 *   The unaltered exposure level is `1.0`.
 * @since SketchUp 2025.0, API 13.0
 * @param[in] environment The environment object.
 * @param[in] exposure The exposure to set the environment object, within the range [0.0, 20.0].
 * @related SUEnvironmentRef
 * @return
 * - \ref SU_ERROR_NONE on success
 * - \ref SU_ERROR_INVALID_INPUT if \p environment is not a valid object
 * - \ref SU_ERROR_OUT_OF_RANGE if \p exposure is not within the range [0.0, 20.0]
 */
SU_RESULT SUEnvironmentSetSkydomeExposure(SUEnvironmentRef environment, double exposure);

/**
 * @brief Retrieves the skydome exposure of the environment.
 * @since SketchUp 2025.0, API 13.0
 * @param[in]  environment The environment object.
 * @param[out] exposure The exposure retrieved.
 * @related SUEnvironmentRef
 * @return
 * - \ref SU_ERROR_NONE on success
 * - \ref SU_ERROR_INVALID_INPUT if \p environment is not a valid object
 * - \ref SU_ERROR_NULL_POINTER_OUTPUT if \p exposure is `NULL`
 */
SU_RESULT SUEnvironmentGetSkydomeExposure(SUEnvironmentRef environment, double* exposure);

/**
 * @brief Sets the reflection exposure of the environment.
 * @since SketchUp 2025.0, API 13.0
 * @param[in] environment The environment object.
 * @param[in] exposure The exposure to set the environment object, within the range [0.0, 10.0].
 * @related SUEnvironmentRef
 * @return
 * - \ref SU_ERROR_NONE on success
 * - \ref SU_ERROR_INVALID_INPUT if \p environment is not a valid object
 * - \ref SU_ERROR_OUT_OF_RANGE if \p exposure is not within the range [0.0, 10.0]
 */
SU_RESULT SUEnvironmentSetReflectionExposure(SUEnvironmentRef environment, double exposure);

/**
 * @brief Retrieves the reflection exposure of the environment.
 * @since SketchUp 2025.0, API 13.0
 * @param[in]  environment The environment object.
 * @param[out] exposure The exposure retrieved.
 * @related SUEnvironmentRef
 * @return
 * - \ref SU_ERROR_NONE on success
 * - \ref SU_ERROR_INVALID_INPUT if \p environment is not a valid object
 * - \ref SU_ERROR_NULL_POINTER_OUTPUT if \p exposure is `NULL`
 */
SU_RESULT SUEnvironmentGetReflectionExposure(SUEnvironmentRef environment, double* exposure);

/**
 * @brief Sets the linked sun flag of the environment, enabling the shadow-casting light.
 *   Corresponding to "Set Sun Location" in the SketchUp UI.
 * @since SketchUp 2025.0, API 13.0
 * @param[in] environment The environment object.
 * @param[in] linked_sun The flag to set the environment object.
 * @related SUEnvironmentRef
 * @return
 * - \ref SU_ERROR_NONE on success
 * - \ref SU_ERROR_INVALID_INPUT if \p environment is not a valid object
 */
SU_RESULT SUEnvironmentSetLinkedSun(SUEnvironmentRef environment, bool linked_sun);

/**
 * @brief Retrieves whether the environment is linked sun is enabled.
 * @since SketchUp 2025.0, API 13.0
 * @param[in]  environment The environment object.
 * @param[out] linked_sun The flag retrieved.
 * @related SUEnvironmentRef
 * @return
 * - \ref SU_ERROR_NONE on success
 * - \ref SU_ERROR_INVALID_INPUT if \p environment is not a valid object
 * - \ref SU_ERROR_NULL_POINTER_OUTPUT if \p linked_sun is `NULL`
 */
SU_RESULT SUEnvironmentGetLinkedSun(SUEnvironmentRef environment, bool* linked_sun);

/**
 * @brief Sets the linked sun position in the environment.
 * @since SketchUp 2025.0, API 13.0
 * @param[in] environment The environment object.
 * @param[in] position The position to set the environment object.
 *   `x` corresponds to longitude with the range `[0.0, 1.0]`,
 *   `y` corresponds to latitude with the range `[-1.0, 1.0]`.
 * @related SUEnvironmentRef
 * @return
 * - \ref SU_ERROR_NONE on success
 * - \ref SU_ERROR_INVALID_INPUT if \p environment is not a valid object
 * - \ref SU_ERROR_NULL_POINTER_INPUT if \p position is `NULL`
 * - \ref SU_ERROR_OUT_OF_RANGE if \p position has invalid x or y values
 */
SU_RESULT SUEnvironmentSetLinkedSunPosition(
    SUEnvironmentRef environment, const struct SUPoint2D* position);

/**
 * @brief Retrieves the linked sun position in the environment.
 * @since SketchUp 2025.0, API 13.0
 * @param[in]  environment The environment object.
 * @param[out] position The position retrieved.
 * @related SUEnvironmentRef
 * @return
 * - \ref SU_ERROR_NONE on success
 * - \ref SU_ERROR_INVALID_INPUT if \p environment is not a valid object
 * - \ref SU_ERROR_NULL_POINTER_OUTPUT if \p position is `NULL`
 */
SU_RESULT SUEnvironmentGetLinkedSunPosition(
    SUEnvironmentRef environment, struct SUPoint2D* position);

/**
 * @brief Retrieves the thumbnail preview image for the given environment.
 * @since SketchUp 2025.0, API 13.0
 * @param[in]  environment The environment object.
 * @param[out] image The thumbnail to be retrieved.
 * @related SUEnvironmentRef
 * @return
 * - \ref SU_ERROR_NONE on success
 * - \ref SU_ERROR_INVALID_INPUT if \p environment is not a valid object
 * - \ref SU_ERROR_NULL_POINTER_OUTPUT if \p image is NULL
 * - \ref SU_ERROR_INVALID_OUTPUT if \p image does not point to a valid \ref
       SUImageRepRef object
 * - \ref SU_ERROR_NO_DATA if the thumbnail can not be retrieved
 */
SU_RESULT SUEnvironmentGetThumbnail(SUEnvironmentRef environment, SUImageRepRef* image);

/**
 * @brief Writes the HDR image of the environment to a file in its original file type.
 * @since SketchUp 2025.0, API 13.0
 * @param[in] environment The environment object.
 * @param[in] dir_path The directory path to save the HDR image to.
 * @param[out] full_path_written The full path of the written file.
 * @related SUEnvironmentRef
 * @return
 * - \ref SU_ERROR_NONE on success
 * - \ref SU_ERROR_INVALID_INPUT if \p environment is not a valid object
 * - \ref SU_ERROR_NULL_POINTER_INPUT if \p dir_path or \p full_path_written is `NULL`
 * - \ref SU_ERROR_INVALID_ARGUMENT if \p dir_path is an empty string
 * - \ref SU_ERROR_SERIALIZATION if the HDR image could not be written to \p dir_path
 */
SU_RESULT SUEnvironmentWriteHDRImageToFile(
    SUEnvironmentRef environment, const char* dir_path, SUStringRef* full_path_written);

#ifdef __cplusplus
}  // extern "C"
#endif

#endif  // SKETCHUP_MODEL_ENVIRONMENT_H_

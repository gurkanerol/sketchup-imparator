// Copyright 2024-2025 Trimble Inc. All Rights Reserved.

/**
 * @file
 * @brief Interfaces for SUEnvironmentsRef.
 */
#ifndef SKETCHUP_MODEL_ENVIRONMENTS_H_
#define SKETCHUP_MODEL_ENVIRONMENTS_H_

#include <SketchUpAPI/common.h>
#include <SketchUpAPI/model/defs.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
@struct SUEnvironmentsRef
@brief References a container object for all environments in a model.
@since SketchUp 2025.0, API 13.0
*/

/**
 * @brief Retrieves the number of environment objects in an environments object.
 * @since SketchUp 2025.0, API 13.0
 * @param[in]  environments The environments object.
 * @param[out] count        The number of environments.
 * @related SUEnvironmentsRef
 * @return
 * - \ref SU_ERROR_NONE on success
 * - \ref SU_ERROR_INVALID_INPUT if \p environments is not a valid object
 * - \ref SU_ERROR_NULL_POINTER_OUTPUT if \p count is `NULL`
 */
SU_RESULT SUEnvironmentsGetCount(SUEnvironmentsRef environments, size_t* count);

/**
 * @brief Retrieves every environment associated with an environments object.
 * @since SketchUp 2025.0, API 13.0
 * @param[in]  environments The environments object.
 * @param[in]  len          The number of environments to retrieve.
 * @param[out] items        The environments retrieved.
 * @param[out] count        The number of environments retrieved.
 * @related SUEnvironmentsRef
 * @return
 * - \ref SU_ERROR_NONE on success
 * - \ref SU_ERROR_INVALID_INPUT if \p environments is not a valid object
 * - \ref SU_ERROR_NULL_POINTER_OUTPUT if \p items or \p count is `NULL`
 */
SU_RESULT SUEnvironmentsGetAll(
    SUEnvironmentsRef environments, size_t len, SUEnvironmentRef items[], size_t* count);

/**
 * @brief Retrieves the currently selected environment.
 * @since SketchUp 2025.0, API 13.0
 * @param[in]  environments The environments object.
 * @param[out] environment  The selected environment object.
 * @related SUEnvironmentsRef
 * @return
 * - \ref SU_ERROR_NONE on success
 * - \ref SU_ERROR_INVALID_INPUT if \p environments is not a valid object
 * - \ref SU_ERROR_NULL_POINTER_OUTPUT if \p environment is `NULL`
 * - \ref SU_ERROR_NO_DATA if no environment is currently selected
 */
SU_RESULT SUEnvironmentsGetSelectedEnvironment(
    SUEnvironmentsRef environments, SUEnvironmentRef* environment);

/**
 * @brief Retrieves an environment by persistent ID.
 * @since SketchUp 2025.0, API 13.0
 * @param[in]  environments The environments object.
 * @param[in]  pid          The PID of the environment object to retrieve.
 * @param[out] environment  The environment object with the given PID.
 * @related SUEnvironmentsRef
 * @return
 * - \ref SU_ERROR_NONE on success
 * - \ref SU_ERROR_INVALID_INPUT if \p environments is not a valid object
 * - \ref SU_ERROR_NULL_POINTER_OUTPUT if \p environment is `NULL`
 * - \ref SU_ERROR_NO_DATA if no environment can be found with the given PID
 */
SU_RESULT SUEnvironmentsGetEnvironmentByPersistentID(
    SUEnvironmentsRef environments, uint64_t pid, SUEnvironmentRef* environment);

/**
 * @brief Retrieves an environment by name.
 * @since SketchUp 2025.0, API 13.0
 * @param[in]  environments The environments object.
 * @param[in]  name         The name of the environment object to retrieve.
 * @param[out] environment  The environment object with the given name.
 * @related SUEnvironmentsRef
 * @return
 * - \ref SU_ERROR_NONE on success
 * - \ref SU_ERROR_INVALID_INPUT if \p environments is not a valid object
 * - \ref SU_ERROR_NULL_POINTER_OUTPUT if \p environment is `NULL`
 * - \ref SU_ERROR_NO_DATA if no environment can be found with the given name
 */
SU_RESULT SUEnvironmentsGetEnvironmentByName(
    SUEnvironmentsRef environments, const char* name, SUEnvironmentRef* environment);

/**
 * @brief Adds an environment to an environments object.
 * @note This method transfers ownership of the \p environment to the model. Do not call
 *   \p SUEnvironmentRelease on \p environment after calling this method.
 * @since SketchUp 2025.0, API 13.0
 * @param[in] environments The environments object.
 * @param[in] environment  The environment object to add.
 * @related SUEnvironmentsRef
 * @return
 * - \ref SU_ERROR_NONE on success
 * - \ref SU_ERROR_INVALID_INPUT if \p environment or \p environments is not a valid object
 * - \ref SU_ERROR_DUPLICATE if the \p environment is already part of the environments
 *        object
 * - \ref SU_ERROR_INVALID_ARGUMENT if the environment name is already in use
 */
SU_RESULT SUEnvironmentsAdd(SUEnvironmentsRef environments, SUEnvironmentRef environment);

/**
 * @brief Removes an environment from an environments object.
 * @since SketchUp 2025.0, API 13.0
 * @param[in] environments The environments object.
 * @param[in] environment  The environment object to remove.
 * @related SUEnvironmentsRef
 * @return
 * - \ref SU_ERROR_NONE on success
 * - \ref SU_ERROR_INVALID_INPUT if \p environment or \p environments is not a valid object
 * - \ref SU_ERROR_INVALID_OPERATION if \p environment is not part of the \p environments object
 */
SU_RESULT SUEnvironmentsRemove(SUEnvironmentsRef environments, SUEnvironmentRef environment);

#ifdef __cplusplus
}  // extern "C"
#endif

#endif  // SKETCHUP_SLAPI_PUBLIC_MODEL_ENVIRONMENTS_H_
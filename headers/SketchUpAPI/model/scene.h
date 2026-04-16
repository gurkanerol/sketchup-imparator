// Copyright 2013-2025 Trimble Inc. All Rights Reserved.

/**
 * @file
 * @brief Interfaces for SUSceneRef.
 */
#ifndef SKETCHUP_MODEL_SCENE_H_
#define SKETCHUP_MODEL_SCENE_H_

#include <SketchUpAPI/common.h>
#include <SketchUpAPI/unicodestring.h>
#include <SketchUpAPI/model/defs.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
@struct SUSceneRef
@extends SUEntityRef
@brief Used to get and set a scene's camera views, using the \ref SUCameraRef
       object.

@note Add the scene to the model before setting its properties, except for the name which should
  be set before adding it.
*/

/**
 * @anchor SUSceneFlags
 * @name Scene Flags
 * @brief Flags for SUSceneGetFlags() and SUSceneSetFlags(). These are combined
 *   bitwise.
 * @see SUSceneRef
 * @{
 */
#define FLAG_USE_CAMERA 0x0001             ///< @since SketchUp 2017, API 5.0
#define FLAG_USE_RENDERING_OPTIONS 0x0002  ///< @since SketchUp 2017, API 5.0
#define FLAG_USE_SHADOWINFO 0x0004         ///< @since SketchUp 2017, API 5.0
#define FLAG_USE_AXES 0x0008               ///< @since SketchUp 2017, API 5.0
/// @deprecated Obsolete since SketchUp 2020.1, API 8.1. Instead, use
///   \ref FLAG_USE_HIDDEN_GEOMETRY and \ref FLAG_USE_HIDDEN_OBJECTS.
///
/// @since SketchUp 2017, API 5.0
#define FLAG_USE_HIDDEN 0x0010
#define FLAG_USE_LAYER_VISIBILITY 0x0020  ///< @since SketchUp 2017, API 5.0
#define FLAG_USE_SECTION_PLANES 0x0040    ///< @since SketchUp 2017, API 5.0
#define FLAG_USE_HIDDEN_GEOMETRY 0x0080   ///< @since SketchUp 2020.1, API 8.1
#define FLAG_USE_HIDDEN_OBJECTS 0x0100    ///< @since SketchUp 2020.1, API 8.1
#define FLAG_USE_ENVIRONMENT 0x0200       ///< @since SketchUp 2025.0, API 13.0

#define FLAG_USE_ALL 0x0fff    ///< @since SketchUp 2017, API 5.0
#define FLAG_NO_CAMERA 0x0ffe  ///< @since SketchUp 2017, API 5.0
/**@}*/

/**
@brief Converts from an \ref SUSceneRef to an \ref SUEntityRef.  This is
       essentially an upcast operation.
@param[in] scene The given scene reference.
@related SUSceneRef
@return
- The converted \ref SUEntityRef if scene is a valid object. If not, the
  returned reference will be invalid.
*/
SU_EXPORT SUEntityRef SUSceneToEntity(SUSceneRef scene);

/**
@brief Converts from an \ref SUEntityRef to an \ref SUSceneRef. This is
       essentially a downcast operation so the given \ref SUEntityRef must be
       convertible to an \ref SUSceneRef.
@param[in] entity The entity reference.
@related SUSceneRef
@return
- The converted \ref SUSceneRef if the downcast operation succeeds. If not, the
  returned reference will be invalid.
*/
SU_EXPORT SUSceneRef SUSceneFromEntity(SUEntityRef entity);

/**
@brief Creates an empty scene object.

@note The created scene will not save any scene properties until
  the \ref SUSceneFlags bits are set.

@param[out] scene The scene object created.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_NULL_POINTER_INPUT if scene is NULL
- \ref SU_ERROR_OVERWRITE_VALID if face already refers to a valid object

@see SUSceneSetFlags
@see SUModelAddScenes

@code
SUScene scene = SU_INVALID;
SUSceneCreate(&scene);
SUSceneSetName(scene, "Example"); // Must be unique.
SUSceneSetFlags(scene, FLAG_USE_ALL); // Set the properties to remember.
SUModelAddScenes(model, 1, &scene); // This will also update the scene based on the flags set.

// Set scene properties after adding it to the model.
// ...
SUSceneSetCamera(scene, eye, target, up);
@endcode
*/
SU_RESULT SUSceneCreate(SUSceneRef* scene);

/**
@brief Releases a scene object.
@param[in] scene The scene object.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is an invalid object
- \ref SU_ERROR_NULL_POINTER_INPUT if scene is NULL
*/
SU_RESULT SUSceneRelease(SUSceneRef* scene);

/**
@brief Retrieves the "use camera" setting of a scene object.
@since SketchUp 2016, API 4.0
@param[in]  scene      The scene object.
@param[out] use_camera The setting retrieved.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if use_camera is NULL
*/
SU_RESULT SUSceneGetUseCamera(SUSceneRef scene, bool* use_camera);

/**
@brief Sets the "use camera" setting of a scene object.
@since SketchUp 2016, API 4.0
@param[in] scene      The scene object.
@param[in] use_camera The current setting for whether or not the camera is used.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is not a valid object
*/
SU_RESULT SUSceneSetUseCamera(SUSceneRef scene, bool use_camera);

/**
@brief Retrieves the camera of a scene object.

@note The returned camera object points to scene's internal camera. So the
  camera must not be released via SUCameraRelease().

@param[in]  scene  The scene object.
@param[out] camera The camera object retrieved.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is not a valid object
- \ref SU_ERROR_NULL_POINTER_INPUT if camera is NULL
*/
SU_RESULT SUSceneGetCamera(SUSceneRef scene, SUCameraRef* camera);

/**
@brief Sets a given scene's camera object.

@note The scene does not take ownership of the provided camera, it just copies
  the properties to the scene's owned camera. If the input camera was created
  using SUCameraCreate() it must be released using SUCameraRelease().

@since SketchUp 2016, API 4.0
@param[in] scene  The scene object.
@param[in] camera The camera object to be set.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene or camera are not a valid objects
*/
SU_RESULT SUSceneSetCamera(SUSceneRef scene, SUCameraRef camera);

/**
 @brief Retrieves the "include in animation" setting of a scene object.
 @since SketchUp 2018, API 6.0
 @param[in]  scene                The scene object.
 @param[out] include_in_animation The current setting for whether or not to
                                  include in animation.
 @related SUSceneRef
 @return
 - \ref SU_ERROR_NONE on success
 - \ref SU_ERROR_INVALID_INPUT if scene is not a valid object
 - \ref SU_ERROR_NULL_POINTER_OUTPUT if include_in_animation is NULL
 */
SU_RESULT SUSceneGetIncludeInAnimation(SUSceneRef scene, bool* include_in_animation);

/**
@brief Sets the "include in animation" setting of a scene object.
@since SketchUp 2018, API 6.0
@param[in] scene                The scene object.
@param[in] include_in_animation The new setting for whether or not to include
                               in animation.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is not a valid object
*/
SU_RESULT SUSceneSetIncludeInAnimation(SUSceneRef scene, bool include_in_animation);

/**
@brief Retrieves the name of a scene object.
@param[in]  scene The scene object.
@param[out] name  The name retrieved.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is an invalid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if name is NULL
- \ref SU_ERROR_INVALID_OUTPUT if name does not point to a valid \ref
  SUStringRef object
*/
SU_RESULT SUSceneGetName(SUSceneRef scene, SUStringRef* name);

/**
@brief Sets the name of a scene object.

@warning Breaking Change: The behavior of SUSceneSetName changed in
         SketchUp 2018, API 6.0 to return \ref SU_ERROR_INVALID_ARGUMENT if the
         given name already exists in the scene's model.

@param[in] scene      The scene object.
@param[in] scene_name The name of the scene object. Assumed to be UTF-8 encoded.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is an invalid object
- \ref SU_ERROR_NULL_POINTER_INPUT if scene_name is NULL
- \ref SU_ERROR_INVALID_ARGUMENT if the name already exists in the scene's model
*/
SU_RESULT SUSceneSetName(SUSceneRef scene, const char* scene_name);

/**
@brief Retrieves the rendering options for the scene object.
@param[in]  scene   The scene object.
@param[out] options The options retrieved.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is an invalid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if options is NULL
- \ref SU_ERROR_NO_DATA if the scene does not use rendering options
*/
SU_RESULT SUSceneGetRenderingOptions(SUSceneRef scene, SURenderingOptionsRef* options);

/**
@brief Retrieves the shadow info of a scene.
@since SketchUp 2015, API 3.0
@param[in]  scene       The scene object.
@param[out] shadow_info The shadow info object retrieved. This object is owned
                        by the scene and must not be explicitly released.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if shadow_info is NULL
- \ref SU_ERROR_NO_DATA if the scene does not use shadow info
*/
SU_RESULT SUSceneGetShadowInfo(SUSceneRef scene, SUShadowInfoRef* shadow_info);

/**
@brief Retrieves the "use shadow info" setting of a scene object.
@since SketchUp 2015, API 3.0
@param[in]  scene           The scene object.
@param[out] use_shadow_info The current setting for whether or not shadow info
                            is used.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if use_shadow_info is NULL
*/
SU_RESULT SUSceneGetUseShadowInfo(SUSceneRef scene, bool* use_shadow_info);

/**
@brief Sets the "use shadow info" setting of a scene object.
@since SketchUp 2015, API 3.0
@param[in] scene           The scene object.
@param[in] use_shadow_info The new setting for whether or not shadow info
                            is used.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is not a valid object
*/
SU_RESULT SUSceneSetUseShadowInfo(SUSceneRef scene, bool use_shadow_info);

/**
@brief Retrieves the "use rendering options" setting of a scene object.
@since SketchUp 2016, API 4.0
@param[in]  scene                 The scene object.
@param[out] use_rendering_options The current setting for whether or not
                                  rendering options are used.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if use_shadow_info is NULL
*/
SU_RESULT SUSceneGetUseRenderingOptions(SUSceneRef scene, bool* use_rendering_options);

/**
@brief Sets the "use rendering options" setting of a scene object.
@since SketchUp 2016, API 4.0
@param[in] scene                 The scene object.
@param[in] use_rendering_options The new setting for whether or not rendering
                                  options are used.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is not a valid object
*/
SU_RESULT SUSceneSetUseRenderingOptions(SUSceneRef scene, bool use_rendering_options);

/**
@brief Gets whether the scene uses the hidden properties of entities.
@since SketchUp 2018 M0, API 6.0
@deprecated The functionality is replaced by SUSceneGetUseHiddenGeometry()
  and SUSceneGetUseHiddenObjects().
@param[in]  scene      The scene object.
@param[out] use_hidden The current setting for whether or not the hidden
                       property of entities is used.
@related SUSceneRef
@see SUSceneGetUseHiddenGeometry
@see SUSceneGetUseHiddenObjects
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if use_hidden is NULL
*/
SU_RESULT SUSceneGetUseHidden(SUSceneRef scene, bool* use_hidden);

/**
@brief Sets whether the scene uses the hidden properties of entities.
@since SketchUp 2018 M0, API 6.0
@deprecated The functionality is replaced by SUSceneSetUseHiddenGeometry()
  and SUSceneSetUseHiddenObjects().
@param[in] scene      The scene object.
@param[in] use_hidden The new setting for whether or not the hidden
                     property of entities is used.
@related SUSceneRef
 @see SUSceneSetUseHiddenGeometry
 @see SUSceneSetUseHiddenObjects
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is not a valid object
*/
SU_RESULT SUSceneSetUseHidden(SUSceneRef scene, bool use_hidden);

/**
@brief Gets whether the scene uses the hidden geometry properties of root-level entities.
@since SketchUp 2020.1, API 8.1
@param[in]  scene      The scene object.
@param[out] use_hidden The current setting for whether or not the hidden
                       property of root-level entities is used.
@related SUSceneRef
@see SUSceneSetUseHiddenGeometry
@see SUSceneGetUseHiddenObjects
@see SUSceneSetUseHiddenObjects
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if use_hidden is NULL
*/
SU_RESULT SUSceneGetUseHiddenGeometry(SUSceneRef scene, bool* use_hidden);

/**
@brief Sets whether the scene uses the hidden properties of root-level entities.
@since SketchUp 2020.1, API 8.1
@param[in] scene      The scene object.
@param[in] use_hidden The new setting for whether or not the hidden
                      property of root-level entities is used.
@related SUSceneRef
@see SUSceneGetUseHiddenGeometry
@see SUSceneGetUseHiddenObjects
@see SUSceneSetUseHiddenObjects
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is not a valid object
*/
SU_RESULT SUSceneSetUseHiddenGeometry(SUSceneRef scene, bool use_hidden);

/**
@brief Gets whether the scene uses the hidden properties of objects.
@since SketchUp 2020.1, API 8.1
@param[in]  scene      The scene object.
@param[out] use_hidden The current setting for whether or not the hidden
                       property of objects is used.
@related SUSceneRef
@see SUSceneGetUseHiddenGeometry
@see SUSceneSetUseHiddenGeometry
@see SUSceneSetUseHiddenObjects
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if use_hidden is NULL
*/
SU_RESULT SUSceneGetUseHiddenObjects(SUSceneRef scene, bool* use_hidden);

/**
@brief Sets whether the scene uses the hidden properties of objects.
@since SketchUp 2020.1, API 8.1
@param[in] scene      The scene object.
@param[in] use_hidden The new setting for whether or not the hidden
                      property of objects is used.
@related SUSceneRef
@see SUSceneGetUseHiddenGeometry
@see SUSceneSetUseHiddenGeometry
@see SUSceneGetUseHiddenObjects
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is not a valid object
*/
SU_RESULT SUSceneSetUseHiddenObjects(SUSceneRef scene, bool use_hidden);

/**
@brief Retrieves the "use hidden layers" setting of a scene object.
@since SketchUp 2016, API 4.0
@param[in]  scene             The scene object.
@param[out] use_hidden_layers The current setting for whether or not hidden
                              layer are used.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if use_hidden_layers is NULL
*/
SU_RESULT SUSceneGetUseHiddenLayers(SUSceneRef scene, bool* use_hidden_layers);

/**
@brief Sets the "use hidden layers" setting of a scene object.
@since SketchUp 2016, API 4.0
@param[in] scene             The scene object.
@param[in] use_hidden_layers The new setting for whether or not hidden layers
                             are used.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is not a valid object
*/
SU_RESULT SUSceneSetUseHiddenLayers(SUSceneRef scene, bool use_hidden_layers);

/**
@brief Gets whether the scene uses section planes.
@since SketchUp 2018 M0, API 6.0
@param[in]  scene              The scene object.
@param[out] use_section_planes The current setting for whether or not section
                               planes property is used.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if use_section_planes is NULL
*/
SU_RESULT SUSceneGetUseSectionPlanes(SUSceneRef scene, bool* use_section_planes);

/**
@brief Sets whether the scene uses section planes.
@since SketchUp 2018 M0, API 6.0
@param[in] scene              The scene object.
@param[in] use_section_planes The new setting for whether or not section planes
                              property is used.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is not a valid object
*/
SU_RESULT SUSceneSetUseSectionPlanes(SUSceneRef scene, bool use_section_planes);

/**
@brief Retrieves the number of layers in the scene object.
@since SketchUp 2016, API 4.0
@param[in]  scene The scene object.
@param[out] count The number of layers.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if count is NULL
*/
SU_RESULT SUSceneGetNumLayers(SUSceneRef scene, size_t* count);

/**
@brief Retrieves the layers in the scene object.
@since SketchUp 2016, API 4.0
@param[in]  scene  The entities object.
@param[in]  len    The number of layers to retrieve.
@param[out] layers The layers retrieved.
@param[out] count  The number of layers retrieved.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if layers or count is NULL
*/
SU_RESULT SUSceneGetLayers(SUSceneRef scene, size_t len, SULayerRef layers[], size_t* count);

/**
@brief Adds the specified layer to the provided scene.

@note Adding a layer to a scene will flag the layer to be the opposite of its
      default scene visibility. See \ref SULayerVisibilityDefaultType. This
      function does not take ownership of the specified layer.

@note Prior to SketchUp 2020.0, API 8.0 this function did not return
      \ref SU_ERROR_INVALID_ARGUMENT.

@since SketchUp 2016, API 4.0
@param[in] scene The scene object.
@param[in] layer The new layer to be added to the scene.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene or layer is not a valid object
- \ref SU_ERROR_NO_DATA if the scene is not owned by a valid model
- \ref SU_ERROR_GENERIC if the scene's model does not contain the layer
- \ref SU_ERROR_INVALID_ARGUMENT if the layer already exists in the scene
*/
SU_RESULT SUSceneAddLayer(SUSceneRef scene, SULayerRef layer);

/**
@brief Removes the specified layer from the provided scene.

@note Removing a layer from a scene will flag the layer to use its default
      scene visibility. See \ref SULayerVisibilityDefaultType. Scenes do not
      own their layers so removing them doesn't release them.

@note Prior to SketchUp 2020.0, API 8.0 this function did not return
      \ref SU_ERROR_INVALID_ARGUMENT.

@since SketchUp 2016, API 4.0
@param[in] scene The scene object.
@param[in] layer The layer to be removed from the scene.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene or layer is not a valid object
- \ref SU_ERROR_INVALID_ARGUMENT if the layer doesn't exist in the scene
*/
SU_RESULT SUSceneRemoveLayer(SUSceneRef scene, SULayerRef layer);

/**
@brief Removes all of the layers from the provided scene. Scenes do not own their
       layers so removing them does not release them.
@since SketchUp 2016, API 4.0
@param[in] scene The scene object.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is not a valid object
*/
SU_RESULT SUSceneClearLayers(SUSceneRef scene);

/**
@brief Retrieves the number of layer folders in the scene object.
@since SketchUp 2021.0, API 9.0
@param[in]  scene The scene object.
@param[out] count The number of layer folders.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p scene is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if \p count is NULL
*/
SU_RESULT SUSceneGetNumLayerFolders(SUSceneRef scene, size_t* count);

/**
@brief Retrieves the layer folders in the scene object.
@since SketchUp 2021.0, API 9.0
@param[in]  scene         The entities object.
@param[in]  len           The number of layer_folders to retrieve.
@param[out] layer_folders The layer_folders retrieved.
@param[out] count         The number of layer_folders retrieved.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p scene is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if \p layer_folders or \p count is NULL
*/
SU_RESULT SUSceneGetLayerFolders(
    SUSceneRef scene, size_t len, SULayerFolderRef layer_folders[], size_t* count);

/**
@brief Adds the specified layer folder to the provided scene.

@note Adding a layer folder to a scene will cause that layer folder to be
      flagged as HIDDEN for the specified scene. Any layers or layer folders
      within that layer folder will also be hidden, and therefore don't need to
      be added to the scene. This function does not take ownership of the
      specified layer folder.

@since SketchUp 2021.0, API 9.0
@param[in] scene        The scene object.
@param[in] layer_folder The new layer folder to be added to \p scene.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p scene or \p layer_folder is not a valid object
- \ref SU_ERROR_NO_DATA if \p scene is not owned by a valid model
- \ref SU_ERROR_GENERIC if \p scene's model does not contain \p layer_folder
- \ref SU_ERROR_INVALID_ARGUMENT if \p layer_folder already exists in \p scene
*/
SU_RESULT SUSceneAddLayerFolder(SUSceneRef scene, SULayerFolderRef layer_folder);

/**
@brief Removes the specified layer folder from the provided scene.

@note Removing a layer folder from a scene will cause that layer folder to be
      flagged as VISIBLE for the specified scene. Scenes do not own their layer
      folders so removing them doesn't release them.

@since SketchUp 2021.0, API 9.0
@param[in] scene        The scene object.
@param[in] layer_folder The layer folder to be removed from \p scene.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p scene or \p layer_folder is not a valid object
- \ref SU_ERROR_INVALID_ARGUMENT if \p layer_folder doesn't exist in \p scene
*/
SU_RESULT SUSceneRemoveLayerFolder(SUSceneRef scene, SULayerFolderRef layer_folder);

/**
@brief Removes all of the layer folders from the provided scene. Scenes do not own
       their layer folders so removing them does not release them.
@since SketchUp 2021.0, API 9.0
@param[in] scene The scene object.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p scene is not a valid object
*/
SU_RESULT SUSceneClearLayerFolders(SUSceneRef scene);

/**
@brief Retrieves the axes of a scene object.
@param[in]  scene The scene object.
@param[out] axes  The axes object retrieved.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is not a valid object
- \ref SU_ERROR_NULL_POINTER_INPUT if axes is NULL
- \ref SU_ERROR_NO_DATA if the scene is not using axes
*/
SU_RESULT SUSceneGetAxes(SUSceneRef scene, SUAxesRef* axes);

/**
@brief Sets the "use axes" setting of a scene object.
@since SketchUp 2017, API 5.0
@param[in] scene    The scene object.
@param[in] use_axes The new setting for whether or not the axes is used.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is not a valid object
*/
SU_RESULT SUSceneSetUseAxes(SUSceneRef scene, bool use_axes);

/**
@brief Retrieves the "use axes" setting of a scene object.
@since SketchUp 2017, API 5.0
@param[in]  scene    The scene object.
@param[out] use_axes The setting retrieved.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if use_axes is NULL
*/
SU_RESULT SUSceneGetUseAxes(SUSceneRef scene, bool* use_axes);

/**
@brief Retrieves the number of hidden entities in the scene object.
@since SketchUp 2017, API 5.0
@param[in]  scene The scene object.
@param[out] count The number of hidden entities.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if count is NULL
*/
SU_RESULT SUSceneGetNumHiddenEntities(SUSceneRef scene, size_t* count);

/**
@brief Retrieves the hidden entities in the scene object.
@since SketchUp 2017, API 5.0
@param[in]  scene    The entities object.
@param[in]  len      The number of hidden entities to retrieve.
@param[out] entities The hidden entities retrieved.
@param[out] count    The number of hidden entities retrieved.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if entities or count is NULL
*/
SU_RESULT SUSceneGetHiddenEntities(
    SUSceneRef scene, size_t len, SUEntityRef entities[], size_t* count);

/**
@brief Sets the flags for a scene object.

@note If this function is called after the scene has been added to the model the API user *must*
  call SUSceneUpdate(). Otherwise it can lead to a crash while interacting with the model.
  In general it is recommended to use the separate `SUSceneSetUse*` setters after the scene has
  been added to the model.

@note \ref FLAG_USE_HIDDEN is deprecated and the bits for \ref FLAG_USE_HIDDEN_GEOMETRY and
  \ref FLAG_USE_HIDDEN_OBJECTS will take precedence.

@since SketchUp 2017, API 5.0
@param[in] scene The scene object.
@param[in] flags A bitwise combination of \ref SUSceneFlags.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is not a valid object

@see SUSceneFlags
@see SUSceneGetFlags
@see SUSceneUpdate
*/
SU_RESULT SUSceneSetFlags(SUSceneRef scene, uint32_t flags);

/**
@brief Retrieves the flags in the scene object.

@since SketchUp 2017, API 5.0
@param[in]  scene The scene object.
@param[out] flags A bitwise combination of \ref SUSceneFlags.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if flags is NULL

@see SUSceneFlags
@see SUSceneSetFlags

*/
SU_RESULT SUSceneGetFlags(SUSceneRef scene, uint32_t* flags);

/**
@brief Sets the "sketch axes displayed" setting of a scene object.
@since SketchUp 2017, API 5.0
@param[in] scene     The scene object.
@param[in] displayed The new setting for whether or not sketch axes should be
                     displayed.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is not a valid object
*/
SU_RESULT SUSceneSetSketchAxesDisplayed(SUSceneRef scene, bool displayed);

/**
@brief Retrieves the "sketch axes displayed" setting of a scene object.
@since SketchUp 2017, API 5.0
@param[in]  scene     The scene object.
@param[out] displayed The setting retrieved.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if displayed is NULL
*/
SU_RESULT SUSceneGetSketchAxesDisplayed(SUSceneRef scene, bool* displayed);

/**
@brief Retrieves the "photo matched image displayed" setting of a scene object.
@since SketchUp 2017, API 5.0
@param[in]  scene     The scene object.
@param[out] displayed The setting retrieved.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if displayed is NULL
*/
SU_RESULT SUSceneGetPhotoMatchImageDisplayed(SUSceneRef scene, bool* displayed);

/**
@brief Clears the provided scene's photo match image.
@since SketchUp 2017, API 5.0
@param[in] scene The scene object.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is not a valid object
*/
SU_RESULT SUSceneClearPhotoMatchImage(SUSceneRef scene);

/**
@brief Retrieves the scene's style.
@since SketchUp 2017, API 5.0
@param[in]  scene The scene object.
@param[out] style The style object retrieved.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is not a valid object
- \ref SU_ERROR_NULL_POINTER_INPUT if style is NULL
- \ref SU_ERROR_NO_DATA if the scene does not have a style
*/
SU_RESULT SUSceneGetStyle(SUSceneRef scene, SUStyleRef* style);

/**
@brief Copies the data from copy_scene to scene.
@since SketchUp 2017, API 5.0
@param[in] scene      The scene object to be altered.
@param[in] copy_scene The scene to be copied.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene or copy_scene are not a valid objects
*/
SU_RESULT SUSceneCopy(SUSceneRef scene, SUSceneRef copy_scene);

/**
@brief Activates the provided scene.
@since SketchUp 2017, API 5.0
@param[in] scene The scene object.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is not a valid object
*/
SU_RESULT SUSceneActivate(SUSceneRef scene);

/**
@brief Set the visibility of a drawing element in a scene.
@since SketchUp 2020, API 8.0
@note Only drawing elements at the root of the model, or nested instances of
       components, groups, and images are controlled by scene visibility.
@param[in] scene           The scene object.
@param[in] drawing_element The drawing element object.
@param[in] is_hidden       The new setting for whether or not the
                           drawing element is hidden in the scene.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene or drawing_element is not a valid object
    or if the drawing_element is geometry in a nested component.
*/
SU_RESULT SUSceneSetDrawingElementHidden(
    SUSceneRef scene, SUDrawingElementRef drawing_element, bool is_hidden);

/**
@brief Get the visibility of a drawing element in a scene.
@since SketchUp 2020, API 8.0
@param[in]  scene           The scene object.
@param[in]  drawing_element The drawing element object.
@param[out] is_hidden       The current setting for whether or not the
                            drawing element is hidden in the scene.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene or drawing_element is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if is_hidden is NULL
*/
SU_RESULT SUSceneGetDrawingElementHidden(
    SUSceneRef scene, SUDrawingElementRef drawing_element, bool* is_hidden);

/**
@brief Retrieves the description of a scene object.
@since SketchUp 2022.0, API 10.0
@param[in]  scene The scene object.
@param[out] desc  The description retrieved.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is an invalid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if desc is NULL
- \ref SU_ERROR_INVALID_OUTPUT if desc does not point to a valid \ref
SUStringRef object
*/
SU_RESULT SUSceneGetDescription(SUSceneRef scene, SUStringRef* desc);

/**
@brief Sets the description of a scene object.
@since SketchUp 2022.0, API 10.0
@param[in] scene The scene object.
@param[in] desc  The new description for the scene. Assumed to be UTF-8 encoded.
@related SUSceneRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if scene is an invalid object
- \ref SU_ERROR_NULL_POINTER_INPUT if desc is NULL
*/
SU_RESULT SUSceneSetDescription(SUSceneRef scene, const char* desc);

/**
 * @brief Enables the use of an environment for a scene.
 * @since SketchUp 2025.0, API 13.0
 * @param[in] scene The scene object.
 * @param[in] use_environment The setting whether a scene should use an environment.
 * @related SUSceneRef
 * @return
 * - \ref SU_ERROR_NONE on success
 * - \ref SU_ERROR_INVALID_INPUT if \p scene is not a valid object
 */
SU_RESULT SUSceneSetUseEnvironment(SUSceneRef scene, bool use_environment);

/**
 * @brief Retrieves the setting whether a scene uses an environment.
 * @since SketchUp 2025.0, API 13.0
 * @param[in] scene The scene object.
 * @param[out] use_environment The setting whether a scene should use an environment.
 * @related SUSceneRef
 * @return
 * - \ref SU_ERROR_NONE on success
 * - \ref SU_ERROR_INVALID_INPUT if \p scene is not a valid object
 * - \ref SU_ERROR_NULL_POINTER_OUTPUT if \p use_environment is `NULL`
 */
SU_RESULT SUSceneGetUseEnvironment(SUSceneRef scene, bool* use_environment);

/**
 * @brief Sets the environment for a scene.
 * @since SketchUp 2025.0, API 13.0
 * @param[in] scene The scene object.
 * @param[in] environment The environment object to be set.
 * @related SUSceneRef
 * @return
 * - \ref SU_ERROR_NONE on success
 * - \ref SU_ERROR_INVALID_INPUT if \p scene is not a valid object
 */
SU_RESULT SUSceneSetEnvironment(SUSceneRef scene, SUEnvironmentRef environment);

/**
 * @brief Retrieves the environment of a scene.
 * @since SketchUp 2025.0, API 13.0
 * @param[in] scene The scene object.
 * @param[out] environment The environment object to be retrieved.
 * @related SUSceneRef
 * @return
 * - \ref SU_ERROR_NONE on success
 * - \ref SU_ERROR_INVALID_INPUT if \p scene is not a valid object
 * - \ref SU_ERROR_NULL_POINTER_OUTPUT if \p environment is `NULL`
 * - \ref SU_ERROR_NO_DATA if the scene does not have an environment
 */
SU_RESULT SUSceneGetEnvironment(SUSceneRef scene, SUEnvironmentRef* environment);

/**
 * @brief Retrieves the number of section planes that will be activated when the scene is activated.
 * @since SketchUp 2025.1, API 13.1
 * @param[in]  scene The scene object.
 * @param[out] count The number of section planes.
 * @related SUSceneRef
 * @return
 * - \ref SU_ERROR_NONE on success
 * - \ref SU_ERROR_INVALID_INPUT if \p scene is not a valid object
 * - \ref SU_ERROR_NULL_POINTER_OUTPUT if \p count is `NULL`
 */
SU_RESULT SUSceneGetNumActiveSectionPlanes(SUSceneRef scene, size_t* count);

/**
 * @brief Retrieves the section planes that will be activated when the scene is activated.
 * @since SketchUp 2025.1, API 13.1
 * @param[in]  scene               The scene object.
 * @param[in]  len                 The number of section planes to retrieve.
 * @param[out] active_section_planes The section planes retrieved.
 * @param[out] count               The number of section planes retrieved.
 * @related SUSceneRef
 * @return
 * - \ref SU_ERROR_NONE on success
 * - \ref SU_ERROR_INVALID_INPUT if \p scene is not a valid object
 * - \ref SU_ERROR_NULL_POINTER_OUTPUT if \p active_section_planes or \p count is `NULL`
 */
SU_RESULT SUSceneGetActiveSectionPlanes(
    SUSceneRef scene, size_t len, SUSectionPlaneRef active_section_planes[], size_t* count);

/**
 * @brief Performs an update on the scene properties based on the current view that the use has.
 *
 * What properties of the Scene get updated are controlled via an integer whose bits corresponds to
 * different properties. These flags can be used individually or combined using bitwise OR.
 *
 * @note The properties updated is determined by the AND operation of the passed in \p flags and
 *   the flags on the scene set by SUSceneSetFlags() or the separate `SUSceneSetUse*` setters.
 *
 * @since SketchUp 2025.0, API 13.0
 *
 * @param[in] scene The \p scene object.
 * @param[in] flags The bitwise OR of \ref SUSceneFlags.
 * @return
 * - \ref SU_ERROR_NONE on success
 * - \ref SU_ERROR_INVALID_INPUT if \p scene is not a valid object
 * - \ref SU_ERROR_INVALID_ARGUMENT if \p scene is not added to a model
 *
 * @related SUSceneRef
 *
 * @see \ref SUSceneFlags
 * @see SUSceneSetFlags
 *
 * @code
 *   SUScene scene = SU_INVALID;
 *   SUSceneCreate(&scene);
 *   SUSceneSetName(scene, "Example");
 *   SUSceneSetFlags(scene, FLAG_USE_ALL); // Set the properties to remember.
 *   SUModelAddScenes(model, 1, &scene);
 *   // ...
 *   SUSceneUpdate(scene, FLAG_USE_CAMERA | FLAG_USE_SECTION_PLANES);
 * @endcode
 */
SU_RESULT SUSceneUpdate(SUSceneRef scene, unsigned int flags);

#ifdef __cplusplus
}
#endif

#endif  // SKETCHUP_MODEL_SCENE_H_

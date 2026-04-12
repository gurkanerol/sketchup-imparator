// Copyright 2012-2024 Trimble Inc. All Rights Reserved.

/**
 * @file
 * @brief Interfaces for SUMaterialRef.
 */
#ifndef SKETCHUP_MODEL_MATERIAL_H_
#define SKETCHUP_MODEL_MATERIAL_H_

#include <SketchUpAPI/color.h>
#include <SketchUpAPI/common.h>
#include <SketchUpAPI/unicodestring.h>
#include <SketchUpAPI/model/defs.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
@struct SUMaterialRef
@extends SUEntityRef
@brief  References a material object.
*/

/**
@enum SUMaterialType
@brief Indicates material type.
*/
enum SUMaterialType {
  SUMaterialType_Colored = 0,      ///< Colored material
  SUMaterialType_Textured,         ///< Textured material
  SUMaterialType_ColorizedTexture  ///< Colored and textured material
};

/**
@enum SUMaterialOwnerType
@brief Indicates material owner type.
@since SketchUp 2019.2, API 7.1
*/
enum SUMaterialOwnerType {
  SUMaterialOwnerType_None = 0,        ///< Not owned
  SUMaterialOwnerType_DrawingElement,  ///< Can be applied to SUDrawingElements
  SUMaterialOwnerType_Image,           ///< Owned exclusively by an Image
  SUMaterialOwnerType_Layer            ///< Owned exclusively by a Layer
};

/**
@enum SUMaterialColorizeType
@brief Indicates material type.
@since SketchUp 2019.2, API 7.1
*/
enum SUMaterialColorizeType {
  SUMaterialColorizeType_Shift = 0,  ///< Shifts the texture's Hue
  SUMaterialColorizeType_Tint,       ///< Colorize the texture
};

/**
@enum SUMaterialWorkflow
@brief Indicates the workflow being used to represent materials
@since SketchUp 2025.0, API 13.0
 */
enum SUMaterialWorkflow {
  SUMaterialWorkflow_Classic = 0,          ///< Classic material workflow
  SUMaterialWorkflow_PBRMetallicRoughness  ///< PBR metallic/roughness material workflow
};

/**
@enum SUMaterialNormalMapStyle
@brief Indicates the normal mapping convention used by the material.
@since SketchUp 2025.0, API 13.0
*/
enum SUMaterialNormalMapStyle {
  SUMaterialNormalMapStyle_OpenGL = 0,  ///< OpenGL style
  SUMaterialNormalMapStyle_DirectX,     ///< DirectX style
};

/**
@brief Converts from an \ref SUMaterialRef to an \ref SUEntityRef.
       This is essentially an upcast operation.
@param[in] material The given material reference.
@related SUMaterialRef
@return
- The converted \ref SUEntityRef if material is a valid object
- If not, the returned reference will be invalid
*/
SU_EXPORT SUEntityRef SUMaterialToEntity(SUMaterialRef material);

/**
@brief Converts from an \ref SUEntityRef to an \ref SUMaterialRef.
       This is essentially a downcast operation so the given SUEntityRef must be
       convertible to an \ref SUMaterialRef.
@param[in] entity The given entity reference.
@related SUMaterialRef
@return
- The converted \ref SUMaterialRef if the downcast operation succeeds
- If not, the returned reference will be invalid
*/
SU_EXPORT SUMaterialRef SUMaterialFromEntity(SUEntityRef entity);

/**
@brief Creates a material.

If the material is not associated with any face, it must be deallocated with
\ref SUMaterialRelease().
@param[out] material The material created.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_OUTPUT if the input parameter is NULL
*/
SU_RESULT SUMaterialCreate(SUMaterialRef* material);

/**
@brief Releases a material and its resources.

The material must not be associated with a parent object such as a face.
@param[in,out] material The material to be released.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT material is not a valid object
- \ref SU_ERROR_NULL_POINTER_INPUT if material is NULL
*/
SU_RESULT SUMaterialRelease(SUMaterialRef* material);

/**
@brief Sets the name of a material object.

@warning Breaking Change: A new failure mode was added in SketchUp 2018,
         API 6.0. Returns \ref SU_ERROR_INVALID_ARGUMENT if the material is
         managed by a model and the provided name was previously associated
         with a different material in the model.

@param[in,out] material The material object.
@param[in]     name     The name to set the material name. Assumed to be UTF-8
                        encoded.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if material is not a valid object
- \ref SU_ERROR_NULL_POINTER_INPUT if name is NULL
- \ref SU_ERROR_INVALID_ARGUMENT if material is managed and name is not unique
*/
SU_RESULT SUMaterialSetName(SUMaterialRef material, const char* name);

/**
@brief Retrieves the internal name of a material object. The internal name is
       the unprocessed  identifier string stored with the material.

@warning Breaking Change: The behavior of this method was changed in
         SketchUp 2017, API 5.0. In previous releases this method retrieved the
         material's non-localized display name but it was changed to retrieve
         the internal name. If the old functionality is required, use \ref
         SUMaterialGetNameLegacyBehavior.

@param[in]  material The material object.
@param[out] name     The name retrieved.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if material is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if name is NULL
- \ref SU_ERROR_INVALID_OUTPUT if name does not point to a valid \ref
  SUStringRef object
*/
SU_RESULT SUMaterialGetName(SUMaterialRef material, SUStringRef* name);

/**
@brief Retrieves the name of a material object. This method was added for users
       who require the functionality of \ref SUMaterialGetName() prior to
       SketchUp 2017, API 5.0. If the internal name is encased in square
       brackets, [], this method will return the name without brackets,
       otherwise the name will match the name retrieved by \ref
       SUMaterialGetName.
@since SketchUp 2017, API 5.0
@param[in]  material The material object.
@param[out] name     The name retrieved.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if material is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if name is NULL
- \ref SU_ERROR_INVALID_OUTPUT if name does not point to a valid \ref
  SUStringRef object
*/
SU_RESULT SUMaterialGetNameLegacyBehavior(SUMaterialRef material, SUStringRef* name);

/**
@brief Sets the color of a material object.
@param[in,out] material The material object.
@param[in]     color    The color value to set the material color.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if material is not a valid object
- \ref SU_ERROR_NULL_POINTER_INPUT if color is NULL
*/
SU_RESULT SUMaterialSetColor(SUMaterialRef material, const SUColor* color);

/**
@brief Retrieves the color value of a material object.
@param[in]  material The material object.
@param[out] color    The color value retrieved.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_NULL_POINTER_OUTPUT if color is NULL
- \ref SU_ERROR_NO_DATA if the material object does not have a color value
*/
SU_RESULT SUMaterialGetColor(SUMaterialRef material, SUColor* color);

/**
@brief Sets the texture of a material object.
@note Materials take ownership of their assigned textures, so textures should not be shared
      accross different materials.
@param[in,out] material The material object.
@param[in]     texture  The texture object to set the material texture.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p material or \p texture is not a valid object
- \ref SU_ERROR_GENERIC if \p texture contains invalid image data
*/
SU_RESULT SUMaterialSetTexture(SUMaterialRef material, SUTextureRef texture);

/**
@brief Retrieves the texture of a material object.
@param[in]  material The material object.
@param[out] texture  The texture object retrieved. This texture should not be released
                     via SUTextureRelease() since it is owned by the material.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if material is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if texture is NULL
- \ref SU_ERROR_NO_DATA if the material object does not have a texture
*/
SU_RESULT SUMaterialGetTexture(SUMaterialRef material, SUTextureRef* texture);

/**
@brief Retrieves the alpha value (0.0 - 1.0) of a material object.
@param[in]  material The material object.
@param[out] alpha    The alpha value retrieved.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if material is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if alpha is NULL
*/
SU_RESULT SUMaterialGetOpacity(SUMaterialRef material, double* alpha);

/**
@brief Sets the alpha value of a material object.
@param[in,out] material The material object.
@param[in]     alpha    The alpha value to set. Must be within range [0.0, 1.0].
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if material is not a valid object
- \ref SU_ERROR_OUT_OF_RANGE if alpha is not within the acceptable range
*/
SU_RESULT SUMaterialSetOpacity(SUMaterialRef material, double alpha);

/**
@brief Retrieves the flag indicating whether alpha values are used from a
       material object.
@param[in]  material    The material object.
@param[out] use_opacity The flag retrieved.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if material is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if use_opacity is NULL
*/
SU_RESULT SUMaterialGetUseOpacity(SUMaterialRef material, bool* use_opacity);

/**
@brief Sets the flag indicating whether alpha values are used on a material
       object.
@param[in,out] material    The material object.
@param[in]     use_opacity The flag boolean value to set.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if material is not a valid object
*/
SU_RESULT SUMaterialSetUseOpacity(SUMaterialRef material, bool use_opacity);

/**
@brief Sets the type of a material object.
@param[in,out] material The material object.
@param[in]     type     The type to set.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if material is not a valid object
*/
SU_RESULT SUMaterialSetType(SUMaterialRef material, enum SUMaterialType type);

/**
@brief Retrieves the type of a material object.
@param[in]  material The material object.
@param[out] type     The type retrieved.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if material is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if type is NULL
*/
SU_RESULT SUMaterialGetType(SUMaterialRef material, enum SUMaterialType* type);

/**
@brief Retrieves the flag indicating whether the material is drawn with
       transparency.
@since SketchUp 2018, API 6.0
@param[in]  material     The material object.
@param[out] transparency The flag retrieved.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if material is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if is_drawn_transparent is NULL
*/
SU_RESULT SUMaterialIsDrawnTransparent(SUMaterialRef material, bool* transparency);

/**
@brief Retrieves the owner type of a material object.

@warning Materials owned by SUImageRef and SULayerRef may not be applied
         to any other entity in the model.

@since SketchUp 2019.2, API 7.1
@param[in]  material The material object.
@param[out] type     The type retrieved.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if material is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if type is NULL
*/
SU_RESULT SUMaterialGetOwnerType(SUMaterialRef material, enum SUMaterialOwnerType* type);

/**
@brief Sets the colorization type of a material object. This is used when the
       material's color is set to a custom value. Call this function after
       calling SUMaterialSetColor as otherwise the colorize type will be reset.
@since SketchUp 2019.2, API 7.1
@param[in,out] material The material object.
@param[in]     type     The type to set.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if material is not a valid object
- \ref SU_ERROR_INVALID_ARGUMENT if type is not a valid value
*/
SU_RESULT SUMaterialSetColorizeType(SUMaterialRef material, enum SUMaterialColorizeType type);

/**
@brief Retrieves the colorization type of a material object.
@since SketchUp 2019.2, API 7.1
@param[in]  material The material object.
@param[out] type     The type retrieved.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if material is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if type is NULL
*/
SU_RESULT SUMaterialGetColorizeType(SUMaterialRef material, enum SUMaterialColorizeType* type);

/**
@brief The colorize_deltas method retrieves the HLS deltas for colorized
       materials.
@since SketchUp 2019.2, API 7.1
@param[in]  material   The material object.
@param[out] hue        The Hue delta.
@param[out] saturation The Saturation delta.
@param[out] lightness  The Lightness delta.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if material is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if either hue, saturation or lightness
                                    is NULL
*/
SU_RESULT SUMaterialGetColorizeDeltas(
    SUMaterialRef material, double* hue, double* saturation, double* lightness);

/**
@brief Writes a material to a SKM file.
@since SketchUp 2021.1, API 9.1
@param[in]  material   The material object.
@param[in]  file_path  The location to save the material to. Assumed to be
                       UTF-8 encoded.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p material is not a valid object
- \ref SU_ERROR_INVALID_INPUT if \p material is not attached to a model
- \ref SU_ERROR_NULL_POINTER_INPUT if \p file_path is NULL
- \ref SU_ERROR_SERIALIZATION if the serialization operation itself fails
*/
SU_RESULT SUMaterialWriteToFile(SUMaterialRef material, const char* file_path);

/** @name PBR Metallic Roughness Workflow
 */
///@{
/**
@brief Queries the workflow type of a material.
@since SketchUp 2025.0, API 13.0
@param[in]  material The material object.
@param[out] workflow The returned workflow type.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p material is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if \p workflow is NULL
*/
SU_RESULT SUMaterialGetWorkflow(SUMaterialRef material, enum SUMaterialWorkflow* workflow);

/**
@brief Enables metalness properties for the material.
@note After this is enabled, a metallic texture and/or a metallic factor can be set.
@since SketchUp 2025.0, API 13.0
@param[in,out]  material The material object.
@param[in]      enable   Whether to enable or disable.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p material is not a valid object
*/
SU_RESULT SUMaterialSetMetalnessEnabled(SUMaterialRef material, bool enable);

/**
@brief Queries whether metalness properties are enabled for the material.
@since SketchUp 2025.0, API 13.0
@param[in]  material The material object.
@param[out] enabled  Whether metalness is enabled or not.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p material is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if \p enabled is NULL
*/
SU_RESULT SUMaterialIsMetalnessEnabled(SUMaterialRef material, bool* enabled);

/**
@brief Sets the metallic texture of a PBR material.
@note Materials take ownership of their assigned textures, so textures should not be shared
      accross different materials.
@since SketchUp 2025.0, API 13.0
@param[in,out] material The material object.
@param[in]     texture  The texture containing the metalness information. Should be an 8 bit per
                        pixel (single channel) image. If an invalid texture reference is given (i.e.
                        \ref SU_INVALID), then any existing metallic texture will be removed from
                        the material.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p material is not a valid object
- \ref SU_ERROR_INVALID_ARGUMENT if \p texture contains invalid metalness data
*/
SU_RESULT SUMaterialSetMetallicTexture(SUMaterialRef material, SUTextureRef texture);

/**
@brief Retrieves the metallic texture of a material.
@since SketchUp 2025.0, API 13.0
@param[in]  material The material object.
@param[out] texture  The texture containing the metalness information, if one exists. This texture
                     should not be released via SUTextureRelease() since it is owned by the
                     material.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p material is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if \p texture is NULL
- \ref SU_ERROR_NO_DATA if \p material does not have a metalness texture
*/
SU_RESULT SUMaterialGetMetallicTexture(SUMaterialRef material, SUTextureRef* texture);

/**
@brief Sets the metallic factor of a material.
@since SketchUp 2025.0, API 13.0
@param[in,out]  material The material object.
@param[in]      factor   Metallic factor to set. The valid range is [0.0, 1.0].
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p material is not a valid object
- \ref SU_ERROR_INVALID_ARGUMENT if \p factor is not within the valid range
*/
SU_RESULT SUMaterialSetMetallicFactor(SUMaterialRef material, double factor);

/**
@brief Retrieves the metallic factor of a material.
@since SketchUp 2025.0, API 13.0
@param[in]  material The material object.
@param[out] factor   The factor returned.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p material is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if \p factor is NULL
*/
SU_RESULT SUMaterialGetMetallicFactor(SUMaterialRef material, double* factor);

/**
@brief Enables roughness properties for the material.
@note After this is enabled, a roughness texture and/or a roughness factor can be set.
@since SketchUp 2025.0, API 13.0
@param[in,out]  material The material object.
@param[in]      enable   Whether to enable or disable.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p material is not a valid object
*/
SU_RESULT SUMaterialSetRoughnessEnabled(SUMaterialRef material, bool enable);

/**
@brief Queries whether roughness properties are enabled for the material.
@since SketchUp 2025.0, API 13.0
@param[in]  material The material object.
@param[out] enabled  Whether roughness is enabled or not.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p material is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if \p enabled is NULL
*/
SU_RESULT SUMaterialIsRoughnessEnabled(SUMaterialRef material, bool* enabled);

/**
@brief Sets the roughness texture of a PBR material.
@note Materials take ownership of their assigned textures, so textures should not be shared
      accross different materials.
@since SketchUp 2025.0, API 13.0
@param[in,out] material The material object.
@param[in]     texture  The texture containing the roughness information. Should be an 8 bit per
                        pixel (single channel) image. If an invalid texture reference is given (i.e.
                        \ref SU_INVALID), then any existing metallic texture will be removed from
                        the material.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p material is not a valid object
- \ref SU_ERROR_INVALID_ARGUMENT if \p texture contains invalid roughness data
*/
SU_RESULT SUMaterialSetRoughnessTexture(SUMaterialRef material, SUTextureRef texture);

/**
@brief Retrieves the roughness texture of a material.
@since SketchUp 2025.0, API 13.0
@param[in]  material The material object.
@param[out] texture  The texture containing the roughness information, if one exists. This texture
                     should not be released via SUTextureRelease() since it is owned by the
                     material.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p material is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if \p texture is NULL
- \ref SU_ERROR_NO_DATA if \p material does not have a roughness texture
*/
SU_RESULT SUMaterialGetRoughnessTexture(SUMaterialRef material, SUTextureRef* texture);

/**
@brief Sets the roughness factor of a material.
@since SketchUp 2025.0, API 13.0
@param[in,out]  material The material object.
@param[in]      factor   Roughness factor to set. The valid range is [0.0, 1.0].
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p material is not a valid object
- \ref SU_ERROR_INVALID_ARGUMENT if \p factor is not within the valid range
*/
SU_RESULT SUMaterialSetRoughnessFactor(SUMaterialRef material, double factor);

/**
@brief Retrieves the roughness factor of a material.
@since SketchUp 2025.0, API 13.0
@param[in]  material The material object.
@param[out] factor   The factor returned.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p material is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if \p factor is NULL
*/
SU_RESULT SUMaterialGetRoughnessFactor(SUMaterialRef material, double* factor);

/**
@brief Enables normal map for the material.
@note  A normal map texture must be set before enabling it.
@since SketchUp 2025.0.2, API 13.1
@param[in,out]  material The material object.
@param[in]      enable   Whether to enable or disable.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_ARGUMENT if a normal map texture was not set before enabling.
*/
SU_RESULT SUMaterialSetNormalEnabled(SUMaterialRef material, bool enable);

/**
@brief Queries whether normal mapping is enabled for the material.
@since SketchUp 2025.0, API 13.0
@param[in]  material The material object.
@param[out] enabled  Whether normal mapping is enabled or not.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p material is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if \p enabled is NULL
*/
SU_RESULT SUMaterialIsNormalEnabled(SUMaterialRef material, bool* enabled);

/**
@brief Sets the normal texture of a PBR material.
@note Materials take ownership of their assigned textures, so textures should not be shared
      accross different materials.
@since SketchUp 2025.0, API 13.0
@param[in,out] material The material object.
@param[in]     texture  The texture containing the normal information. Should be an 24 bit per pixel
                        (3 channel) image. If an invalid texture reference is given (i.e. \ref
                        SU_INVALID), then any existing normal texture will be removed from the
                        material, which will effectively disable normal mapping.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p material is not a valid object
- \ref SU_ERROR_INVALID_ARGUMENT if \p texture contains invalid normal data
*/
SU_RESULT SUMaterialSetNormalTexture(SUMaterialRef material, SUTextureRef texture);

/**
@brief Retrieves the normal texture of a material.
@since SketchUp 2025.0, API 13.0
@param[in]  material The material object.
@param[out] texture  The texture containing the normal information, if one exists. This texture
                     should not be released via SUTextureRelease() since it is owned by the
                     material.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p material is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if \p texture is NULL
- \ref SU_ERROR_NO_DATA if \p material does not have a normal texture
*/
SU_RESULT SUMaterialGetNormalTexture(SUMaterialRef material, SUTextureRef* texture);

/**
@brief Sets the normal scale of a material.
@since SketchUp 2025.0, API 13.0
@param[in]  material The material object.
@param[in]  scale    Normal scale to set. Should be >= 0.0
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p material is not a valid object
- \ref SU_ERROR_INVALID_ARGUMENT if \p scale is not valid
*/
SU_RESULT SUMaterialSetNormalScale(SUMaterialRef material, double scale);

/**
@brief Retrieves the normal scale of a material.
@since SketchUp 2025.0, API 13.0
@param[in]  material The material object.
@param[out] scale    Normal scale returned.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p material is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if \p scale is NULL
*/
SU_RESULT SUMaterialGetNormalScale(SUMaterialRef material, double* scale);

/**
@brief Sets the normal mapping style of a material.
@since SketchUp 2025.0, API 13.0
@param[in]  material The material object.
@param[in]  style    Normal style to set.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p material is not a valid object
*/
SU_RESULT SUMaterialSetNormalStyle(SUMaterialRef material, enum SUMaterialNormalMapStyle style);

/**
@brief Retrieves the normal mapping style of a material.
@since SketchUp 2025.0, API 13.0
@param[in]  material The material object.
@param[out] style    Normal style returned.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p material is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if \p style is NULL
*/
SU_RESULT SUMaterialGetNormalStyle(SUMaterialRef material, enum SUMaterialNormalMapStyle* style);

/**
@brief Enables ambient occlusion map for the material.
@note  An ambient occlusion map texture must be set before enabling it.
@since SketchUp 2025.0.2, API 13.1
@param[in,out]  material The material object.
@param[in]      enable   Whether to enable or disable.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_ARGUMENT if an ambient occlusion map texture was not set before enabling.
*/
SU_RESULT SUMaterialSetAOEnabled(SUMaterialRef material, bool enable);

/**
@brief Queries whether ambient occlusion mapping is enabled for the material.
@since SketchUp 2025.0, API 13.0
@param[in]  material The material object.
@param[out] enabled  Whether occlusion mapping is enabled or not.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p material is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if \p enabled is NULL
*/
SU_RESULT SUMaterialIsAOEnabled(SUMaterialRef material, bool* enabled);

/**
@brief Sets the ambient occlusion texture of a PBR material.
@note Materials take ownership of their assigned textures, so textures should not be shared
      accross different materials.
@since SketchUp 2025.0, API 13.0
@param[in] material The material object.
@param[in] texture  The texture containing the occlusion information. Should be an 8 bit per pixel
                    (single channel) image. If an invalid texture reference is given (i.e. \ref
                    SU_INVALID), then any existing AO texture will be removed from the material,
                    which will effectively disable AO mapping.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p material is not a valid object
- \ref SU_ERROR_INVALID_ARGUMENT if \p texture contains invalid occlusion data
*/
SU_RESULT SUMaterialSetAOTexture(SUMaterialRef material, SUTextureRef texture);

/**
@brief Retrieves the ambient occlusion texture of a material.
@since SketchUp 2025.0, API 13.0
@param[in]  material The material object.
@param[out] texture  The texture containing the occlusion information, if one exists. This texture
                     should not be released via SUTextureRelease() since it is owned by the
                     material.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p material is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if \p texture is NULL
- \ref SU_ERROR_NO_DATA if \p material does not have an AO texture
*/
SU_RESULT SUMaterialGetAOTexture(SUMaterialRef material, SUTextureRef* texture);

/**
@brief Sets the ambient occlusion strength of a material.
@since SketchUp 2025.0, API 13.0
@param[in] material The material object.
@param[in] strength Strength to set. The valid range is [0.0, 1.0].
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p material is not a valid object
- \ref SU_ERROR_INVALID_ARGUMENT if \p strength is not within the valid range
*/
SU_RESULT SUMaterialSetAOStrength(SUMaterialRef material, double strength);

/**
@brief Retrieves the ambient occlusion strength of a material.
@since SketchUp 2025.0, API 13.0
@param[in]  material The material object.
@param[out] strength Occlusion strength returned.
@related SUMaterialRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p material is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if \p strength is NULL
*/
SU_RESULT SUMaterialGetAOStrength(SUMaterialRef material, double* strength);

// End of PBR grouping:
///@}

#ifdef __cplusplus
}  // extern "C"
#endif

#endif  // SKETCHUP_MODEL_MATERIAL_H_

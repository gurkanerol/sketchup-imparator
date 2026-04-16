// Copyright 2013 Trimble Inc.  All rights reserved.

/**
 * @file
 * @brief Interfaces for SURenderingOptionsRef.
 */
#ifndef SKETCHUP_MODEL_RENDERING_OPTIONS_H_
#define SKETCHUP_MODEL_RENDERING_OPTIONS_H_

#include <SketchUpAPI/color.h>
#include <SketchUpAPI/common.h>
#include <SketchUpAPI/unicodestring.h>
#include <SketchUpAPI/model/defs.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
@struct SURenderingOptionsRef
@brief  Used to get and set values in a rendering options object.
*/

/**
@brief  Gets the number of available rendering options keys.
@since SketchUp 2017, API 5.0
@param[in]  rendering_options The rendering options object.
@param[out] count             The number of keys available.
@related SURenderingOptionsRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if rendering_options is not valid
- \ref SU_ERROR_NULL_POINTER_OUTPUT if count is NULL
*/
SU_RESULT SURenderingOptionsGetNumKeys(SURenderingOptionsRef rendering_options, size_t* count);

/**
@brief  Retrieves keys associated with the rendering options object.
@since SketchUp 2017, API 5.0
@param[in]  rendering_options The rendering options object.
@param[in]  len               The number of keys to retrieve.
@param[out] keys              The keys retrieved.
@param[out] count             The number of keys retrieved.
@related SURenderingOptionsRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if rendering_options is not a valid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if keys or count is NULL
- \ref SU_ERROR_INVALID_OUTPUT if any of the strings in the keys array are
  invalid.
*/
SU_RESULT SURenderingOptionsGetKeys(
    SURenderingOptionsRef rendering_options, size_t len, SUStringRef keys[], size_t* count);

/**
@brief  Sets values in a rendering options object.
@param[in] rendering_options The rendering options object.
@param[in] key               The key. Assumed to be UTF-8 encoded.
@param[in] value_in          The value used to set the option.
@related SURenderingOptionsRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if rendering_options or value_in is an invalid
  object
- \ref SU_ERROR_NULL_POINTER_INPUT if key is NULL
*/
SU_RESULT SURenderingOptionsSetValue(
    SURenderingOptionsRef rendering_options, const char* key, SUTypedValueRef value_in);

/**
@brief  Retrieves the value of a given rendering option.
@param[in]  rendering_options The rendering options object.
@param[in]  key               The key. Assumed to be UTF-8 encoded.
@param[out] value_out         The value retrieved.
@related SURenderingOptionsRef
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if rendering_options is an invalid object
- \ref SU_ERROR_NULL_POINTER_INPUT if key is NULL
- \ref SU_ERROR_INVALID_OUTPUT if value_out is an invalid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if value_out is NULL

The breakdown of rendering options and value types is shown in the table below.

Rendering Option             | Value Type                   | Since
---------------------------- | ---------------------------- | -------------------------
`"BackgroundColor"`          | \ref SUTypedValueType_Color  | &nbsp;
`"BandColor"`                | \ref SUTypedValueType_Color  | &nbsp;
`"ConstructionColor"`        | \ref SUTypedValueType_Color  | &nbsp;
`"DepthQueWidth"`            | \ref SUTypedValueType_Int32  | &nbsp;
`"DisplayColorByLayer"`      | \ref SUTypedValueType_Bool   | &nbsp;
`"DisplayDims"`              | \ref SUTypedValueType_Bool   | &nbsp;
`"DisplayFog"`               | \ref SUTypedValueType_Bool   | &nbsp;
`"DisplayInstanceAxes"`      | \ref SUTypedValueType_Bool   | &nbsp;
`"DisplaySectionPlanes"`     | \ref SUTypedValueType_Bool   | SketchUp 2014, API 2.0
`"DisplaySectionCuts"`       | \ref SUTypedValueType_Bool   | SketchUp 2015, API 3.0
`"DisplaySketchAxes"`        | \ref SUTypedValueType_Bool   | &nbsp;
`"DisplayText"`              | \ref SUTypedValueType_Bool   | &nbsp;
`"DisplayWatermarks"`        | \ref SUTypedValueType_Bool   | &nbsp;
`"DrawBackEdges"`            | \ref SUTypedValueType_Bool   | SketchUp 2015, API 3.0
`"DrawDepthQue"`             | \ref SUTypedValueType_Bool   | &nbsp;
`"DrawGround"`               | \ref SUTypedValueType_Bool   | &nbsp;
`"DrawHidden"`               | \ref SUTypedValueType_Bool   | &nbsp;
`"DrawHiddenGeometry"`       | \ref SUTypedValueType_Bool   | SketchUp 2020, API 8.0
`"DrawHiddenObjects"`        | \ref SUTypedValueType_Bool   | SketchUp 2020, API 8.0
`"DrawHorizon"`              | \ref SUTypedValueType_Bool   | &nbsp;
`"DrawLineEnds"`             | \ref SUTypedValueType_Bool   | &nbsp;
`"DrawProfilesOnly"`         | \ref SUTypedValueType_Bool   | &nbsp;
`"DrawSilhouettes"`          | \ref SUTypedValueType_Bool   | &nbsp;
`"DrawUnderground"`          | \ref SUTypedValueType_Bool   | &nbsp;
`"EdgeColorMode"`            | \ref SUTypedValueType_Int32  | &nbsp;
`"EdgeDisplayMode"`          | \ref SUTypedValueType_Int32  | &nbsp;
`"EdgeType"`                 | \ref SUTypedValueType_Int32  | &nbsp;
`"ExtendLines"`              | \ref SUTypedValueType_Bool   | &nbsp;
`"FaceBackColor"`            | \ref SUTypedValueType_Color  | &nbsp;
`"FaceFrontColor"`           | \ref SUTypedValueType_Color  | &nbsp;
`"FogColor"`                 | \ref SUTypedValueType_Color  | &nbsp;
`"FogEndDist"`               | \ref SUTypedValueType_Double | &nbsp;
`"FogStartDist"`             | \ref SUTypedValueType_Double | &nbsp;
`"FogUseBkColor"`            | \ref SUTypedValueType_Bool   | &nbsp;
`"ForegroundColor"`          | \ref SUTypedValueType_Color  | &nbsp;
`"GroundColor"`              | \ref SUTypedValueType_Color  | &nbsp;
`"GroundTransparency"`       | \ref SUTypedValueType_Int32  | &nbsp;
`"HideConstructionGeometry"` | \ref SUTypedValueType_Bool   | &nbsp;
`"HighlightColor"`           | \ref SUTypedValueType_Color  | &nbsp;
`"HorizonColor"`             | \ref SUTypedValueType_Color  | &nbsp;
`"InactiveFade"`             | \ref SUTypedValueType_Double | &nbsp;
`"InactiveHidden"`           | \ref SUTypedValueType_Bool   | &nbsp;
`"InstanceFade"`             | \ref SUTypedValueType_Double | &nbsp;
`"InstanceHidden"`           | \ref SUTypedValueType_Bool   | &nbsp;
`"JitterEdges"`              | \ref SUTypedValueType_Bool   | &nbsp;
`"LineEndWidth"`             | \ref SUTypedValueType_Int32  | &nbsp;
`"LineExtension"`            | \ref SUTypedValueType_Int32  | &nbsp;
`"LockedColor"`              | \ref SUTypedValueType_Color  | &nbsp;
`"MaterialTransparency"`     | \ref SUTypedValueType_Bool   | &nbsp;
`"ModelTransparency"`        | \ref SUTypedValueType_Bool   | &nbsp;
`"RenderMode"`               | \ref SUTypedValueType_Int32  | &nbsp;
`"SectionActiveColor"`       | \ref SUTypedValueType_Color  | &nbsp;
`"SectionCutDrawEdges"`      | \ref SUTypedValueType_Bool   | SketchUp 2015, API 3.0
`"SectionCutFilled"`         | \ref SUTypedValueType_Bool   | SketchUp 2018, API 6.0
`"SectionCutWidth"`          | \ref SUTypedValueType_Int32  | &nbsp;
`"SectionDefaultCutColor"`   | \ref SUTypedValueType_Color  | &nbsp;
`"SectionDefaultFillColor"`  | \ref SUTypedValueType_Color  | SketchUp 2018, API 6.0
`"SectionInactiveColor"`     | \ref SUTypedValueType_Color  | &nbsp;
`"ShowViewName"`             | \ref SUTypedValueType_Bool   | &nbsp;
`"SilhouetteWidth"`          | \ref SUTypedValueType_Int32  | &nbsp;
`"SkyColor"`                 | \ref SUTypedValueType_Color  | &nbsp;
`"Texture"`                  | \ref SUTypedValueType_Bool   | &nbsp;
`"TransparencySort"`         | \ref SUTypedValueType_Int32  | &nbsp;

Some of the options map to enumerated values, as shown in the table below.

Option             | Value | Meaning               | Since
------------------ | ----- | --------------------- | --------------------------
\b EdgeColorMode   | `0`   | ObjectColor           | &nbsp;
&nbsp;             | `1`   | ForegroundColor       | &nbsp;
&nbsp;             | `2`   | DirectionColor        | &nbsp;
\b EdgeDisplayMode | `0`   | EdgeDisplayNone       | &nbsp;
&nbsp;             | `1`   | EdgeDisplayAll        | &nbsp;
&nbsp;             | `2`   | EdgeDisplayStandalone | &nbsp;
\b RenderMode      | `0`   | RenderWireframe       | &nbsp;
&nbsp;             | `1`   | RenderHidden          | &nbsp;
&nbsp;             | `2`   | RenderFlat            | &nbsp;
&nbsp;             | `3`   | RenderSmooth          | &nbsp;
&nbsp;             | `4`   | RenderTextureObsolete | &nbsp;
&nbsp;             | `5`   | RenderNoMaterials     | &nbsp;
&nbsp;             | `6`   | RenderPhysicallyBased | SketchUp 2025.0, API 13.0
\b EdgeType        | `0`   | EdgeStandard          | &nbsp;
&nbsp;             | `1`   | EdgeNPR               | &nbsp;

@note The rendering option FaceColorMode was removed in SketchUp 2019.1.
*/
SU_RESULT SURenderingOptionsGetValue(
    SURenderingOptionsRef rendering_options, const char* key, SUTypedValueRef* value_out);

#ifdef __cplusplus
}
#endif

#endif  // SKETCHUP_MODEL_RENDERING_OPTIONS_H_

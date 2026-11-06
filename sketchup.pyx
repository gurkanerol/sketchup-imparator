# -*- coding: utf-8 -*-

from libcpp cimport bool
from libc.stddef cimport size_t
from libc.stdlib cimport malloc, free

# --- Inlined C API declarations (formerly slapi .pxd files) ---

# --- slapi/model/defs.pxd ---
# -*- coding: utf-8 -*-
from libcpp cimport bool
from libc.stdint cimport int64_t, uint32_t

ctypedef int SU_RESULT

ctypedef unsigned char SUByte

cdef extern from "SketchUpAPI/model/defs.h":
    ctypedef struct SUArcCurveRef:
        void *ptr
    ctypedef struct SUAttributeDictionaryRef:
        void *ptr
    ctypedef struct SUAxesRef:
        void *ptr
    ctypedef struct SUCameraRef:
        void *ptr
    ctypedef struct SUClassificationsRef:
        void *ptr
    ctypedef struct SUClassificationAttributeRef:
        void *ptr
    ctypedef struct SUClassificationInfoRef:
        void *ptr
    ctypedef struct SUComponentBehavior:
        pass
    ctypedef struct SUComponentDefinitionRef:
        void *ptr
    ctypedef struct SUComponentInstanceRef:
        void *ptr
    ctypedef struct SUCurveRef:
        void *ptr
    ctypedef struct SUDimensionRef:
        void *ptr
    ctypedef struct SUDimensionLinearRef:
        void *ptr
    ctypedef struct SUDimensionRadialRef:
        void *ptr
    ctypedef struct SUDimensionStyleRef:
        void *ptr
    ctypedef struct SUDrawingElementRef:
        void *ptr
    ctypedef struct SUDynamicComponentInfoRef:
        void *ptr
    ctypedef struct SUDynamicComponentAttributeRef:
        void *ptr
    ctypedef struct SUEdgeRef:
        void *ptr
    ctypedef struct SUEdgeUseRef:
        void *ptr
    ctypedef struct SUEntitiesRef:
        void *ptr
    ctypedef struct SUEntityListRef:
        void *ptr
    ctypedef struct SUEntityListIteratorRef:
        void *ptr
    ctypedef struct SUEntityRef:
        void *ptr
    ctypedef struct SUEnvironmentRef:
        void *ptr
    ctypedef struct SUEnvironmentsRef:
        void *ptr
    ctypedef struct SUFaceRef:
        void *ptr
    ctypedef struct SUFontRef:
        void *ptr
    ctypedef struct SUGeometryInputRef:
        void *ptr
    ctypedef struct SUGroupRef:
        void *ptr
    ctypedef struct SUGuideLineRef:
        void *ptr
    ctypedef struct SUGuidePointRef:
        void *ptr
    ctypedef struct SUImageRef:
        void *ptr
    ctypedef struct SUImageRepRef:
        void *ptr
    ctypedef struct SUInstancePathRef:
        void *ptr
    ctypedef struct SULayerRef:
        void *ptr
    ctypedef struct SULayerFolderRef:
        void *ptr
    ctypedef struct SULengthFormatterRef:
        void *ptr
    ctypedef struct SULineStyleRef:
        void *ptr
    ctypedef struct SULineStylesRef:
        void *ptr
    ctypedef struct SULocationRef:
        void *ptr
    ctypedef struct SULoopInputRef:
        void *ptr
    ctypedef struct SULoopRef:
        void *ptr
    ctypedef struct SUMaterialRef:
        void *ptr
    ctypedef struct SUMeshHelperRef:
        void *ptr
    ctypedef struct SUModelRef:
        void *ptr
    ctypedef struct SUOpeningRef:
        void *ptr
    ctypedef struct SUOptionsManagerRef:
        void *ptr
    ctypedef struct SUOptionsProviderRef:
        void *ptr
    ctypedef struct SUOverlayRef:
        void *ptr
    ctypedef struct SUPolyline3dRef:
        void *ptr
    ctypedef struct SURenderingOptionsRef:
        void *ptr
    ctypedef struct SUSceneRef:
        void *ptr
    ctypedef struct SUSchemaRef:
        void *ptr
    ctypedef struct SUSchemaTypeRef:
        void *ptr
    ctypedef struct SUSectionPlaneRef:
        void *ptr
    ctypedef struct SUSelectionRef:
        void *ptr
    ctypedef struct SUShadowInfoRef:
        void *ptr
    ctypedef struct SUSnapRef:
        void *ptr
    ctypedef struct SUStyleRef:
        void *ptr
    ctypedef struct SUStylesRef:
        void *ptr
    ctypedef struct SUTextRef:
        void *ptr
    ctypedef struct SUTextureRef:
        void *ptr
    ctypedef struct SUTextureWriterRef:
        void *ptr
    ctypedef struct SUTypedValueRef:
        void *ptr
    ctypedef struct SUUVHelperRef:
        void *ptr
    ctypedef struct SUVertexRef:
        void *ptr

    cdef enum SURefType:
        SURefType_Unknown = 0,
        SURefType_AttributeDictionary,
        SURefType_Camera,
        SURefType_ComponentDefinition,
        SURefType_ComponentInstance,
        SURefType_Curve,
        SURefType_Edge,
        SURefType_EdgeUse,
        SURefType_Environment,
        SURefType_Environments,
        SURefType_Entities,
        SURefType_Face,
        SURefType_Group,
        SURefType_Image,
        SURefType_Layer,
        SURefType_Location,
        SURefType_Loop,
        SURefType_MeshHelper,
        SURefType_Material,
        SURefType_Model,
        SURefType_Polyline3D,
        SURefType_Scene,
        SURefType_Texture,
        SURefType_TextureWriter,
        SURefType_TypedValue,
        SURefType_UVHelper,
        SURefType_Vertex,
        SURefType_RenderingOptions,
        SURefType_GuidePoint,
        SURefType_GuideLine,
        SURefType_Schema,
        SURefType_SchemaType,
        SURefType_ShadowInfo,
        SURefType_Axes,
        SURefType_ArcCurve,
        SURefType_SectionPlane,
        SURefType_DynamicComponentInfo,
        SURefType_DynamicComponentAttribute,
        SURefType_Style,
        SURefType_Styles,
        SURefType_ImageRep,
        SURefType_InstancePath,
        SURefType_Font,
        SURefType_Dimension,
        SURefType_DimensionLinear,
        SURefType_DimensionRadial,
        SURefType_DimensionStyle,
        SURefType_Text,
        SURefType_EntityList,
        SURefType_EntityListIterator,
        SURefType_DrawingElement,
        SURefType_Entity,
        SURefType_LengthFormatter,
        SURefType_LineStyle,
        SURefType_LineStyleManager,
        SURefType_Selection,
        SURefType_LayerFolder,
        SURefType_Snap

# --- slapi/unicodestring.pxd ---
# -*- coding: utf-8 -*-
from libc.stddef cimport wchar_t


ctypedef wchar_t unichar
cdef extern from "SketchUpAPI/unicodestring.h":
    ctypedef struct SUStringRef:
        void *ptr

    SU_RESULT SUStringCreate(SUStringRef* out_string_ref)
    SU_RESULT SUStringCreateFromUTF8(SUStringRef* out_string_ref, const char* char_array)
    SU_RESULT SUStringCreateFromUTF16(SUStringRef* out_string_ref, const unichar* char_array)
    SU_RESULT SUStringRelease(SUStringRef* string_ref)
    SU_RESULT SUStringGetUTF8Length(SUStringRef string_ref, size_t* out_length)
    SU_RESULT SUStringGetUTF16Length(SUStringRef string_ref, size_t* out_length)
    SU_RESULT SUStringSetUTF8(SUStringRef string_ref, const char* char_array)
    SU_RESULT SUStringSetUTF16(SUStringRef string_ref, const unichar* char_array)
    SU_RESULT SUStringGetUTF8(SUStringRef string_ref, size_t char_array_length, char* out_char_array, size_t* out_number_of_chars_copied)
    SU_RESULT SUStringGetUTF16(SUStringRef string_ref, size_t char_array_length, unichar* out_char_array, size_t* out_number_of_chars_copied)

    # since SketchUp 2017, API 5.0
    SU_RESULT SUStringTrimLeft(SUStringRef string_ref)
    SU_RESULT SUStringTrimRight(SUStringRef string_ref)
    SU_RESULT SUStringCompare(SUStringRef a, SUStringRef b, int *result)


# --- slapi/color.pxd ---
# -*- coding: utf-8 -*-


cdef extern from "SketchUpAPI/color.h":
    ctypedef struct SUColor:
        SUByte red,
        SUByte green,
        SUByte blue,
        SUByte alpha
        
        
    SU_RESULT SUColorBlend(SUColor color1, SUColor color2, double weight, SUColor* blended_color)
    
    SU_RESULT SUColorGetNumNames(size_t* size)
    
    SU_RESULT SUColorGetNames(SUStringRef names[], size_t size)
    
    SU_RESULT SUColorSetByName(SUColor* color, const char* name)
    
    SU_RESULT SUColorSetByValue(SUColor* color, size_t value)

# --- slapi/geometry.pxd ---
# -*- coding: utf-8 -*-
cdef extern from "SketchUpAPI/geometry.h":
    struct SUPoint2D:
        double x
        double y

    struct SUVector2D:
        double x
        double y

    struct SUPoint3D:
        double x
        double y
        double z

    struct SUVector3D:
        double x
        double y
        double z

    struct SUPlane3D:
        double a
        double b
        double c
        double d

    struct SUBoundingBox3D:
        SUPoint3D min_point
        SUPoint3D max_point

    struct SUAxisAlignedRect2D:
        SUPoint2D upper_left
        SUPoint2D lower_right

# --- slapi/geometry/point2d.pxd ---
# -*- coding: utf-8 -*-

cdef extern from "SketchUpAPI/geometry/point2d.h":
    SU_RESULT SUPoint2DToSUPoint2D(const SUPoint2D* point1, const SUPoint2D* point2, SUVector2D* vector)
    SU_RESULT SUPoint2DGetEqual(const SUPoint2D* point1, const SUPoint2D* point2, bool* equal)
    SU_RESULT SUPoint2DOffset(const SUPoint2D* point1, const SUVector2D* vector, SUPoint2D* point2)
    SU_RESULT SUPoint2DDistanceToSUPoint2D(const SUPoint2D* point1,  const SUPoint2D* point2, double* distance)

# --- slapi/geometry/vector2d.pxd ---
# -*- coding: utf-8 -*-
from libcpp cimport bool

cdef extern from "SketchUpAPI/geometry/vector2d.h":
    SU_RESULT SUVector2DIsValid(const SUVector2D* vector, bool* valid)
    SU_RESULT SUVector2DIsParallelTo(const SUVector2D* vector1, const SUVector2D* vector2, bool* parallel)
    SU_RESULT SUVector2DIsPerpendicularTo(const SUVector2D* vector1, const SUVector2D* vector2, bool* perpendicular)
    SU_RESULT SUVector2DIsSameDirectionAs(const SUVector2D* vector1, const SUVector2D* vector2, bool* same_direction)
    SU_RESULT SUVector2DIsEqual(const SUVector2D* vector1, const SUVector2D* vector2, bool* equal)
    SU_RESULT SUVector2DNormalize(SUVector2D* vector)
    SU_RESULT SUVector2DReverse(SUVector2D* vector)
    SU_RESULT SUVector2DDot(const SUVector2D* vector1, const SUVector2D* vector2, double* dot)
    SU_RESULT SUVector2DCross(const SUVector2D* vector1, const SUVector2D* vector2, double* cross)
    SU_RESULT SUVector2DIsUnitVector(const SUVector2D* vector, bool* is_unit_vector)
    SU_RESULT SUVector2DGetLength(const SUVector2D* vector, double* length)
    SU_RESULT SUVector2DSetLength(SUVector2D* vector, double length)
    SU_RESULT SUVector2DAngleBetween(const SUVector2D* vector1, const SUVector2D* vector2, double* angle)

# --- slapi/transformation.pxd ---
# -*- coding: utf-8 -*-

cdef extern from "SketchUpAPI/transformation.h":
    struct SUTransformation:
        double values[16] #; ///< Matrix values in column-major order.

# --- slapi/initialize.pxd ---
# -*- coding: utf-8 -*-

cdef extern from "SketchUpAPI/initialize.h":
    void SUInitialize()
    void SUTerminate()
    void SUGetAPIVersion(size_t* major, size_t* minor)

# --- slapi/slapi.pxd ---
# -*- coding: utf-8 -*-


cdef extern from "SketchUpAPI/slapi.h":
    cdef enum SUResult:
        SU_ERROR_NONE = 0               # Indicates success
        SU_ERROR_NULL_POINTER_INPUT     # A pointer for a required input was NULL.
        SU_ERROR_INVALID_INPUT          # An API object input to the function was not created properly.
        SU_ERROR_NULL_POINTER_OUTPUT    # A pointer for a required output was NULL.
        SU_ERROR_INVALID_OUTPUT         # An API object to be written with output from the function was not created properly.
        SU_ERROR_OVERWRITE_VALID        # Indicates that an input object reference already references an object where it was expected to be \ref SU_INVALID.
        SU_ERROR_GENERIC                # Indicates an unspecified error.
        SU_ERROR_SERIALIZATION          # Indicate an error occurred during loading or
                                        # saving of a file.
        SU_ERROR_OUT_OF_RANGE           # An input contained a value that was outside the
                                        # range of allowed values.
        SU_ERROR_NO_DATA                # The requested operation has no data to return to the
                                        # user. This usually occurs when a request is made for
                                        # data that is only available conditionally.
        SU_ERROR_INSUFFICIENT_SIZE      # Indicates that the size of an output
                                        # parameter is insufficient.
        SU_ERROR_UNKNOWN_EXCEPTION      # An unknown exception occurred.
        SU_ERROR_MODEL_INVALID          # The model requested is invalid and cannot be loaded.
        SU_ERROR_MODEL_VERSION          # The model cannot be loaded or saved due to an
        SU_ERROR_LAYER_LOCKED           # The layer that is being modified is locked.
        SU_ERROR_DUPLICATE              # The user requested an operation that would result in duplicate data.
        SU_ERROR_PARTIAL_SUCCESS        # The requested operation was not fully completed but it returned an intermediate successful result.
        SU_ERROR_UNSUPPORTED            # The requested operation is not supported
        SU_ERROR_INVALID_ARGUMENT       # An argument contains invalid information
        SU_ERROR_ENTITY_LOCKED          # The entity being modified is locked
        SU_ERROR_INVALID_OPERATION      # The requested operation is invalid.

cdef extern from "SketchUpAPI/application/application.h":
    SU_RESULT SUApplicationGetActiveModel(SUModelRef* model)


cdef extern from "SketchUpAPI/sketchup_info.h":
    cdef enum SUEdition:
        SUEdition_Unknown
        SUEdition_Make      # SketchUp Make
        SUEdition_Pro       # SketchUp Pro

    SU_RESULT SUGetVersionStringUtf8(size_t length, char* version)
    SU_RESULT SUGetEdition(SUEdition* edition)

# --- slapi/model/drawing_element.pxd ---
# -*- coding: utf-8 -*-
from libcpp cimport bool

cdef extern from "SketchUpAPI/model/drawing_element.h":
    SUEntityRef SUDrawingElementToEntity(SUDrawingElementRef elem)
    SUDrawingElementRef SUDrawingElementFromEntity(SUEntityRef entity)
    SURefType SUDrawingElementGetType(SUDrawingElementRef elem)
    SU_RESULT SUDrawingElementGetBoundingBox(SUDrawingElementRef elem, SUBoundingBox3D* bbox)
    SU_RESULT SUDrawingElementGetMaterial(SUDrawingElementRef elem, SUMaterialRef* material)
    SU_RESULT SUDrawingElementSetMaterial(SUDrawingElementRef elem, SUMaterialRef material)
    SU_RESULT SUDrawingElementGetLayer(SUDrawingElementRef elem, SULayerRef* layer)
    SU_RESULT SUDrawingElementSetLayer(SUDrawingElementRef elem, SULayerRef layer)
    SU_RESULT SUDrawingElementSetHidden(SUDrawingElementRef elem, bool hide_flag)
    SU_RESULT SUDrawingElementGetHidden(SUDrawingElementRef elem, bool* hide_flag)
    SU_RESULT SUDrawingElementSetCastsShadows(SUDrawingElementRef elem, bool casts_shadows_flag)
    SU_RESULT SUDrawingElementGetCastsShadows(SUDrawingElementRef elem, bool* casts_shadows_flag)
    SU_RESULT SUDrawingElementSetReceivesShadows(SUDrawingElementRef elem, bool receives_shadows_flag)
    SU_RESULT SUDrawingElementGetReceivesShadows(SUDrawingElementRef elem, bool* receives_shadows_flag)

# --- slapi/model/entities.pxd ---
# -*- coding: utf-8 -*-
from libcpp cimport bool

cdef extern from "SketchUpAPI/model/entities.h":
    SU_RESULT SUEntitiesFill(SUEntitiesRef entities, SUGeometryInputRef geom_input, bool weld_vertices)
    SU_RESULT SUEntitiesGetBoundingBox(SUEntitiesRef entities, SUBoundingBox3D* bbox)
    SU_RESULT SUEntitiesGetNumFaces(SUEntitiesRef entities, size_t* count)
    SU_RESULT SUEntitiesGetFaces(SUEntitiesRef entities, size_t len,  SUFaceRef faces[], size_t*  count)
    SU_RESULT SUEntitiesGetNumCurves(SUEntitiesRef entities, size_t* count)
    SU_RESULT SUEntitiesGetCurves(SUEntitiesRef entities, size_t len, SUCurveRef curves[], size_t* count)
    SU_RESULT SUEntitiesGetNumGuidePoints(SUEntitiesRef entities, size_t* count)
    SU_RESULT SUEntitiesGetGuidePoints(SUEntitiesRef entities, size_t len, SUGuidePointRef guide_points[], size_t* count)
    SU_RESULT SUEntitiesGetNumEdges(SUEntitiesRef entities,  bool standalone_only, size_t* count)
    SU_RESULT SUEntitiesGetEdges(SUEntitiesRef entities, bool standalone_only, size_t len, SUEdgeRef edges[], size_t* count)
    SU_RESULT SUEntitiesGetNumPolyline3ds(SUEntitiesRef entities, size_t* count)
    SU_RESULT SUEntitiesGetPolyline3ds(SUEntitiesRef entities, size_t len, SUPolyline3dRef lines[], size_t* count)
    SU_RESULT SUEntitiesAddFaces(SUEntitiesRef entities, size_t len, const SUFaceRef faces[])
    SU_RESULT SUEntitiesAddCurves(SUEntitiesRef entities, size_t len, const SUCurveRef curves[])
    SU_RESULT SUEntitiesAddGuidePoints(SUEntitiesRef entities, size_t len, const SUGuidePointRef guide_points[])
    SU_RESULT SUEntitiesAddGroup(SUEntitiesRef entities, SUGroupRef group)
    SU_RESULT SUEntitiesAddImage(SUEntitiesRef entities, SUImageRef image)
    SU_RESULT SUEntitiesAddInstance(SUEntitiesRef entities, SUComponentInstanceRef instance, SUStringRef* name)
    SU_RESULT SUEntitiesGetNumGroups(SUEntitiesRef entities, size_t* count)
    SU_RESULT SUEntitiesGetGroups(SUEntitiesRef entities, size_t len, SUGroupRef groups[], size_t* count)
    SU_RESULT SUEntitiesGetNumImages(SUEntitiesRef entities, size_t* count)
    SU_RESULT SUEntitiesGetImages(SUEntitiesRef entities,  size_t len, SUImageRef images[], size_t* count)
    SU_RESULT SUEntitiesGetNumInstances(SUEntitiesRef entities, size_t* count)
    SU_RESULT SUEntitiesGetInstances(SUEntitiesRef entities, size_t len, SUComponentInstanceRef instances[], size_t* count)

# --- slapi/model/entity.pxd ---
# -*- coding: utf-8 -*-
from libc.stdint cimport int32_t

cdef extern from "SketchUpAPI/model/entity.h":
    SURefType SUEntityGetType(SUEntityRef entity)
    SU_RESULT SUEntityGetID(SUEntityRef entity, int32_t* entity_id)
    SU_RESULT SUEntityGetNumAttributeDictionaries(SUEntityRef entity, size_t* count)
    SU_RESULT SUEntityGetAttributeDictionaries(SUEntityRef entity, size_t len, SUAttributeDictionaryRef dictionaries[], size_t* count)
    SU_RESULT SUEntityGetAttributeDictionary(SUEntityRef entity, const char* name, SUAttributeDictionaryRef* dictionary)

# --- slapi/model/camera.pxd ---
# -*- coding: utf-8 -*-
from libcpp cimport bool

cdef extern from "SketchUpAPI/model/camera.h":

    SU_RESULT SUCameraCreate(SUCameraRef* camera)
    SU_RESULT SUCameraRelease(SUCameraRef* camera)
    SU_RESULT SUCameraGetOrientation(SUCameraRef camera, SUPoint3D* position, SUPoint3D* target, SUVector3D* up_vector)
    SU_RESULT SUCameraSetOrientation(SUCameraRef camera, const SUPoint3D* position, const SUPoint3D* target, const SUVector3D* up_vector)
    SU_RESULT SUCameraSetPerspectiveFrustumFOV(SUCameraRef camera, double fov)
    SU_RESULT SUCameraGetPerspectiveFrustumFOV(SUCameraRef camera, double* fov)
    SU_RESULT SUCameraGetAspectRatio(SUCameraRef camera, double* aspect_ratio)
    SU_RESULT SUCameraSetOrthographicFrustumHeight(SUCameraRef camera, double height)
    SU_RESULT SUCameraGetOrthographicFrustumHeight(SUCameraRef camera, double* height)
    SU_RESULT SUCameraSetPerspective(SUCameraRef camera, bool perspective)
    SU_RESULT SUCameraGetPerspective(SUCameraRef camera, bool* perspective)

    #since SketchUp 2017, API 5.0
    SU_RESULT SUCameraGetViewTransformation(SUCameraRef camera, SUTransformation* transformation)
    SU_RESULT SUCameraSetAspectRatio(SUCameraRef camera, double aspect_ratio)
    SU_RESULT SUCameraSetAspectRatio(SUCameraRef camera, double aspect_ratio)
    SU_RESULT SUCameraGetClippingDistances(SUCameraRef camera, double* znear, double* zfar)
    SU_RESULT SUCameraSetFOVIsHeight(SUCameraRef camera, bool is_fov_height)
    SU_RESULT SUCameraGetFOVIsHeight(SUCameraRef camera, bool* is_fov_height)
    SU_RESULT SUCameraSetImageWidth(SUCameraRef camera, double width)
    SU_RESULT SUCameraGetImageWidth(SUCameraRef camera, double* width)
    SU_RESULT SUCameraSetDescription(SUCameraRef camera, const char* desc)
    SU_RESULT SUCameraGetDescription(SUCameraRef camera, SUStringRef* desc)
    SU_RESULT SUCameraGetDirection(SUCameraRef camera, SUVector3D* direction)
    SU_RESULT SUCameraSet2D(SUCameraRef camera, bool make_2d)
    SU_RESULT SUCameraGet2D(SUCameraRef camera, bool* is_2d)
    SU_RESULT SUCameraSetScale2D(SUCameraRef camera, double scale)
    SU_RESULT SUCameraGetScale2D(SUCameraRef camera, double* scale)
    SU_RESULT SUCameraSetCenter2D(SUCameraRef camera, const SUPoint3D* center)
    SU_RESULT SUCameraGetCenter2D(SUCameraRef camera, SUPoint3D* center)

# --- slapi/model/geometry_input.pxd ---
# -*- coding: utf-8 -*-
from libcpp cimport bool

cdef extern from "SketchUpAPI/model/geometry_input.h":
    ctypedef struct SULoopInputRef:
        void *ptr

    ctypedef struct SUMaterialInput:
        size_t num_uv_coords
        SUPoint2D uv_coords[4]
        size_t vertex_indices[4]
        SUMaterialRef material

    SU_RESULT SUGeometryInputCreate(SUGeometryInputRef* geom_input)
    SU_RESULT SUGeometryInputRelease(SUGeometryInputRef* geom_input)
    SU_RESULT SUGeometryInputAddVertex(SUGeometryInputRef geom_input, const SUPoint3D* point)
    SU_RESULT SUGeometryInputSetVertices(SUGeometryInputRef geom_input, size_t num_vertices, const SUPoint3D points[])
    SU_RESULT SULoopInputCreate(SULoopInputRef* loop_input)
    SU_RESULT SULoopInputRelease(SULoopInputRef* loop_input)
    SU_RESULT SULoopInputAddVertexIndex(SULoopInputRef loop_input, size_t vertex_index)
    SU_RESULT SULoopInputEdgeSetHidden(SULoopInputRef loop_input, size_t edge_index, bool hidden)
    SU_RESULT SULoopInputEdgeSetSoft(SULoopInputRef loop_input, size_t edge_index, bool soft)
    SU_RESULT SULoopInputEdgeSetSmooth(SULoopInputRef loop_input, size_t edge_index, bool smooth)
    SU_RESULT SULoopInputAddCurve(SULoopInputRef loop_input, size_t first_edge_index, size_t last_edge_index)
    SU_RESULT SUGeometryInputAddFace(SUGeometryInputRef geom_input, SULoopInputRef* outer_loop, size_t* added_face_index)
    SU_RESULT SUGeometryInputFaceSetReverse(SUGeometryInputRef geom_input, size_t face_index, bool reverse)
    SU_RESULT SUGeometryInputFaceSetLayer(SUGeometryInputRef geom_input, size_t face_index, SULayerRef layer)
    SU_RESULT SUGeometryInputFaceAddInnerLoop(SUGeometryInputRef geom_input, size_t face_index, SULoopInputRef* loop_input)
    SU_RESULT SUGeometryInputFaceSetFrontMaterial(SUGeometryInputRef geom_input, size_t face_index, const SUMaterialInput* material_input)
    SU_RESULT SUGeometryInputFaceSetBackMaterial(SUGeometryInputRef geom_input, size_t face_index, const SUMaterialInput* material_input)

# --- slapi/model/model.pxd ---
# -*- coding: utf-8 -*-
from libcpp cimport bool

cdef extern from "SketchUpAPI/model/model.h":
    enum SUEntityType "SUModelStatistics::SUEntityType":
        SUEntityType_Edge = 0,
        SUEntityType_Face
        SUEntityType_ComponentInstance
        SUEntityType_Group
        SUEntityType_Image
        SUEntityType_ComponentDefinition
        SUEntityType_Layer
        SUEntityType_Material
        SUNumEntityTypes

    struct SUModelStatistics:
        int entity_counts[<int>SUNumEntityTypes]

    enum SUModelUnits:
        SUModelUnits_Inches,
        SUModelUnits_Feet,
        SUModelUnits_Millimeters,
        SUModelUnits_Centimeters,
        SUModelUnits_Meters

    enum SUModelLoadStatus:
        SUModelLoadStatus_Success = 0,
        SUModelLoadStatus_Success_MoreRecent

    enum SUModelVersion:
        SUModelVersion_SU3,
        SUModelVersion_SU4,
        SUModelVersion_SU5,
        SUModelVersion_SU6,
        SUModelVersion_SU7,
        SUModelVersion_SU8,
        SUModelVersion_SU2013,
        SUModelVersion_SU2014,
        SUModelVersion_SU2015,
        SUModelVersion_SU2016,
        SUModelVersion_SU2017,
        SUModelVersion_SU2018,
        SUModelVersion_SU2019,
        SUModelVersion_SU2020,
        SUModelVersion_SU2021,
        SUModelVersion_SU2022,
        SUModelVersion_SU2023,
        SUModelVersion_SU2024,
        SUModelVersion_SU2025

    # Entity type flags for SUModelGetEntitiesOfTypeByPersistentIDs
    int FLAG_GET_ENTITIES_TYPE_DEFINITION_ENTITIES
    int FLAG_GET_ENTITIES_TYPE_LAYERS
    int FLAG_GET_ENTITIES_TYPE_LAYER_FOLDERS
    int FLAG_GET_ENTITIES_TYPE_MATERIALS
    int FLAG_GET_ENTITIES_TYPE_SCENES
    int FLAG_GET_ENTITIES_TYPE_STYLES
    int FLAG_GET_ENTITIES_TYPE_DEFINITIONS
    int FLAG_GET_ENTITIES_TYPE_ALL

    SU_RESULT SUModelCreate(SUModelRef* model)
    SU_RESULT SUModelCreateFromFile(SUModelRef* model, const char* file_path)
    SU_RESULT SUModelCreateFromFileWithStatus(SUModelRef* model, const char* file_path, SUModelLoadStatus* status)
    SU_RESULT SUModelCreateFromBuffer(SUModelRef* model, const unsigned char* buffer, size_t buffer_size)
    SU_RESULT SUModelCreateFromBufferWithStatus(SUModelRef* model, const unsigned char* buffer, size_t buffer_size, SUModelLoadStatus* status)
    SU_RESULT SUModelRelease(SUModelRef* model)
    #SUModelRef SUModelFromExisting(uintptr_t data)
    SU_RESULT SUModelGetEntities(SUModelRef model, SUEntitiesRef* entities)
    SU_RESULT SUModelGetActiveEntities(SUModelRef model, SUEntitiesRef* entities)
    SU_RESULT SUModelGetActivePath(SUModelRef model, SUInstancePathRef* instance_path)
    SU_RESULT SUModelGetNumMaterials(SUModelRef model, size_t* count)
    SU_RESULT SUModelGetMaterials(SUModelRef model, size_t len, SUMaterialRef materials[], size_t* count)
    SU_RESULT SUModelGetEnvironments(SUModelRef model, SUEnvironmentsRef* environments)
    SU_RESULT SUModelAddMaterials(SUModelRef model, size_t len, const SUMaterialRef materials[])
    SU_RESULT SUModelLoadMaterial(SUModelRef model, const char* file_path, SUMaterialRef* material)
    SU_RESULT SUModelGetNumComponentDefinitions(SUModelRef model, size_t* count)
    SU_RESULT SUModelGetComponentDefinitions(SUModelRef model, size_t len, SUComponentDefinitionRef components[], size_t* count)
    SU_RESULT SUModelGetNumGroupDefinitions(SUModelRef model, size_t* count)
    SU_RESULT SUModelGetGroupDefinitions(SUModelRef model, size_t len, SUComponentDefinitionRef definitions[], size_t* count)
    SU_RESULT SUModelGetNumImageDefinitions(SUModelRef model, size_t* count)
    SU_RESULT SUModelGetImageDefinitions(SUModelRef model, size_t len, SUComponentDefinitionRef definitions[], size_t* count)
    SU_RESULT SUModelAddComponentDefinitions(SUModelRef model, size_t len, const SUComponentDefinitionRef components[])
    SU_RESULT SUModelRemoveComponentDefinitions(SUModelRef model, size_t len, SUComponentDefinitionRef components[])
    SU_RESULT SUModelSaveToFile(SUModelRef model, const char* file_path)
    SU_RESULT SUModelSaveToFileWithVersion(SUModelRef model, const char* file_path, SUModelVersion version)
    SU_RESULT SUModelGetCamera(SUModelRef model, SUCameraRef* camera)
    SU_RESULT SUModelSetCamera(SUModelRef model, SUCameraRef* camera)
    SU_RESULT SUModelGetNumScenes(SUModelRef model, size_t* num_scenes)
    SU_RESULT SUModelGetNumLayers(SUModelRef model, size_t* count)
    SU_RESULT SUModelGetLayers(SUModelRef model, size_t len, SULayerRef layers[], size_t* count)
    SU_RESULT SUModelAddLayers(SUModelRef model, size_t len, const SULayerRef layers[])
    SU_RESULT SUModelGetDefaultLayer(SUModelRef model, SULayerRef* layer)
    SU_RESULT SUModelRemoveLayers(SUModelRef model, size_t len, SULayerRef layers[])
    SU_RESULT SUModelGetActiveLayer(SUModelRef model, SULayerRef* layer)
    SU_RESULT SUModelSetActiveLayer(SUModelRef model, SULayerRef layer)
    SU_RESULT SUModelGetVersion(SUModelRef model, int* major, int* minor, int* build)
    SU_RESULT SUModelGetNumAttributeDictionaries(SUModelRef model, size_t* count)
    SU_RESULT SUModelGetAttributeDictionaries(SUModelRef model, size_t len, SUAttributeDictionaryRef dictionaries[], size_t* count)
    SU_RESULT SUModelGetAttributeDictionary(SUModelRef model, const char* name, SUAttributeDictionaryRef* dictionary)
    SU_RESULT SUModelIsGeoReferenced(SUModelRef model, bool* is_geo_ref)
    SU_RESULT SUModelGetLocation(SUModelRef model, SULocationRef* location)
    SU_RESULT SUModelGetStatistics(SUModelRef model, SUModelStatistics* statistics)
    SU_RESULT SUModelSetGeoReference(SUModelRef model, double latitude, double longitude, double altitude, bool is_z_value_centered, bool is_on_ocean_floor)
    SU_RESULT SUModelGetRenderingOptions(SUModelRef model, SURenderingOptionsRef* rendering_options)
    SU_RESULT SUModelGetShadowInfo(SUModelRef model, SUShadowInfoRef* shadow_info)
    SU_RESULT SUModelGetOptionsManager(SUModelRef model, SUOptionsManagerRef* options_manager)
    SU_RESULT SUModelGetNorthCorrection(SUModelRef model, double* north_correction)
    SU_RESULT SUModelMergeCoplanarFaces(SUModelRef model)
    SU_RESULT SUModelGetScenes(SUModelRef model, size_t len, SUSceneRef scenes[], size_t* count)
    SU_RESULT SUModelGetSceneWithName(SUModelRef model, const char* name, SUSceneRef* scene)
    SU_RESULT SUModelAddScenes(SUModelRef model, size_t len, const SUSceneRef scenes[])
    SU_RESULT SUModelAddScene(SUModelRef model, int index, SUSceneRef scene, int* out_index)
    SU_RESULT SUModelReorderScene(SUModelRef model, SUSceneRef scene, size_t new_index)
    SU_RESULT SUModelGetActiveScene(SUModelRef model, SUSceneRef *scene)
    SU_RESULT SUModelSetActiveScene(SUModelRef model, SUSceneRef scene)
    SU_RESULT SUModelAddMatchPhotoScene(SUModelRef model, const char* image_file, SUCameraRef camera, const char* scene_name, SUSceneRef *scene)
    SU_RESULT SUModelGetName(SUModelRef model, SUStringRef* name)
    SU_RESULT SUModelSetName(SUModelRef model, const char* name)
    SU_RESULT SUModelGetPath(SUModelRef model, SUStringRef* path)
    SU_RESULT SUModelGetTitle(SUModelRef model, SUStringRef* title)
    SU_RESULT SUModelGetDescription(SUModelRef model, SUStringRef* description)
    SU_RESULT SUModelSetDescription(SUModelRef model, const char* description)
    SU_RESULT SUModelGetUnits(SUModelRef model, SUModelUnits* units)
    SU_RESULT SUModelGetClassifications(SUModelRef model, SUClassificationsRef* classifications)
    SU_RESULT SUModelGetAxes(SUModelRef model, SUAxesRef* axes)
    SU_RESULT SUModelGetStyles(SUModelRef model, SUStylesRef* styles)
    SU_RESULT SUModelGetInstancePathByPid(SUModelRef model, SUStringRef pid_ref, SUInstancePathRef* instance_path_ref)
    SU_RESULT SUModelGetNumFonts(SUModelRef model, size_t* count)
    SU_RESULT SUModelGetFonts(SUModelRef model, size_t len, SUFontRef fonts[], size_t* count)
    SU_RESULT SUModelGetDimensionStyle(SUModelRef model, SUDimensionStyleRef* style)
    SU_RESULT SUModelGetLengthFormatter(SUModelRef model, SULengthFormatterRef* formatter)
    SU_RESULT SUModelGenerateUniqueMaterialName(SUModelRef model, const char* in_name, SUStringRef* out_name)
    SU_RESULT SUModelFixErrors(SUModelRef model)
    SU_RESULT SUModelOrientFacesConsistently(SUModelRef model, bool recurse_components)
    SU_RESULT SUModelGetLineStyles(SUModelRef model, SULineStylesRef* line_styles)
    SU_RESULT SUModelLoadDefinition(SUModelRef model, const char* filename, SUComponentDefinitionRef* definition)
    SU_RESULT SUModelLoadDefinitionWithStatus(SUModelRef model, const char* filename, SUComponentDefinitionRef* definition, SUModelLoadStatus* status)
    SU_RESULT SUModelRemoveMaterials(SUModelRef model, size_t len, SUMaterialRef materials[])
    SU_RESULT SUModelRemoveScenes(SUModelRef model, size_t len, SUSceneRef scenes[])
    SU_RESULT SUModelGetNumAllMaterials(SUModelRef model, size_t* count)
    SU_RESULT SUModelGetAllMaterials(SUModelRef model, size_t len, SUMaterialRef materials[], size_t* count)
    SU_RESULT SUModelGetGuid(SUModelRef model, SUStringRef* guid)
    SU_RESULT SUModelGetLayersByPersistentIDs(SUModelRef model, size_t num_pids, const int64_t pids[], SULayerRef layers[])
    SU_RESULT SUModelIsDrawingElementVisible(SUModelRef model, SUInstancePathRef path, bool* visible)
    SU_RESULT SUModelGetEntitiesByPersistentIDs(SUModelRef model, size_t num_pids, const int64_t pids[], SUEntityRef entities[])
    SU_RESULT SUModelGetEntitiesOfTypeByPersistentIDs(SUModelRef model, const uint32_t type_flags, const size_t num_pids, const int64_t pids[], SUEntityRef entities[])
    SU_RESULT SUModelGetSelection(SUModelRef model, SUSelectionRef* selection)
    SU_RESULT SUModelGetNumLayerFolders(SUModelRef model, size_t* count)
    SU_RESULT SUModelGetLayerFolders(SUModelRef model, size_t len, SULayerFolderRef* layer_folders, size_t* count)
    SU_RESULT SUModelPurgeEmptyLayerFolders(SUModelRef model, size_t* count)
    SU_RESULT SUModelAddLayerFolder(SUModelRef model, SULayerFolderRef layer_folder)
    SU_RESULT SUModelPurgeUnusedLayers(SUModelRef model, size_t* count)
    SU_RESULT SUModelGetNumTopLevelLayers(SUModelRef model, size_t* count)
    SU_RESULT SUModelGetTopLevelLayers(SUModelRef model, size_t len, SULayerRef layers[], size_t* count)
    SU_RESULT SUModelRemoveLayerFolders(SUModelRef model, size_t len, SULayerFolderRef layer_folders[])
    SU_RESULT SUModelGetBehavior(SUModelRef model, SUComponentBehavior* behavior)
    SU_RESULT SUModelSetBehavior(SUModelRef model, const SUComponentBehavior* behavior)

# --- slapi/model/component_definition.pxd ---
# -*- coding: utf-8 -*-
from libcpp cimport bool

from libc.time cimport tm


cdef extern from "SketchUpAPI/model/component_definition.h":
    cdef enum SUSnapToBehavior:
            SUSnapToBehavior_None = 0,
            SUSnapToBehavior_Any,
            SUSnapToBehavior_Horizontal,
            SUSnapToBehavior_Vertical,
            SUSnapToBehavior_Sloped

    cdef struct SUComponentBehavior:
        SUSnapToBehavior component_snap
        bool component_cuts_opening
        bool component_always_face_camera
        bool component_shadows_face_sun
        size_t component_no_scale_mask

    cdef enum SUComponentType:
        SUComponentType_Normal, # Regular component definition
        SUComponentType_Group   # Group definition

    SUEntityRef SUComponentDefinitionToEntity(SUComponentDefinitionRef comp_def)
    SUComponentDefinitionRef SUComponentDefinitionFromEntity(SUEntityRef entity)
    SUDrawingElementRef SUComponentDefinitionToDrawingElement(SUComponentDefinitionRef comp_def)
    SUComponentDefinitionRef SUComponentDefinitionFromDrawingElement(SUDrawingElementRef drawing_elem)
    SU_RESULT SUComponentDefinitionCreate(SUComponentDefinitionRef* comp_def)
    SU_RESULT SUComponentDefinitionRelease(SUComponentDefinitionRef* comp_def)
    SU_RESULT SUComponentDefinitionGetName(SUComponentDefinitionRef comp_def, SUStringRef* name)
    SU_RESULT SUComponentDefinitionSetName(SUComponentDefinitionRef comp_def, const char* name)
    SU_RESULT SUComponentDefinitionGetGuid(SUComponentDefinitionRef comp_def, SUStringRef* guid_ref)
    SU_RESULT SUComponentDefinitionGetEntities(SUComponentDefinitionRef comp_def, SUEntitiesRef* entities)
    SU_RESULT SUComponentDefinitionGetDescription(SUComponentDefinitionRef comp_def, SUStringRef* desc)
    SU_RESULT SUComponentDefinitionSetDescription(SUComponentDefinitionRef comp_def, const char* desc)
    SU_RESULT SUComponentDefinitionCreateInstance(SUComponentDefinitionRef comp_def, SUComponentInstanceRef* instance)
    SU_RESULT SUComponentDefinitionGetNumUsedInstances(SUComponentDefinitionRef comp_def, size_t* count) # API 5.0
    SU_RESULT SUComponentDefinitionGetNumInstances(SUComponentDefinitionRef comp_def, size_t* count) # API 5.0
    SU_RESULT SUComponentDefinitionGetInstances(SUComponentDefinitionRef comp_def, size_t len, SUComponentInstanceRef instances[], size_t* count) # API 5.0
    SU_RESULT SUComponentDefinitionGetBehavior(SUComponentDefinitionRef comp_def, SUComponentBehavior* behavior)
    SU_RESULT SUComponentDefinitionSetBehavior(SUComponentDefinitionRef comp_def, const SUComponentBehavior* behavior)
    SU_RESULT SUComponentDefinitionApplySchemaType(SUComponentDefinitionRef comp_def,SUSchemaRef schema_ref, SUSchemaTypeRef schema_type_ref)
    SU_RESULT SUComponentDefinitionIsInternal(SUComponentDefinitionRef comp_def, bool* is_internal) # API 4.0
    SU_RESULT SUComponentDefinitionGetPath(SUComponentDefinitionRef comp_def, SUStringRef* path) # API 4.0
    SU_RESULT SUComponentDefinitionGetLoadTime(SUComponentDefinitionRef comp_def, tm* load_time) # API 4.0
    SU_RESULT SUComponentDefinitionGetNumOpenings(SUComponentDefinitionRef comp_def, size_t* count) # API 4.0
    SU_RESULT SUComponentDefinitionGetOpenings(SUComponentDefinitionRef comp_def, size_t len, SUOpeningRef openings[], size_t* count) # API 4.0
    SU_RESULT SUComponentDefinitionGetInsertPoint(SUComponentDefinitionRef comp_def, SUPoint3D* point) # API 4.0
    SU_RESULT SUComponentDefinitionGetType(SUComponentDefinitionRef comp_def, SUComponentType* type) # API 4.0
    SU_RESULT SUComponentDefinitionOrientFacesConsistently(SUComponentDefinitionRef comp_def) # API 4.0
    SU_RESULT SUComponentDefinitionSetInsertPoint(SUComponentDefinitionRef comp_def, SUPoint3D* point) # API 4.0
    SU_RESULT SUComponentDefinitionSetAxes(SUComponentDefinitionRef comp_def, SUAxesRef axes) # API 4.0



# --- slapi/model/component_instance.pxd ---
# -*- coding: utf-8 -*-
from libcpp cimport bool

cdef extern from "SketchUpAPI/model/component_instance.h":
    SUEntityRef SUComponentInstanceToEntity(SUComponentInstanceRef instance)
    SUComponentInstanceRef SUComponentInstanceFromEntity(SUEntityRef entity)
    SUDrawingElementRef SUComponentInstanceToDrawingElement(SUComponentInstanceRef instance)
    SUComponentInstanceRef SUComponentInstanceFromDrawingElement(SUDrawingElementRef drawing_elem)
    SU_RESULT SUComponentInstanceSetName(SUComponentInstanceRef instance,const char* name)
    SU_RESULT SUComponentInstanceRelease(SUComponentInstanceRef* instance)
    SU_RESULT SUComponentInstanceGetName(SUComponentInstanceRef instance, SUStringRef* name)
    SU_RESULT SUComponentInstanceSetGuid(SUComponentInstanceRef instance, const char* guid)
    SU_RESULT SUComponentInstanceGetGuid(SUComponentInstanceRef instance, SUStringRef* guid)
    SU_RESULT SUComponentInstanceSetTransform(SUComponentInstanceRef instance,const SUTransformation* transform)
    SU_RESULT SUComponentInstanceGetTransform(SUComponentInstanceRef instance, SUTransformation* transform);
    SU_RESULT SUComponentInstanceGetDefinition(SUComponentInstanceRef instance, SUComponentDefinitionRef* component)
    SU_RESULT SUComponentInstanceSetLocked(SUComponentInstanceRef instance, bool lock) # API 4.0
    SU_RESULT SUComponentInstanceIsLocked(SUComponentInstanceRef instance, bool* is_locked) # API 4.0
    SU_RESULT SUComponentInstanceSaveAs(SUComponentInstanceRef instance, const char* file_path)
    SU_RESULT SUComponentInstanceComputeVolume(SUComponentInstanceRef instance, const SUTransformation* transform, double* volume) # API 4.0
    SU_RESULT SUComponentInstanceCreateDCInfo(SUComponentInstanceRef instance, SUDynamicComponentInfoRef* dc_info) # API 4.0
    SU_RESULT SUComponentInstanceCreateClassificationInfo(SUComponentInstanceRef instance, SUClassificationInfoRef* classification_info) # API 5.0
    SU_RESULT SUComponentInstanceGetNumAttachedInstances(SUComponentInstanceRef instance, size_t* count)
    SU_RESULT SUComponentInstanceGetAttachedInstances(SUComponentInstanceRef instance, size_t len, SUComponentInstanceRef instances[], size_t* count)

# --- slapi/model/material.pxd ---
# -*- coding: utf-8 -*-
from libcpp cimport bool

cdef extern from "SketchUpAPI/model/material.h":
    cdef enum SUMaterialType:
        SUMaterialType_Colored = 0,  # Colored material
        SUMaterialType_Textured,     # Textured material
        SUMaterialType_ColorizedTexture #Colored and textured material

    cdef enum SUMaterialOwnerType:
        SUMaterialOwnerType_None = 0,        # Not owned
        SUMaterialOwnerType_DrawingElement,  # Can be applied to SUDrawingElements
        SUMaterialOwnerType_Image,           # Owned exclusively by an Image
        SUMaterialOwnerType_Layer            # Owned exclusively by a Layer

    cdef enum SUMaterialColorizeType:
        SUMaterialColorizeType_Shift = 0,  # Shifts the texture's Hue
        SUMaterialColorizeType_Tint        # Colorize the texture

    cdef enum SUMaterialWorkflow:
        SUMaterialWorkflow_Classic = 0,          # Classic material workflow
        SUMaterialWorkflow_PBRMetallicRoughness  # PBR metallic/roughness material workflow

    cdef enum SUMaterialNormalMapStyle:
        SUMaterialNormalMapStyle_OpenGL = 0,  # OpenGL style
        SUMaterialNormalMapStyle_DirectX     # DirectX style

    SUEntityRef SUMaterialToEntity(SUMaterialRef material)
    SUMaterialRef SUMaterialFromEntity(SUEntityRef entity)
    SU_RESULT SUMaterialCreate(SUMaterialRef* material)
    SU_RESULT SUMaterialRelease(SUMaterialRef* material)
    SU_RESULT SUMaterialSetName(SUMaterialRef material, const char* name)
    SU_RESULT SUMaterialGetName(SUMaterialRef material, SUStringRef* name)
    SU_RESULT SUMaterialGetNameLegacyBehavior(SUMaterialRef material, SUStringRef* name) # API 5.0
    SU_RESULT SUMaterialSetColor(SUMaterialRef material, const SUColor* color)
    SU_RESULT SUMaterialGetColor(SUMaterialRef material, SUColor* color)
    SU_RESULT SUMaterialSetTexture(SUMaterialRef material, SUTextureRef texture)
    SU_RESULT SUMaterialGetTexture(SUMaterialRef material,  SUTextureRef* texture)
    SU_RESULT SUMaterialGetOpacity(SUMaterialRef material, double* alpha)
    SU_RESULT SUMaterialSetOpacity(SUMaterialRef material, double alpha)
    SU_RESULT SUMaterialGetUseOpacity(SUMaterialRef material, bool* use_opacity)
    SU_RESULT SUMaterialSetUseOpacity(SUMaterialRef material, bool use_opacity)
    SU_RESULT SUMaterialSetType(SUMaterialRef material, SUMaterialType type)
    SU_RESULT SUMaterialGetType(SUMaterialRef material, SUMaterialType* type)
    SU_RESULT SUMaterialIsDrawnTransparent(SUMaterialRef material, bool* transparency)  # API 6.0
    SU_RESULT SUMaterialGetOwnerType(SUMaterialRef material, SUMaterialOwnerType* type)  # API 7.1
    SU_RESULT SUMaterialSetColorizeType(SUMaterialRef material, SUMaterialColorizeType type)  # API 7.1
    SU_RESULT SUMaterialGetColorizeType(SUMaterialRef material, SUMaterialColorizeType* type)  # API 7.1
    SU_RESULT SUMaterialGetColorizeDeltas(SUMaterialRef material, double* hue, double* saturation, double* lightness)  # API 7.1
    SU_RESULT SUMaterialWriteToFile(SUMaterialRef material, const char* file_path)  # API 9.1
    
    # PBR Metallic Roughness Workflow - API 13.0
    SU_RESULT SUMaterialGetWorkflow(SUMaterialRef material, SUMaterialWorkflow* workflow)
    SU_RESULT SUMaterialSetMetalnessEnabled(SUMaterialRef material, bool enable)
    SU_RESULT SUMaterialIsMetalnessEnabled(SUMaterialRef material, bool* enabled)
    SU_RESULT SUMaterialSetMetallicTexture(SUMaterialRef material, SUTextureRef texture)
    SU_RESULT SUMaterialGetMetallicTexture(SUMaterialRef material, SUTextureRef* texture)
    SU_RESULT SUMaterialSetMetallicFactor(SUMaterialRef material, double factor)
    SU_RESULT SUMaterialGetMetallicFactor(SUMaterialRef material, double* factor)
    SU_RESULT SUMaterialSetRoughnessEnabled(SUMaterialRef material, bool enable)
    SU_RESULT SUMaterialIsRoughnessEnabled(SUMaterialRef material, bool* enabled)
    SU_RESULT SUMaterialSetRoughnessTexture(SUMaterialRef material, SUTextureRef texture)
    SU_RESULT SUMaterialGetRoughnessTexture(SUMaterialRef material, SUTextureRef* texture)
    SU_RESULT SUMaterialSetRoughnessFactor(SUMaterialRef material, double factor)
    SU_RESULT SUMaterialGetRoughnessFactor(SUMaterialRef material, double* factor)
    SU_RESULT SUMaterialIsNormalEnabled(SUMaterialRef material, bool* enabled)
    SU_RESULT SUMaterialSetNormalTexture(SUMaterialRef material, SUTextureRef texture)
    SU_RESULT SUMaterialGetNormalTexture(SUMaterialRef material, SUTextureRef* texture)
    SU_RESULT SUMaterialSetNormalScale(SUMaterialRef material, double scale)
    SU_RESULT SUMaterialGetNormalScale(SUMaterialRef material, double* scale)
    SU_RESULT SUMaterialSetNormalStyle(SUMaterialRef material, SUMaterialNormalMapStyle style)
    SU_RESULT SUMaterialGetNormalStyle(SUMaterialRef material, SUMaterialNormalMapStyle* style)
    SU_RESULT SUMaterialIsAOEnabled(SUMaterialRef material, bool* enabled)
    SU_RESULT SUMaterialSetAOTexture(SUMaterialRef material, SUTextureRef texture)
    SU_RESULT SUMaterialGetAOTexture(SUMaterialRef material, SUTextureRef* texture)
    SU_RESULT SUMaterialSetAOStrength(SUMaterialRef material, double strength)
    SU_RESULT SUMaterialGetAOStrength(SUMaterialRef material, double* strength)

# --- slapi/model/group.pxd ---
# -*- coding: utf-8 -*-

cdef extern from "SketchUpAPI/model/group.h":
    SUEntityRef SUGroupToEntity(SUGroupRef group)
    SUGroupRef SUGroupFromEntity(SUEntityRef entity)
    SUDrawingElementRef SUGroupToDrawingElement(SUGroupRef group)
    SUGroupRef SUGroupFromDrawingElement(SUDrawingElementRef drawing_elem)
    SUComponentInstanceRef SUGroupToComponentInstance(SUGroupRef group)  # API 4.0
    SUGroupRef SUGroupFromComponentInstance(SUComponentInstanceRef component_inst)  # API 4.0
    SU_RESULT SUGroupCreate(SUGroupRef* group)
    SU_RESULT SUGroupSetName(SUGroupRef group, const char* name)
    SU_RESULT SUGroupGetName(SUGroupRef group, SUStringRef* name)
    SU_RESULT SUGroupGetGuid(SUGroupRef group, SUStringRef* guid)
    SU_RESULT SUGroupSetGuid(SUGroupRef group, const char* guid_str)
    SU_RESULT SUGroupSetTransform(SUGroupRef group, const SUTransformation* transform)
    SU_RESULT SUGroupGetTransform(SUGroupRef group,  SUTransformation* transform)
    SU_RESULT SUGroupGetEntities(SUGroupRef group, SUEntitiesRef* entities)
    SU_RESULT SUGroupGetDefinition(SUGroupRef group, SUComponentDefinitionRef* component)

# --- slapi/model/texture.pxd ---
# -*- coding: utf-8 -*-
from libcpp cimport bool

cdef extern from "SketchUpAPI/model/texture.h":
    SUEntityRef SUTextureToEntity(SUTextureRef texture)
    SUTextureRef SUTextureFromEntity(SUEntityRef entity)
    SU_RESULT SUTextureCreateFromImageRep(SUTextureRef* texture, SUImageRepRef image)   # API 5.0
    SU_RESULT SUTextureCreateFromFile(SUTextureRef* texture, const char* file_path, double s_scale, double t_scale)
    SU_RESULT SUTextureRelease(SUTextureRef* texture)
    SU_RESULT SUTextureGetDimensions(SUTextureRef texture, size_t* width, size_t* height, double* s_scale, double* t_scale)
    SU_RESULT SUTextureSetDimensions(SUTextureRef texture, double s_scale, double t_scale)  # API 13.0
    SU_RESULT SUTextureGetImageRep(SUTextureRef texture, SUImageRepRef* image) # API 5.0
    SU_RESULT SUTextureWriteToFile(SUTextureRef texture, const char* file_path)
    SU_RESULT SUTextureSetFileName(SUTextureRef texture, const char* name) # API 5.0
    SU_RESULT SUTextureGetFileName(SUTextureRef texture,  SUStringRef* file_name)
    SU_RESULT SUTextureGetFilePath(SUTextureRef texture, SUStringRef* file_path)  # API 11.1
    SU_RESULT SUTextureGetUseAlphaChannel(SUTextureRef texture, bool* alpha_channel_used)
    SU_RESULT SUTextureGetAverageColor(SUTextureRef texture, SUColor* color_val)
    SU_RESULT SUTextureGetColorizedImageRep(SUTextureRef texture, SUImageRepRef* image_rep)  # API 6.0
    SU_RESULT SUTextureWriteOriginalToFile(SUTextureRef texture, const char* file_path)  # API 7.1

    # deprecated
    SU_RESULT SUTextureCreateFromImageData(SUTextureRef* texture, size_t width, size_t height, size_t bits_per_pixel, SUByte pixel_data[])
    SU_RESULT SUTextureGetImageDataSize(SUTextureRef texture,  size_t* data_size, size_t* bits_per_pixel)
    SU_RESULT SUTextureGetImageData(SUTextureRef texture, size_t data_size, SUByte pixel_data[])

# --- slapi/model/scene.pxd ---
# -*- coding: utf-8 -*-
from libcpp cimport bool
from libc.stdint cimport uint32_t

cdef extern from "SketchUpAPI/model/scene.h":


    SUEntityRef SUSceneToEntity(SUSceneRef scene)
    SUSceneRef SUSceneFromEntity(SUEntityRef entity)
    SU_RESULT SUSceneCreate(SUSceneRef* scene)
    SU_RESULT SUSceneRelease(SUSceneRef* scene)
    SU_RESULT SUSceneGetUseCamera(SUSceneRef scene, bool* use_camera)
    SU_RESULT SUSceneSetUseCamera(SUSceneRef scene, bool use_camera)
    SU_RESULT SUSceneGetCamera(SUSceneRef scene, SUCameraRef* camera)
    SU_RESULT SUSceneSetCamera(SUSceneRef scene, SUCameraRef camera)
    SU_RESULT SUSceneGetName(SUSceneRef scene, SUStringRef* name)
    SU_RESULT SUSceneSetName(SUSceneRef scene, const char* scene_name)
    SU_RESULT SUSceneGetRenderingOptions(SUSceneRef scene, SURenderingOptionsRef* options)
    SU_RESULT SUSceneGetShadowInfo(SUSceneRef scene, SUShadowInfoRef* shadow_info)
    SU_RESULT SUSceneGetUseShadowInfo(SUSceneRef scene, bool* use_shadow_info)
    SU_RESULT SUSceneSetUseShadowInfo(SUSceneRef scene, bool use_shadow_info)
    SU_RESULT SUSceneGetUseRenderingOptions(SUSceneRef scene, bool* use_rendering_options) # API 4.0
    SU_RESULT SUSceneSetUseRenderingOptions(SUSceneRef scene, bool use_rendering_options) # API 4.0
    SU_RESULT SUSceneGetUseHiddenLayers(SUSceneRef scene, bool* use_hidden_layers) # API 4.0
    SU_RESULT SUSceneSetUseHiddenLayers(SUSceneRef scene, bool use_hidden_layers) # API 4.0
    SU_RESULT SUSceneGetNumLayers(SUSceneRef scene, size_t *count) # API 4.0
    SU_RESULT SUSceneGetLayers(SUSceneRef scene, size_t len, SULayerRef layers[], size_t*  count) # API 4.0
    SU_RESULT SUSceneAddLayer(SUSceneRef scene, SULayerRef layer) # API 4.0
    SU_RESULT SUSceneRemoveLayer(SUSceneRef scene, SULayerRef layer) # API 4.0
    SU_RESULT SUSceneClearLayers(SUSceneRef scene) # API 4.0
    SU_RESULT SUSceneGetAxes(SUSceneRef scene, SUAxesRef* axes) # API 4.0
    SU_RESULT SUSceneSetUseAxes(SUSceneRef scene, bool use_axes)  # API 5.0
    SU_RESULT SUSceneGetUseAxes(SUSceneRef scene, bool* use_axes)  # API 5.0
    SU_RESULT SUSceneGetNumHiddenEntities(SUSceneRef scene, size_t* count)  # API 5.0
    SU_RESULT SUSceneGetHiddenEntities(SUSceneRef scene, size_t len, SUEntityRef entities[], size_t* count)  # API 5.0
    SU_RESULT SUSceneSetFlags(SUSceneRef scene, uint32_t flags)  # API 5.0
    SU_RESULT SUSceneGetFlags(SUSceneRef scene, uint32_t* flags)  # API 5.0
    SU_RESULT SUSceneSetSketchAxesDisplayed(SUSceneRef scene, bool displayed)  # API 5.0
    SU_RESULT SUSceneGetSketchAxesDisplayed(SUSceneRef scene, bool* displayed)  # API 5.0
    SU_RESULT SUSceneGetPhotoMatchImageDisplayed(SUSceneRef scene, bool* displayed)  # API 5.0
    SU_RESULT SUSceneClearPhotoMatchImage(SUSceneRef scene)  # API 5.0
    SU_RESULT SUSceneGetStyle(SUSceneRef scene, SUStyleRef* style)  # API 5.0
    SU_RESULT SUSceneCopy(SUSceneRef scene, SUSceneRef copy_scene)  # API 5.0
    SU_RESULT SUSceneActivate(SUSceneRef scene)  # API 5.0

# --- slapi/model/edge.pxd ---
# -*- coding: utf-8 -*-
from libcpp cimport bool

cdef extern from "SketchUpAPI/model/edge.h":
    SUEntityRef SUEdgeToEntity(SUEdgeRef edge)
    SUEdgeRef SUEdgeFromEntity(SUEntityRef entity)
    SUDrawingElementRef SUEdgeToDrawingElement(SUEdgeRef edge)
    SUEdgeRef SUEdgeFromDrawingElement(SUDrawingElementRef drawing_elem)
    SU_RESULT SUEdgeCreate(SUEdgeRef* edge, const SUPoint3D* start, const SUPoint3D* end)
    SU_RESULT SUEdgeRelease(SUEdgeRef* edge)
    SU_RESULT SUEdgeGetCurve(SUEdgeRef edge, SUCurveRef* curve)
    SU_RESULT SUEdgeGetStartVertex(SUEdgeRef edge, SUVertexRef* vertex)
    SU_RESULT SUEdgeGetEndVertex(SUEdgeRef edge, SUVertexRef* vertex)
    SU_RESULT SUEdgeSetSoft(SUEdgeRef edge, bool soft_flag)
    SU_RESULT SUEdgeGetSoft(SUEdgeRef edge, bool* soft_flag)
    SU_RESULT SUEdgeSetSmooth(SUEdgeRef edge, bool smooth_flag)
    SU_RESULT SUEdgeGetSmooth(SUEdgeRef edge, bool* smooth_flag)
    SU_RESULT SUEdgeGetNumFaces(SUEdgeRef edge, size_t* count)
    SU_RESULT SUEdgeGetFaces(SUEdgeRef edge, size_t len, SUFaceRef faces[], size_t* count)
    SU_RESULT SUEdgeGetColor(SUEdgeRef edge, SUColor* color)
    SU_RESULT SUEdgeGetLengthWithTransform(SUEdgeRef edge, const SUTransformation* transform, double* length)
    SU_RESULT SUEdgeSetColor(SUEdgeRef edge, const SUColor* color)

# --- slapi/model/layer.pxd ---
# -*- coding: utf-8 -*-
from libcpp cimport bool

cdef extern from "SketchUpAPI/model/layer.h":
    SUEntityRef SULayerToEntity(SULayerRef layer)
    SULayerRef SULayerFromEntity(SUEntityRef entity)
    SU_RESULT SULayerCreate(SULayerRef* layer)
    SU_RESULT SULayerRelease(SULayerRef* layer)
    SU_RESULT SULayerGetName(SULayerRef layer, SUStringRef* name)
    SU_RESULT SULayerSetName(SULayerRef layer, const char* name)
    SU_RESULT SULayerGetMaterial(SULayerRef layer, SUMaterialRef* material)
    SU_RESULT SULayerGetVisibility(SULayerRef layer, bool* visible)
    SU_RESULT SULayerSetVisibility(SULayerRef layer, bool visible)

# --- slapi/model/face.pxd ---
# -*- coding: utf-8 -*-
from libcpp cimport bool

cdef extern from "SketchUpAPI/model/face.h":
    SUEntityRef SUFaceToEntity(SUFaceRef face)
    SUFaceRef SUFaceFromEntity(SUEntityRef entity)
    SUDrawingElementRef SUFaceToDrawingElement(SUFaceRef face)
    SUFaceRef SUFaceFromDrawingElement(SUDrawingElementRef drawing_elem)
    SU_RESULT SUFaceCreate(SUFaceRef* face,const SUPoint3D vertices3d[], SULoopInputRef* outer_loop)
    SU_RESULT SUFaceCreateSimple(SUFaceRef* face, const  SUPoint3D vertices3d[], size_t len)
    SU_RESULT SUFaceGetNormal(SUFaceRef face, SUVector3D* normal)
    SU_RESULT SUFaceRelease(SUFaceRef* face)
    SU_RESULT SUFaceGetNumEdges(SUFaceRef face, size_t* count)
    SU_RESULT SUFaceGetEdges(SUFaceRef face, size_t len, SUEdgeRef edges[],  size_t* count)
    SU_RESULT SUFaceGetPlane(SUFaceRef face, SUPlane3D* plane)
    SU_RESULT SUFaceGetNumVertices(SUFaceRef face, size_t* count)
    SU_RESULT SUFaceGetVertices(SUFaceRef face, size_t len, SUVertexRef vertices[], size_t* count)
    SU_RESULT SUFaceGetOuterLoop(SUFaceRef face, SULoopRef* loop)
    SU_RESULT SUFaceGetNumInnerLoops(SUFaceRef face, size_t* count)
    SU_RESULT SUFaceGetInnerLoops(SUFaceRef face, size_t len, SULoopRef loops[], size_t* count)
    SU_RESULT SUFaceAddInnerLoop(SUFaceRef face, const SUPoint3D vertices3d[], SULoopInputRef* loop)
    SU_RESULT SUFaceGetNumOpenings(SUFaceRef face, size_t* count)
    SU_RESULT SUFaceGetOpenings(SUFaceRef face, size_t len, SUOpeningRef openings[], size_t* count)
    SU_RESULT SUFaceGetFrontMaterial(SUFaceRef face, SUMaterialRef* material)
    SU_RESULT SUFaceSetFrontMaterial(SUFaceRef face, SUMaterialRef material)
    SU_RESULT SUFaceGetBackMaterial(SUFaceRef face, SUMaterialRef* material)
    SU_RESULT SUFaceSetBackMaterial(SUFaceRef face, SUMaterialRef material)
    SU_RESULT SUFaceIsFrontMaterialAffine(SUFaceRef face, bool* is_affine)
    SU_RESULT SUFaceIsBackMaterialAffine(SUFaceRef face, bool* is_affine)
    SU_RESULT SUFaceGetArea(SUFaceRef face, double* area)
    SU_RESULT SUFaceGetAreaWithTransform(SUFaceRef face, const SUTransformation* transform, double *area) # API 4.0
    SU_RESULT SUFaceIsComplex(SUFaceRef face, bool* is_complex)
    SU_RESULT SUFaceGetUVHelper(SUFaceRef face, bool front, bool back, SUTextureWriterRef texture_writer,  SUUVHelperRef* uv_helper)
    SU_RESULT SUFaceGetUVHelperWithTextureHandle(SUFaceRef face,  bool front, bool back, SUTextureWriterRef texture_writer, long textureHandle,  SUUVHelperRef* uv_helper)
    SU_RESULT SUFaceGetNumAttachedDrawingElements(SUFaceRef face, size_t* count) # API 4.0
    SU_RESULT SUFaceGetAttachedDrawingElements(SUFaceRef face, size_t len, SUDrawingElementRef elems[], size_t* count) # API 4.0
    SU_RESULT SUFaceReverse(SUFaceRef face)

# --- slapi/model/mesh_helper.pxd ---
# -*- coding: utf-8 -*-

cdef extern from  "SketchUpAPI/model/mesh_helper.h":
    SU_RESULT SUMeshHelperCreate(SUMeshHelperRef* mesh_ref, SUFaceRef face_ref)
    SU_RESULT SUMeshHelperCreateWithTextureWriter(SUMeshHelperRef* mesh_ref, SUFaceRef face_ref, SUTextureWriterRef texture_writer_ref)
    SU_RESULT SUMeshHelperCreateWithUVHelper(SUMeshHelperRef* mesh_ref, SUFaceRef face_ref, SUUVHelperRef uv_helper_ref)
    SU_RESULT SUMeshHelperRelease(SUMeshHelperRef* mesh_ref)
    SU_RESULT SUMeshHelperGetNumTriangles(SUMeshHelperRef mesh_ref, size_t* count)
    SU_RESULT SUMeshHelperGetNumVertices(SUMeshHelperRef mesh_ref, size_t* count)
    SU_RESULT SUMeshHelperGetVertexIndices(SUMeshHelperRef mesh_ref, size_t len, size_t indices[], size_t* count)
    SU_RESULT SUMeshHelperGetVertices(SUMeshHelperRef mesh_ref, size_t len, SUPoint3D vertices[], size_t* count)
    SU_RESULT SUMeshHelperGetFrontSTQCoords(SUMeshHelperRef mesh_ref, size_t len, SUPoint3D stq[], size_t* count)
    SU_RESULT SUMeshHelperGetBackSTQCoords(SUMeshHelperRef mesh_ref, size_t len, SUPoint3D stq[], size_t* count)
    SU_RESULT SUMeshHelperGetNormals(SUMeshHelperRef mesh_ref, size_t len, SUVector3D normals[], size_t* count)

# --- slapi/model/texture_writer.pxd ---
# -*- coding: utf-8 -*-
from libcpp cimport bool

cdef extern from "SketchUpAPI/model/texture_writer.h":
    SU_RESULT SUTextureWriterCreate(SUTextureWriterRef* writer)
    SU_RESULT SUTextureWriterRelease(SUTextureWriterRef* writer)
    SU_RESULT SUTextureWriterLoadEntity(SUTextureWriterRef writer, SUEntityRef entity, long* texture_id)
    SU_RESULT SUTextureWriterLoadFace(SUTextureWriterRef writer, SUFaceRef face, long* front_texture_id, long* back_texture_id)
    SU_RESULT SUTextureWriterGetNumTextures(SUTextureWriterRef writer, size_t* count)
    SU_RESULT SUTextureWriterWriteTexture(SUTextureWriterRef writer, long texture_id, const char* path, bool reduce_size)
    SU_RESULT SUTextureWriterWriteAllTextures(SUTextureWriterRef writer, const char* directory)
    SU_RESULT SUTextureWriterIsTextureAffine(SUTextureWriterRef writer, long texture_id, bool* is_affine)
    SU_RESULT SUTextureWriterGetTextureFilePath(SUTextureWriterRef writer, long texture_id, SUStringRef* file_path)
    SU_RESULT SUTextureWriterGetFrontFaceUVCoords(SUTextureWriterRef writer, SUFaceRef face, size_t len, const SUPoint3D points[], SUPoint2D uv_coords[])
    SU_RESULT SUTextureWriterGetBackFaceUVCoords(SUTextureWriterRef writer, SUFaceRef face, size_t len, const SUPoint3D points[], SUPoint2D uv_coords[])
    SU_RESULT SUTextureWriterGetTextureIdForEntity(SUTextureWriterRef writer, SUEntityRef entity, long* texture_id)
    SU_RESULT SUTextureWriterGetTextureIdForFace(SUTextureWriterRef writer, SUFaceRef face, bool front, long* texture_id)

# --- slapi/model/rendering_options.pxd ---
# -*- coding: utf-8 -*-

cdef extern from "SketchUpAPI/model/rendering_options.h":
    SU_RESULT SURenderingOptionsGetValue(SURenderingOptionsRef rendering_options, const char* key, SUTypedValueRef* value_out)
    SU_RESULT SURenderingOptionsSetValue(SURenderingOptionsRef rendering_options, const char* key, SUTypedValueRef value_in)

    # since SetchUp 2017, API 5.0
    SU_RESULT SURenderingOptionsGetNumKeys(SURenderingOptionsRef rendering_options, size_t* count)
    SU_RESULT SURenderingOptionsGetKeys(SURenderingOptionsRef rendering_options, size_t len, SUStringRef keys[], size_t* count)

# --- slapi/model/attribute_dictionary.pxd ---

cdef extern from "SketchUpAPI/model/attribute_dictionary.h":
    SUEntityRef SUAttributeDictionaryToEntity(SUAttributeDictionaryRef dictionary)
    SUAttributeDictionaryRef SUAttributeDictionaryFromEntity(SUEntityRef entity)
    SU_RESULT SUAttributeDictionaryGetName(SUAttributeDictionaryRef dictionary, SUStringRef* name)
    SU_RESULT SUAttributeDictionarySetValue(SUAttributeDictionaryRef dictionary, const char* key, SUTypedValueRef value_in)
    SU_RESULT SUAttributeDictionaryGetValue(SUAttributeDictionaryRef dictionary, const char* key, SUTypedValueRef* value_out)
    SU_RESULT SUAttributeDictionaryGetNumKeys (SUAttributeDictionaryRef dictionary, size_t *count)
    SU_RESULT SUAttributeDictionaryGetKeys(SUAttributeDictionaryRef dictionary, size_t len, SUStringRef keys[], size_t* count)

# --- slapi/model/arccurve.pxd ---

cdef extern from "SketchUpAPI/model/arccurve.h":
    SUEntityRef SUArcCurveToEntity(SUArcCurveRef arccurve)
    SUArcCurveRef SUArcCurveFromEntity(SUEntityRef entity)
    SUCurveRef SUArcCurveToCurve(SUArcCurveRef arccurve)
    SUArcCurveRef SUArcCurveFromCurve(SUCurveRef curve)
    SU_RESULT SUArcCurveCreate(SUArcCurveRef* arccurve,
                           const SUPoint3D* center,
                           const SUPoint3D* start_point,
                           const SUPoint3D* end_point,
                           const SUVector3D* normal,
                           size_t num_edges)
    SU_RESULT SUArcCurveRelease(SUArcCurveRef* arccurve)
    SU_RESULT SUArcCurveGetRadius(SUArcCurveRef arccurve, double* radius)
    SU_RESULT SUArcCurveGetStartPoint(SUArcCurveRef arccurve, SUPoint3D* point)
    SU_RESULT SUArcCurveGetEndPoint(SUArcCurveRef arccurve, SUPoint3D* point)
    SU_RESULT SUArcCurveGetXAxis(SUArcCurveRef arccurve, SUVector3D* axis)
    SU_RESULT SUArcCurveGetYAxis(SUArcCurveRef arccurve, SUVector3D* axis)
    SU_RESULT SUArcCurveGetCenter(SUArcCurveRef arccurve, SUPoint3D* point)
    SU_RESULT SUArcCurveGetNormal(SUArcCurveRef arccurve, SUVector3D* normal)
    SU_RESULT SUArcCurveGetStartAngle(SUArcCurveRef arccurve, double* angle)
    SU_RESULT SUArcCurveGetEndAngle(SUArcCurveRef arccurve, double* angle)
    SU_RESULT SUArcCurveGetIsFullCircle(SUArcCurveRef arccurve, bool* is_full)

# --- slapi/model/typed_value.pxd ---
# -*- coding: utf-8 -*-
from libcpp cimport bool
from libc.stdint cimport int16_t, int32_t, int64_t

cdef extern from "SketchUpAPI/model/typed_value.h":
    cdef enum SUTypedValueType:
        SUTypedValueType_Empty = 0,
        SUTypedValueType_Byte,
        SUTypedValueType_Short,
        SUTypedValueType_Int32,
        SUTypedValueType_Float,
        SUTypedValueType_Double,
        SUTypedValueType_Bool,
        SUTypedValueType_Color,
        SUTypedValueType_Time,
        SUTypedValueType_String,
        SUTypedValueType_Vector3D,
        SUTypedValueType_Array

    SU_RESULT SUTypedValueCreate(SUTypedValueRef* typed_value)
    SU_RESULT SUTypedValueRelease(SUTypedValueRef* typed_value)
    SU_RESULT SUTypedValueGetType(SUTypedValueRef typed_value, SUTypedValueType* type)
    SU_RESULT SUTypedValueGetByte(SUTypedValueRef typed_value, char* byte_value)
    SU_RESULT SUTypedValueSetByte(SUTypedValueRef typed_value, char byte_value)
    SU_RESULT SUTypedValueGetInt16(SUTypedValueRef typed_value, int16_t* int16_value)
    SU_RESULT SUTypedValueSetInt16(SUTypedValueRef typed_value, int16_t int16_value)
    SU_RESULT SUTypedValueGetInt32(SUTypedValueRef typed_value, int32_t* int32_value)
    SU_RESULT SUTypedValueSetInt32(SUTypedValueRef typed_value, int32_t int32_value)
    SU_RESULT SUTypedValueGetFloat(SUTypedValueRef typed_value, float* float_value)
    SU_RESULT SUTypedValueSetFloat(SUTypedValueRef typed_value, float float_value)
    SU_RESULT SUTypedValueGetDouble(SUTypedValueRef typed_value, double* double_value)
    SU_RESULT SUTypedValueSetDouble(SUTypedValueRef typed_value, double double_value)
    SU_RESULT SUTypedValueGetBool(SUTypedValueRef typed_value, bool* bool_value)
    SU_RESULT SUTypedValueSetBool(SUTypedValueRef typed_value, bool bool_value)
    SU_RESULT SUTypedValueGetColor(SUTypedValueRef typed_value, SUColor* color)
    SU_RESULT SUTypedValueSetColor(SUTypedValueRef typed_value, const SUColor* color)
    SU_RESULT SUTypedValueGetTime(SUTypedValueRef typed_value, int64_t* time_value)
    SU_RESULT SUTypedValueSetTime(SUTypedValueRef typed_value, int64_t time_value)
    SU_RESULT SUTypedValueGetString(SUTypedValueRef typed_value, SUStringRef* string_value)
    SU_RESULT SUTypedValueSetString(SUTypedValueRef typed_value, const char* string_value)
    SU_RESULT SUTypedValueGetVector3d(SUTypedValueRef typed_value, double vector3d_value[3])
    SU_RESULT SUTypedValueSetVector3d(SUTypedValueRef typed_value, const double vector3d_value[3])
    SU_RESULT SUTypedValueSetUnitVector3d(SUTypedValueRef typed_value, const double vector3d_value[3])
    SU_RESULT SUTypedValueGetArrayItems(SUTypedValueRef typed_value, size_t len, SUTypedValueRef values[], size_t* count)
    SU_RESULT SUTypedValueSetArrayItems(SUTypedValueRef typed_value, size_t len, SUTypedValueRef values[])
    SU_RESULT SUTypedValueGetNumArrayItems(SUTypedValueRef typed_value, size_t* count)


# --- slapi/model/axes.pxd ---

cdef extern from "SketchUpAPI/model/axes.h":
    SUEntityRef SUAxesToEntity(SUAxesRef axes)
    SUAxesRef SUAxesFromEntity(SUEntityRef entity)
    SUDrawingElementRef SUAxesToDrawingElement(SUAxesRef axes)
    SUAxesRef SUAxesFromDrawingElement(SUDrawingElementRef drawing_elem)
    SU_RESULT SUAxesCreate(SUAxesRef* axes)
    SU_RESULT SUAxesCreateCustom(SUAxesRef* axes,
                             const SUPoint3D* origin,
                             const SUVector3D* xaxis,
                             const SUVector3D* yaxis,
                             const SUVector3D* zaxis)
    SU_RESULT SUAxesRelease(SUAxesRef* axes)
    SU_RESULT SUAxesGetOrigin(SUAxesRef axes, SUPoint3D* origin)
    SU_RESULT SUAxesSetOrigin(SUAxesRef axes, const SUPoint3D* origin)
    SU_RESULT SUAxesGetXAxis(SUAxesRef axes, SUVector3D* axis)
    SU_RESULT SUAxesGetYAxis(SUAxesRef axes, SUVector3D* axis)
    SU_RESULT SUAxesGetZAxis(SUAxesRef axes, SUVector3D* axis)
    SU_RESULT SUAxesSetAxesVecs(SUAxesRef axes,
                            const SUVector3D* xaxis,
                            const SUVector3D* yaxis,
                            const SUVector3D* zaxis)
    SU_RESULT SUAxesGetTransform(SUAxesRef axes,
                                 SUTransformation* transform);
    SU_RESULT SUAxesGetPlane(SUAxesRef axes, SUPlane3D* plane)


cdef extern from "SketchUpAPI/model/loop.h":
    SU_RESULT SULoopGetNumVertices(SULoopRef loop, size_t* count)
    SU_RESULT SULoopGetVertices(SULoopRef loop, size_t len, SUVertexRef vertices[], size_t* count)

cdef extern from "SketchUpAPI/model/vertex.h":
    SU_RESULT SUVertexGetPosition(SUVertexRef vertex, SUPoint3D* position)

cdef extern from "SketchUpAPI/model/uv_helper.h":
    ctypedef struct SUUVQ:
        double u
        double v
        double q
    SU_RESULT SUFaceGetUVHelper(SUFaceRef face, bool front, bool back, SUTextureWriterRef texture_writer, SUUVHelperRef* uv_helper)
    SU_RESULT SUUVHelperGetFrontUVQ(SUUVHelperRef uv_helper, const SUPoint3D* point, SUUVQ* uvq)
    SU_RESULT SUUVHelperGetBackUVQ(SUUVHelperRef uv_helper, const SUPoint3D* point, SUUVQ* uvq)
    SU_RESULT SUUVHelperRelease(SUUVHelperRef* uv_helper)




cdef inline double m(double& v):
    """
    :param v: value to be converted from inches to meters
    :return: value in meters
    """
    return <double> 0.0254 * v

def get_API_version():
    cdef size_t major, minor
    SUGetAPIVersion(&major, &minor)
    return (major, minor)

cdef check_result(SU_RESULT r):
    if not r is SU_ERROR_NONE:
        print(__str_from_SU_RESULT(r))
        raise RuntimeError("Sketchup library giving unexpected results {}".format(__str_from_SU_RESULT(r)))

cdef inline void release_string_ref(SUStringRef* string_ref):
    if string_ref is not NULL and string_ref.ptr != NULL:
        SUStringRelease(string_ref)
        string_ref.ptr = <void*> 0

cdef __str_from_SU_RESULT(SU_RESULT r):
    if r is SU_ERROR_NONE:
        return "SU_ERROR_NONE"
    if r is SU_ERROR_NULL_POINTER_INPUT:
        return "SU_ERROR_NONE"
    if r is SU_ERROR_INVALID_INPUT:
        return "SU_ERROR_INVALID_INPUT"
    if r is SU_ERROR_NULL_POINTER_OUTPUT:
        return "SU_ERROR_NULL_POINTER_OUTPUT"
    if r is SU_ERROR_INVALID_OUTPUT:
        return "SU_ERROR_INVALID_OUTPUT"
    if r is SU_ERROR_OVERWRITE_VALID:
        return "SU_ERROR_OVERWRITE_VALID"
    if r is SU_ERROR_GENERIC:
        return "SU_ERROR_GENERIC"
    if r is SU_ERROR_SERIALIZATION:
        return "SU_ERROR_SERIALIZATION"
    if r is SU_ERROR_OUT_OF_RANGE:
        return "SU_ERROR_OUT_OF_RANGE"
    if r is SU_ERROR_NO_DATA:
        return "SU_ERROR_NO_DATA"
    if r is SU_ERROR_INSUFFICIENT_SIZE:
        return "SU_ERROR_INSUFFICIENT_SIZE"
    if r is SU_ERROR_UNKNOWN_EXCEPTION:
        return "SU_ERROR_UNKNOWN_EXCEPTION"
    if r is SU_ERROR_MODEL_INVALID:
        return "SU_ERROR_MODEL_INVALID"
    if r is SU_ERROR_MODEL_VERSION:
        return "SU_ERROR_MODEL_VERSION"

cdef StringRef2Py(SUStringRef& suStr):
    cdef size_t out_length = 0
    cdef SU_RESULT res = SUStringGetUTF8Length(suStr, &out_length)
    cdef char* out_char_array
    cdef size_t out_number_of_chars_copied
    if out_length == 0:
        return ""
    else:
        out_char_array = <char*> malloc(sizeof(char) * (out_length * 2))
        SUStringGetUTF8(suStr, out_length, out_char_array, &out_number_of_chars_copied)
        try:
            py_result = out_char_array[:out_number_of_chars_copied].decode('UTF-8')
        finally:
            free(out_char_array)
        return py_result

cdef SUStringRef Py2StringRef(s):
    cdef SUStringRef out_string_ref
    cdef SU_RESULT res
    if isinstance(s, str):
        res = SUStringCreateFromUTF8(&out_string_ref, <str> s)
    else:
        raise TypeError("Cannot make sense of string {}".format(s))
    return out_string_ref

cdef class Vertex:
    cdef SUVertexRef vertex

    def __cinit__(self):
        self.vertex.ptr = <void*> 0

    property position:
        def __get__(self):
            cdef SUPoint3D p
            check_result(SUVertexGetPosition(self.vertex, &p))
            return (m(p.x), m(p.y), m(p.z))

cdef class Loop:
    cdef SULoopRef loop

    def __cinit__(self):
        self.loop.ptr = <void*> 0

    property vertices:
        def __get__(self):
            cdef size_t num_vertices = 0
            check_result(SULoopGetNumVertices(self.loop, &num_vertices))
            cdef SUVertexRef* vertices_array = <SUVertexRef*> malloc(sizeof(SUVertexRef) * num_vertices)
            cdef size_t count = 0
            check_result(SULoopGetVertices(self.loop, num_vertices, vertices_array, &count))
            for i in range(count):
                v = Vertex()
                v.vertex.ptr = vertices_array[i].ptr
                yield v
            free(vertices_array)

cdef class Entity:
    cdef SUEntityRef entity

    def __cinit__(self):
        self.entity.ptr = <void*> 0

    property id:
        def __get__(self):
            cdef int32_t entity_id
            check_result(SUEntityGetID(self.entity, &entity_id))
            return entity_id

    def __len__(self):
        cdef size_t count
        check_result(SUEntityGetNumAttributeDictionaries(self.entity, &count))
        return count

cdef class Point2D:
    cdef SUPoint2D p

    def __cinit__(self, double x, double y):
        self.p.x = x
        self.p.y = y

    property x:
        def __get__(self): return self.p.x
        def __set__(self, double x): self.p.x = x

    property y:
        def __get__(self): return self.p.y
        def __set__(self, double y): self.p.y = y

cdef class Point3D:
    cdef SUPoint3D p

    def __cinit__(self, double x=0, double y=0, double z=0):
        self.p.x = x
        self.p.y = y
        self.p.z = z

    property x:
        def __get__(self): return self.p.x
        def __set__(self, double x): self.p.x = x

    property y:
        def __get__(self): return self.p.y
        def __set__(self, double y): self.p.y = y

    property z:
        def __get__(self): return self.p.z
        def __set__(self, double z): self.p.z = z

    def __str__(self):
        return "Point3d<{},{},{}>".format(self.p.x, self.p.y, self.p.z)

    def __repr__(self):
        return "Point3d @{} [{},{},{}]".format(<size_t> &(self.p), self.p.x, self.p.y, self.p.z)

cdef class Vector3D:
    cdef SUVector3D p

    def __cinit__(self, double x, double y, double z):
        self.p.x = x
        self.p.y = y
        self.p.z = z

    property x:
        def __get__(self): return self.p.x
        def __set__(self, double x): self.p.x = x

    property y:
        def __get__(self): return self.p.y
        def __set__(self, double y): self.p.y = y

    property z:
        def __get__(self): return self.p.z
        def __set__(self, double z): self.p.z = z

cdef class Edge:
    cdef SUEdgeRef edge

    def __cinit__(self):
        self.edge.ptr = <void *> 0

    cdef set_ptr(self, void* ptr):
        self.edge.ptr = ptr

    def GetSoft(self):
        cdef bool soft_flag = 0
        check_result(SUEdgeGetSoft(self.edge, &soft_flag))
        return soft_flag

    def GetSmooth(self):
        cdef bool smooth_flag = 0
        check_result(SUEdgeGetSmooth(self.edge, &smooth_flag))
        return smooth_flag

    property start_vertex:
        def __get__(self):
            cdef SUVertexRef v
            v.ptr = <void*> 0
            check_result(SUEdgeGetStartVertex(self.edge, &v))
            res = Vertex()
            res.vertex.ptr = v.ptr
            return res

    property end_vertex:
        def __get__(self):
            cdef SUVertexRef v
            v.ptr = <void*> 0
            check_result(SUEdgeGetEndVertex(self.edge, &v))
            res = Vertex()
            res.vertex.ptr = v.ptr
            return res

cdef class Plane3D:
    cdef Plane3D p
    cdef bool cleanup

    def __cinit__(self, double a, double b, double c, double d):
        self.p.a = a
        self.p.b = b
        self.p.c = c
        self.p.d = d

    property a:
        def __get__(self): return self.p.a
        def __set__(self, double a): self.p.a = a

    property b:
        def __get__(self): return self.p.b
        def __set__(self, double b): self.p.b = b

    property c:
        def __get__(self): return self.p.c
        def __set__(self, double c): self.p.c = c

    property d:
        def __get__(self): return self.p.d
        def __set__(self, double d): self.p.d = d

cdef class Camera:
    cdef SUCameraRef camera

    def __cinit__(self):
        self.camera.ptr = <void *> 0

    cdef set_ptr(self, void* ptr):
        self.camera.ptr = ptr

    def GetOrientation(self):
        cdef SUPoint3D position
        cdef SUPoint3D target
        cdef SUVector3D up_vector = [0, 0, 0]
        check_result(SUCameraGetOrientation(self.camera, &position, &target, &up_vector))
        return (m(position.x), m(position.y), m(position.z)), \
               (m(target.x), m(target.y), m(target.z)), \
               (m(up_vector.x), m(up_vector.y), m(up_vector.z))

    property fov:
        def __get__(self):
            #Retrieves the field of view in degrees of a camera object. The field of view is measured along the vertical direction of the camera.
            cdef double fov
            cdef SU_RESULT res = SUCameraGetPerspectiveFrustumFOV(self.camera, &fov)
            if res == SU_ERROR_NONE:
                return fov
            if res == SU_ERROR_NO_DATA:
                return False
            raise RuntimeError("Sketchup library giving unexpected results {}".format(__str_from_SU_RESULT(res)))

        def __set__(self, double fov):
            check_result(SUCameraSetPerspectiveFrustumFOV(self.camera, fov))

    property perspective:
        def __get__(self):
            cdef bool p
            check_result(SUCameraGetPerspective(self.camera, &p))
            return p

        def __set__(self, bool p):
            check_result(SUCameraSetPerspective(self.camera, p))

    property scale:
        def __get__(self):
            cdef double height = 0
            check_result(SUCameraGetOrthographicFrustumHeight(self.camera, &height))
            return height

        def __set__(self, double height):
            check_result(SUCameraSetOrthographicFrustumHeight(self.camera, height))

    property ortho:
        def __get__(self):
            cdef double o = 0
            cdef SU_RESULT res = SUCameraGetOrthographicFrustumHeight(self.camera, &o)
            if res == SU_ERROR_NONE:
                return o
            if res == SU_ERROR_NO_DATA:
                return False
            raise RuntimeError("Sketchup library giving unexpected results {}".format(__str_from_SU_RESULT(res)))

    property aspect_ratio:
        def __get__(self):
            cdef double asp = 1.0
            cdef SU_RESULT res = SUCameraGetAspectRatio(self.camera, &asp)
            if res == SU_ERROR_NONE:
                return asp
            if res == SU_ERROR_NO_DATA:
                return False
            raise RuntimeError("Sketchup library giving unexpected results {}".format(__str_from_SU_RESULT(res)))

cdef class Texture:
    cdef SUTextureRef tex_ref

    def __cinit__(self):
        self.tex_ref.ptr = <void*> 0

    def write(self, filename):
        py_byte_string = filename.encode('UTF-8')
        cdef const char* file_path = py_byte_string
        check_result(SUTextureWriteToFile(self.tex_ref, file_path))

    property name:
        def __get__(self):
            cdef SUStringRef n
            n.ptr = <void*> 0
            try:
                SUStringCreate(&n)
                check_result(SUTextureGetFileName(self.tex_ref, &n))
                return StringRef2Py(n)
            finally:
                release_string_ref(&n)

    property dimensions:
        def __get__(self):
            cdef double s_scale = 1.0
            cdef double t_scale = 1.0
            cdef size_t width = 0
            cdef size_t height = 0
            cdef SUMaterialRef mat
            check_result(SUTextureGetDimensions(self.tex_ref, &width, &height, &s_scale, &t_scale))
            return width, height, s_scale, t_scale

    property use_alpha_channel:
        def __get__(self):
            cdef bool alpha_channel_used
            check_result(SUTextureGetUseAlphaChannel(self.tex_ref, &alpha_channel_used))
            return alpha_channel_used

cdef class Instance:
    cdef SUComponentInstanceRef instance

    def __cinit__(self):
        self.instance.ptr = <void*> 0

    property name:
        def __get__(self):
            cdef SUStringRef n
            n.ptr = <void*> 0
            try:
                SUStringCreate(&n)
                check_result(SUComponentInstanceGetName(self.instance, &n))
                return StringRef2Py(n)
            finally:
                release_string_ref(&n)

    property entity:
        def __get__(self):
            cdef SUEntityRef ref
            ref = SUComponentInstanceToEntity(self.instance)
            res = Entity()
            res.entity.ptr = ref.ptr
            return res

    property definition:
        def __get__(self):
            cdef SUComponentDefinitionRef component
            component.ptr = <void*> 0
            SUComponentInstanceGetDefinition(self.instance, &component)
            c = Component()
            c.comp_def.ptr = component.ptr
            return c

    property transform:
        def __get__(self):
            cdef SUTransformation t
            check_result(SUComponentInstanceGetTransform(self.instance, &t))
            return [[t.values[0], t.values[4], t.values[8], m(t.values[12])],
                    [t.values[1], t.values[5], t.values[9], m(t.values[13])],
                    [t.values[2], t.values[6], t.values[10], m(t.values[14])],
                    [t.values[3], t.values[7], t.values[11], t.values[15]]]  # * transform

    property material:
        def __get__(self):
            cdef SUDrawingElementRef draw_elem = SUComponentInstanceToDrawingElement(self.instance)
            cdef SUMaterialRef mat
            mat.ptr = <void*> 0
            cdef SU_RESULT = SUDrawingElementGetMaterial(draw_elem, &mat)
            if SU_RESULT == SU_ERROR_NONE:
                m = Material()
                m.material.ptr = mat.ptr
                return m
            else:
                return None

    property layer:
        def __get__(self):
            cdef SUDrawingElementRef draw_elem = SUComponentInstanceToDrawingElement(self.instance)
            cdef SULayerRef lay
            lay.ptr = <void*> 0
            cdef SU_RESULT res = SUDrawingElementGetLayer(draw_elem, &lay)
            if res == SU_ERROR_NONE:
                l = Layer()
                l.layer.ptr = lay.ptr
                return l
            else:
                return None

    property hidden:
        def __get__(self):
            cdef SUDrawingElementRef draw_elem = SUComponentInstanceToDrawingElement(self.instance)
            cdef bool hide_flag = False
            check_result(SUDrawingElementGetHidden(draw_elem, &hide_flag))
            return hide_flag

        def __set__(self, bool hide_flag):
            cdef SUDrawingElementRef draw_elem = SUComponentInstanceToDrawingElement(self.instance)
            check_result(SUDrawingElementSetHidden(draw_elem, hide_flag))

cdef instance_from_ptr(SUComponentInstanceRef r):
    res = Instance()
    res.instance.ptr = r.ptr
    #print("Instance {}".format(hex(<int> r.ptr)))
    return res

cdef class Component:
    cdef SUComponentDefinitionRef comp_def

    def __cinit__(self):
        self.comp_def.ptr = <void*> 0

    property entities:
        def __get__(self):
            cdef SUEntitiesRef e
            e.ptr = <void*> 0
            SUComponentDefinitionGetEntities(self.comp_def, &e);
            res = Entities()
            res.set_ptr(e.ptr)
            return res

    property name:
        def __get__(self):
            cdef SUStringRef n
            n.ptr = <void*> 0
            try:
                SUStringCreate(&n)
                check_result(SUComponentDefinitionGetName(self.comp_def, &n))
                return StringRef2Py(n)
            finally:
                release_string_ref(&n)

    property numInstances:
        def __get__(self):
            cdef size_t n = 0
            check_result(SUComponentDefinitionGetNumInstances(self.comp_def, &n))
            return n

    property numUsedInstances:
        def __get__(self):
            cdef size_t n = 0
            check_result(SUComponentDefinitionGetNumUsedInstances(self.comp_def, &n))
            return n

    property handle:
        def __get__(self):
            return f"0x{<size_t>self.comp_def.ptr:x}"

cdef class Layer:
    cdef SULayerRef layer

    def __cinit__(self, **kwargs):
        self.layer.ptr = <void*> 0
        if not '__skip_init' in kwargs:
            check_result(SULayerCreate(&(self.layer)))

    property name:
        def __get__(self):
            cdef SUStringRef n
            n.ptr = <void*> 0
            try:
                SUStringCreate(&n)
                check_result(SULayerGetName(self.layer, &n))
                return StringRef2Py(n)
            finally:
                release_string_ref(&n)

    property visible:
        def __get__(self):
            cdef bool visible_flag = False
            check_result(SULayerGetVisibility(self.layer, &visible_flag))
            return visible_flag
        def __set__(self, bool vflag):
            check_result(SULayerSetVisibility(self.layer, vflag))

    def __richcmp__(Layer self, Layer other not None, int op):
        if op == 2:  # __eq__
            return f"0x{<size_t>self.layer.ptr:x}" == <size_t> other.layer.ptr

cdef class Group:
    cdef SUGroupRef group

    def __cinit__(self):
        pass

    property name:
        def __get__(self):
            cdef SUStringRef n
            n.ptr = <void*> 0
            try:
                SUStringCreate(&n)
                check_result(SUGroupGetName(self.group, &n))
                return StringRef2Py(n)
            finally:
                release_string_ref(&n)

    property transform:
        def __get__(self):
            cdef SUTransformation t
            check_result(SUGroupGetTransform(self.group, &t))
            return [[t.values[0], t.values[4], t.values[8], m(t.values[12])],
                    [t.values[1], t.values[5], t.values[9], m(t.values[13])],
                    [t.values[2], t.values[6], t.values[10], m(t.values[14])],
                    [t.values[3], t.values[7], t.values[11], t.values[15]]]  # * transform

    property entities:
        def __get__(self):
            cdef SUEntitiesRef entities
            entities.ptr = <void*> 0
            check_result(SUGroupGetEntities(self.group, &entities))
            res = Entities()
            res.set_ptr(entities.ptr)
            return res

    property material:
        def __get__(self):
            cdef SUDrawingElementRef draw_elem = SUGroupToDrawingElement(self.group)
            cdef SUMaterialRef mat
            mat.ptr = <void*> 0
            cdef SU_RESULT res = SUDrawingElementGetMaterial(draw_elem, &mat)
            if res == SU_ERROR_NONE:
                m = Material()
                m.material.ptr = mat.ptr
                return m
            else:
                return None

    property layer:
        def __get__(self):
            cdef SUDrawingElementRef draw_elem = SUGroupToDrawingElement(self.group)
            cdef SULayerRef lay
            lay.ptr = <void*> 0
            cdef SU_RESULT res = SUDrawingElementGetLayer(draw_elem, &lay)
            if res == SU_ERROR_NONE:
                l = Layer(__skip_init=True)
                l.layer.ptr = lay.ptr
                return l
            else:
                return None

    property hidden:
        def __get__(self):
            cdef SUDrawingElementRef draw_elem = SUGroupToDrawingElement(self.group)
            cdef bool hide_flag = False
            check_result(SUDrawingElementGetHidden(draw_elem, &hide_flag))
            return hide_flag

    def __repr__(self):
        return "Group {} \n\ttransform {}".format(self.name, self.transform)

cdef class Face:
    cdef SUFaceRef face_ref
    cdef double s_scale
    cdef double t_scale

    def __cinit__(self):
        self.face_ref.ptr = <void*> 0
        self.s_scale = 1.0
        self.t_scale = 1.0

    @staticmethod
    def create():
        cdef SUPoint3D[4] vl = [
            [0, 0, 0],
            [100, 100, 0],
            [100, 100, 100],
            [0, 0, 100]]

        cdef SULoopInputRef outer_loop
        outer_loop.ptr = <void*> 0
        check_result(SULoopInputCreate(&outer_loop))
        for i in range(4):
            check_result(SULoopInputAddVertexIndex(outer_loop, i))

        res = Face()
        check_result(SUFaceCreate(&(res.face_ref), vl, &outer_loop))
        print("Face {}".format(<size_t> res.face_ref.ptr))
        return res

    @staticmethod
    def create_simple(list vertices):
        cdef size_t face_len = len(vertices)
        cdef SUPoint3D *vl = <SUPoint3D*> malloc(sizeof(SUPoint3D) * face_len)
        for i, vert in enumerate(vertices):
            if len(vert) != 3:
                raise ValueError('Vertices should have 3 coordinates')
            vl[i].x = float(vert[0])
            vl[i].y = float(vert[1])
            vl[i].z = float(vert[2])

        res = Face()
        check_result(SUFaceCreateSimple(&(res.face_ref), vl, face_len))
        return res

    property st_scale:
        def __set__(self, v):
            self.s_scale = v[0]
            self.t_scale = v[1]

        def __get__(self):
            return self.s_scale, self.t_scale

    property tessfaces:
        def __get__(self):
            cdef double z
            cdef SUMeshHelperRef mesh_ref
            mesh_ref.ptr = <void*> 0
            check_result(SUMeshHelperCreate(&mesh_ref, self.face_ref))
            cdef size_t triangle_count = 0
            cdef size_t vertex_count = 0
            check_result(SUMeshHelperGetNumTriangles(mesh_ref, &triangle_count))
            check_result(SUMeshHelperGetNumVertices(mesh_ref, &vertex_count))
            cdef size_t*indices = <size_t*> malloc(triangle_count * 3 * sizeof(size_t))
            cdef size_t index_count = 0
            check_result(SUMeshHelperGetVertexIndices(mesh_ref, triangle_count * 3, indices, &index_count))
            cdef size_t got_vertex_count = 0
            cdef SUPoint3D*vertices = <SUPoint3D*> malloc(sizeof(SUPoint3D) * vertex_count)
            check_result(SUMeshHelperGetVertices(mesh_ref, vertex_count, vertices, &got_vertex_count))
            cdef SUPoint3D*stq = <SUPoint3D*> malloc(sizeof(SUPoint3D) * vertex_count)
            cdef size_t got_stq_count = 0
            check_result(SUMeshHelperGetFrontSTQCoords(mesh_ref, vertex_count, stq, &got_stq_count))

            vertices_list = []
            uv_list = []
            for i in range(got_vertex_count):
                ind = int(i)
                vertices_list.append((m(vertices[ind].x), m(vertices[ind].y), m(vertices[ind].z)))
            for i in range(got_stq_count):
                q = stq[i].z
                if abs(q) < 1e-6: q = 1.0
                uv_list.append(((stq[i].x / q) * self.s_scale, 
                                (stq[i].y / q) * self.t_scale))
            triangles_list = []
            for ii in range(index_count // 3):
                ind = int(ii * 3)
                triangles_list.append((indices[ind], indices[ind + 1], indices[ind + 2]))
            free(vertices)
            free(stq)
            free(indices)
            SUMeshHelperRelease(&mesh_ref)
            return (vertices_list, triangles_list, uv_list)

    property edges:
        def __get__(self):
            cdef size_t edge_count = 0
            check_result(SUFaceGetNumEdges(self.face_ref, &edge_count))
            cdef SUEdgeRef*edges_array = <SUEdgeRef*>malloc(sizeof(SUEdgeRef) * edge_count)
            cdef size_t count = 0
            check_result(SUFaceGetEdges(self.face_ref, edge_count, edges_array, &count))
            
            edges_list = []

            for i in range(count):
                e = Edge()
                e.edge.ptr = edges_array[i].ptr
                edges_list.append(e)

            free(edges_array)
            return edges_list

    property material:
        def __get__(self):
            cdef SUMaterialRef mat
            mat.ptr = <void*> 0
            cdef SU_RESULT res = SUFaceGetFrontMaterial(self.face_ref, &mat)
            if res == SU_ERROR_NONE:
                m = Material()
                m.material.ptr = mat.ptr
                return m
            return None

    property back_material:
        def __get__(self):
            cdef SUMaterialRef mat
            mat.ptr = <void*> 0
            cdef SU_RESULT res = SUFaceGetBackMaterial(self.face_ref, &mat)
            if res == SU_ERROR_NONE:
                m = Material()
                m.material.ptr = mat.ptr
                return m
            return None

    property layer_name:
        def __get__(self):
            cdef SULayerRef layer
            layer.ptr = <void*> 0
            cdef SUDrawingElementRef draw_elem = SUFaceToDrawingElement(self.face_ref)
            cdef SU_RESULT res = SUDrawingElementGetLayer(draw_elem, &layer)
            if res == SU_ERROR_NONE:
                l = Layer(__skip_init=True)
                l.layer.ptr = layer.ptr
                return l.name
            return None

    property loops:
        def __get__(self):
            cdef SULoopRef loop
            loop.ptr = <void*> 0
            check_result(SUFaceGetOuterLoop(self.face_ref, &loop))
            outer = Loop()
            outer.loop.ptr = loop.ptr
            
            cdef size_t num_inner = 0
            check_result(SUFaceGetNumInnerLoops(self.face_ref, &num_inner))
            inners = []
            cdef SULoopRef* loops_array
            if num_inner > 0:
                loops_array = <SULoopRef*> malloc(sizeof(SULoopRef) * num_inner)
                check_result(SUFaceGetInnerLoops(self.face_ref, num_inner, loops_array, &num_inner))
                for i in range(num_inner):
                    res = Loop()
                    res.loop.ptr = loops_array[i].ptr
                    inners.append(res)
                free(loops_array)
            return outer, inners

    def __repr__(self):
        return "SUFaceRef 0x%0.16X" % <size_t> self.face_ref.ptr

cdef class Entities:
    cdef SUEntitiesRef entities

    def __cinit__(self):
        self.entities.ptr = <void*> 0

    def get_version(self):
        return "2.1-Professional-BMesh"

    cdef set_ptr(self, void* ptr):
        self.entities.ptr = ptr

    property handle:
        def __get__(self):
            return f"0x{<size_t>self.entities.ptr:x}"

    def NumFaces(self):
        cdef size_t count = 0
        check_result(SUEntitiesGetNumFaces(self.entities, &count))
        return count

    def NumCurves(self):
        cdef size_t count = 0
        check_result(SUEntitiesGetNumCurves(self.entities, &count))
        return count

    def NumGuidePoints(self):
        cdef size_t count = 0
        check_result(SUEntitiesGetNumGuidePoints(self.entities, &count))
        return count

    def NumEdges(self, bool standalone_only=False):
        cdef size_t count = 0
        check_result(SUEntitiesGetNumEdges(self.entities, standalone_only, &count))
        return count

    def NumPolyline3ds(self):
        cdef size_t count = 0
        check_result(SUEntitiesGetNumPolyline3ds(self.entities, &count))
        return count

    def NumGroups(self):
        cdef size_t count = 0
        check_result(SUEntitiesGetNumGroups(self.entities, &count))
        return count

    def NumImages(self):
        cdef size_t count = 0
        check_result(SUEntitiesGetNumImages(self.entities, &count))
        return count

    def NumInstances(self):
        cdef size_t count = 0
        check_result(SUEntitiesGetNumInstances(self.entities, &count))
        return count

    property faces:
        def __get__(self):
            cdef size_t len = 0
            check_result(SUEntitiesGetNumFaces(self.entities, &len))
            cdef SUFaceRef*faces_array = <SUFaceRef*> malloc(sizeof(SUFaceRef) * len)
            cdef size_t count = 0
            check_result(SUEntitiesGetFaces(self.entities, len, faces_array, &count))
            for i in range(count):
                res = Face()
                res.face_ref.ptr = faces_array[i].ptr
                yield res
            free(faces_array)

    property standalone_edges:
        def __get__(self):
            cdef size_t num_edges = 0
            check_result(SUEntitiesGetNumEdges(self.entities, True, &num_edges))
            cdef SUEdgeRef* edges_array = <SUEdgeRef*> malloc(sizeof(SUEdgeRef) * num_edges)
            cdef size_t count = 0
            check_result(SUEntitiesGetEdges(self.entities, True, num_edges, edges_array, &count))
            for i in range(count):
                e = Edge()
                e.edge.ptr = edges_array[i].ptr
                yield e
            free(edges_array)

    def get_textured_ngon_lists(self, default_material, material_scales=None):
        verts = []
        faces_data = [] # List of dicts with detailed face info
        mats = {}
        seen = {}

        cdef Face face_item
        cdef Material mat_item
        cdef Material back_mat_item
        cdef Texture tex_item
        cdef SUMeshHelperRef mesh_ref
        cdef size_t tri_count = 0
        cdef size_t v_count = 0
        cdef size_t got_v = 0
        cdef size_t got_stq = 0
        cdef size_t* tri_indices = NULL
        cdef SUPoint3D* mesh_verts = NULL
        cdef SUPoint3D* mesh_stq_front = NULL
        cdef SUPoint3D* mesh_stq_back = NULL
        cdef double s_scale, t_scale, q
        cdef size_t t, k

        for face in self.faces:
            face_item = face

            # Front Material
            # FIX: STQ/Q already gives correct tile-space UV for faces with a
            # direct material. Only faces inheriting material from a parent
            # group/component need s/t scale multiplication (SketchUp docs:
            # SUTextureGetDimensions scale is only useful for inherited mats).
            mat_item = face_item.material
            s_scale = 1.0
            t_scale = 1.0
            if mat_item:
                mat_name = mat_item.name
                if mat_name not in mats: mats[mat_name] = len(mats)
                mat_number = mats[mat_name]
                s_scale = 1.0
                t_scale = 1.0
            else:
                mat_name = default_material
                if mat_name not in mats: mats[mat_name] = len(mats)
                mat_number = mats[mat_name]
                if material_scales is not None and mat_name in material_scales:
                    try:
                        sc = material_scales.get(mat_name)
                        s_scale = float(sc[0])
                        t_scale = float(sc[1])
                        if abs(s_scale) < 0.0001: s_scale = 1.0
                        if abs(t_scale) < 0.0001: t_scale = 1.0
                    except Exception:
                        s_scale = 1.0
                        t_scale = 1.0
                else:
                    s_scale = 1.0
                    t_scale = 1.0

            # Back Material
            back_mat_item = face_item.back_material
            back_mat_number = -1
            if back_mat_item:
                back_mat_name = back_mat_item.name
                if back_mat_name not in mats: mats[back_mat_name] = len(mats)
                back_mat_number = mats[back_mat_name]

            layer_name = face_item.layer_name

            mesh_ref.ptr = <void*> 0
            check_result(SUMeshHelperCreate(&mesh_ref, face_item.face_ref))
            check_result(SUMeshHelperGetNumTriangles(mesh_ref, &tri_count))
            check_result(SUMeshHelperGetNumVertices(mesh_ref, &v_count))
            
            if tri_count == 0:
                SUMeshHelperRelease(&mesh_ref)
                continue
            
            try:
                tri_indices = <size_t*> malloc(tri_count * 3 * sizeof(size_t))
                mesh_verts = <SUPoint3D*> malloc(v_count * sizeof(SUPoint3D))
                mesh_stq_front = <SUPoint3D*> malloc(v_count * sizeof(SUPoint3D))
                mesh_stq_back = <SUPoint3D*> malloc(v_count * sizeof(SUPoint3D))
                
                check_result(SUMeshHelperGetVertexIndices(mesh_ref, tri_count * 3, tri_indices, &got_v))
                check_result(SUMeshHelperGetVertices(mesh_ref, v_count, mesh_verts, &got_v))
                check_result(SUMeshHelperGetFrontSTQCoords(mesh_ref, v_count, mesh_stq_front, &got_stq))
                check_result(SUMeshHelperGetBackSTQCoords(mesh_ref, v_count, mesh_stq_back, &got_stq))
                
                face_tri_loops = []
                face_front_uvs = []
                face_back_uvs = []
                
                for t in range(tri_count):
                    tri_indices_list = []
                    tri_uvs_front = []
                    tri_uvs_back = []
                    for k in range(3):
                        v_idx = tri_indices[t * 3 + k]
                        pos = (round(m(mesh_verts[v_idx].x), 6), 
                               round(m(mesh_verts[v_idx].y), 6), 
                               round(m(mesh_verts[v_idx].z), 6))
                        
                        if pos not in seen:
                            seen[pos] = len(seen)
                            verts.append(pos)
                        tri_indices_list.append(seen[pos])
                        
                        # Front UVs - STQ to normalized UV conversion (No inch-to-meter here!)
                        q = mesh_stq_front[v_idx].z
                        if abs(q) < 1e-6: q = 1.0
                        tri_uvs_front.append((round((mesh_stq_front[v_idx].x / q) * s_scale, 6), 
                                              round((mesh_stq_front[v_idx].y / q) * t_scale, 6)))
                                              
                        # Back UVs - STQ to normalized UV conversion (No inch-to-meter here!)
                        q = mesh_stq_back[v_idx].z
                        if abs(q) < 1e-6: q = 1.0
                        tri_uvs_back.append((round((mesh_stq_back[v_idx].x / q) * s_scale, 6), 
                                             round((mesh_stq_back[v_idx].y / q) * t_scale, 6)))
                    
                    face_tri_loops.append(tri_indices_list)
                    face_front_uvs.append(tri_uvs_front)
                    face_back_uvs.append(tri_uvs_back)
                    
                faces_data.append({
                    'mat_idx': mat_number,
                    'back_mat_idx': back_mat_number,
                    'layer_name': layer_name,
                    'loops': face_tri_loops,
                    'front_uvs': face_front_uvs,
                    'back_uvs': face_back_uvs
                })
            finally:
                if tri_indices: free(tri_indices)
                if mesh_verts: free(mesh_verts)
                if mesh_stq_front: free(mesh_stq_front)
                if mesh_stq_back: free(mesh_stq_back)
                SUMeshHelperRelease(&mesh_ref)
            
        return verts, faces_data, mats

    def get__triangles_lists(self, default_material):
        verts = []
        faces = []
        mat_index = []
        mats = {}
        seen = {}
        uv_list = []
        alpha = False  # We assume object does not need alpha flag
        uvs_used = False  # We assume no uvs need to be added

        for f in self.faces:
            vs, tri, uvs = f.triangles

            if f.material:
                mat_name = f.material.name
                if mat_name not in mats:
                    mats[mat_name] = len(mats)
                mat_number = mats[mat_name]
            else:
                mat_name = default_material
                if mat_name not in mats:
                    mats[mat_name] = len(mats)
                mat_number = mats[mat_name]

            mapping = {}
            for i, (v, uv) in enumerate(zip(vs, uvs)):
                if v not in seen:
                    seen[v] = len(seen)
                    verts.append(v)
                mapping[i] = seen[v]
                uvs.append(uv)

            for face in tri:
                f0, f1, f2 = face[0], face[1], face[2]
                if f2 == 0:  ## eeekadoodle dance
                    faces.append((mapping[f1], mapping[f2], mapping[f0]))
                    uv_list.append((uvs[f2][0], uvs[f2][1],
                                    uvs[f1][0], uvs[f1][1],
                                    uvs[f0][0], uvs[f0][1],
                                    0, 0))
                else:
                    faces.append((mapping[f0], mapping[f1], mapping[f2]))
                    uv_list.append((uvs[f0][0], uvs[f0][1],
                                    uvs[f1][0], uvs[f1][1],
                                    uvs[f2][0], uvs[f2][1],
                                    0, 0))
                mat_index.append(mat_number)
        return verts, faces, uv_list, mat_index, mats

    property groups:
        def __get__(self):
            cdef size_t num_groups = 0
            check_result(SUEntitiesGetNumGroups(self.entities, &num_groups))
            cdef SUGroupRef*groups = <SUGroupRef*> malloc(sizeof(SUGroupRef) * num_groups)
            cdef size_t count = 0
            check_result(SUEntitiesGetGroups(self.entities, num_groups, groups, &count))
            for i in range(count):
                res = Group()
                res.group.ptr = groups[i].ptr
                yield res
            free(groups)

    property instances:
        def __get__(self):
            cdef size_t num_instances = 0
            check_result(SUEntitiesGetNumInstances(self.entities, &num_instances))
            cdef SUComponentInstanceRef*instances = <SUComponentInstanceRef*> malloc(
                sizeof(SUComponentInstanceRef) * num_instances)
            cdef size_t count = 0
            check_result(SUEntitiesGetInstances(self.entities, num_instances, instances, &count))
            for i in range(count):
                yield instance_from_ptr(instances[i])
            free(instances)

    def addFace(self, Face face):
        check_result(SUEntitiesAddFaces(self.entities, 1, &face.face_ref))

    def __repr__(self):
        return "<sketchup.Entities at {}> groups {} instances {}".format(hex(<size_t> &self.entities),
                                                                         self.NumGroups(), self.NumInstances())

cdef class Material:
    cdef SUMaterialRef material

    def __cinit__(self):
        self.material.ptr = <void*> 0

    property name:
        def __get__(self):
            cdef SUStringRef n
            n.ptr = <void*> 0
            SUStringCreate(&n)
            check_result(SUMaterialGetName(self.material, &n))
            return StringRef2Py(n)

    property color:
        def __get__(self):
            cdef SUColor c
            check_result(SUMaterialGetColor(self.material, &c))
            return (c.red, c.green, c.blue, c.alpha)

    property opacity:
        def __get__(self):
            cdef double alpha
            check_result(SUMaterialGetOpacity(self.material, &alpha))
            return alpha

        def __set__(self, double alpha):
            check_result(SUMaterialSetOpacity(self.material, alpha))

    property texture:
        def __get__(self):
            cdef SUTextureRef t
            t.ptr = <void*> 0
            cdef SU_RESULT res = SUMaterialGetTexture(self.material, &t)
            if res == SU_ERROR_NONE:
                tex = Texture()
                tex.tex_ref.ptr = t.ptr
                return tex
            else:
                return False

cdef class RenderingOptions:
    cdef SURenderingOptionsRef options

    def __cinit__(self):
        self.options.ptr = <void*> 0

cdef class Scene:
    cdef SUSceneRef scene

    def __cinit__(self):
        self.scene.ptr = <void*> 0

    property name:
        def __get__(self):
            cdef SUStringRef n
            n.ptr = <void*> 0
            try:
                SUStringCreate(&n)
                check_result(SUSceneGetName(self.scene, &n))
                return StringRef2Py(n)
            finally:
                release_string_ref(&n)

    property camera:
        def __get__(self):
            cdef SUCameraRef c
            c.ptr = <void*> 0
            check_result(SUSceneGetCamera(self.scene, &c))
            res = Camera()
            res.set_ptr(c.ptr)
            return res

    property rendering_options:
        def __get__(self):
            cdef SURenderingOptionsRef options
            options.ptr = <void*> 0
            check_result(SUSceneGetRenderingOptions(self.scene, &options))
            res = RenderingOptions()
            res.options = options
            return res

    property entity:
        def __get__(self):
            res = Entity()
            res.entity = SUSceneToEntity(self.scene)
            return res

    property layers:
        def __get__(self):
            cdef size_t num_layers
            check_result(SUSceneGetNumLayers(self.scene, &num_layers))
            cdef SULayerRef*layers_array = <SULayerRef*> malloc(sizeof(SULayerRef) * num_layers)
            for i in range(num_layers):
                layers_array[i].ptr = <void*> 0
            cdef size_t count = 0
            check_result(SUSceneGetLayers(self.scene, num_layers, layers_array, &count))
            for i in range(count):
                l = Layer(__skip_init=True)
                l.layer.ptr = layers_array[i].ptr
                yield l
            free(layers_array)

cdef class LoopInput:
    cdef SULoopInputRef loop

    def __cinit__(self, **kwargs):
        self.loop.ptr = <void*> 0
        if not '__skip_init' in kwargs:
            check_result(SULoopInputCreate(&(self.loop)))

    def AddVertexIndex(self, i):
        check_result(SULoopInputAddVertexIndex(self.loop, i))

cdef class Model:
    cdef SUModelRef model

    def __cinit__(self, **kwargs):
        self.model.ptr = <void*> 0
        SUInitialize()
        if not '__skip_init' in kwargs:
            check_result(SUModelCreate(&(self.model)))

    @staticmethod
    def from_file(filename):
        if isinstance(filename, str) and "\x00" in filename:
            raise ValueError("Invalid filename: embedded NUL character")
        res = Model(__skip_init=True)
        py_byte_string = filename.encode('UTF-8')
        cdef const char* f = py_byte_string
        cdef SUModelLoadStatus status = SUModelLoadStatus_Success
        cdef SU_RESULT result = SUModelCreateFromFileWithStatus(&(res.model), f, &status)
        if result != SU_ERROR_NONE:
            raise RuntimeError("Sketchup library giving unexpected results {}".format(__str_from_SU_RESULT(result)))
        if status != SUModelLoadStatus_Success:
            print("SU | WARNING: Model was saved by a newer SketchUp version; some data may be omitted.")
        return res

    def save(self, filename):
        py_byte_string = filename.encode('UTF-8')
        cdef const char* f = py_byte_string
        check_result(SUModelSaveToFile(self.model, f))
        return True

    def __dealloc__(self):
        self.close()

    def close(self):
        if self.model.ptr:
            SUModelRelease(&self.model)
            self.model.ptr = <void*> 0
            SUTerminate()

    def NumMaterials(self):
        cdef size_t count = 0
        check_result(SUModelGetNumMaterials(self.model, &count))
        return count

    def NumComponentDefinitions(self):
        cdef size_t count = 0
        check_result(SUModelGetNumComponentDefinitions(self.model, &count))
        return count

    def NumScenes(self):
        cdef size_t count = 0
        check_result(SUModelGetNumScenes(self.model, &count))
        return count

    def NumLayers(self):
        cdef size_t count = 0
        check_result(SUModelGetNumLayers(self.model, &count))
        return count

    def NumAttributeDictionaries(self):
        cdef size_t count = 0
        check_result(SUModelGetNumAttributeDictionaries(self.model, &count))
        return count

    property units:
        def __get__(self):
            cdef SUModelUnits u
            check_result(SUModelGetUnits(self.model, &u))
            return <int>u

    property camera:
        def __get__(self):
            cdef SUCameraRef c
            c.ptr = <void*> 0
            check_result(SUModelGetCamera(self.model, &c))
            res = Camera()
            res.set_ptr(c.ptr)
            return res

    property entities:
        def __get__(self):
            cdef SUEntitiesRef entities
            entities.ptr = <void*> 0
            check_result(SUModelGetEntities(self.model, &entities))
            res = Entities()
            res.set_ptr(entities.ptr)
            return res

    property materials:
        def __get__(self):
            cdef size_t num_materials = 0
            check_result(SUModelGetNumMaterials(self.model, &num_materials))
            cdef SUMaterialRef*materials = <SUMaterialRef*> malloc(sizeof(SUMaterialRef) * num_materials)
            cdef size_t count = 0
            check_result(SUModelGetMaterials(self.model, num_materials, materials, &count))
            for i in range(count):
                m = Material()
                m.material.ptr = materials[i].ptr
                yield m
            free(materials)

    property component_definitions:
        def __get__(self):
            cdef size_t num_component_defs = 0
            check_result(SUModelGetNumComponentDefinitions(self.model, &num_component_defs))
            cdef SUComponentDefinitionRef*components = <SUComponentDefinitionRef*> malloc(
                sizeof(SUComponentDefinitionRef) * num_component_defs)
            cdef size_t count = 0
            check_result(SUModelGetComponentDefinitions(self.model, num_component_defs, components, &count))
            for i in range(count):
                c = Component()
                c.comp_def.ptr = components[i].ptr
                yield c
            free(components)

    property scenes:
        def __get__(self):
            cdef size_t num_scenes = 0
            check_result(SUModelGetNumScenes(self.model, &num_scenes))
            cdef SUSceneRef*scenes_array = <SUSceneRef*> malloc(sizeof(SUSceneRef) * num_scenes)
            for i in range(num_scenes):
                scenes_array[i].ptr = <void*> 0
            cdef size_t count = 0
            check_result(SUModelGetScenes(self.model, num_scenes, scenes_array, &count))
            for i in range(count):
                s = Scene()
                s.scene.ptr = scenes_array[i].ptr
                yield s
            free(scenes_array)

    property component_definition_as_dict:
        def __get__(self):
            res = {}
            for c in self.component_definitions:
                res[c.name] = c
            return res

    property layers:
        def __get__(self):
            cdef size_t num_layers = 0
            check_result(SUModelGetNumLayers(self.model, &num_layers))
            cdef SULayerRef*layers_array = <SULayerRef*> malloc(sizeof(SULayerRef) * num_layers)
            for i in range(num_layers):
                layers_array[i].ptr = <void*> 0
            cdef size_t count = 0
            check_result(SUModelGetLayers(self.model, num_layers, layers_array, &count))
            for i in range(count):
                l = Layer(__skip_init=True)
                l.layer.ptr = layers_array[i].ptr
                yield l
            free(layers_array)

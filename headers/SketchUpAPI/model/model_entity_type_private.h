/**
 * @file
 * @brief Definition for \ref SUEntityType. Don't include directly.
 *
 * @warning Do not include this header directly. This file is part of a
 *   compatibility shim. Instead include `SketchUpAPI/model.h`.
 */

/**
@enum SUEntityType
@headerfile <SketchUpAPI/model.h>
@brief Types of \ref SUEntityRef objects.

@see SUModelStatistics

@bug This enum was incorrectly defined inside the \ref SUModelStatistics struct. This is
  not valid C. As of SketchUp 2025.0 (API 13.0), this enum is conditionally defined outside
  of the struct when the header is consumed by a C compiler.

@code
// Usage from a C compiler:
SUModelStatistics statistics;
SUModelGetStatistics(model, &statistics);
std::cout << "Faces: " << statistics.entity_counts[SUEntityType_Face] << "\n";
@endcode

@code
// Usage from a C++ compiler:
SUModelStatistics statistics;
SUModelGetStatistics(model, &statistics);
std::cout << "Faces: " << statistics.entity_counts[SUModelStatistics::SUEntityType_Face] << "\n";
@endcode
*/
enum SUEntityType {
  SUEntityType_Edge = 0,             ///< SUEdgeRef entities
  SUEntityType_Face,                 ///< SUFaceRef entities
  SUEntityType_ComponentInstance,    ///< SUComponentInstanceRef entities
  SUEntityType_Group,                ///< SUGroupRef entities
  SUEntityType_Image,                ///< SUImageRef entities
  SUEntityType_ComponentDefinition,  ///< SUComponentDefinitionRef entities
  SUEntityType_Layer,                ///< SULayerRef entities
  SUEntityType_Material,             ///< SUMaterialRef entities
  SUNumEntityTypes                   ///< Number of entity types
};

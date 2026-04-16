// Copyright 2022 Trimble Inc. All rights reserved.
// This file is intended for public distribution.

#ifndef LAYOUT_MODEL_SELECTIONSET_H_
#define LAYOUT_MODEL_SELECTIONSET_H_

#include <LayOutAPI/common.h>
#include <LayOutAPI/model/defs.h>

/**
@struct LOSelectionSetRef
@brief References a selection set. A selection set tracks the current selection
       in a \ref LODocumentRef.
@since LayOut 2023.1, API 8.1
*/

#ifdef __cplusplus
extern "C" {
#endif

/**
@brief Selects the entity, adding it to the current selection set.
@since LayOut 2023.1, API 8.1
@param[in] selection_set The selection set object.
@param[in] entity        The entity to add to the current selection.
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p selection_set or \p entity is an invalid object
*/
LO_RESULT LOSelectionSetAddEntity(LOSelectionSetRef selection_set, LOEntityRef entity);

/**
@brief Selects the entities, adding them to the current selection set.
@since LayOut 2023.1, API 8.1
@param[in] selection_set The selection set object.
@param[in] entities      The entities to add to the current selection.
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p selection_set or \p entities is an invalid object
*/
LO_RESULT LOSelectionSetAddEntities(LOSelectionSetRef selection_set, LOEntityListRef entities);

/**
@brief Selects the entity, replacing the current selection set.
@since LayOut 2023.1, API 8.1
@param[in] selection_set The selection set object.
@param[in] entity        The entity to set as the current selection.
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p selection_set or \p entity is an invalid object
*/
LO_RESULT LOSelectionSetSelectEntity(LOSelectionSetRef selection_set, LOEntityRef entity);

/**
@brief Selects the entities, replacing the current selection set.
@since LayOut 2023.1, API 8.1
@param[in] selection_set The selection set object.
@param[in] entities      The entities to set as the current selection.
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if selection_set or entities is an invalid object
*/
LO_RESULT LOSelectionSetSelectEntities(LOSelectionSetRef selection_set, LOEntityListRef entities);

/**
@brief Removes the entity from the current selection set.
@since LayOut 2023.1, API 8.1
@param[in] selection_set The selection set object.
@param[in] entity        The entity to remove from the current selection.
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p selection_set or \p entity is an invalid object
*/
LO_RESULT LOSelectionSetRemoveEntity(LOSelectionSetRef selection_set, LOEntityRef entity);

/**
@brief Removes the entities from the current selection set.
@since LayOut 2023.1, API 8.1
@param[in] selection_set The selection set object.
@param[in] entities      The entities to remove from the current selection.
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p selection_set or \p entities is an invalid object
*/
LO_RESULT LOSelectionSetRemoveEntities(LOSelectionSetRef selection_set, LOEntityListRef entities);

/**
@brief Removes all entities from the selection set.
@since LayOut 2023.1, API 8.1
@param[in] selection_set The selection set object.
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p selection_set is an invalid object
*/
LO_RESULT LOSelectionSetClear(LOSelectionSetRef selection_set);

/**
@brief Gets the number of entities in the selection set.
@since LayOut 2023.1, API 8.1
@param[in]  selection_set The selection set object.
@param[out] num_entities  The number of entities in the selection set.
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p selection_set is an invalid object
- \ref SU_ERROR_NULL_POINTER_OUTPUT if \p num_entities is NULL
*/
LO_RESULT LOSelectionSetGetNumberOfEntities(LOSelectionSetRef selection_set, size_t* num_entities);

/**
@brief Gets the entity at the specified index in a selection set object.
@since LayOut 2023.1, API 8.1
@param[in]  selection_set The selection set object.
@param[in]  index         The index of the entity to get.
@param[out] entity        The entity object.
@return
- \ref SU_ERROR_NONE on success
- \ref SU_ERROR_INVALID_INPUT if \p selection_set does not refer to a valid object
- \ref SU_ERROR_OUT_OF_RANGE if \p index is out of range for the selection set
- \ref SU_ERROR_NULL_POINTER_OUTPUT if \p entity is NULL
- \ref SU_ERROR_OVERWRITE_VALID if *entity already refers to a valid object
*/
LO_RESULT LOSelectionSetGetEntityAtIndex(
    LOSelectionSetRef selection_set, size_t index, LOEntityRef* entity);

#ifdef __cplusplus
}  // extern "C" {
#endif

#endif  // LAYOUT_MODEL_SELECTIONSET_H_

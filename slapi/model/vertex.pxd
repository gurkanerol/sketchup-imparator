# -*- coding: utf-8 -*-
from slapi.model.defs cimport *
from slapi.geometry cimport *

cdef extern from "SketchUpAPI/model/vertex.h":
    SU_RESULT SUVertexGetPosition(SUVertexRef vertex, SUPoint3D* position)
    SU_RESULT SUVertexGetNumEdges(SUVertexRef vertex, size_t* count)
    SU_RESULT SUVertexGetEdges(SUVertexRef vertex, size_t len, SUEdgeRef edges[], size_t* count)

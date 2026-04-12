# -*- coding: utf-8 -*-
from slapi.model.defs cimport *
from slapi.geometry cimport *

cdef extern from "SketchUpAPI/model/loop.h":
    SU_RESULT SULoopGetNumVertices(SULoopRef loop, size_t* count)
    SU_RESULT SULoopGetVertices(SULoopRef loop, size_t len, SUVertexRef vertices[], size_t* count)
    SU_RESULT SULoopGetEdges(SULoopRef loop, size_t len, SUEdgeRef edges[], size_t* count)

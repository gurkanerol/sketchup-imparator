# <pep8-80 compliant>
# -*- coding: utf-8 -*-

__author__ = "Martijn Berger"

import platform
from distutils.core import setup
from distutils.extension import Extension

from Cython.Distutils import build_ext

if platform.system() == "Linux":
    libraries = ["SketchUpAPI"]
    extra_compile_args = []
    extra_link_args = ["-Lbinaries/sketchup/x86-64"]

elif platform.system() == "Darwin":  # OS X
    libraries = []
    extra_compile_args = ["-mmacosx-version-min=11.0", "-F."]
    extra_link_args = [
        "-mmacosx-version-min=11.0",
        "-F",
        ".",
        "-framework",
        "SketchUpAPI",
    ]

else:
    libraries = ["SketchUpAPI"]
    extra_compile_args = ["/Zp8"]
    extra_link_args = ["/LIBPATH:binaries/sketchup/x64/"]

import sysconfig

include_dirs = ["headers"]
py_include = sysconfig.get_path("include")
if py_include:
    include_dirs.append(py_include)

# Python Stable ABI (ABI3) Configuration
min_python_version = 0x030B0000  # Target Python 3.11+

ext_modules = [
    Extension(
        "sketchup",
        ["sketchup.pyx"],
        language="c++",
        include_dirs=include_dirs,
        libraries=libraries,
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
        define_macros=[("Py_LIMITED_API", min_python_version)],
        py_limited_api=True,
    )
]

for e in ext_modules:
    e.cython_directives = {"language_level": "3"}  # all are Python-3

setup(name="Sketchup", cmdclass={"build_ext": build_ext}, ext_modules=ext_modules)

# install_name_tool -change "@rpath/SketchUpAPI.framework/Versions/Current/SketchUpAPI" "@loader_path/SketchUpAPI.framework/Versions/Current/SketchUpAPI" sketchup.so
# install_name_tool -change "@rpath/SketchUpAPI.framework/Versions/A/SketchUpAPI" "@loader_path/SketchUpAPI.framework/Versions/A/SketchUpAPI" sketchup.cpython-35m-darwin.so

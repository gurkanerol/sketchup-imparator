"""Vendored third-party package: openskp, imported as part of the add-on.

It is never put on ``sys.path``: Blender's extension policy forbids making an
extension's own directory importable as top-level modules.  openskp's own
third-party needs (``defusedxml``, ``mapbox_earcut``) are met with wheels,
and ``shapely`` with :mod:`shapely_fallback`.
"""

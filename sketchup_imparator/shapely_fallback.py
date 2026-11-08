"""Fallback for ``shapely``, openskp's optional overlapping-hole dependency.

openskp merges genuinely overlapping face holes with shapely before it
triangulates a face that carries two or more holes.  shapely is not shipped
here: it needs GEOS (3 MB of native code per Python ABI) and Blender's
extension policy forbids putting this add-on's own directory on ``sys.path``,
so it cannot be vendored as source either.

When shapely is missing, this module leaves the hole loops exactly as they
are.  That is also what openskp's own union returns for holes that do not
overlap, so the two paths agree everywhere except on files that really do
record overlapping holes - and there earcut still triangulates the input it
is given, which is what the add-on shipped before this fallback existed.

Measured on the reference model: with shapely 2.2.0 and without it, openskp
emits the same 157,840 triangles from the same 141,277 triangulated faces
(11 multi-hole faces, 0 merges).

If shapely *is* importable, openskp keeps its own merge and this module does
nothing.
"""

from __future__ import annotations


def install() -> bool:
    """Let openskp merge holes itself when it can; otherwise keep them as-is."""
    try:
        import shapely  # noqa: F401
    except Exception:  # missing *or* broken: never let it break the import
        pass
    else:
        return False

    from ._vendor.openskp import _core

    if not hasattr(_core, "_merge_overlapping_hole_loops"):
        print(
            "SketchUp Imparator | openskp no longer has "
            "_merge_overlapping_hole_loops: shapely fallback not installed"
        )
        return False

    _core._merge_overlapping_hole_loops = _keep_hole_loops
    return True


def _keep_hole_loops(loops, *_args, **_kwargs):
    return loops

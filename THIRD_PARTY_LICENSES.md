# Third-party components

SketchUp Imparator is GPL-3.0-or-later. It bundles or installs the following
third-party components.

## OpenSKP 1.5.0 — MIT

Vendored under `_vendor/openskp/` (full licence: `_vendor/openskp/LICENSE`),
byte-for-byte the upstream PyPI release - no file in it is modified.
Clean-room SketchUp `.skp` parser. https://github.com/iamahsanmehmood/openskp

    MIT License

    Copyright (c) 2024-2026 Ahsan Mehmood

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

## defusedxml 0.7.1 — PSF-2.0

Installed as a wheel from `wheels/` (its upstream PyPI wheel
`defusedxml-0.7.1-py2.py3-none-any.whl`); licence:
https://github.com/tiran/defusedxml/blob/main/LICENSE
Hardened XML parsing, imported by OpenSKP.

## shapely — NOT bundled

OpenSKP can use `shapely` to merge overlapping hole loops. The Blender
extension deliberately does not ship it (the two wheels add 3.0 MB and they
bundle GEOS): `shapely_fallback.py` leaves those loops alone instead, so
holes go to `mapbox_earcut` unchanged - which is what openskp's own union
returns for disjoint holes, and what a measurement on the reference model
confirms (157,840 triangles with shapely 2.2.0 and without it). Users who
install `shapely` themselves get the union path back.

## mapbox_earcut 2.1.0 — ISC

Installed as a wheel from `wheels/`. Ear-clipping triangulation for concave
faces. Copyright (c) 2018 Samuel Kogler.

    Permission to use, copy, modify, and/or distribute this software for any
    purpose with or without fee is hereby granted, provided that the above
    copyright notice and this permission notice appear in all copies.

    THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
    WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
    MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
    SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
    WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION
    OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
    CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

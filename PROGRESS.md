# Sürüm Notları

## 2026.7.0 — SDK'sız sürüm

`SketchUpAPI.framework` bağımlılığı tamamen kaldırıldı. Ayrıştırma artık
gömülü OpenSKP 1.5.0 (MIT, saf Python) ile yapılıyor; eklenti derlenmiş ikili
dosya içermiyor ve Blender uzantısı olarak kuruluyor.

**Geometri**
- `build_instanced_scene`: tanım başına tek mesh, yerleşim başına tek nesne.
  Component origin/rotasyon/ölçek korunur, örnekleme (instancing) gerçek kalır.
- Üçgenleme `mapbox_earcut` ile: delikli ve konkav yüzler doğru.
- SketchUp per-vertex normalleri custom split normal olarak uygulanır.
- Bağımsız kenarlar curve nesnesi; hem yüz hem kenar içeren tanımlarda kenarlar
  mesh nesnesinin altında `(Edges)` olarak korunur.
- Empty yalnızca çocuğu olup geometrisi olmayan düğümler için.

**Materyal ve doku**
- glTF materyalleri Principled BSDF'e çevriliyor; renk, saydamlık,
  colourized doku (Multiply) korunur. Dokular `.blend` içine pack edilir.
- Materyal adları SketchUp adlarıyla eşleştirilir; eşleşmeyen renkler
  `Material_RRGGBB` / `Material_RRGGBB_texN` olarak ayrıştırılır (aynı renkli
  farklı dokular birleşmez).
- Tag'ler koleksiyona, gizlilik durumu viewport + render'a taşınır.

**Blender tarafı**
- Yeni `skp_scene.py`: parse → koleksiyonlar → materyaller → mesh/curve →
  nesneler → kameralar, aşamalı ilerleme raporuyla.
- `SceneImporter` ince bir facade; reload dünya matrisi, materyal slotu,
  desteklenen modifier'lar ve Smooth-by-Angle'ı geri yüklüyor.
- Kenar içe aktarma tercihi koleksiyonda saklanıyor, reload onu koruyor.
- Mesh kurulum sırası: `from_pydata → UV → material → validate → custom normal`.
  `validate()` bozuk (sıfır alanlı) poligonları temizliyor; normal yazımı ondan
  sonraki hale getirildi. Eski sıralamada Blender 5.x'te
  `mesh_normals_corner_custom_set` üzerinde ara sıra segfault çıkıyordu
  (`mesh.validate()` 2 tanımı, 34 poligonu değiştiriyordu).
- SDK'ya bağlı `ExportSKP` operatörü ve `dedub_*` / `max_instance` /
  `reuse_existing_groups` seçenekleri kaldırıldı.

**Paketleme**
- `blender_manifest.toml` (id `sketchup_imparator`, `blender_version_min 4.2.0`,
  `SPDX:GPL-3.0-or-later`, `macos-arm64`), GPL metni, üçüncü taraf lisansları.
- `wheels/`: `defusedxml` 0.7.1 (`py2.py3-none-any`) + `mapbox_earcut`
  2.1.0, cp311 (Blender 4.2-5.0) + cp313 (Blender 5.1+) arm64 — hiçbir
  Blender Python 3.12 kullanmıyor
- **Vendor budaması geri alındı:** `_vendor/openskp/` PyPI `openskp 1.5.0`
  ile birebir aynı (`diff -rq` → yalnız bizim `LICENSE`). `export/`,
  `_fragments_fb/`, `create.py`, `edit.py`, `codegen.py`, `triangulator.py`
  geri yüklendi; `__init__.py` / `_core.py` / `materials.py` yamaları geri
  alındı. Bunların hiçbiri import edilmiyor (doğrulandı) → çalışmaya etkisi yok.
- **Bağımlılıklar vendor dışında karşılanıyor:** `defusedxml` → PyPI wheel
  (`_vendor/defusedxml/` kaynağı kaldırıldı); `shapely` → bizim
  `shapely_fallback.py`, shapely yokken openskp'nin
  `_merge_overlapping_hole_loops` fonksiyonunu delikleri olduğu gibi
  bırakacak şekilde değiştiriyor. Ölçüm: shapely 2.2.0 ile **ve** olmadan
  aynı 157.840 üçgen / 141.277 triangulate / 11 birleştirme çağrısı / 0 gerçek
  birleştirme.
- **Politika düzeltmesi:** `sys.path.insert(_vendor)` kaldırıldı;
  `skp_scene.py` artık `._vendor.openskp` göreli import kullanıyor,
  `_vendor/__init__.py` eklendi. `openskp` yalnızca uzantı paketinin altında,
  `defusedxml` wheel site-packages'tan. Blender 4.2.9 ve 5.2.3'te politika
  ihlali listesi boş.
- `build_addons.py` artık paket kökündeki tüm `.py` dosyalarını kopyalıyor
  (elle tutulan liste değil) — yeni bir modülün zip'e düşmeme riski yok.
- `website` + `[permissions] files` manifest'e eklendi (uzantı platformu
  listelemesi için); `files` değeri 64 karakteri aşamıyor.
- Otomatik reload: `skp_auto_reload` + kalıcı timer, mtime tabanlı.
- `build_addons.py` uzantı düzeninde zip üretiyor (manifest ve paket dosyaları
  arşiv kökünde), sürümü manifestten okuyor.
- `tests/import_smoke.py`: Blender içinde import + reload + proxy + purge +
  delete akışını doğrulayan headless test.

**Doğrulama** (`studio sahne villa.skp`, 80 MB): 23.839 nesne
(19.138 mesh + 4.692 empty + 9 curve), 137 mesh datablock, 54 materyal,
16 packed doku, 446.371 vertex, 162.016 üçgen, dünya alanı 1526.75 m²,
bbox 12.3434 × 16.3728 × 5.7423 m, import ~13 s.

## 2026.6.0.0 — Framework sürümü (legacy)

Son `SketchUpAPI.framework` tabanlı sürüm. Cython binding + gömülü framework
ile çalışır, yalnızca macOS arm64. Arşivde referans olarak duruyor.

## 2026.1 — Modernizasyon

- N-gon hattı: "triangulate + dissolve" ile delikli yüzler.
- UV ölçek düzeltmesi (STQ / `s_scale`, `t_scale`).
- Blender 5.1 / Python 3.13 uyumu, otomatik build.
- Smart Update (non-destructive reload), geometry-based hierarchy, shared mesh
  data (Alt+D).
- Fake User korumalı purge, Deep Purge, kararlı etiketleme.

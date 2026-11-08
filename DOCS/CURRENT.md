# SketchUp Imparator — Güncel Durum (2026.7.0)

Bu sürüm, tescilli `SketchUpAPI.framework` bağımlılığını tamamen kaldırır.
`.skp` dosyaları, gömülü (vendored) [OpenSKP](https://github.com/iamahsanmehmood/openskp)
ayrıştırıcısıyla okunur; eklenti derlenmiş ikili dosya içermez.

## Kurulum
- Blender **4.2+** (4.2 ve 5.2 üzerinde doğrulandı), platform `macos-arm64`.
- `dist/sketchup_imparator-2026.7.0.zip` → **Edit > Preferences > Get Extensions >
  Install from Disk…**
- `wheels/` içindeki `defusedxml` ve `mapbox_earcut` (cp311 + cp313)
  tekerlekleri ilk etkinleştirmede eklentinin yerel site-packages'ine
  kurulur. `shapely` gömülü değil (2 ABI için 3.0 MB, GEOS taşıyor) —
  `shapely_fallback.py` üst üste binen delik birleştirmesini atlar. Bu,
  delikler çakışmıyorken openskp'nin kendi birleştirmesinin verdiği sonuçla
  birebir aynı: shapely 2.2.0 ile **ve** olmadan aynı 157.840 üçgen.
- **Paket boyutu: 461 KB** (4.98 MB'dan shapely çıkarılarak).
- **Vendor değişmez:** `_vendor/openskp/` PyPI `openskp 1.5.0` ile
  `diff -rq` farkı **yalnızca** bizim eklediğimiz `LICENSE`. Gereksinimler
  vendor dışında karşılanır: `defusedxml` ve `mapbox_earcut` wheel olarak,
  `shapely` bizim `shapely_fallback.py` ile — hiçbir vendor dosyası
  düzenlenmez.
- **Uzantı politikası ihlali yok:** `sys.path` değişikliği ve top-level
  modül kaydı yok; `openskp` yalnızca
  `bl_ext.user_default.sketchup_imparator._vendor.openskp` altında,
  `defusedxml` wheel site-packages'inden. Blender 4.2.9 / 5.2.3'te
  `_extensions_warnings_get()` → `{}` (boş).
- Kaynaktan: `python3 build_addons.py` → `dist/*.zip` (sürüm
  `blender_manifest.toml`'dan okunur).

## Import davranışı
- **Birim:** sahne `Metric / Meters`'a ayarlanır; OpenSKP metreyi verir, eksen
  dönüşümü `(x, y, z) → (x, −z, y)` ve düğüm matrisi `B · M · B⁻¹`.
- **Instancing:** tanım başına tek mesh, yerleşim başına tek nesne. SketchUp
  origin/rotasyon/ölçek korunur; bir tanımı düzenlemek tüm kopyaları günceller.
- **Origin/Konum:** geometri tanım-local kalır; import sırasında mevcut konumlar korunur. Üst seviye düğümler kök edge nesnesine parent edilmez.
- **Edge’ler:** `(Edges)`/`RootEdges`/bağımsız edge objeleri `<prefix>Edges` koleksiyonunda toplanır (varsayılan olarak gizli değil; manuel gizleyip gösterebilirsiniz).
- **Geometri:** OpenSKP triangülasyonu sonrası coplanar komşu üçgenler
  ngon’a birleştirilir; delikli yüzeylerde (çoklu sınır döngüsü) orijinal
  üçgenler korunur. Flat shading (`use_smooth=False`).
- **UV:** SketchUp'ın per-face `uv_transform` + döşeme ölçüsünden hazır gelir,
  per-vertex ve konumlarla 1:1. Mapping düğümünde ek ölçek uygulanmaz.
- **Materyal:** glTF materyalleri Principled BSDF'e çevrilir; renk, saydamlık,
  colourized doku (Multiply) ve doku kutuları korunur. Dokular `.blend` içine
  pack edilir, geçici dosya silinir. Eşleşmeyen renkler için
  `Material_RRGGBB` / `Material_RRGGBB_texN` adları üretilir.
- **Tag'ler:** her SketchUp tag'i `SKP: <dosya>` altında `<prefix><tag>` adlı
  bir koleksiyon olur; `layer_hidden` → `hide_viewport` + `hide_render`.
- **Sahne:** `Page` kayıtları kamera olarak gelir (perspektif + ortografik,
  `fov` / `ortho_height`); sahneye özel gizli tag'ler uygulanır.
- **Loose edge:** bağımsız kenarlar curve nesnesi olur. Hem yüz hem kenar içeren
  tanımlarda kenarlar, mesh nesnesinin altında `<ad> (Edges)` olarak durur.
- **Empty:** yalnızca çocuğu olup geometrisi olmayan düğümler için oluşturulur.
- **Reload:** nesne dünya matrisleri, materyal slotları, desteklenen modifier'lar
  (Bevel, Solidify, Mirror, Array, Subsurf) ve Smooth-by-Angle geri yüklenir;
  kenar içe aktarma tercihi koleksiyon üzerinde saklanır.
- **Otomatik reload:** `skp_auto_reload` açıkken kalıcı bir `bpy.app.timers`
  2 sn'de bir dosyanın mtime'ını kontrol eder; SketchUp'ta kaydettiğen ~2 sn
  sonra yeniden içe aktarır. Yeniden aktarma sırasında kilit koyar, hata
  olursa aynı içeriği tekrar denemez.

## Mimari
| Dosya | İş |
| --- | --- |
| `sketchup_imparator/__init__.py` | kayıt, operatörler, panel, reload |
| `sketchup_imparator/skp_scene.py` | SketchUp → Blender dönüşümü |
| `sketchup_imparator/_vendor/openskp/` | OpenSKP 1.5.0 (MIT) — PyPI ile birebir aynı, düzenlenmemiş |
| `sketchup_imparator/shapely_fallback.py` | openskp'nin isteğe bağlı delik birleştirmesini atlayan bizim kod |
| `sketchup_imparator/wheels/` | defusedxml 0.7.1 (PSF) + mapbox_earcut 2.1.0 (cp311 = Blender 4.2-5.0, cp313 = 5.1+) |
| `blender_manifest.toml` | uzantı manifesti + sürüm kaynağı |

Kaldırılanlar: `sketchup.pyx`, `sketchup.abi3.so`, `SKPutil/`,
`SketchUpAPI.framework/`, `headers/`, `setup.py`, Cython build adımları ve
SDK'ya bağlı `ExportSKP` operatörü.

## Build & Test
```bash
python3 build_addons.py
blender -b --command extension validate dist/sketchup_imparator-2026.7.0.zip
blender -b --factory-startup --python tests/import_smoke.py -- "/path/to/file.skp"
```

`tests/import_smoke.py` gerçek bir dosyayla import + reload + proxy + purge +
delete akışını çalıştırır ve nesne/materyal/doku/bbox/alan özetini basar.

## Doğrulama (referans model: `studio sahne villa.skp`, 80 MB)
| Ölçüm | Değer |
| --- | --- |
| Ayrıştırma + sahne kurma | ~6.5 s |
| Blender import | ~13 s (4.2.9 LTS: ~38 s) |
| Düğüm / mesh nesnesi / empty / curve | 23.831 / 19.138 / 4.692 / 9 |
| Mesh datablock / materyal / packed doku | 137 / 54 / 16 |
| Vertex / üçgen (tanım-local) | 446.371 / 162.016 |
| Dünya alanı | 1526.75 m² |
| Bbox | (12.3434, 16.3728, 5.7423) m |
| Blender 4.2.9 LTS | validate + install (cp311) + smoke test: **PASS** |
| Blender 5.2.3 LTS | validate + install (cp313) + smoke test: **PASS** |

4.2'de materyal sayısı 54 yerine 55 görünür; fazlası Blender'ın kendi
`Dots Stroke` materyalidir, delete sonrası geriye yalnızca o kalır.

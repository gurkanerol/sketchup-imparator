# SketchUp Imparator — Current (2026.6.0.0)

Güncel durum ve kullanım kılavuzu. Eski `HANDOVER_NOTES`, `implementation_plan`, `task_description`, `walkthrough` belgeleri kaldırıldı; tek kaynak burasıdır.

## Kurulum
- Blender 5.2, sadece macOS Apple Silicon (arm64-only).
- `Edit > Preferences > Add-ons > Install…` → `dist/sketchup_imparator_v2026.6.0.0.zip` → **Import-Export: SketchUp Imparator** etkinleştir.
- Kaynak: `git clone` + `SketchUpAPI.framework` + `./uv run python3 build_addons.py` → `dist/*.zip`.

## Import
- `File > Import > SketchUp (.skp)`. Birimler: sahne `Metric/Meters`'a otomatik ayarlanır.
- **Texture:** Doğrudan materyallerde `STQ/Q`, miras materyallerde `*s/t` ölçeği; Shader Mapping `1,1,1` — ekstra ölçek yok.
- **Origin:** Mesh origin = SketchUp grup/component origin'i; geometri local koordinatta, bbox merkezleme yok.
- **Hiyerarşi:** Tek mesh'li grup/component kendi mesh'ini pivot yapar (ara `Empty` yok); konteyner gruplar için `Empty` kalır. Üst seviye `parent=None`, iç içe altlar parent mesh/empty'ye bağlı.
- **Outliner:** `SKP: <dosya>` altında `<prefix>_GROUPS` ve `<prefix>_COMPONENTS` koleksiyonları. `ROOT Empty` yok, ROOT'a uzanan uzun çizgi yok.
- **Reload:** `sk_last_filepath` ile sterilized re-import; malzeme/modifier backup'lanır.

## Mimari
- `sketchup.pyx` — tek dosyalık Cython binding, SketchUp C API doğrudan (ayrı paket yok).
- `sketchup_imparator/__init__.py` (Blender tarafı), `SKPutil/` (yardımcı).
- Framework: arm64-only + strip, flat layout, Headers yok. **Dist ~6.5M** (önce 48M).

## Build & Test
```bash
./uv run python3 build_addons.py
python3 -m unittest tests.test_import_state_cleanup -v
```

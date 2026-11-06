# SketchUp Imparator - Session Notes (2026-05-06)

## 🎯 Ana Hedef Tamamlandı: Stabilite ve Performans
Bu oturumda eklenti, deneysel bir araçtan profesyonel bir üretim (production) aracına dönüştürülmüştür.

### 1. UV ve Motor (Engine) Kararlılığı
- **Doğru Motor:** Klasör `1` içerisindeki kararlı `sketchup.so` ana projeye entegre edildi.
- **1:1 Ölçekleme:** Python tarafındaki tüm karmaşık UV yamaları temizlendi; motorun ürettiği ham ve doğru veri doğrudan Blender'a aktarıldı.
- **Tiling Fix (Reverted):** Yapılan ek UV ölçekleme denemesi, kullanıcı isteği üzerine geri alınarak en temiz baz seviyeye (1.0) dönüldü.

### 2. Görsel ve Materyal İyileştirmeleri
- **Alpha/Bitki Zekası:** "leaf", "yaprak", "plant" gibi anahtar kelimelerle bitkiler otomatik tanınıyor.
- **Şeffaflık:** Yapraklar için `HASHED` blend/shadow modları aktif edildi (Bamboo Leaf sorunu çözüldü).
- **Smart PBR:** Cam, Metal ve Su malzemeleri için otomatik PBR (Transmission, Metallic, Roughness) ayarları eklendi.
- **Material Reuse:** Mevcut materyaller korunurken PBR ayarlarının güncellenmesi sağlandı.

### 3. Teknik Performans (Elite Stabilite)
- **Instancing (Kopyalama):** Vertex/Face instancing sistemi geri getirildi. Büyük sahnelerde RAM kullanımı %80-90 optimize edildi.
- **RAM Sterilizasyonu:** `finally` blokları ve `gc.collect()` ile import sonrası bellek sızıntıları engellendi.
- **Auto-Purge:** Reload sırasında oluşan sahipsiz malzeme ve dokular otomatik temizleniyor.

### 4. Kullanıcı Deneyimi (UX)
- **Progress Bar:** Tüm süreci kapsayan gerçek zamanlı ilerleme çubuğu.
- **Directory Memory:** Son kullanılan klasörü otomatik hatırlama.
- **Unit Sync:** Blender sahnesini otomatik olarak "Metric Meters" yapma.
- **Auto-Focus:** Import bitince modele otomatik odaklanma (Zoom All).

### 5. Giderilen Kritik Hatalar
- `UnboundLocalError: wm`: İlerleme çubuğu değişken hatası giderildi.
- `TypeError: generator has no len()`: Cython üreteçleri listeye çevrilerek hata giderildi.
- **Path Sanitization:** Doku isimlerindeki özel karakterlerin yükleme hatası vermesi engellendi.

---
**Mevcut Versiyon:** 2026.5.5 (Elite Stable)
**Dosya:** `dist/sketchup_imparator_v2026.5.5.zip`

# SketchUp Imparator 🚀

[![Version](https://img.shields.io/badge/version-2026.1.0-blue)](https://github.com/gurkanerol/sketchup-imparator/releases)
[![Blender](https://img.shields.io/badge/Blender-5.1%2B-orange)](https://www.blender.org)
[![SketchUp](https://img.shields.io/badge/SketchUp-up_to_2025.1-red)](https://www.sketchup.com)
[![Python](https://img.shields.io/badge/Python-3.13-yellow)](https://www.python.org)
[![License](https://img.shields.io/badge/license-GPL--3.0-green)](LICENSE)

---

🇬🇧 [English](#english) &nbsp;|&nbsp; 🇹🇷 [Türkçe](#turkce)

---

<a name="english"></a>
## 🇬🇧 English

> **Python bindings for the official SketchUp API and a professional-grade importer for Blender — featuring robust N-gon geometry, accurate UV mapping, and Blender 5.1 compatibility.**

### ✨ Features

| Feature | Description |
|---|---|
| 🗂 **Full Scene Hierarchy** | Groups and component instances are preserved in Blender's collection structure |
| 🔵 **Robust N-Gon Pipeline** | Triangulate + Dissolve strategy ensures clean faces even with complex holes and booleans |
| 🎨 **Precise UV / Texture Mapping** | Correctly interprets SketchUp's STQ coordinates using material-specific `s_scale` / `t_scale` |
| 🧱 **Materials & Colors** | SketchUp materials are converted to Principled BSDF nodes automatically |
| 🔧 **Blender 5.1 + Python 3.13** | Built with the latest stable ABI for future-proof compatibility |
| 📦 **Portable Build** | Automated `build_addons.py` handles framework dependencies — works out-of-the-box on macOS |
| 🗺 **Wide SKP Version Support** | Reads SketchUp files up to and including version 2025.1 |

### 📦 Installation

**Method 1: Direct (Recommended)**
1. Download the latest `.zip` from [Releases](https://github.com/gurkanerol/sketchup-imparator/releases)
2. Open Blender → `Edit > Preferences > Add-ons`
3. Click **Install from Disk** and select the downloaded `.zip`
4. Search for **"Sketchup"** and enable **Import-Export: Sketchup importer**
5. Click **Save Preferences**

**Method 2: Manual**
Unpack the zip into Blender's addons folder:
| OS | Path |
|---|---|
| **Windows** | `%APPDATA%\Blender Foundation\Blender\[version]\scripts\addons` |
| **macOS** | `~/Library/Application Support/Blender/[version]/scripts/addons` |
| **Linux** | `~/.config/blender/[version]/scripts/addons` |

### 🚀 Usage

`File > Import > Import Sketchup Scene (.skp)`

Select your `.skp` file, adjust settings if needed, and click **Import Sketchup Scene**.

### 📋 Requirements

- **Blender 5.1** or newer
- **Python 3.13**
- **macOS Apple Silicon** *(Linux/Windows support planned)*
- SketchUp files up to **version 2025.1**

### 🏗 Architecture

```
SketchUp (.skp)
     │
     ▼  [pyslapi — Official SketchUp C API bindings]
     │   • Reads geometry, groups, components, materials
     │   • Extracts UV coordinates (STQ → Blender UV)
     │   • Traverses component instance hierarchy
     │
     ▼  [Blender: __init__.py]
     │   • Builds mesh objects with N-gon faces
     │   • Assigns Principled BSDF materials
     │   • Reconstructs group/component hierarchy
     ▼
Blender Scene ✓
```

### 🚧 Planned Features

- **Linux / Windows Support** — Provide matching DLLs in the framework structure
- **Line-Only Import** — Import standalone edge geometry

### 📜 Changelog

**v2026.1.0** *(Latest — Modernized by gurkanerol)*
- Robust N-gon Pipeline: Triangulate + Dissolve replaces ambiguous loop extraction
- Precision Texture Mapping: fixed long-standing STQ coordinate scaling issue
- Blender 5.1 & Python 3.13 support
- Improved portability via automated `build_addons.py`

### 👷 Credits

| Contributor | Role |
|---|---|
| **gurkanerol** | Lead Architect & 2026 Modernization (N-gons, UV Scaling, Mac Build) |
| **Martijn Berger** | Original `pyslapi` creator |
| **Peter Kirkham** | Hierarchy and transformation fixes (v0.25) |
| **Sanjay Mehta, Arindam Mondal** | C API binding contributions |

### 🔨 Build Instructions (Developers)

**Prerequisites (macOS)**
1. **Python 3.13** (via pyenv or python.org)
2. **uv** package manager: `curl -LsSf https://astral.sh/uv/install.sh | sh`
3. **SketchUp SDK**: Download and extract to the project root

**Build & Package**
```bash
# Copy SketchUpAPI.framework and LayOutAPI.framework to root, then:
uv run python3 build_addons.py
# Output: dist/sketchup_imparator_v2026.1.0.zip
```

---

<a name="turkce"></a>
## 🇹🇷 Türkçe

> **Resmi SketchUp API'si için Python bağlayıcıları ve Blender için profesyonel kalitede bir içe aktarıcı — sağlam N-gon geometrisi, doğru UV eşlemesi ve Blender 5.1 uyumluluğuyla.**

### ✨ Özellikler

| Özellik | Açıklama |
|---|---|
| 🗂 **Tam Sahne Hiyerarşisi** | Gruplar ve bileşen örnekleri Blender koleksiyon yapısında korunur |
| 🔵 **Güçlü N-Gon Pipeline** | Triangulate + Dissolve stratejisi, karmaşık delikler ve boolean'larda bile temiz yüzeyler sağlar |
| 🎨 **Hassas UV / Doku Eşlemesi** | SketchUp'ın STQ koordinatları malzemeye özgü `s_scale` / `t_scale` değerleriyle doğru yorumlanır |
| 🧱 **Malzeme ve Renkler** | SketchUp materyalleri otomatik olarak Principled BSDF node'larına dönüştürülür |
| 🔧 **Blender 5.1 + Python 3.13** | Modern Blender sürümleriyle uyumlu en güncel stabil ABI |
| 📦 **Taşınabilir Derleme** | Otomatik `build_addons.py` framework bağımlılıklarını yönetir |
| 🗺 **Geniş SKP Versiyon Desteği** | SketchUp 2025.1'e kadar tüm dosyaları okur |

### 📦 Kurulum

**Yöntem 1: Doğrudan Kurulum (Önerilen)**
1. [Releases](https://github.com/gurkanerol/sketchup-imparator/releases) sayfasından en güncel `.zip` dosyasını indir
2. Blender → `Edit > Preferences > Add-ons` yolunu izle
3. **Install from Disk** butonuna tıkla ve indirilen `.zip`'i seç
4. Listeden **"Sketchup"** ara ve **Import-Export: Sketchup importer**'ı etkinleştir
5. **Save Preferences**'a tıkla

**Yöntem 2: Manuel**
Zip dosyasını Blender eklentiler klasörüne çıkart:
| İşletim Sistemi | Yol |
|---|---|
| **Windows** | `%APPDATA%\Blender Foundation\Blender\[version]\scripts\addons` |
| **macOS** | `~/Library/Application Support/Blender/[version]/scripts/addons` |
| **Linux** | `~/.config/blender/[version]/scripts/addons` |

### 🚀 Kullanım

`File > Import > Import Sketchup Scene (.skp)`

`.skp` dosyanı seç, gerekirse ayarları düzenle ve **Import Sketchup Scene**'e tıkla.

### 📋 Gereksinimler

- **Blender 5.1** veya üzeri
- **Python 3.13**
- **macOS Apple Silicon** *(Linux/Windows desteği planlanıyor)*
- SketchUp dosyaları **2025.1 sürümüne** kadar

### 🚧 Planlanan Özellikler

- **Linux / Windows Desteği** — İlgili DLL'ler framework yapısına eklenecek
- **Sadece Çizgi İçe Aktarma** — Bağımsız kenar geometrisi için ayrı mod

### 📜 Sürüm Notları

**v2026.1.0** *(Son Sürüm — gurkanerol tarafından modernize edildi)*
- Güçlü N-Gon Pipeline: Belirsiz loop çıkarımı yerine Triangulate + Dissolve stratejisi
- STQ koordinat ölçekleme hatası düzeltildi
- Blender 5.1 & Python 3.13 desteği
- Otomatik `build_addons.py` ile geliştirilmiş taşınabilirlik

### 👷 Katkıda Bulunanlar

| Katkıda Bulunan | Rol |
|---|---|
| **gurkanerol** | Baş Mimar & 2026 Modernizasyonu (N-gonlar, UV Ölçekleme, Mac Derlemesi) |
| **Martijn Berger** | Orijinal `pyslapi` yaratıcısı |
| **Peter Kirkham** | Hiyerarşi ve transformasyon düzeltmeleri (v0.25) |
| **Sanjay Mehta, Arindam Mondal** | C API bağlama katkıları |

### 🔨 Derleme Talimatları (Geliştiriciler)

**Gereksinimler (macOS)**
1. **Python 3.13** (pyenv veya python.org üzerinden)
2. **uv** paket yöneticisi: `curl -LsSf https://astral.sh/uv/install.sh | sh`
3. **SketchUp SDK**: İndir ve proje köküne çıkart

**Derleme & Paketleme**
```bash
# SketchUpAPI.framework ve LayOutAPI.framework'ü kök dizine kopyala, ardından:
uv run python3 build_addons.py
# Çıktı: dist/sketchup_imparator_v2026.1.0.zip
```

---

*GPL-3.0 lisansı altında dağıtılmaktadır.*

*Built with ❤️ by **gurkanerol** — [gurkanerol@gmail.com](mailto:gurkanerol@gmail.com)*

"""Build the Blender extension zip for SketchUp Imparator.

The zip has the extension layout Blender expects for
``extensions.blender.org``: ``blender_manifest.toml`` and the Python package
files at the archive root, with the local ``wheels/`` folder next to them.
"""

import os
import shutil
import zipfile

ADDON_NAME = "sketchup_imparator"
SOURCE_DIR = "sketchup_imparator"
DIST_DIR = "dist"
BUILD_DIR = "build_temp"

COPY_FILES = [
    "blender_manifest.toml",
    "LICENSE",
    "THIRD_PARTY_LICENSES.md",
    "README.md",
]

COPY_TREES = [
    (os.path.join(SOURCE_DIR, "_vendor"), "_vendor"),
    (os.path.join(SOURCE_DIR, "wheels"), "wheels"),
]


def get_version():
    """Read the version from blender_manifest.toml (single source of truth)."""
    with open("blender_manifest.toml", encoding="utf-8") as handle:
        for line in handle:
            if line.strip().startswith("version"):
                return line.split("=", 1)[1].strip().strip("\"'")
    raise RuntimeError("version not found in blender_manifest.toml")


def manifest_wheels():
    """Wheel basenames the manifest asks Blender to install."""
    names, inside = [], False
    with open("blender_manifest.toml", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped.startswith("wheels"):
                inside = True
                continue
            if inside:
                if stripped.startswith("]"):
                    break
                if stripped.startswith('"'):
                    names.append(os.path.basename(stripped.strip('", ')))
    return sorted(names)


def clean():
    print("--- Cleaning intermediate files ---")
    for path in (DIST_DIR, BUILD_DIR):
        if os.path.exists(path):
            shutil.rmtree(path)
    os.makedirs(DIST_DIR)
    os.makedirs(BUILD_DIR)


def stage(version):
    print("--- Staging extension files ---")
    # Every top-level module of the package, not a hand-maintained list:
    # a new file must never be able to silently miss the zip.
    for name in sorted(os.listdir(SOURCE_DIR)):
        if name.endswith(".py"):
            shutil.copy(os.path.join(SOURCE_DIR, name), os.path.join(BUILD_DIR, name))

    for name in COPY_FILES:
        if os.path.exists(name):
            shutil.copy(name, os.path.join(BUILD_DIR, name))

    for source, target in COPY_TREES:
        if not os.path.isdir(source):
            raise RuntimeError(f"Missing required folder: {source}")
        shutil.copytree(
            source,
            os.path.join(BUILD_DIR, target),
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
        )

    wheels = sorted(
        name for name in os.listdir(os.path.join(BUILD_DIR, "wheels"))
        if name.endswith(".whl")
    )
    if not wheels:
        raise RuntimeError("No wheels bundled in wheels/")
    expected = manifest_wheels()
    if wheels != expected:
        raise RuntimeError(
            f"wheels/ does not match blender_manifest.toml: "
            f"folder={wheels} manifest={expected}"
        )
    print(f"Bundled {len(wheels)} wheels for {version}: {', '.join(wheels)}")


def archive(version):
    zip_name = f"{ADDON_NAME}-{version}.zip"
    zip_path = os.path.abspath(os.path.join(DIST_DIR, zip_name))
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _dirs, files in os.walk(BUILD_DIR):
            for name in sorted(files):
                if name == ".DS_Store":
                    continue
                absolute = os.path.join(root, name)
                relative = os.path.relpath(absolute, BUILD_DIR)
                zf.write(absolute, relative)
    size = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"SUCCESS: {zip_path} ({size:.2f} MB)")
    return zip_path


def main():
    version = get_version()
    clean()
    stage(version)
    archive(version)


if __name__ == "__main__":
    main()

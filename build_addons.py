import os
import subprocess
import shutil
import glob

# Configuration
ADDON_NAME = "sketchup_imparator"
DIST_DIR = "dist"
BUILD_DIR = "build_temp"
UV_BIN = "uv"

def get_version():
    init_path = os.path.join(ADDON_NAME, "__init__.py")
    if not os.path.exists(init_path):
        return "2026.6.0.0" # Fallback
    with open(init_path, "r") as f:
        for line in f:
            if '"version":' in line:
                # Extract (2026, 6, 0, 0) -> 2026.6.0.0
                parts = line.split("(")[1].split(")")[0].split(",")
                return ".".join(p.strip() for p in parts)
    return "2026.6.0.0"

def run_command(cmd, cwd=None):
    print(f"Running: {' '.join(cmd)}")
    env = os.environ.copy()
    env["UV_CACHE_DIR"] = os.path.abspath(".uv_cache")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        raise Exception(f"Command failed: {' '.join(cmd)}")
    return result.stdout

def clean():
    print("--- Cleaning intermediate files ---")
    for path in [DIST_DIR, BUILD_DIR]:
        if os.path.exists(path):
            shutil.rmtree(path)
    
    # Clean root directory from stale binaries and generated C++
    for f in glob.glob("sketchup*.so") + glob.glob("sketchup.cpp"):
        os.remove(f)
        print(f"Removed stale: {f}")

    os.makedirs(DIST_DIR)
    os.makedirs(BUILD_DIR)

def build():
    print("--- Starting Sterilized Build ---")
    
    # 1. Smart Compilation
    pyx_file = "sketchup.pyx"
    so_files = glob.glob("sketchup_imparator/sketchup*.so")
    
    needs_compile = True
    if so_files and os.path.exists(pyx_file):
        so_files.sort(key=os.path.getmtime, reverse=True)
        latest_so = so_files[0]
        if os.path.getmtime(latest_so) > os.path.getmtime(pyx_file):
            needs_compile = False
            print("Cython binary is up to date, skipping compilation.")
            
    if needs_compile:
        print("Compiling Cython extension...")
        try:
            run_command(["python3", "setup.py", "build_ext", "--inplace"])
        except Exception as e:
            print(f"Compilation failed ({e}), but attempting to package existing binary...")
            if not so_files:
                raise Exception("No existing binary found and compilation failed.")
        new_so_files = glob.glob("sketchup*.so")
        for so in new_so_files:
            shutil.move(so, os.path.join("sketchup_imparator", so))
    
    # 2. Find the generated binary
    # We look for the one with cpython/abi3 suffix first, or just sketchup.so
    binaries = glob.glob("sketchup_imparator/sketchup.cpython-*.so") + glob.glob("sketchup_imparator/sketchup.abi3.so")
    if not binaries:
        binaries = glob.glob("sketchup_imparator/sketchup.so")
        
    if not binaries:
        raise Exception("Failed to find compiled .so file after build")
    
    # Use the most recently modified one if multiple exist
    binaries.sort(key=os.path.getmtime, reverse=True)
    src_bin = binaries[0]
    print(f"Using binary: {src_bin}")
    
    target_bin = os.path.join(BUILD_DIR, ADDON_NAME, "sketchup.so")
    
    os.makedirs(os.path.join(BUILD_DIR, ADDON_NAME), exist_ok=True)
    shutil.copy(src_bin, target_bin)
    print(f"Copied {src_bin} to {target_bin}")

    # 3. Copy Frameworks (preserve symlinks to avoid 3x duplication)
    for fw in ["SketchUpAPI.framework"]:
        if os.path.exists(fw):
            target_fw_path = os.path.join(BUILD_DIR, ADDON_NAME, fw)
            shutil.copytree(fw, target_fw_path, dirs_exist_ok=True, symlinks=True)
            print(f"Bundled {fw}")

            # Remove Headers (compile-time only, not needed at runtime)
            for _h in [os.path.join(target_fw_path, "Headers"),
                       os.path.join(target_fw_path, "Versions", "A", "Headers")]:
                if os.path.islink(_h) or os.path.exists(_h):
                    try:
                        if os.path.islink(_h) or os.path.isfile(_h):
                            os.remove(_h)
                        else:
                            shutil.rmtree(_h)
                        print(f"  --> Removed Headers (runtime not needed): {_h}")
                    except Exception as _e:
                        print(f"  Headers remove skipped {_h}: {_e}")

            # Thin to arm64 + strip debug symbols (Apple Silicon only per README)
            _binaries = [os.path.join(target_fw_path, "Versions", "A", "SketchUpAPI")]
            _fw_dir = os.path.join(target_fw_path, "Versions", "A", "Frameworks")
            if os.path.isdir(_fw_dir):
                for _f in os.listdir(_fw_dir):
                    _binaries.append(os.path.join(_fw_dir, _f))
            for _bin in _binaries:
                if os.path.isfile(_bin) and not os.path.islink(_bin):
                    try:
                        run_command(["lipo", "-thin", "arm64", _bin, "-output", _bin + ".thin"])
                        shutil.move(_bin + ".thin", _bin)
                        print(f"  --> Thinned to arm64: {os.path.basename(_bin)}")
                    except Exception as _e:
                        print(f"  lipo thin skipped {os.path.basename(_bin)}: {_e}")
                    try:
                        run_command(["strip", "-x", _bin])
                    except Exception:
                        pass
                    try:
                        run_command(["codesign", "-s", "-", "--force", _bin])
                    except Exception:
                        pass

            # Flatten: Blender's zip installer turns symlinks into text files
            # (broken framework). Create flat layout with real files only:
            # SketchUpAPI.framework/SketchUpAPI + Frameworks/*.dylib, no Versions.
            try:
                _src_bin = os.path.join(target_fw_path, "Versions", "A", "SketchUpAPI")
                _dst_bin = os.path.join(target_fw_path, "SketchUpAPI")
                if os.path.islink(_dst_bin) or os.path.exists(_dst_bin):
                    os.remove(_dst_bin)
                if os.path.exists(_src_bin):
                    shutil.copy2(_src_bin, _dst_bin)
                    print(f"  --> Flattened SketchUpAPI binary to root")
                _src_fwdir = os.path.join(target_fw_path, "Versions", "A", "Frameworks")
                _dst_fwdir = os.path.join(target_fw_path, "Frameworks")
                if os.path.islink(_dst_fwdir) or os.path.exists(_dst_fwdir):
                    if os.path.islink(_dst_fwdir):
                        os.remove(_dst_fwdir)
                    else:
                        shutil.rmtree(_dst_fwdir)
                if os.path.exists(_src_fwdir):
                    shutil.copytree(_src_fwdir, _dst_fwdir)
                    print(f"  --> Flattened Frameworks to root")
                _src_res = os.path.join(target_fw_path, "Versions", "A", "Resources")
                _dst_res = os.path.join(target_fw_path, "Resources")
                if os.path.exists(_src_res):
                    if os.path.islink(_dst_res):
                        os.remove(_dst_res)
                    elif os.path.exists(_dst_res):
                        shutil.rmtree(_dst_res)
                    shutil.copytree(_src_res, _dst_res)
                    print(f"  --> Flattened Resources to root")
                # Remove Versions entirely (single copy only)
                _versions = os.path.join(target_fw_path, "Versions")
                if os.path.exists(_versions):
                    shutil.rmtree(_versions)
                    print(f"  --> Removed Versions (flat layout)")
            except Exception as _e:
                print(f"  Flatten failed {_e}")
    
    # 4. Copy Python sources
    shutil.copy("sketchup_imparator/__init__.py", os.path.join(BUILD_DIR, ADDON_NAME, "__init__.py"))
    if os.path.exists("sketchup_imparator/SKPutil"):
        shutil.copytree("sketchup_imparator/SKPutil", os.path.join(BUILD_DIR, ADDON_NAME, "SKPutil"), dirs_exist_ok=True)

    # 5. Fix internal paths with install_name_tool
    # We target the binary inside the build folder
    # We use the root level binary in the framework folder to avoid broken symlink issues in ZIPs
    print("Fixing framework link paths...")
    
    # List of possible rpath strings to replace (SDK versions vary)
    rpath_targets = [
        "@rpath/SketchUpAPI.framework/Versions/Current/SketchUpAPI",
        "@rpath/SketchUpAPI.framework/Versions/A/SketchUpAPI"
    ]
    
    for target in rpath_targets:
        fw_name = "SketchUpAPI"
        loader_path = f"@loader_path/{fw_name}.framework/{fw_name}"
        
        # Try to change each possible rpath found in the binary
        run_command([
            "install_name_tool", 
            "-change", 
            target, 
            loader_path, 
            target_bin
        ])

    # 6. Create Zip (flat layout, no symlinks -> Blender installer safe)
    version = get_version()
    zip_name = f"{ADDON_NAME}_v{version}.zip"
    zip_path = os.path.abspath(os.path.join(DIST_DIR, zip_name))
    shutil.make_archive(os.path.join(DIST_DIR, f"{ADDON_NAME}_v{version}"), 'zip', BUILD_DIR, ADDON_NAME)
    print(f"SUCCESS: Created {zip_path}")

if __name__ == "__main__":
    try:
        clean()
        build()
    except Exception as e:
        print(f"FATAL ERROR: {e}")

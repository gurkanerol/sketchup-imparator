import os
import subprocess
import shutil
import glob

# Configuration
ADDON_NAME = "sketchup_imparator"
DIST_DIR = "dist"
BUILD_DIR = "build_temp"
UV_BIN = "./uv"

def run_command(cmd, cwd=None):
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
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
    
    # 1. Compile extension using local uv environment
    run_command([UV_BIN, "run", "python", "setup.py", "build_ext", "--inplace"])
    
    # 2. Find the generated binary
    # We look for the one with cpython/abi3 suffix first, or just sketchup.so
    binaries = glob.glob("sketchup.cpython-*.so") + glob.glob("sketchup.abi3.so")
    if not binaries:
        binaries = glob.glob("sketchup.so")
        
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

    # 3. Copy Frameworks
    for fw in ["SketchUpAPI.framework", "LayOutAPI.framework"]:
        if os.path.exists(fw):
            target_fw_path = os.path.join(BUILD_DIR, ADDON_NAME, fw)
            shutil.copytree(fw, target_fw_path, dirs_exist_ok=True)
            print(f"Bundled {fw}")
            
            # CRITICAL: Copy internal dependency folders to the root to fix @rpath issues
            # ZIP often flattens or breaks symlinks, so we put files where the loader expects them.
            internal_paths = [
                (os.path.join(fw, "Versions/A/Frameworks"), os.path.join(target_fw_path, "Frameworks")),
                (os.path.join(fw, "Versions/A/Libraries"), os.path.join(target_fw_path, "Libraries"))
            ]
            for src, dst in internal_paths:
                if os.path.exists(src):
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                    print(f"  --> Fixed internal dependency path: {src} to {dst}")
    
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
        "@rpath/SketchUpAPI.framework/Versions/A/SketchUpAPI",
        "@rpath/LayOutAPI.framework/Versions/Current/LayOutAPI",
        "@rpath/LayOutAPI.framework/Versions/A/LayOutAPI"
    ]
    
    for target in rpath_targets:
        fw_name = "SketchUpAPI" if "SketchUpAPI" in target else "LayOutAPI"
        loader_path = f"@loader_path/{fw_name}.framework/{fw_name}"
        
        # Try to change each possible rpath found in the binary
        run_command([
            "install_name_tool", 
            "-change", 
            target, 
            loader_path, 
            target_bin
        ])

    # 6. Create Zip
    zip_name = f"sketchup_imparator_v2026"
    shutil.make_archive(os.path.join(DIST_DIR, zip_name), 'zip', BUILD_DIR, ADDON_NAME)
    print(f"SUCCESS: Created {DIST_DIR}/{zip_name}.zip")

if __name__ == "__main__":
    try:
        clean()
        build()
    except Exception as e:
        print(f"FATAL ERROR: {e}")

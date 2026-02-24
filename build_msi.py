"""
NeuroVault MSI Installer Builder
Wraps the PyInstaller-built NeuroVault.exe into a standard Windows .msi installer.

Usage:
    1. First build with PyInstaller:  .venv\\Scripts\\python.exe -m PyInstaller NeuroVault.spec
    2. Then create MSI:               .venv\\Scripts\\python.exe build_msi.py

Output: dist/NeuroVault-v4.0-Setup.msi
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

# All paths as absolute
PROJECT_DIR = Path(__file__).parent.resolve()
DIST_DIR = PROJECT_DIR / "dist"
EXE_PATH = DIST_DIR / "NeuroVault.exe"
ASSETS_DIR = PROJECT_DIR / "assets"
LICENSE_FILE = PROJECT_DIR / "LICENSE"
VENV_PYTHON = PROJECT_DIR / ".venv" / "Scripts" / "python.exe"

BUILD_TMP = PROJECT_DIR / "_msi_build_tmp"
STAGING = BUILD_TMP / "app_files"
OUTPUT_MSI_NAME = "NeuroVault-v4.0-Setup.msi"


def clean():
    if BUILD_TMP.exists():
        shutil.rmtree(BUILD_TMP, ignore_errors=True)


def stage_files():
    """Copy app files into staging directory"""
    print("📦 Staging files for MSI...")
    
    STAGING.mkdir(parents=True, exist_ok=True)
    
    # Main executable
    shutil.copy2(EXE_PATH, STAGING / "NeuroVault.exe")
    
    # Assets
    if ASSETS_DIR.exists():
        shutil.copytree(ASSETS_DIR, STAGING / "assets", dirs_exist_ok=True)
    
    # License
    if LICENSE_FILE.exists():
        shutil.copy2(LICENSE_FILE, STAGING / "LICENSE")
    
    print(f"   ✅ Staged {sum(1 for _ in STAGING.rglob('*') if _.is_file())} files")


def create_launcher():
    """Create a minimal launcher.py that cx_Freeze will freeze"""
    launcher = BUILD_TMP / "launcher.py"
    launcher.write_text(
        "import os, sys, subprocess\n"
        "d = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__))\n"
        "e = os.path.join(d, 'NeuroVault.exe')\n"
        "if os.path.exists(e):\n"
        "    subprocess.Popen([e], cwd=d)\n"
        "else:\n"
        "    print('NeuroVault.exe not found')\n",
        encoding="utf-8"
    )
    return launcher


def create_cx_setup(launcher_path):
    """Create setup.py for cx_Freeze inside the build temp directory"""
    
    # Use forward slashes for Python path strings
    staged_exe = str(STAGING / "NeuroVault.exe").replace("\\", "/")
    staged_assets = str(STAGING / "assets").replace("\\", "/")
    ico_path = str(ASSETS_DIR / "logo.ico").replace("\\", "/")
    launcher_str = str(launcher_path).replace("\\", "/")
    
    setup_py = BUILD_TMP / "setup.py"
    setup_py.write_text(f'''
import sys
from cx_Freeze import setup, Executable

setup(
    name="NeuroVault",
    version="4.0.0",
    description="NeuroVault - AI-Powered Second Brain",
    author="Madhur Tyagi",
    options={{
        "build_exe": {{
            "include_files": [
                ("{staged_exe}", "NeuroVault.exe"),
                ("{staged_assets}", "assets"),
            ],
            "excludes": [
                "tkinter", "unittest", "email", "html", "http", "xml",
                "pydoc", "doctest", "argparse", "difflib", "inspect",
                "logging", "multiprocessing", "test",
            ],
        }},
        "bdist_msi": {{
            "upgrade_code": "{{12345678-1234-1234-1234-111111111111}}",
            "add_to_path": False,
            "summary_data": {{
                "author": "Madhur Tyagi",
                "comments": "NeuroVault - AI-Powered Second Brain",
            }},
        }},
    }},
    executables=[
        Executable(
            script="{launcher_str}",
            base="gui",
            target_name="NeuroVaultLauncher.exe",
            icon="{ico_path}",
            shortcut_name="NeuroVault",
            shortcut_dir="DesktopFolder",
        )
    ],
)
'''.strip(), encoding="utf-8")
    return setup_py


def build_msi():
    """Main build function"""
    
    if not EXE_PATH.exists():
        print("❌ Error: dist/NeuroVault.exe not found!")
        print("   Run PyInstaller first:")
        print(f"   {VENV_PYTHON} -m PyInstaller NeuroVault.spec")
        sys.exit(1)
    
    exe_size_mb = EXE_PATH.stat().st_size / (1024 * 1024)
    print(f"🚀 NeuroVault MSI Builder")
    print(f"   Source EXE: {EXE_PATH} ({exe_size_mb:.1f} MB)")
    print()
    
    # Step 1: Stage files
    stage_files()
    
    # Step 2: Create launcher
    launcher = create_launcher()
    print(f"   ✅ Created launcher script")
    
    # Step 3: Create cx_Freeze setup.py
    setup_py = create_cx_setup(launcher)
    print(f"   ✅ Created cx_Freeze setup.py")
    
    # Step 4: Run cx_Freeze bdist_msi
    print("\n🔨 Building MSI (this may take a minute)...")
    
    python_exe = str(VENV_PYTHON) if VENV_PYTHON.exists() else sys.executable
    
    result = subprocess.run(
        [python_exe, str(setup_py), "bdist_msi"],
        cwd=str(BUILD_TMP),
        capture_output=True,
        text=True,
        timeout=300,
    )
    
    if result.returncode != 0:
        print(f"❌ Build failed! (exit code {result.returncode})")
        err_text = result.stderr or result.stdout
        # Show last 2000 chars of error
        print(err_text[-2000:] if len(err_text) > 2000 else err_text)
        clean()
        sys.exit(1)
    
    # Step 5: Find and copy MSI output
    msi_dist = BUILD_TMP / "dist"
    msi_files = list(msi_dist.glob("*.msi")) if msi_dist.exists() else []
    
    if not msi_files:
        print("❌ No MSI file was generated!")
        print("stdout:", result.stdout[-500:])
        clean()
        sys.exit(1)
    
    output_msi = DIST_DIR / OUTPUT_MSI_NAME
    shutil.copy2(msi_files[0], output_msi)
    
    # Clean up temp directory
    clean()
    
    msi_size_mb = output_msi.stat().st_size / (1024 * 1024)
    print(f"\n{'='*50}")
    print(f"🎉 MSI installer created successfully!")
    print(f"📁 Location: {output_msi.absolute()}")
    print(f"📏 Size: {msi_size_mb:.1f} MB")
    print(f"{'='*50}")
    print(f"\n💡 Users can install NeuroVault by double-clicking the .msi file!")


if __name__ == "__main__":
    try:
        clean()  # Start fresh
        build_msi()
    except KeyboardInterrupt:
        print("\n⚠️ Build cancelled.")
        clean()
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        clean()
        sys.exit(1)

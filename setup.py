from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but some modules need manual inclusion
build_exe_options = {
    "zip_include_packages": ["ASS", "wx"],
    "packages": ["ASS", "appdirs", "github", "json", "os", "psutil", "python-dotenv", "pywin32", "requests", "shutil", "sys", "vdf", "wx"],  # List additional packages to include
    "excludes": ["asyncio", "concurrent", "curses", "html", "multiprocessing", "PIL", "pip", "pkg_resources", "pycparser", "pydoc_data", "setuptools", "tkinter", "tomllib", "wheel", "xml", "xmlrpc"],    # Exclude modules you don't need
    "include_files": ['data/']  # Include any files, such as data folders
}

# GUI applications require a different base on Windows (the default is for a console application).
base = None
import sys
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "AccessibleStardewSetup",
    version = "0.1",
    description = "Installs Stardew-Access and required dependencies.",
    options = {"build_exe": build_exe_options},
    executables = [Executable("main.py", base=base, target_name="ass")]
)

import sys
from cx_Freeze import setup, Executable
import os.path

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = {"packages": ["os", "ttkthemes","mutagen","pygame"],'include_files':['tcl86t.dll','tk86t.dll']}

# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"



setup(
    name="Melody",
    version="0.1",
    description="Music Player",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base)],
    shortcutName = "Melody",
    shortcutDir = "MelodyFolder",
)
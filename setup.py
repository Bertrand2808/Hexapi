# setup.py
import sys

from cx_Freeze import Executable, setup

# Inclure ton script principal
executables = [
    Executable(
        script="main.py",
        target_name="HexAPI Generator.exe",
        icon="generator/assets/icons/java.png",
        base="Win32GUI" if sys.platform == "win32" else None,
    )
]

# Options de build
buildOptions = dict(
    packages=[
        "jinja2",
        "tkinter",
        "ttkbootstrap",
        "faker",
    ],  # cx_Freeze embarquera faker sans peine
    includes=[],
    include_files=[
        ("generator/templates", "generator/templates"),
        ("generator/gui/style.py", "generator/gui"),
        ("generator/config/settings.json", "generator/config/settings.json"),
        ("generator/config/roadmap.txt", "generator/config/roadmap.txt"),
        ("generator/assets", "generator/assets"),
        ("generator/assets/icons", "generator/assets/icons"),
        ("generator/assets/icons/java.png", "generator/assets/icons/java.png"),
        ("generator/assets/images", "generator/assets/images"),
        ("README_hexAPI.md", "README_hexAPI.md"),
    ],
)

setup(
    name="HexAPI Generator",
    version="0.1.0",
    description="HexAPI Generator GUI",
    options=dict(build_exe=buildOptions),
    executables=executables,
)

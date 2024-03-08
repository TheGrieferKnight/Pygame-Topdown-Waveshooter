# This code snippet is setting up a script to freeze a Python application using cx_Freeze. Freezing a
# Python application means converting it into an executable that can be run on a system without
# requiring the Python interpreter to be installed.
import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="Pygame",
    options={
        "build_exe": {
            "packages": ["pygame"],
            "include_files": ["assets/"],
        }
    },
    executables=executables,
)

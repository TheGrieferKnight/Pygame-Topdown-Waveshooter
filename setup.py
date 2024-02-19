import cx_Freeze

executables = [cx_Freeze.Executable("baller.py")]

cx_Freeze.setup(
    name="A bit Racey",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["background.png", "pewpew.png", "enemy.png", "sprite.png"]}},
    executables = executables

    )
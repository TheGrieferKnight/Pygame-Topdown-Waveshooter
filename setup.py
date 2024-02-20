import cx_Freeze

executables = [cx_Freeze.Executable("baller.py")]

cx_Freeze.setup(
    name="A bit Racey",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["assets/environment/background.png", "assets/player/bullet.png", "assets/enemy/enemy.png", "assets/player/sprite.png", "menu_clicksound.mp3"]}},
    executables = executables

    )
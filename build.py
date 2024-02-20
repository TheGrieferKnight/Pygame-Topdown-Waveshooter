import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="Pygame",
    options={
        "build_exe": {
            "packages": ["pygame"],
            "include_files": [
                "assets/",
                "main_game.py",
                "bullet.py",
                "sprites.py",
                "enemy.py",
                "player.py",
                "default_settings.py",
                "waves.py",
                "health_bar.py",
                "round_if_not_float.py"
            ],
        }
    },
    executables=executables,
)

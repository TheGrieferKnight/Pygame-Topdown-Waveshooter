import platform

if platform.system() == "Windows":
    import ctypes
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    WIDTH = screensize[0]
    HEIGHT = screensize[1]

if platform.system() == "Linux":
    import gi
    gi.require_version('Gdk', '3.0')
    from gi.repository import Gdk
    WIDTH = Gdk.Screen.width()
    HEIGHT = Gdk.Screen.height()

# Game setup
FPS = 60
PYGAME_DISPLAY = 0

# Player default_settings
PLAYER_START_X = WIDTH / 2
PLAYER_START_Y = HEIGHT / 2
PLAYER_SIZE = 0.5
PLAYER_SPEED = 3
PLAYER_STARTING_HEALTH = 200
PLAYER_HIT_INTERVAL = 1

# Weapon default_settings
BULLET_LIFETIME = 750
PLAYER_BASE_AMMOCOUNT = 6
SPLIT_SHOT_PRICE = ["10", "15", "30"]
PENETRATION_PRICE = ["30","40", "50"]

# Enemy default_settings
ENEMY_SIZE = 0.5
ENEMY_BASE_SPEED = 2
ENEMY_BASE_HEALTH = 100
ENEMY_BASE_DAMAGE = 50
ENEMY_BASE_SPAWN_COOLDOWN = 3000
ENEMY_BASE_WORTH = 1

# Bullet Default Settings
SHOT_CD_0 = 200
BULLET_SIZE = 1.4
BULLET_SPEED = 40

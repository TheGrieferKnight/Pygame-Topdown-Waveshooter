import pygame
import pygame_menu
from sprites import *
from pygame_menu import Theme
from pygame_menu import sound
from default_settings import *
from main_game import *

pygame.init()
menu_font = pygame_menu.font.FONT_COMIC_NEUE
difficulty = 1

# Create Pygame Window
pygame.display.set_caption("Baller")
screen = pygame.display.set_mode((WIDTH, HEIGHT), display=PYGAME_DISPLAY)
clock = pygame.time.Clock()

def settings():
    pass


# Defining the main menu theme
myimage = pygame_menu.baseimage.BaseImage(
    image_path="assets/enviroment/background.png",
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY,
)


def change_difficulty(prev_value, value):
    
    global difficulty

    if value == "easy":

        difficulty = 1

    elif value == "medium":

        difficulty = 2

    elif value == "hard":

        difficulty = 3


main_menu_theme = pygame_menu.Theme(
    title_offset=(WIDTH / 2 - 100, 0),
    title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE,
    title_font=menu_font,
    background_color=myimage,
    title_background_color=(255, 0, 0),
    title_font_shadow=False,
    widget_padding=25,
)

# Create the main menu
main_menu = pygame_menu.Menu("Main Menu", WIDTH, HEIGHT, theme=main_menu_theme)

# Defining the main menu sounds
engine = sound.Sound()
engine.set_sound(sound.SOUND_TYPE_CLICK_MOUSE, "assets/enviroment/menu_click.mp3")
engine.set_sound(sound.SOUND_TYPE_KEY_ADDITION, "assets/enviroment/menu_click.mp3")
engine.set_sound(sound.SOUND_TYPE_OPEN_MENU, "assets/enviroment/menu_click.mp3")
engine.set_sound(sound.SOUND_TYPE_WIDGET_SELECTION, "assets/enviroment/menu_click.mp3")
engine.set_sound(sound.SOUND_TYPE_OPEN_MENU, "assets/enviroment/menu_click.mp3")
main_menu.set_sound(engine, recursive=True)

# Adding options to the menu
# main_menu.add.button("Play", main_game(difficulty))
main_menu.add.button('Play', lambda: main_game(difficulty))
main_menu.add.selector(
    "Difficulty:",
    [("Easy", "easy"), ("Medium", "medium"), ("Hard", "hard")],
    onchange=change_difficulty
)
main_menu.add.button("Settings", settings)  # WIP
main_menu.add.button("Quit", pygame_menu.events.EXIT)

main_menu.mainloop(screen)

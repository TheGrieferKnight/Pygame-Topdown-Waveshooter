import pygame
import pygame_menu
from sprites import *
from pygame_menu import Theme
from pygame_menu import sound
from default_settings import *
import main_game
from main_game import player

def main():
    # Initialize pygame
    pygame.init()
    
    # Set the font for the menu
    menu_font = pygame_menu.font.FONT_COMIC_NEUE

    # Initialize the difficulty level
    difficulty = 1

    # Create the Pygame window
    # pygame.display.set_caption("Baller")
    # screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN, display=PYGAME_DISPLAY)
    # clock = pygame.time.Clock()

    # Function to handle settings changes
    def settings():
        print('Tag')
        pass

    # Function to change the difficulty level based on the selected option
    def change_difficulty(prev_value, value):
        global difficulty

        # Set the difficulty level based on the selected option
        if value == "easy":
            difficulty = 1
        elif value == "medium":
            difficulty = 2
        elif value == "hard":
            difficulty = 3

    def play(difficulty):
        main_game.main_game(difficulty)

    # Create the main menu theme
    myimage = pygame_menu.baseimage.BaseImage(
        image_path="assets/enviroment/background.png",
        drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY,
    )

    main_menu_theme = pygame_menu.Theme(
        title_offset=(WIDTH / 2 - 100, 0),
        title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE,
        title_font=menu_font,
        background_color=myimage,
        title_background_color=(255, 0, 0),
        title_font_shadow=False,
        widget_padding=25,
    )

    settings_menu = pygame_menu.Menu("Settings", WIDTH, HEIGHT, theme=main_menu_theme)

    stat_menu = pygame_menu.Menu("Stats",
                                    WIDTH,
                                    HEIGHT,
                                    theme=main_menu_theme)
    stat_menu.add.button("Bullet Damage")

    # Create the main menu
    main_menu = pygame_menu.Menu("Main Menu",
                                 WIDTH,
                                 HEIGHT,
                                 theme=main_menu_theme)

    # Set up the menu sounds
    engine = sound.Sound()
    engine.set_sound(sound.SOUND_TYPE_CLICK_MOUSE,
                     "assets/enviroment/menu_click.mp3")
    engine.set_sound(sound.SOUND_TYPE_KEY_ADDITION,
                     "assets/enviroment/menu_click.mp3")
    engine.set_sound(sound.SOUND_TYPE_OPEN_MENU,
                     "assets/enviroment/menu_click.mp3")
    engine.set_sound(sound.SOUND_TYPE_WIDGET_SELECTION,
                     "assets/enviroment/menu_click.mp3")
    engine.set_sound(sound.SOUND_TYPE_OPEN_MENU,
                     "assets/enviroment/menu_click.mp3")
    main_menu.set_sound(engine, recursive=True)

    # Add options to the menu
    main_menu.add.button('Play', lambda: play(difficulty))
    main_menu.add.button(f"Stats {player.stat_points}", stat_menu)
    main_menu.add.selector("Difficulty:", [("Easy", "easy"),
                                           ("Medium", "medium"),
                                           ("Hard", "hard")],
                           onchange=change_difficulty)
    main_menu.add.menu_link(stat_menu)
    main_menu.add.button("Settings", settings_menu)  # WIP
    main_menu.add.button("Quit", pygame_menu.events.EXIT)

    # Run the main menu loop
    main_menu.mainloop(main_game.screen)


# Run the main function
main()

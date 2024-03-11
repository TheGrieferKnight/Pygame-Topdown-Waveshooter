import pygame_menu
from pygame_menu import sound
from default_settings import WIDTH, HEIGHT
import main_game

main_game.player.stat_points = 100


def main():
    """
    The `main()` function sets up a main menu with options for playing the
    game, adjusting difficulty,
    viewing stats, accessing settings, and quitting the game.
    """

    # Set the font for the menu
    menu_font = pygame_menu.font.FONT_COMIC_NEUE

    # Initialize the difficulty level
    difficulty = [1]

    def change_difficulty(_, value, difficulty_var):
        """
        Callback function to change the difficulty level based on the selected
        option.

        Parameters:
        - _: Placeholder for the first argument (not used).
        - value (str): The selected difficulty option ("easy", "medium", or
            "hard").
        - difficulty_var (list): A mutable list containing the current
            difficulty level.

        Returns:
        None
        """
        options_mapping = {"easy": 1, "medium": 2, "hard": 3}

        # Set the difficulty level based on the selected option
        difficulty_var[0] = options_mapping.get(value, 1)

    def upgrade_stat(stat_name, player_stat_points):
        # Determine the cost of upgrading the specified stat
        upgrade_cost = main_game.player_statss.get_upgrade_cost(stat_name)

        if player_stat_points is not None:

            if player_stat_points >= upgrade_cost:
                # Perform the stat upgrade
                getattr(main_game.player_statss, f"upgrade_{stat_name.replace(
                    ' ', '_').lower()}")()  # Use lowercase
                player_stat_points -= upgrade_cost

                # Update the button text with the new cost
                stat_button = stat_buttons[stat_name]
                stat_button.set_title("Upgrade {} ({} points)".format(
                    stat_name, main_game.player_statss.get_upgrade_cost(
                        stat_name)))
                stat_label = stat_labels[stat_name]
                stat_label.set_title("{}: {}".format(stat_name, getattr(
                    main_game.player_statss, stat_name.replace(' ', '_').lower(
                    ))))

                # Return any relevant information about the upgrade
                return True
            else:
                # Return any relevant information
                return False

    def play(difficulty):
        main_game.main_game(difficulty)

    def stats(_, __):
        # Add stat buttons and labels
        for stat_name in ["Bullet Damage", "Max Health", "Speed"]:
            stat_button = stat_buttons[stat_name]
            stat_button.set_title("Upgrade {} ({} points)".format(
               stat_name, main_game.player_statss.get_upgrade_cost(stat_name)))
            stat_label = stat_labels[stat_name]
            stat_label.set_title("{}: {}".format(stat_name, getattr(
                main_game.player_statss, stat_name.replace(' ', '_').lower())))

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

    # # settings_menu = pygame_menu.Menu("Settings",
    # #                                  WIDTH,
    # #                                  HEIGHT,
    # #                                  theme=main_menu_theme)

    stat_menu = pygame_menu.Menu("Stats", WIDTH, HEIGHT,
                                 theme=main_menu_theme)

    stat_buttons = {}
    stat_labels = {}

    # Add stat buttons and labels
    for stat_name in ["Bullet Damage", "Max Health", "Speed"]:
        stat_label = stat_menu.add.label("{}: {}".format(stat_name, getattr(
            main_game.player_statss, stat_name.replace(' ', '_').lower())))
        stat_button = stat_menu.add.button("Upgrade {} ({} points)".format(
            stat_name, main_game.player_statss.get_upgrade_cost(stat_name)),
                                        lambda name=stat_name: upgrade_stat(
                                           name, main_game.player.stat_points))
        stat_buttons[stat_name] = stat_button
        stat_labels[stat_name] = stat_label

    stat_menu.set_onbeforeopen(stats)

    # Create the main menu
    main_menu = pygame_menu.Menu("Main Menu",
                                 WIDTH,
                                 HEIGHT,
                                 theme=main_menu_theme)

    def reset_stat_labels():
        for stat_name, stat_label in stat_labels.items():
            stat_label.set_title("{}: {}".format(stat_name, getattr(
                main_game.player_statss, stat_name.replace(" ", "_").lower())))

    main_menu.add.menu_link(stat_menu)

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
    main_menu.add.button("Stats", stat_menu)
    main_menu.add.selector(
        "Difficulty:", [("Easy", "easy"), ("Medium", "medium"),
                        ("Hard", "hard")],
        onchange=lambda _, value: change_difficulty(_, value, difficulty))
    # # main_menu.add.button("Settings", settings_menu)  # WIP
    main_menu.add.button("Quit", pygame_menu.events.EXIT)

    # Run the main menu loop
    main_menu.mainloop(main_game.screen)


# Run the main function
main()

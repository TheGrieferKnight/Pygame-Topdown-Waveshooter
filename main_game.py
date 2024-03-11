import pygame
import os
from sprites import sprites_group
from waves import Waves
from default_settings import (PLAYER_START_X, PLAYER_START_Y,
                              PENETRATION_PRICE, SPLIT_SHOT_PRICE,
                              PLAYER_STARTING_HEALTH, FPS)
from player import player, Bullet, background, screen, clock, player_statss
from health_bar import HealthBar, font_upgrades, font
from enemy import Enemy


def reset():
    player.penetrationStatus = True
    player.num_bullets = 1
    player.health = PLAYER_STARTING_HEALTH
    player.money = 0
    player.pos = pygame.Vector2(PLAYER_START_X, PLAYER_START_Y)
    for sprite in sprites_group:
        if isinstance(sprite, Enemy):
            sprite.kill()
        elif isinstance(sprite, Bullet):
            sprite.kill()
    player_statss.reset()


def create_music_queue(folder_path):
    pygame.mixer.pre_init(44100, -16, 2, 1024)
    pygame.mixer.init()

    pygame.mixer.music.load("assets/enviroment/background-music/Event Horizon.mp3")

    file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    if not file_names:
        print("No files found in the folder.")
        return

    for file_name in file_names:
        file_path = os.path.join(folder_path, file_name)
        pygame.mixer.music.queue(file_path)

    pygame.mixer.music.set_endevent(pygame.USEREVENT)

    pygame.mixer.music.set_volume(0.25)

    pygame.mixer.music.play()


def main_game(difficulty):
    """
    Main game function for a Pygame-based wave-shooting game.
    This function initializes and runs the main game loop, handling player
    input, upgrades, health bars, and wave progression.
    Parameters:
        difficulty (int): The difficulty level of the game.
    Returns:
        None
    Note: Ensure that the required classes and variables are properly defined
    before calling this function.
    """

    player.max_health = player_statss.max_health
    player.bullet_damage = player_statss.bullet_damage
    player.speed = player_statss.speed

    # Setup Background Music
    pygame.mixer.pre_init(44100, -16, 2, 1024)
    pygame.mixer.init()

    pygame.mixer.music.load("assets/enviroment/ost.mp3")

    # Convert difficulty from list to integer
    difficulty = int(difficulty[0])

    # Get screen dimensions
    w, h = pygame.display.get_surface().get_size()

    # Initialize waves based on difficulty
    waves = Waves(difficulty)

    # Add player to sprite groups
    sprites_group.add(player)

    # Get scaled prices for player upgrades
    SPLIT_SHOT_PRICE_SCALED = int(SPLIT_SHOT_PRICE[difficulty - 1])
    PENETRATION_PRICE_SCALED = int(PENETRATION_PRICE[difficulty - 1])

    while True:
        # Check for player defeat
        if player.health <= 0:
            pygame.mixer.music.fadeout(1000)
            reset()
            return

        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()

            if event.type == pygame.USEREVENT:  # End event triggered
                pygame.mixer.music.queue(pygame.mixer.music.get_queue())

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Upgrade Split Shot button interaction
            if 5 <= mouse[0] <= 5 + 200 and 50 <= mouse[1] <= 50 + 30:
                pygame.draw.rect(background, 'gray', [5, 50, 200, 30])
            else:
                pygame.draw.rect(background, 'white', [5, 50, 200, 30])

            if 5 <= mouse[0] <= 5 + 200 and 50 <= mouse[1] <= 50 + 30 and \
                    player.money >= SPLIT_SHOT_PRICE_SCALED:

                if event.type == pygame.MOUSEBUTTONDOWN:
                    player.upgrade_split_shot()
                    player.money -= SPLIT_SHOT_PRICE_SCALED
                    SPLIT_SHOT_PRICE_SCALED *= 2

            # Upgrade Penetration button interaction
            if 5 <= mouse[0] <= 5 + 200 and 90 <= mouse[1] <= 90 + 30:
                pygame.draw.rect(background, 'gray', [5, 90, 200, 30])
            else:
                pygame.draw.rect(background, 'white', [5, 90, 200, 30])

            if PENETRATION_PRICE_SCALED is not None:

                if 5 <= mouse[0] <= 5 + 200 and 90 <= mouse[1] <= 90 + 30 and \
                        player.money >= PENETRATION_PRICE_SCALED:

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        player.penetrationStatus = False
                        player.money -= PENETRATION_PRICE_SCALED
                        PENETRATION_PRICE_SCALED = None

        # Initialize health bar
        health_bar = HealthBar(10, h - 50, 300, 40, player.health,
                               player.max_health)

        # Render upgrade texts
        splitshot_text = font_upgrades.render("Splitshot:" +
                                              f"{SPLIT_SHOT_PRICE_SCALED}",
                                              True, 'black')
        penetration_text = font_upgrades.render("Penetration:" +
                                                f"{PENETRATION_PRICE_SCALED}",
                                                True, 'black')
        player_money = font.render('Money: ' + str(round(player.money, 1)),
                                   True, "white")

        # Draw game elements
        screen.blit(background, (0, 0))
        sprites_group.draw(screen)
        screen.blit(health_bar.health_text, (20, h - 37))
        screen.blit(player_money, (5, 5))
        screen.blit(splitshot_text, (10, 58))
        screen.blit(penetration_text, (10, 98))
        health_bar.draw(background)

        # Draw ammo indicators
        for i in range(player.ammo):
            pygame.draw.rect(screen, (255, 0, 0, 1),
                             (w/2 - (10 * (player.max_ammo/2))
                              + ((20 * i) - 15), 50, 10, 40))

        # Update sprites and waves
        sprites_group.update()
        waves.update()
        player.update()

        # Update display
        pygame.display.update()
        clock.tick(FPS)

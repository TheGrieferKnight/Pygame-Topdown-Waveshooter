import pygame
from sprites import sprites_group
from waves import Waves
from default_settings import (PLAYER_START_X, PLAYER_START_Y,
                              PLAYER_STARTING_HEALTH, FPS)
from player import player, Bullet, background, screen, clock, player_statss
from health_bar import HealthBar, font
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

    pygame.mixer.music.play()

    # Convert difficulty from list to integer
    difficulty = int(difficulty[0])

    # Get screen dimensions
    w, h = pygame.display.get_surface().get_size()

    # Initialize waves based on difficulty
    waves = Waves(difficulty)

    # Add player to sprite groups
    sprites_group.add(player)

    while True:
        # Check for player defeat
        if player.health <= 0:
            pygame.mixer.music.fadeout(1000)
            reset()
            return

        for event in pygame.event.get():

            if event.type == pygame.USEREVENT:  # End event triggered
                pygame.mixer.music.queue(pygame.mixer.music.get_queue())

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Initialize health bar
        health_bar = HealthBar(10, h - 50, 300, 40, player.health,
                               player.max_health)

        player_money = font.render('Money: ' + str(round(player.money, 1)),
                                   True, "white")

        # Draw game elements
        screen.blit(background, (0, 0))
        sprites_group.draw(screen)
        screen.blit(health_bar.health_text, (20, h - 37))
        screen.blit(player_money, (5, 5))
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

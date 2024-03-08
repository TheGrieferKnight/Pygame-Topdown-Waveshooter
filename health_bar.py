import pygame
from default_settings import PLAYER_STARTING_HEALTH

font = pygame.font.Font("assets/enviroment/ARCADECLASSIC.TTF", 20)
font_upgrades = pygame.font.Font("assets/enviroment/ARCADECLASSIC.TTF", 12)


class HealthBar():
    """
    HealthBar class for displaying and managing the player's health bar in a Pygame-based game.

    This class provides functionality for rendering and updating a health bar on the game screen.

    Attributes:
        x (int): The x-coordinate of the top-left corner of the health bar.
        y (int): The y-coordinate of the top-left corner of the health bar.
        w (int): The width of the health bar.
        h (int): The height of the health bar.
        player_health (int): The current health points of the player.
        health_text (pygame.Surface): Rendered text displaying the player's health.

    Methods:
        __init__(self, x, y, w, h, player_health): Initializes the HealthBar object with specified parameters.
        draw(self, surface): Draws the health bar on the specified surface with the current health status.

    Note: Ensure that the Pygame library and the default_settings module are properly configured before using this class.
    """
    def __init__(self, x, y, w, h, player_health):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.player_health = player_health
        self.health_text = font.render(str(self.player_health), True, "red")

    def draw(self, surface):
        ratio = self.player_health / PLAYER_STARTING_HEALTH
        pygame.draw.rect(surface, (0, 0, 0, 0.5),
                         (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, (31, 0, 54, 0.5),
                         (self.x, self.y, self.w * ratio, self.h))

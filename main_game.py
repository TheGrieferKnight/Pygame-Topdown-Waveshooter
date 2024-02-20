import pygame
import pygame_menu
import random
from sprites import *
from waves import Waves
from pygame_menu import Theme
from pygame_menu import sound
from default_settings import *
from player import *
from health_bar import *

def main_game(difficulty):
    waves = Waves(difficulty)
    # enemy = Enemy((400, 400))
    # enemy2 = Enemy((-400, -400))

    sprites_group.add(player)
    text_surface = font.render(str(player.health), True, "red")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        print(difficulty)
        health_bar = HealthBar(100, 1020, 300, 40, player.health)
        screen.blit(background, (0, 0))
        sprites_group.draw(screen)
        screen.blit(health_bar.text_surface, (20,1025))
        health_bar.draw(screen)
        sprites_group.update()

        waves.update()
        player.update()
        # Hitbox / Base rectangles
        pygame.draw.rect(screen, "red", player.hitbox, width=2)
        pygame.draw.rect(screen, "yellow", player.rect, width=2)

        pygame.display.update()
        clock.tick(FPS)

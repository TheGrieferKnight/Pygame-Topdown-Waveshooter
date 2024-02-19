import pygame
import pygame_menu
import random
from sprites import *
from enemy import Enemy
from waves import Waves
from pygame_menu import Theme
from pygame_menu import sound
from settings import *
from player import *

def main_game():
    waves = Waves()
    # enemy = Enemy((400, 400))
    # enemy2 = Enemy((-400, -400))

    sprites_group.add(player)
    text_surface = font.render(str(player.health), True, "red")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.blit(background, (0, 0))
        screen.blit(player.health_display, (0, 0))
        sprites_group.draw(screen)
        sprites_group.update()

        waves.update()
        player.update()
        # Hitbox / Base rectangles
        pygame.draw.rect(screen, "red", player.hitbox, width=2)
        pygame.draw.rect(screen, "yellow", player.rect, width=2)

        pygame.display.update()
        clock.tick(FPS)
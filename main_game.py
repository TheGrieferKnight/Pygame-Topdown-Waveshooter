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
from enemy import Enemy

def main_game(difficulty):
    
    waves = Waves(difficulty)
    SPLIT_SHOT_PRICE_SCALED = SPLIT_SHOT_PRICE
    sprites_group.add(player)
    player_money = font.render(str(player.money), True, "white")
    mouse = pygame.mouse.get_pos()
    while True:
        if player.health <= 0:
            player.health = PLAYER_STARTING_HEALTH
            player.money = 0
            for sprite in sprites_group:
                   if isinstance(sprite, Enemy):
                    sprite.kill()
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if 5 <= mouse[0] <= 5 + 140 and 50 <= mouse[1] <= 50 + 40:
                pygame.draw.rect(background, 'gray', [5, 50, 160, 30])
            else:
                pygame.draw.rect(background, 'white', [5, 50, 160, 30])

            if 5 <= mouse[0] <= 5 + 140 and 50 <= mouse[
                    1] <= 50 + 40 and player.money >= SPLIT_SHOT_PRICE_SCALED:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    player.upgrade_split_shot()
                    player.money -= SPLIT_SHOT_PRICE_SCALED
                    SPLIT_SHOT_PRICE_SCALED *= 2
        

        player_money = font.render("Money: " + str(player.money), True,
                                   "white")
        splitshot_text = font_upgrades.render(
            f"Splitshot:" + str(SPLIT_SHOT_PRICE_SCALED), True, 'black')

        w, h = pygame.display.get_surface().get_size()
        screen.blit(background, (0, 0))
        sprites_group.draw(screen)

        health_bar = HealthBar(w - w + 10, h - 50, 300, 40, player.health)    
        screen.blit(health_bar.health_text, (20, h - 35))
        screen.blit(player_money, (5, 5))
        screen.blit(splitshot_text, (10, 58))

        health_bar.draw(background)
        sprites_group.update()
        waves.update()
        player.update()

        pygame.display.update()
        clock.tick(FPS)

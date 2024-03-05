import pygame
import pygame_menu
import random
import sprites
from waves import Waves
from pygame_menu import Theme
from pygame_menu import sound
from default_settings import *
from player import *
from health_bar import *
from enemy import Enemy
import time

def reset():
    player.health = PLAYER_STARTING_HEALTH
    player.money = 0
    player.pos = pygame.Vector2(PLAYER_START_X, PLAYER_START_Y)
    for sprite in sprites_group:
            if isinstance(sprite, Enemy):
                sprite.kill()

def main_game(difficulty):
    w, h = pygame.display.get_surface().get_size()
    waves = Waves(difficulty)
    sprites_group.add(player)
    SPLIT_SHOT_PRICE_SCALED = int(SPLIT_SHOT_PRICE[difficulty-1])
    PENETRATION_PRICE_SCALED = int(PENETRATION_PRICE[difficulty-1]) 
    
    health_bar = HealthBar(w - w + 10, h - 50, 300, 40, player.health)    
    
    while True:
        if player.health <= 0:
            reset()
            return
        
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                

            if 5 <= mouse[0] <= 5 + 140 and 50 <= mouse[1] <= 50 + 40:
                pygame.draw.rect(background, 'gray', [5, 50, 160, 30])
            else:
                pygame.draw.rect(background, 'white', [5, 50, 160, 30])
            if 5 <= mouse[0] <= 5 + 140 and 50 <= mouse[1] <= 50 + 40 and player.money >= SPLIT_SHOT_PRICE_SCALED:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    player.upgrade_split_shot()
                    player.money -= SPLIT_SHOT_PRICE_SCALED
                    SPLIT_SHOT_PRICE_SCALED *= 2
            
            if 5 <= mouse[0] <= 5 + 160 and 90 <= mouse[1] <= 90 + 30:
                pygame.draw.rect(background, 'gray', [5, 90, 160, 30])
            else:
                pygame.draw.rect(background, 'white', [5, 90, 160, 30])
            
            if PENETRATION_PRICE_SCALED != None:
                if 5 <= mouse[0] <= 5 + 160 and 90 <= mouse[1] <= 90 + 30 and player.money >= PENETRATION_PRICE_SCALED:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        player.penetrationStatus = False
                        player.money -= PENETRATION_PRICE_SCALED
                        PENETRATION_PRICE_SCALED = None  
        
        splitshot_text = font_upgrades.render(
            f"Splitshot:" + str(SPLIT_SHOT_PRICE_SCALED), True, 'black')
        player_money = font.render('Money: ' + str(round(player.money,1)), True, "white")
        screen.blit(background, (0, 0))
        sprites.sprites_group.draw(screen)

        screen.blit(health_bar.health_text, (20, h - 37))
        screen.blit(player_money, (5, 5))
        screen.blit(splitshot_text, (10, 58))
        health_bar.draw(background)

        sprites.sprites_group.update()
        waves.update()
        player.update()

        pygame.display.update()
        clock.tick(FPS)

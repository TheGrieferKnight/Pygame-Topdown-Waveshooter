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
    SPLIT_SHOT_PRICE_SCALED = SPLIT_SHOT_PRICE
    # enemy = Enemy((400, 400))
    # enemy2 = Enemy((-400, -400))

    sprites_group.add(player)
    player_money = font.render(str(player.money), True, "white")
    
    while True:
        if player.health <= 0:
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
            if 5 <= mouse[0] <= 5+140 and 50 <= mouse[1] <= 50+40: 
                pygame.draw.rect(background,'gray',[5,50,160,30]) 
            else: 
                pygame.draw.rect(background,'white',[5,50,160,30])    
                
            if 5 <= mouse[0] <= 5+140 and 50 <= mouse[1] <= 50+40 and player.money >= SPLIT_SHOT_PRICE_SCALED:
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    player.upgrade_split_shot()
                    player.money -= SPLIT_SHOT_PRICE_SCALED
                    SPLIT_SHOT_PRICE_SCALED *= 2
                
     
        player_money = font.render("Money: " + str(player.money), True, "white")
        splitshot_text = font_upgrades.render(f"Splitshot:" + str(SPLIT_SHOT_PRICE_SCALED), True, 'black')
        # splitshot_price = font_upgrades.render(, True, "black")
        mouse = pygame.mouse.get_pos() 
        health_bar = HealthBar(100, 1020, 300, 40, player.health)
        
        screen.blit(background, (0, 0))
        sprites_group.draw(screen)
        
        screen.blit(health_bar.health_text, (20,1025))
        screen.blit(player_money,(5,5))
        screen.blit(splitshot_text,(10,58))
        # screen.blit(splitshot_price,(15, 60))
        
        health_bar.draw(screen)
        sprites_group.update()
        waves.update()
        player.update()
        # Hitbox / Base rectangles
        pygame.draw.rect(screen, "red", player.hitbox, width=2)
        pygame.draw.rect(screen, "yellow", player.rect, width=2)

        pygame.display.update()
        clock.tick(FPS)

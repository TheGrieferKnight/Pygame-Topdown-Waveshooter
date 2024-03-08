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
            elif isinstance(sprite, Bullet):
                sprite.kill()
                

def main_game(difficulty):
    """
    Main game function for a Pygame-based wave-shooting game.

    This function initializes and runs the main game loop, handling player input, upgrades, health bars, and wave progression.

    Parameters:
        difficulty (int): The difficulty level of the game.

    Returns:
        None

    Note: Ensure that the required classes and variables are properly defined before calling this function.

    """
    
    # Convert difficulty from string to integer
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
    
    # Initialize health bar
    health_bar = HealthBar(10, h - 50, 300, 40, player.health)    
    
    while True:
        # Check for player defeat
        if player.health <= 0:
            reset()
            return
        
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
            # Upgrade Split Shot button interaction
            if 5 <= mouse[0] <= 5 + 140 and 50 <= mouse[1] <= 50 + 40:
                pygame.draw.rect(background, 'gray', [5, 50, 160, 30])
            else:
                pygame.draw.rect(background, 'white', [5, 50, 160, 30])
            
            if 5 <= mouse[0] <= 5 + 140 and 50 <= mouse[1] <= 50 + 40 and player.money >= SPLIT_SHOT_PRICE_SCALED:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    player.upgrade_split_shot()
                    player.money -= SPLIT_SHOT_PRICE_SCALED
                    SPLIT_SHOT_PRICE_SCALED *= 2
            
            # Upgrade Penetration button interaction
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
        
        # Render upgrade texts
        splitshot_text = font_upgrades.render(f"Splitshot: {SPLIT_SHOT_PRICE_SCALED}", True, 'black')
        player_money = font.render('Money: ' + str(round(player.money, 1)), True, "white")
        
        # Draw game elements
        screen.blit(background, (0, 0))
        sprites.sprites_group.draw(screen)
        screen.blit(health_bar.health_text, (20, h - 37))
        screen.blit(player_money, (5, 5))
        screen.blit(splitshot_text, (10, 58))
        health_bar.draw(background)
        
        # Draw ammo indicators
        for i in range(player.ammo):
            pygame.draw.rect(screen, (255, 0, 0, 1), (w/2 - (10 * (player.max_ammo/2)) + ((20 * i) - 15), 50, 10, 40))
        
        # Update sprites and waves
        sprites.sprites_group.update()
        waves.update()
        player.update()
        
        # Update display
        pygame.display.update()
        clock.tick(FPS)
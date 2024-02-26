import pygame
from default_settings import *
from player import *

# Split Shot Upgrade
def upgrade_split_shot(mouse, SPLIT_SHOT_PRICE_SCALED):
    if 5 <= mouse[0] <= 5 + 160 and 50 <= mouse[1] <= 50 + 30:
        pygame.draw.rect(background, 'gray', [5, 50, 160, 30])
    else:
        pygame.draw.rect(background, 'white', [5, 50, 160, 30])

    if 5 <= mouse[0] <= 5 + 160 and 90 <= mouse[1] <= 50 + 30 and player.money >= int(SPLIT_SHOT_PRICE_SCALED):
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.upgrade_split_shot()
            player.money -= int(SPLIT_SHOT_PRICE_SCALED)
            SPLIT_SHOT_PRICE_SCALED *= 2
        
# Penetration Upgrade         
def upgrade_penetration(mouse, PENETRATION_PRICE_SCALED):
    if 5 <= mouse[0] <= 5 + 160 and 90 <= mouse[1] <= 90 + 30:
        pygame.draw.rect(background, 'gray', [5, 90, 160, 30])
    else:
        pygame.draw.rect(background, 'white', [5, 90, 160, 30])

    if 5 <= mouse[0] <= 5 + 160 and 90 <= mouse[1] <= 90 + 30 and player.money >= PENETRATION_PRICE_SCALED:
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.penetrationStatus = False
            player.money -= PENETRATION_PRICE_SCALED
            PENETRATION_PRICE_SCALED = None
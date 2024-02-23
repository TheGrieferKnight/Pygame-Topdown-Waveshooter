import pygame
from default_settings import PLAYER_STARTING_HEALTH

font = pygame.font.Font("assets\enviroment\ARCADECLASSIC.TTF", 30)

class HealthBar():
  def __init__(self, x, y, w, h, player_health):
    self.x = x
    self.y = y
    self.w = w
    self.h = h
    self.player_health = player_health
    self.health_text = font.render(str(self.player_health), True, "red")

  def draw(self, surface):
    #calculate health ratio
    if  self.player_health <= 0:
      return
    ratio = self.player_health / PLAYER_STARTING_HEALTH
    pygame.draw.rect(surface, (0, 0, 0, 0.5), (self.x, self.y, self.w, self.h))
    pygame.draw.rect(surface, (31, 0, 54, 0.5), (self.x, self.y, self.w * ratio, self.h))

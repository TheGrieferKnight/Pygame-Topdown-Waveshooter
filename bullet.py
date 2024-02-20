import pygame
import pygame_menu
import math
from default_settings import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.image.load("assets/player/bullet.png")
        self.image = pygame.transform.rotozoom(self.image, 0, BULLET_SIZE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = BULLET_SPEED
        self.angle = angle
        self.x = x
        self.y = y
        self.x_vel = math.cos(self.angle * (2 * math.pi / 360)) * self.speed
        self.y_vel = math.sin(self.angle * (2 * math.pi / 360)) * self.speed
        self.lifetime = BULLET_LIFETIME
        self.spawn_time = pygame.time.get_ticks()
        self.damage = 50

    def bullet_movement(self):
        self.x += self.x_vel
        self.y += self.y_vel

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()

    def update(self):
        self.bullet_movement()

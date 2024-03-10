import math
import pygame
from default_settings import BULLET_SPEED, BULLET_LIFETIME, BULLET_SIZE


class Bullet(pygame.sprite.Sprite):
    """
    A class representing a bullet in the game.
    Attributes:
    - image (pygame.Surface): The image of the bullet.
    - rect (pygame.Rect): The rectangular area that represents the position
      and size of the bullet.
    - speed (float): The speed of the bullet.
    - angle (float): The angle at which the bullet is fired.
    - x (float): The x-coordinate of the bullet's current position.
    - y (float): The y-coordinate of the bullet's current position.
    - x_vel (float): The x-component of the bullet's velocity.
    - y_vel (float): The y-component of the bullet's velocity.
    - lifetime (int): The maximum time the bullet is allowed to exist (in
      milliseconds).
    - spawn_time (int): The time at which the bullet was spawned
      (in milliseconds).
    - damage (int): The damage inflicted by the bullet upon hitting a target.
    Methods:
    - bullet_movement(): Updates the bullet's position based on its velocity
      and checks if it exceeds its lifetime.
    - update(): Calls the bullet_movement() method to update the bullet's
      position.
    Parameters:
    - x (int): The initial x-coordinate of the bullet's spawn position.
    - y (int): The initial y-coordinate of the bullet's spawn position.
    - angle (float): The angle at which the bullet is fired (in degrees).
    """
    def __init__(self, x, y, angle, damage):
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
        self.damage = damage

    def bullet_movement(self):
        """
        Updates the bullet's position based on its velocity and checks if it
        exceeds its lifetime.
        If the bullet exceeds its lifetime, it is marked for removal.
        """
        self.x += self.x_vel
        self.y += self.y_vel
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()

    def update(self):
        """
        Calls the bullet_movement() method to update the bullet's position.
        """
        self.bullet_movement()

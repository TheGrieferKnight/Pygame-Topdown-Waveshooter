import pygame
import math
import time
from default_settings import *
from sprites import *
from player import *
from bullet import *
from round_if_not_float import round_if_not_float

class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__(enemy_group, sprites_group)
        self.image = pygame.image.load("assets/enemy/enemy.png")
        self.image = pygame.transform.rotozoom(self.image, 0, ENEMY_SIZE)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.x = position[0]
        self.y = position[1]
        self.direction = pygame.math.Vector2()
        self.velocity = pygame.math.Vector2()
        self.position = pygame.math.Vector2(position)
        self.damage_cd = ENEMY_BASE_SPAWN_COOLDOWN
        self.health = ENEMY_BASE_HEALTH
        self.damage = ENEMY_BASE_DAMAGE
        self.speed = ENEMY_BASE_SPEED
        self.count = 0

    def pathing(self):
        player_vector = pygame.math.Vector2(player.hitbox.center)
        enemy_vector = pygame.math.Vector2(self.rect.center)
        distance = (player_vector - enemy_vector).magnitude()

        if not pygame.sprite.collide_rect(self, player):
            self.direction = (player_vector - enemy_vector).normalize()
            self.timer = 0
            self.damage_applied = False
        else:
            self.count += 1
            self.direction = pygame.math.Vector2()
            if self.count == 1:
                self.timer = time.time()
                self.damage_applied = False

            if not self.damage_applied and (time.time() - self.timer) >= self.damage_cd:
                player.health -= self.damage
                self.count = 0
                self.damage_applied = True

        self.velocity = self.direction * self.speed
        self.position += self.velocity

        self.rect.centerx = self.position.x
        self.rect.centery = self.position.y

    def hit(self):
        bullet_hit = pygame.sprite.spritecollide(self, bullet_sprites_group, True)
        for bullet in bullet_hit:
            self.health -= bullet.damage

    def death(self):
        if self.health == 0 or self.health < 0:
            player.money += 1
            self.kill()

    def update(self):
        self.pathing()
        self.hit()
        self.death()

    def calculate_distance(self, vector_1, vector_2):
        return vector

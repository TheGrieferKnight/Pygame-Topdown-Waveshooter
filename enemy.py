import pygame
import math
import time
from settings import *
from sprites import *
from player import *
from bullet import *
from round_if_not_float import round_if_not_float

enemy_counter = 0
difficulty = 10

class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__(enemy_group, sprites_group)
        self.image = pygame.image.load("assets/enemy/enemy.png")
        self.image = pygame.transform.rotozoom(self.image, 0, ENEMY_SIZE)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.speed = ENEMY_SPEED + enemy_counter * difficulty * 0.1
        self.x = position[0]
        self.y = position[1]
        self.direction = pygame.math.Vector2()
        self.velocity = pygame.math.Vector2()
        self.position = pygame.math.Vector2(position)
        self.damage_cd = DAMAGE_CD
        self.count = 0
        self.health = 100 + enemy_counter * difficulty * 5
        self.damage = 10 + enemy_counter * difficulty * 0.5

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
                player.health = round_if_not_float(player.health)
                player.health_display = font.render(str(player.health), True, "red")

        self.velocity = self.direction * self.speed
        self.position += self.velocity

        self.rect.centerx = self.position.x
        self.rect.centery = self.position.y

    def hit(self):
        bullet_hit = pygame.sprite.spritecollide(self, bullet_sprites_group, True)
        for bullet in bullet_hit:
            self.health -= bullet.damage

    def death(self, enemy_counter1):
        if self.health == 0 or self.health < 0:
            self.kill()
            global enemy_counter
            enemy_counter = enemy_counter1 + 1

    def update(self):
        self.pathing()
        self.hit()
        self.death(enemy_counter)

    def calculate_distance(self, vector_1, vector_2):
        return vector

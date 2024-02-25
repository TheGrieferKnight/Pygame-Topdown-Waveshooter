import math

import random

import pygame

from pygame.locals import *

from pygame.math import Vector2

from pygame.sprite import Sprite, Group

from bullet import Bullet

from default_settings import *

from sprites import sprites_group, player_group, bullet_sprites_group

clock = pygame.time.Clock()

# Create Pygame Window
screen = pygame.display.set_mode((WIDTH, HEIGHT), display=PYGAME_DISPLAY)
background = pygame.transform.scale(
    pygame.image.load("assets/enviroment/background.png").convert(),
    (WIDTH, HEIGHT))

pygame.init()
pygame.font.init()
font = pygame.font.Font("assets\enviroment\ARCADECLASSIC.TTF", 30)


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__(sprites_group, player_group)
        self.pos = pygame.Vector2(PLAYER_START_X, PLAYER_START_Y)
        self.image_1 = pygame.transform.rotozoom(
            pygame.image.load("assets/player/sprite.png").convert_alpha(),
            0,
            PLAYER_SIZE,
        )
        self.image = pygame.transform.rotate(self.image_1, -90)
        self.base = self.image
        self.hitbox = self.base.get_rect(center=self.pos)
        self.rect = self.hitbox.copy()
        self.speed = PLAYER_SPEED
        self.shoot = False
        self.shot_cd = 0
        self.barrel = pygame.math.Vector2(40, -5)
        self.health = PLAYER_STARTING_HEALTH
        self.health_display = font.render(str(self.health), True, "red")
        self.num_bullets = 1
        self.money = 0
        self.shot_sound = pygame.mixer.Sound("assets\player\shot_sound.mp3")
        self.shot_sound.set_volume(0.1)

    def player_rotation(self):
        self.mouse_cords = pygame.mouse.get_pos()
        self.x_diff_mouse_player = self.mouse_cords[0] - self.hitbox.centerx
        self.y_diff_mouse_player = self.mouse_cords[1] - self.hitbox.centery
        self.angle = math.degrees(
            math.atan2(self.y_diff_mouse_player, self.x_diff_mouse_player))
        self.image = pygame.transform.rotate(self.base, -self.angle)
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def player_input(self):
        self.velocity_x = 0
        self.velocity_y = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.velocity_y = -self.speed
        if keys[pygame.K_s]:
            self.velocity_y = self.speed
        if keys[pygame.K_a]:
            self.velocity_x = -self.speed
        if keys[pygame.K_d]:
            self.velocity_x = self.speed

        # Check for diagonal movement
        if self.velocity_x != 0 and self.velocity_y != 0:
            self.velocity_x /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)

        if keys[pygame.K_SPACE]:
            self.shoot = True
            self.shooting(self.num_bullets)
        else:
            self.shoot = False

    def shooting(self, num_bullets=1):
        if self.shot_cd == 0:
            self.shot_cd = SHOT_CD_0
            SPLIT_SHOT_ANGLE = 360 / num_bullets
            bullet_spawn_pos = self.pos + self.barrel.rotate(self.angle)
            pygame.mixer.Sound.play(self.shot_sound, fade_ms=100)
            for i in range(num_bullets):
                bullet_angle = self.angle - (
                    i - num_bullets // 2) * SPLIT_SHOT_ANGLE
                self.bullet = Bullet(bullet_spawn_pos[0], bullet_spawn_pos[1],
                                     bullet_angle)
                bullet_sprites_group.add(self.bullet)
                sprites_group.add(self.bullet)

    def upgrade_split_shot(self):
        player.num_bullets += 1

    def move(self):
        self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)
        self.hitbox.center = self.pos
        self.rect.center = self.hitbox.center

    def death(self):
        if self.health == 0 or self.health < 0:
            self.kill()

    def update(self):
        self.player_input()
        self.move()
        self.player_rotation()
        self.death()

        if self.shot_cd > 0:
            self.shot_cd -= 1


player = Player()

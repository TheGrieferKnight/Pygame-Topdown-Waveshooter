import math

import random

import pygame

from pygame.locals import *

from pygame.math import Vector2

from pygame.sprite import Sprite, Group

from bullet import Bullet

from default_settings import WIDTH, HEIGHT, PLAYER_START_X, PLAYER_START_Y, PLAYER_SPEED, PLAYER_BASE_AMMOCOUNT, PLAYER_STARTING_HEALTH, PYGAME_DISPLAY, PLAYER_SIZE, SHOT_CD_0

from sprites import sprites_group, player_group, bullet_sprites_group

clock = pygame.time.Clock()

# Create Pygame Window
screen = pygame.display.set_mode((WIDTH, HEIGHT), display=PYGAME_DISPLAY)
background = pygame.transform.scale(
    pygame.image.load("assets/enviroment/background.png").convert(),
    (WIDTH, HEIGHT))

pygame.init()
pygame.display.toggle_fullscreen()
pygame.font.init()
font = pygame.font.Font("assets/enviroment/ARCADECLASSIC.TTF", 30)

class Player(pygame.sprite.Sprite):
    """
    Player class for a Pygame-based wave-shooting game.

    This class represents the player character and includes attributes and methods for player movement, shooting, upgrades, and health management.

    Attributes:
        pos (pygame.Vector2): The position vector of the player.
        image_1 (pygame.Surface): Original image of the player.
        image (pygame.Surface): Rotated image of the player.
        base (pygame.Surface): Base image of the player.
        hitbox (pygame.Rect): Rectangle representing the player's hitbox.
        rect (pygame.Rect): Rectangle representing the player's position on the screen.
        speed (int): Movement speed of the player.
        shoot (bool): Flag indicating whether the player is shooting.
        shot_cd (int): Cooldown between shots.
        barrel (pygame.math.Vector2): Vector representing the barrel position for shooting.
        health (int): Current health points of the player.
        health_display (pygame.Surface): Rendered text displaying the player's health.
        num_bullets (int): Number of bullets shot per firing instance.
        money (float): Player's money or currency.
        shot_sound (pygame.mixer.Sound): Sound effect for player shots.
        penetrationStatus (bool): Flag indicating whether player bullets penetrate targets.
        max_ammo (int): Maximum ammo capacity.
        ammo (int): Current ammo count.
        timer (int): Timer for various cooldowns and actions.
        stat_points (int): Points for player statistics or upgrades.

    Methods:
        player_rotation(self): Rotates the player's image based on the mouse position.
        player_input(self): Handles player input for movement and shooting.
        shooting(self, num_bullets=1): Initiates the shooting mechanism for the player.
        reload(self): Reloads the player's ammo after a cooldown.
        upgrade_split_shot(self): Upgrades the player's split-shot ability.
        move(self): Updates the player's position based on velocity.
        death(self): Handles player death conditions.
        update(self): Updates player actions and conditions.

    Note: Ensure that the required classes and variables are properly defined before creating an instance of this class.
    """
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
        self.shot_sound = pygame.mixer.Sound("assets/player/shot_sound.ogg")
        self.shot_sound.set_volume(0.1)
        self.penetrationStatus = True
        self.max_ammo = PLAYER_BASE_AMMOCOUNT
        self.ammo = PLAYER_BASE_AMMOCOUNT
        self.timer = pygame.time.get_ticks()
        self.stat_points = 0
        self.bullet = None
    
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

        # if keys[pygame.K_ESCAPE]:
        #     pause = True
        #     while pause == True:
        #         keys = pygame.key.get_pressed()
        #         if keys[pygame.K_f]:
        #             pause = False

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
        if (pygame.time.get_ticks() - self.timer) >= SHOT_CD_0 and self.ammo > 0:
            self.shot_cd = SHOT_CD_0
            self.timer = pygame.time.get_ticks()
            self.ammo -= 1
            SPLIT_SHOT_ANGLE = 360 / num_bullets
            bullet_spawn_pos = self.pos + self.barrel.rotate(self.angle)
            pygame.mixer.Sound.stop(self.shot_sound)
            pygame.mixer.Sound.play(self.shot_sound, fade_ms=100)
            for i in range(num_bullets):
                # TODO: #1 Work on angle to be infront of player only
                bullet_angle = self.angle - (
                    i - num_bullets // 2) * SPLIT_SHOT_ANGLE
                self.bullet = Bullet(bullet_spawn_pos[0], bullet_spawn_pos[1],
                                        bullet_angle)
                bullet_sprites_group.add(self.bullet)
                sprites_group.add(self.bullet)
                
    def reload(self):
        if self.ammo < self.max_ammo and (pygame.time.get_ticks() - self.timer) >= SHOT_CD_0 * 3:
            self.timer = pygame.time.get_ticks()
            self.ammo += 1

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
        self.reload()
        self.death()

        if self.shot_cd > 0:
            self.shot_cd -= 1


player = Player()

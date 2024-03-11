import time
import pygame
from random import randint
from default_settings import (
    ENEMY_BASE_DAMAGE,
    ENEMY_BASE_HEALTH,
    ENEMY_BASE_SPEED,
    ENEMY_SIZE,
    PLAYER_HIT_INTERVAL
)
from sprites import enemy_group, sprites_group, bullet_sprites_group
from player import player


class Enemy(pygame.sprite.Sprite):
    """
    This module defines the Enemy class for a game, which is a subclass of
    pygame.sprite.Sprite.
    The Enemy class represents an enemy character in the game, with attributes
    such as health, damage, speed,
    and a method for pathing towards the player. It also includes methods for
    handling hits from bullets,
    death conditions, and updating the enemy's state.
    Attributes:
        image (pygame.Surface): The image of the enemy.
        rect (pygame.Rect): The rectangular area of the enemy.
        x (int): The x-coordinate of the enemy's position.
        y (int): The y-coordinate of the enemy's position.
        direction (pygame.math.Vector2): The direction the enemy is moving
            towards.
        velocity (pygame.math.Vector2): The speed and direction of the enemy's
            movement.
        position (pygame.math.Vector2): The current position of the enemy.
        health (int): The health of the enemy.
        damage (int): The damage the enemy can inflict on the player.
        speed (int): The speed at which the enemy moves.
        worth (int): The amount of money the player earns upon defeating the
            enemy.
        count (int): A counter used for timing the enemy's attack.
        hit_interval (float): The interval between each hit the enemy can
            apply to the player.
        last_bullet (pygame.sprite.Sprite): The last bullet that hit the enemy.
    Methods:
        __init__(self, position): Initializes the enemy with a given position.
        pathing(self): Calculates the enemy's path towards the player.
        hit(self): Handles the enemy being hit by a bullet.
        death(self): Handles the enemy's death, including updating the
            player's money and stats.
        update(self): Updates the enemy's state, including pathing, handling
            hits, and checking for death.
        calculate_distance(self, vector_1, vector_2): Calculates the distance
            between two vectors.
    """
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
        self.health = ENEMY_BASE_HEALTH
        self.damage = ENEMY_BASE_DAMAGE
        self.speed = ENEMY_BASE_SPEED
        self.worth = 10
        self.count = 0
        self.hit_interval = PLAYER_HIT_INTERVAL
        self.last_bullet = None
        self.rotation_angle = 0
        self.rotated_images = []
        self.pre_render_images()

    def pre_render_images(self):
        """
        Pre-renders rotated images and stores them in a list.
        """
        angles = range(0, 360, 5)

        for angle in angles:
            rotated_image = pygame.transform.rotozoom(self.image, -angle, 1)
            self.rotated_images.append(rotated_image)

    def rotate(self):
        """
        Continuously updates the rotation angle for the enemy.
        """
        self.rotation_angle += 1  # You can adjust the rotation speed here
        rotated_index = int(self.rotation_angle) % len(self.rotated_images)
        self.image = self.rotated_images[rotated_index]
        self.rect = self.image.get_rect(center=self.rect.center)

    def pathing(self):
        """
        This function calculates updates the enemy's
        direction and position based on the player's location, and applies
        damage to the player if they
        collide.
        """
        player_vector = pygame.math.Vector2(player.hitbox.center)
        enemy_vector = pygame.math.Vector2(self.rect.center)

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
            if (not self.damage_applied) and (time.time() -
                                              self.timer) >= self.hit_interval:
                player.health -= self.damage
                self.count = 0
                self.damage_applied = True

        self.velocity = self.direction * self.speed
        self.position += self.velocity
        self.rect.centerx = self.position.x
        self.rect.centery = self.position.y
        self.rotate()

    def hit(self):
        """
        This function checks for collisions between the player object and
        bullets, deducting health based
        on the damage of the bullets.
        """
        bullet_hit = pygame.sprite.spritecollide(self, bullet_sprites_group,
                                                 player.penetrationStatus)
        for bullet in bullet_hit:
            if bullet != self.last_bullet:
                self.health -= player.bullet_damage
                self.last_bullet = bullet

    def death(self):
        """
        This function checks if a character's health is zero or less, and if
        so, adds their worth to the
        player's money and potentially increases the player's stat points.
        """
        chance = randint(0, 10)

        if self.health <= 0:
            player.money = round(player.money + self.worth, 2)

            if chance == 10:
                player.stat_points += 1

            self.kill()

    def update(self):
        self.pathing()
        self.hit()
        self.death()

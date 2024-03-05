import pygame
import random
from default_settings import (
    ENEMY_BASE_SPAWN_COOLDOWN,
    ENEMY_BASE_DAMAGE,
    WIDTH,
    HEIGHT,
)
from enemy import Enemy


class Waves:

    def __init__(self, difficulty):
        super().__init__()
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_cd = ENEMY_BASE_SPAWN_COOLDOWN
        self.enemy_counter = 0
        self.spawn_multiplier = 0.009
        self.difficulty = difficulty
        self.enemy_counter = 0
        
        if self.difficulty == 1:
            self.spawn_multiplier = 1.0125
        elif self.difficulty == 2:
            self.spawn_multiplier = 1.025
        elif self.difficulty == 3:
            self.spawn_multiplier = 1.05

    def spawn_enemy(self):

        x = random.randint(0, WIDTH)

        y = random.randint(0, HEIGHT)

        enemy = Enemy((x, y))

        # Adjust enemy properties based on the enemy_counter

        base_health = (
            100 + 2 * self.enemy_counter
        )  # Base health starts at 100 and increases by 2 per enemy_counter

        base_speed = (
            2 + 0.02 * self.enemy_counter
        )  # Base speed starts at 2 and increases by 0.02 per enemy_counter

        base_worth = (
            1 + 0.1 * self.enemy_counter
        )  # Base worth starts at 1000 and increases by 100 per enemy_counter

        self.enemy_counter += 1

        enemy.speed = base_speed

        enemy.damage = ENEMY_BASE_DAMAGE

        enemy.health = base_health

        if self.enemy_counter % 10 == 0 and self.spawn_cd > 400:
            self.spawn_cd -= 300

    def update(self):
        if (pygame.time.get_ticks() - self.last_spawn_time) >= self.spawn_cd:
            self.last_spawn_time = pygame.time.get_ticks()
            self.spawn_enemy()

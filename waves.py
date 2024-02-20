import pygame
import random
from default_settings import ENEMY_BASE_SPAWN_COOLDOWN, ENEMY_BASE_SPEED, ENEMY_BASE_HEALTH, ENEMY_BASE_DAMAGE
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

    def check_difficulty(self):
        if difficulty == 1:
            self.spawn_multiplier = 1.0125
        elif difficulty == 2:
            self.spawn_multiplier = 1.025
        elif difficulty == 3:
            self.spawn_multiplier = 1.05

    def spawn_enemy(self):
        x = random.randint(0, 1920)
        y = random.randint(0, 1080)
        enemy = Enemy((x, y))
        self.enemy_counter += 1
        enemy.speed = ENEMY_BASE_SPEED + self.enemy_counter * self.difficulty * self.spawn_multiplier
        enemy.damage = int(ENEMY_BASE_DAMAGE + self.enemy_counter * self.difficulty * self.spawn_multiplier)
        enemy.health = ENEMY_BASE_HEALTH + self.enemy_counter * self.difficulty * self.spawn_multiplier
        self.spawn_cd = ENEMY_BASE_SPAWN_COOLDOWN - self.enemy_counter * self.difficulty * 1
        print(
            f"Spawn CD: {self.spawn_cd}; Enemy Counter: {self.enemy_counter}; Difficulty: {self.difficulty}"
        )

    def update(self):
        if (pygame.time.get_ticks() - self.last_spawn_time) >= self.spawn_cd:
            self.last_spawn_time = pygame.time.get_ticks()
            self.spawn_enemy()

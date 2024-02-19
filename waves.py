import pygame
import random
from settings import SPAWN_CD
from enemy import Enemy


class Waves:
    def __init__(self):
        super().__init__()
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_cd = SPAWN_CD
        self.enemy_counter = 0
        self.spawn_multiplier = 0.009
        self.health_threshhold = 30

    def check_difficulty(self):
        if difficulty == 1:
            self.spawn_multiplier = 1.0125
            self.health_threshhold = 30
        elif difficulty == 2:
            self.spawn_multiplier = 1.025
            self.health_threshhold = 20
        elif difficulty == 3:
            self.spawn_multiplier = 1.05
            self.health_threshhold = 10

    def spawn_enemy(self):
        x = random.randint(0, 1920)
        y = random.randint(0, 1080)
        enemy = Enemy((x, y))
        enemy.health = 100 + enemy_counter * self.spawn_multiplier * difficulty
        self.spawn_cd -= enemy_counter * difficulty * 100
        print(
            f"Spawn CD: {self.spawn_cd}; Enemy Counter: {enemy_counter}; Difficulty: {difficulty}"
        )

    def update(self):
        self.check_difficulty()
        if (pygame.time.get_ticks() - self.last_spawn_time) >= self.spawn_cd:
            self.last_spawn_time = pygame.time.get_ticks()
            self.spawn_enemy()

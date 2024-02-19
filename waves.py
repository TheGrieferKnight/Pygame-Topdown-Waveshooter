import pygame
import random
from enemy import Enemy

enemy = Enemy()

class Waves:
    def __init__(self):
        super().__init__()
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_cd = 3000
        self.enemy_counter = 0
        self.spawn_multiplier = 0.009
        
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
        Enemy((x, y))

    def update(self):
        if (pygame.time.get_ticks() - self.last_spawn_time) >= self.spawn_cd:
            self.last_spawn_time = pygame.time.get_ticks()
            self.spawn_enemy()
            self.enemy_counter += 1

            if self.enemy_counter % self.health_threshhold == 1:
                enemy.health += 1
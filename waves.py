import pygame
import random
from enemy import Enemy

class Waves:
    def __init__(self):
        super().__init__()
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_cd = 3000
        self.enemy_counter = 0

    def check_difficulty(self):
        pass

    def spawn_enemy(self):
        x = random.randint(0, 1920)
        y = random.randint(0, 1080)
        Enemy((x, y))

    def update(self):
        if (pygame.time.get_ticks() - self.last_spawn_time) >= self.spawn_cd:
            self.last_spawn_time = pygame.time.get_ticks()
            self.spawn_enemy()
            self.enemy_counter += 1

            if self.enemy_counter >= 50:
                Enemy.kill()
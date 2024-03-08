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
    """
    Waves class for managing enemy wave spawning in a Pygame-based shooting game.

    This class handles the timing and properties of enemy wave spawns based on the game difficulty.

    Attributes:
        last_spawn_time (int): Time of the last enemy spawn.
        spawn_cd (int): Cooldown duration between enemy spawns.
        enemy_counter (int): Counter tracking the number of spawned enemies.
        spawn_multiplier (float): Multiplier affecting enemy spawn rates.
        difficulty (int): Difficulty level of the game.

    Methods:
        __init__(self, difficulty): Initializes the Waves object with specified difficulty and initial values.
        spawn_enemy(self): Spawns an enemy at a random location with adjusted properties based on the enemy counter.
        update(self): Updates the enemy wave, checking for cooldown and triggering enemy spawns.

    Note: Ensure that the required classes and variables are properly defined before creating an instance of this class.
    """

    def __init__(self, difficulty):
        super().__init__()
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_cd = ENEMY_BASE_SPAWN_COOLDOWN
        self.enemy_counter = 0
        self.spawn_multiplier = 0.009
        self.difficulty = difficulty
        
        # Adjusted spawn_multiplier based on difficulty for more granular control
        if self.difficulty == 1:
            self.spawn_multiplier = 1.0125
        elif self.difficulty == 2:
            self.spawn_multiplier = 1.025
        elif self.difficulty == 3:
            self.spawn_multiplier = 1.05

    def spawn_enemy(self):
        """
        Spawns an enemy at a random location with adjusted properties based on the enemy counter.
        """
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        enemy = Enemy((x, y))

        # Adjust enemy properties based on the enemy_counter and difficulty
        base_health = 100 + int(2 * self.spawn_multiplier * self.enemy_counter)
        base_speed = 2 + (0.02 * self.spawn_multiplier * self.enemy_counter)
        base_worth = 1 + (0.1 * self.spawn_multiplier * self.enemy_counter)

        self.enemy_counter += 1

        enemy.speed = base_speed
        enemy.damage = ENEMY_BASE_DAMAGE
        enemy.health = base_health

        # Increase spawn rate every 10 enemies, with a cooldown reduction
        if self.enemy_counter % 10 == 0 and self.spawn_cd > 400:
            self.spawn_cd -= 300

    def update(self):
        """
        Updates the enemy wave, checking for cooldown and triggering enemy spawns.
        """
        if (pygame.time.get_ticks() - self.last_spawn_time) >= self.spawn_cd:
            self.last_spawn_time = pygame.time.get_ticks()
            self.spawn_enemy()
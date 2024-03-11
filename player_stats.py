from default_settings import (BASE_BULLET_DAMAGE, PLAYER_STARTING_HEALTH,
                              PLAYER_SPEED)


class Stats:
    def __init__(self):
        self.reset()

    def reset(self):
        self.bullet_damage = BASE_BULLET_DAMAGE
        self.max_health = PLAYER_STARTING_HEALTH
        self.speed = PLAYER_SPEED
        self.upgrade_cost_bullet_damage = 1
        self.upgrade_cost_max_health = 1
        self.upgrade_cost_speed = 1

    def upgrade_bullet_damage(self):
        if self.upgrade_cost_bullet_damage == 5:
            return

        self.bullet_damage += 25
        self.upgrade_cost_bullet_damage += 1

    def upgrade_max_health(self):
        if self.upgrade_cost_max_health == 5:
            return
        self.max_health += 25
        self.upgrade_cost_max_health += 1

    def upgrade_speed(self):
        if self.upgrade_cost_speed == 5:
            return

        self.speed += 1
        self.upgrade_cost_speed += 1

    def upgrade_stat(self, stat_name):
        if stat_name == "Bullet Damage":  # Use lowercase
            self.upgrade_bullet_damage()

        if stat_name == "Max Health":
            self.upgrade_max_health()

        if stat_name == "Speed":
            self.upgrade_speed()

    def get_upgrade_cost(self, stat_name):
        if stat_name == "Bullet Damage":  # Use lowercase
            return self.upgrade_cost_bullet_damage

        if stat_name == "Max Health":  # Use lowercase
            return self.upgrade_cost_max_health

        if stat_name == "Speed":  # Use lowercase
            return self.upgrade_cost_speed

import pygame
import pygame_menu
import math
import time
import random
from pygame_menu import Theme
from pygame_menu import sound
from settings import *

pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Comic Sans MS", 30)
menu_font = pygame_menu.font.FONT_COMIC_NEUE

# Create Pygame Window
pygame.display.set_caption("Baller")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Loading images
background = pygame.transform.scale(
    pygame.image.load("background.png").convert(), (WIDTH, HEIGHT)
)



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(sprites_group, player_group)
        self.pos = pygame.Vector2(PLAYER_START_X, PLAYER_START_Y)
        self.image_1 = pygame.transform.rotozoom(
            pygame.image.load("sprite.png").convert_alpha(), 0, PLAYER_SIZE
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

    def player_rotation(self):
        self.mouse_cords = pygame.mouse.get_pos()
        self.x_diff_mouse_player = self.mouse_cords[0] - self.hitbox.centerx
        self.y_diff_mouse_player = self.mouse_cords[1] - self.hitbox.centery
        self.angle = math.degrees(
            math.atan2(self.y_diff_mouse_player, self.x_diff_mouse_player)
        )
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
            self.shooting()
        else:
            self.shoot = False

    def shooting(self):
        if self.shot_cd == 0:
            self.shot_cd = SHOT_CD_0
            bullet_spawn_pos = self.pos + self.barrel.rotate(self.angle)
            self.bullet = Bullet(bullet_spawn_pos[0], bullet_spawn_pos[1], self.angle)
            bullet_sprites_group.add(self.bullet)
            sprites_group.add(self.bullet)

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


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.image.load("pewpew.png")
        self.image = pygame.transform.rotozoom(self.image, 0, BULLET_SIZE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = BULLET_SPEED
        self.angle = angle
        self.x = x
        self.y = y
        self.x_vel = math.cos(self.angle * (2 * math.pi / 360)) * self.speed
        self.y_vel = math.sin(self.angle * (2 * math.pi / 360)) * self.speed
        self.lifetime = BULLET_LIFETIME
        self.spawn_time = pygame.time.get_ticks()

    def bullet_movement(self):
        self.x += self.x_vel
        self.y += self.y_vel

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()

    def update(self):
        self.bullet_movement()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__(enemy_group, sprites_group)
        self.image = pygame.image.load("enemy.png")
        self.image = pygame.transform.rotozoom(self.image, 0, ENEMY_SIZE)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.speed = ENEMY_SPEED
        self.x = position[0]
        self.y = position[1]
        self.direction = pygame.math.Vector2()
        self.velocity = pygame.math.Vector2()
        self.position = pygame.math.Vector2(position)
        self.damage_cd = DAMAGE_CD
        self.count = 0
        self.health = 3

    def pathing(self):
        player_vector = pygame.math.Vector2(player.hitbox.center)
        enemy_vector = pygame.math.Vector2(self.rect.center)
        distance = (player_vector - enemy_vector).magnitude()

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

            if not self.damage_applied and (time.time() - self.timer) >= self.damage_cd:
                player.health -= 1
                self.count = 0
                self.damage_applied = True
                player.health_display = font.render(str(player.health), True, "red")

        self.velocity = self.direction * self.speed
        self.position += self.velocity

        self.rect.centerx = self.position.x
        self.rect.centery = self.position.y

    def hit(self):
        bullet_hit = pygame.sprite.spritecollide(self, bullet_sprites_group, True)
        for bullet in bullet_hit:
            self.health -= 1

    def death(self):
        if self.health == 0 or self.health < 0:
            self.kill()

    def update(self):
        self.pathing()
        self.hit()
        self.death()

    def calculate_distance(self, vector_1, vector_2):
        return vector


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


difficulty = 1

sprites_group = pygame.sprite.Group()
bullet_sprites_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def main_game():
    global waves, player
    waves = Waves()
    player = Player()
    # enemy = Enemy((400, 400))
    # enemy2 = Enemy((-400, -400))

    sprites_group.add(player)
    text_surface = font.render(str(player.health), True, "red")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.blit(background, (0, 0))
        screen.blit(player.health_display, (0, 0))
        sprites_group.draw(screen)
        sprites_group.update()

        waves.update()
        player.update()
        # Hitbox / Base rectangles
        pygame.draw.rect(screen, "red", player.hitbox, width=2)
        pygame.draw.rect(screen, "yellow", player.rect, width=2)

        pygame.display.update()
        clock.tick(FPS)


def settings():
    pass


def change_difficulty(value, prev_value):

    if value == "easy":

        difficulty = 1

    elif value == "medium":

        difficulty = 2

    elif value == "hard":

        difficulty = 3

# Defining the main menu theme
myimage = pygame_menu.baseimage.BaseImage(
    image_path="background.png",
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY,
)
        
main_menu_theme = pygame_menu.Theme(
    title_offset=(WIDTH / 2 - 100, 0),
    title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE,
    title_font=menu_font,
    background_color=myimage,
    title_background_color=(255, 0, 0),
    title_font_shadow=False,
    widget_padding=25,
)

# Create the main menu
main_menu = pygame_menu.Menu("Main Menu", WIDTH, HEIGHT, theme=main_menu_theme)

# Defining the main menu sounds
engine = sound.Sound()
engine.set_sound(sound.SOUND_TYPE_CLICK_MOUSE, 'menu_click.mp3')
engine.set_sound(sound.SOUND_TYPE_KEY_ADDITION, 'menu_click.mp3')
engine.set_sound(sound.SOUND_TYPE_OPEN_MENU, 'menu_click.mp3')
engine.set_sound(sound.SOUND_TYPE_WIDGET_SELECTION, 'menu_click.mp3')
engine.set_sound(sound.SOUND_TYPE_OPEN_MENU, 'menu_click.mp3')

main_menu.set_sound(engine, recursive=True)

# Adding options to the menu
main_menu.add.button("Play", main_game)
main_menu.add.selector(
    "Difficulty:",
    [("Easy", "easy"), ("Medium", "medium"), ("Hard", "hard")],
    onchange=change_difficulty,
)
main_menu.add.button("Settings", settings)  # WIP
main_menu.add.button("Quit", pygame_menu.events.EXIT)


main_menu.mainloop(screen)

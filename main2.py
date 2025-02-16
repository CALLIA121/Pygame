import pygame
import sys
import random

pygame.init()
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Primitives War")

starting_coins = 1000
current_coins = starting_coins
player_HP = 100

units = []
enemies = []
bullets = []

shooters_last_shoot_time = {}

typeHP = {
    'Attaker': 50,
    'Defender': 140,
    'Shooter': 100
}

typeCost = {
    'Attaker': 10,
    'Defender': 50,
    'Shooter': 50
}

class Unit:
    def __init__(self, type, x, y):
        self.type = type
        self.x = x
        self.y = y
        self.HP = typeHP[type]

        if type == 'Attaker':
            self.color = (255, 0, 0)
            self.size = (50, 50)
        elif type == 'Defender':
            self.color = (0, 255, 0)
            self.size = (40, 40)
        elif type == 'Shooter':
            self.color = (0, 0, 255)
            self.size = (50, 50)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, *self.size))

    def is_colliding(self, enemy):
        return (self.x < enemy.x + enemy.size[0] and
                self.x + self.size[0] > enemy.x and
                self.y < enemy.y + enemy.size[1] and
                self.y + self.size[1] > enemy.y)

    def shoot(self):
        if self.type == 'Shooter':
            bullet = Bullet(self.x + self.size[0], self.y + (self.size[1] // 2))
            bullets.append(bullet)

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = (50, 30)
        self.color = (0, 0, 0)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, *self.size))

    def update(self):
        self.x -= 1

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = (10, 5)
        self.color = (255, 215, 0)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, *self.size))

    def update(self):
        self.x += 5

def spawn_enemy():
    y = random.randint(72, HEIGHT - 50)
    new_enemy = Enemy(WIDTH, y)
    enemies.append(new_enemy)

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.action = action

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, current_color, self.rect)
        pygame.draw.rect(screen, 'black', self.rect, 3)

        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, 'black')
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()

def spawn_unit(x, y):
    global currType, current_coins
    if currType != 'None' and x < (WIDTH // 2 - 45):
        unit_cost = typeCost[currType]
        if current_coins >= unit_cost:
            new_unit = Unit(currType, x, y)
            units.append(new_unit)
            current_coins -= unit_cost

def handle_event(event, buttons):
    for butt in buttons:
        butt.handle_event(event)
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        x, y = event.pos
        if y > 72:
            spawn_unit(x, y)

def draw_objects(screen, objs):
    for obj in objs:
        obj.draw(screen)

def reset_game():
    global currType, current_coins, player_HP, units, enemies
    currType = 'None'
    current_coins = starting_coins
    player_HP = 100
    units.clear()
    enemies.clear()
    shooters_last_shoot_time.clear()

running = True
currType = 'None'
enemy_spawn_time = 0
shoot_interval = 5 * 1000

startBtn = Button('Ready!', 0, 20, 100, 50, (128, 0, 128),
                  (128 - 20, 0, 128 - 20), reset_game)

classAttak = Button('Attacker', 100, 20, 100, 50, (255, 165, 0),
                    (240, 150, 0), lambda: setClass('Attaker'))
classDefender = Button('Defender', 200, 20, 150, 50, (0, 128, 128),
                       (0, 128 - 15, 128 - 15), lambda: setClass('Defender'))
classShooter = Button('Shooter', 350, 20, 110, 50, (0, 255, 0),
                      (0, 255 - 25, 0), lambda: setClass('Shooter'))

buttons = [startBtn, classAttak, classDefender, classShooter]
damage_on_collision = 10

def setClass(cl):
    global currType
    if currType != cl:
        currType = cl
    else:
        currType = 'None'

while running:
    for event in pygame.event.get():
        handle_event(event, buttons)
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    enemy_spawn_time += 1
    if enemy_spawn_time > 30:
        spawn_enemy()
        enemy_spawn_time = 0

    for enemy in enemies[:]:
        enemy.update()
        if enemy.x < 0:
            player_HP -= 1
            enemies.remove(enemy)

    for unit in units[:]:
        for enemy in enemies[:]:
            if unit.is_colliding(enemy):
                unit.HP -= damage_on_collision
                if unit.HP <= 0:
                    units.remove(unit)
                enemies.remove(enemy)
                current_coins += 10
                break

    current_time = pygame.time.get_ticks()
    for unit in units:
        if unit.type == 'Shooter':
            if (unit.x not in shooters_last_shoot_time or
                    current_time - shooters_last_shoot_time[unit.x] > shoot_interval):
                unit.shoot()
                shooters_last_shoot_time[unit.x] = current_time

    bullets[:] = [bullet for bullet in bullets if bullet.x < WIDTH]
    for bullet in bullets:
        bullet.update()

    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.x + bullet.size[0] > enemy.x and bullet.y + bullet.size[1] > enemy.y and bullet.y < enemy.y + \
                    enemy.size[1]:
                bullets.remove(bullet)
                enemies.remove(enemy)
                current_coins += 10
                break

    draw_objects(screen, buttons)
    draw_objects(screen, units)
    draw_objects(screen, enemies)
    draw_objects(screen, bullets)

    font = pygame.font.Font(None, 36)
    hp_text = f"HP: {player_HP}"
    text_surface = font.render(hp_text, True, 'red')
    text_rect = text_surface.get_rect(topright=(WIDTH - 10, 10))
    screen.blit(text_surface, text_rect)

    coins_text = f"Coins: {current_coins}"
    coins_surface = font.render(coins_text, True, 'gold')
    coins_rect = coins_surface.get_rect(topright=(WIDTH - 10, 40))
    screen.blit(coins_surface, coins_rect)

    if player_HP <= 0:
        print("Game Over!")
        running = False

    pygame.display.flip()


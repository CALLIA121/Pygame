import pygame
import sys
import random
from settings import *

pygame.init()
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Primitives War")

units = []
enemies = []

typeHP = {
    'Attaker': 50,
    'Defender': 140,
    'Shooter': 100
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


def spawn_enemy():
    y = random.randint(72, HEIGHT - 50)
    new_enemy = Enemy(WIDTH, y)
    enemies.append(new_enemy)


class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, action=None, argv=None, about=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.argv = argv
        self.about = about

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
                    if self.argv:
                        self.action(self.argv)
                    else:
                        self.action()

    def draw2(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.about and self.rect.collidepoint(mouse_pos):
            lines = self.about.splitlines()
            count = len(lines)
            maxLen = max(len(x) for x in lines)
            width = 10 * maxLen
            height = 25 * count
            LineX, LineY = self.rect.centerx, self.rect.bottom + 10

            pygame.draw.rect(screen, (255, 255, 255), (LineX - width // 2 - 10, LineY, width + 20, height + 10))
            pygame.draw.rect(screen, (0, 0, 0), (LineX - width // 2 - 10, LineY, width + 20, height + 10), 2)

            font = pygame.font.Font(None, 25)
            for i, line in enumerate(lines):
                text_surface = font.render(line, True, 'black')
                text_rect = text_surface.get_rect(center=(LineX, LineY + (i * 25) + 5))
                screen.blit(text_surface, text_rect)


def spawn_unit(x, y):
    global currType
    if currType != 'None' and x < (WIDTH // 2 - 45):
        new_unit = Unit(currType, x, y)
        units.append(new_unit)


def handle_event(event, buttons: list):
    for butt in buttons:
        butt.handle_event(event)

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        x, y = event.pos
        if y > 72:
            spawn_unit(x, y)


def drower(screen, objs):
    for obj in objs:
        obj.draw(screen)
        obj.draw2(screen)

    for unit in units:
        unit.draw(screen)

    for enemy in enemies:
        enemy.draw(screen)


enemy_spawn_time = 0
start = False


def startGame():
    global startBtn, start, typeLabel, currType
    if not start:
        start = True
        typeLabel = 'Lock'
        currType = 'None'
        startBtn.text = 'Заново'
        startBtn.color = (255, 0, 0)
        startBtn.hover_color = (255 - 25, 0, 0)
    else:
        start = False
        typeLabel = 'None'
        currType = 'None'
        startBtn.text = 'Готов!'
        startBtn.color = (128, 0, 128)
        startBtn.hover_color = (128 - 20, 0, 128 - 20)


def setClass(cl):
    global currType, typeLabel
    if currType != cl:
        currType = cl
        typeLabel = typeRus[cl]
    else:
        currType = 'None'
        typeLabel = 'None'


running = True
typeLabel = 'None'
currType = 'None'
startBtn = Button('Готов!', 0, 20, 100, 50, (128, 0, 128),
                  (128 - 20, 0, 128 - 20), startGame)

classAttak = Button('Атакер', 100, 20, 100, 50, (255, 165, 0),
                    (240, 150, 0), setClass, ('Attaker'),
                    f'Урон {typeDamag["Attaker"]}\nОЗ {typeHP["Attaker"]}\nСтоит {typeCost["Attaker"]}$\nБлижний бой')
classDefender = Button('Защитник', 200, 20, 150, 50, (0, 128, 128),
                       (0, 128 - 15, 128 - 15), setClass, ('Defender'),
                       f'Урон {typeDamag["Defender"]}\nОЗ {typeHP["Defender"]}\nСтоит {typeCost["Defender"]}$\nБлижний бой')
classShooter = Button('Стрелок', 350, 20, 110, 50, (0, 255, 0),
                      (0, 255 - 25, 0), setClass, ('Shooter'),
                      f'Урон {typeDamag["Shooter"]}\nОЗ {typeHP["Shooter"]}\nСтоит {typeCost["Shooter"]}$\nДальний бой')

buttons = [startBtn, classAttak, classDefender, classShooter]

damage_on_collision = 10

while running:
    for event in pygame.event.get():
        handle_event(event, buttons)
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    if enemy_spawn_time > 30:
        spawn_enemy()
        enemy_spawn_time = 0

    for enemy in enemies:
        enemy.update()

    for unit in units:
        for enemy in enemies:
            if unit.is_colliding(enemy):
                unit.HP -= damage_on_collision
                if unit.HP <= 0:
                    units.remove(unit)
                enemies.remove(enemy)
                break

    enemies = [enemy for enemy in enemies if enemy.x > 0]

    drower(screen, buttons)

    font = pygame.font.Font(None, 36)
    if typeLabel == 'None':
        text_surface = font.render('Классы', True, 'black')
    elif typeLabel == 'Lock':
        text_surface = font.render('Идет бой', True, 'black')
    else:
        text_surface = font.render(f'Выбран: {typeLabel}', True, 'black')
    text_rect = text_surface.get_rect(center=((100 + 350 + 110) // 2, 10))
    screen.blit(text_surface, text_rect)

    pygame.draw.line(screen, (0, 0, 0), (0, 72), (WIDTH, 72), 1)
    pygame.draw.line(screen, (128, 0, 0), (WIDTH / 2, 72), (WIDTH / 2, HEIGHT), 5)

    font = pygame.font.Font(None, 50)
    coinsText = f"10^9 $"
    text_surface = font.render(coinsText, True, 'gold')
    text_rect = text_surface.get_rect(center=(WIDTH - (10 * len(coinsText)), 20))
    screen.blit(text_surface, text_rect)

    pygame.display.flip()

    enemy_spawn_time += 1

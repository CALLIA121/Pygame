import pygame
import sys

from pygame import MOUSEBUTTONDOWN

from settings import *

pygame.init()
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
coins = 10000

pygame.display.set_caption("Primitives War")

units = []


class Unit:
    def __init__(self, type):
        self.type = type
        self.x = 0
        self.y = 0
        self.HP = typeHP[type]


class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, action=None, argv=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.argv = argv

    def draw(self, screen):
        # Проверка наведения курсора
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, 'black', self.rect, 3)

        # Отображение текста
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
                else:
                    print('Button has no action(')

    def draw2(self, screen):
        pass


def handle_event(event, buttons: list):
    for butt in buttons:
        butt.handle_event(event)


def drower(screen, objs):
    for obj in objs:
        obj.draw(screen)

    for obj in objs:
        obj.draw2(screen)


start = False


def startGame():
    global startBtn, start, typeLabel, units, currType
    print('Start')
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
        startBtn.color = (128, 0, 128),
        startBtn.hover_color = (128 - 20, 0, 128 - 20)
        units = []
        coins = 10000


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
                    (240, 150, 0), setClass, ('Attaker'))
classDefender = Button('Защитник', 200, 20, 150, 50, (0, 128, 128),
                       (0, 128 - 15, 128 - 15), setClass, ('Defender'))
classShooter = Button('Стрелок', 350, 20, 110, 50, (0, 255, 0),
                      (0, 255 - 25, 0), setClass, ('Shoter'))

buttons = [startBtn, classAttak, classDefender, classShooter]


while running:
    for event in pygame.event.get():
        handle_event(event, buttons)

        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if not start and currType != 'None':
                x, y = event.pos
                if x < WIDTH / 2 and y > 72:
                    cost = typeCost.get(currType, 0)
                    if coins >= cost:
                        unit = Unit(currType)
                        unit.x = x
                        unit.y = y
                        units.append(unit)
                        coins -= cost
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    drower(screen, buttons)
    for unit in units:
        color = typeColors.get(unit.type)
        pygame.draw.rect(screen, color, (unit.x - 15, unit.y - 15, 30, 30))
        pygame.draw.rect(screen, 'black', (unit.x - 15, unit.y - 15, 30, 30), 2)

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
    pygame.draw.line(screen, (128, 0, 0), (WIDTH / 2, 72),
                     (WIDTH / 2, HEIGHT), 5)

    font = pygame.font.Font(None, 50)
    text_surface = font.render(f'{coins}$', True, 'gold')
    text_rect = text_surface.get_rect(
        center=(WIDTH - (10 * len(f'{coins}$')), 20))
    screen.blit(text_surface, text_rect)

    pygame.display.flip()

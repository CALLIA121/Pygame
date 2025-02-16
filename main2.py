import pygame
import sys
from pygame import MOUSEBUTTONDOWN
from settings import *

# Инициализация Pygame
pygame.init()
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Primitives War")

# Состояния игры
SCREENS = {
    "main_menu": 0,
    "level_select": 1,
    "game": 2
}

current_screen = SCREENS["main_menu"]

# Игровые переменные
coins = 10000
units = []
start = False
typeLabel = 'None'
currType = 'None'


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
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, 'black', self.rect, 3)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, 'black')
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.action:
                if self.argv is not None:
                    self.action(self.argv)
                else:
                    self.action()


# Функции для кнопок
def quit_game():
    pygame.quit()
    sys.exit()


def switch_screen(screen_name):
    global current_screen
    current_screen = screen_name


def start_level(level_num):
    global current_screen, start, coins, units, currType, typeLabel
    current_screen = SCREENS["game"]
    start = False
    coins = 10000
    units = []
    currType = 'None'
    typeLabel = 'None'


# Кнопки главного меню
main_menu_buttons = [
    Button(
        "Выбор уровня", WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 50,
        (0, 128, 128), (0, 100, 100),
        lambda: switch_screen(SCREENS["level_select"])
    ),
    Button(
        "Выход", WIDTH // 2 - 150, HEIGHT // 2 + 50, 300, 50,
        (128, 0, 0), (100, 0, 0),
        quit_game
    )
]

# Кнопки выбора уровня
level_select_buttons = [
    Button(
        "1 уровень", WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 50,
        (0, 200, 0), (0, 150, 0),
        start_level, 1
    ),
    Button(
        "Назад", WIDTH // 2 - 150, HEIGHT // 2 + 50, 300, 50,
        (128, 128, 128), (100, 100, 100),
        lambda: switch_screen(SCREENS["main_menu"])
    )
]

# Кнопки игры
startBtn = Button('Готов!', 0, 40, 100, 50,
                  (128, 0, 128), (108, 0, 108),
                  lambda: startGame())
classAttak = Button('Атакер', 100, 40, 100, 50,
                    (255, 165, 0), (230, 140, 0),
                    lambda: setClass('Attaker'))
classDefender = Button('Защитник', 200, 40, 150, 50,
                       (0, 128, 128), (0, 103, 103),
                       lambda: setClass('Defender'))
classShooter = Button('Стрелок', 350, 40, 110, 50,
                      (0, 255, 0), (0, 230, 0),
                      lambda: setClass('Shooter'))
game_buttons = [startBtn, classAttak, classDefender, classShooter]


def startGame():
    global start, startBtn, typeLabel, currType
    if not start:
        start = True
        typeLabel = 'Lock'
        currType = 'None'
        startBtn.text = 'Заново'
        startBtn.color = (255, 0, 0)
        startBtn.hover_color = (230, 0, 0)
    else:
        start = False
        typeLabel = 'None'
        currType = 'None'
        startBtn.text = 'Готов!'
        startBtn.color = (128, 0, 128)
        startBtn.hover_color = (108, 0, 108)
        units.clear()


def setClass(cl):
    global currType, typeLabel
    currType = cl if currType != cl else 'None'
    typeLabel = typeRus[cl] if currType != 'None' else 'None'


# Основной цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if current_screen == SCREENS["main_menu"]:
            for btn in main_menu_buttons:
                btn.handle_event(event)

        elif current_screen == SCREENS["level_select"]:
            for btn in level_select_buttons:
                btn.handle_event(event)

        elif current_screen == SCREENS["game"]:
            for btn in game_buttons:
                btn.handle_event(event)

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if not start and currType != 'None':
                    x, y = event.pos
                    if x < WIDTH / 2 and y > 90:
                        cost = typeCost.get(currType, 0)
                        if coins >= cost:
                            unit = Unit(currType)
                            unit.x = x
                            unit.y = y
                            units.append(unit)
                            coins -= cost

    # Отрисовка
    screen.fill((255, 255, 255))

    if current_screen == SCREENS["main_menu"]:
        # Заголовок
        font = pygame.font.Font(None, 72)
        text = font.render("Primitives War", True, (0, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(text, text_rect)
        # Кнопки
        for btn in main_menu_buttons:
            btn.draw(screen)

    elif current_screen == SCREENS["level_select"]:
        # Заголовок
        font = pygame.font.Font(None, 72)
        text = font.render("Выберите уровень", True, (0, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(text, text_rect)
        # Кнопки
        for btn in level_select_buttons:
            btn.draw(screen)

    elif current_screen == SCREENS["game"]:
        # Игровой интерфейс
        for btn in game_buttons:
            btn.draw(screen)

        # Юниты
        for unit in units:
            color = typeColors.get(unit.type, (0, 0, 0))
            pygame.draw.rect(screen, color, (unit.x - 15, unit.y - 15, 30, 30))
            pygame.draw.rect(screen, 'black', (unit.x - 15, unit.y - 15, 30, 30), 2)

        # Текстовые метки
        font = pygame.font.Font(None, 36)
        status_text = 'Идет бой' if typeLabel == 'Lock' else f'Выбран: {typeLabel}'
        text = font.render(status_text, True, 'black')
        screen.blit(text, ((100 + 350 + 110) // 2 - 50, 10))

        # Разделители
        pygame.draw.line(screen, (0, 0, 0), (0, 90), (WIDTH, 90), 1)
        pygame.draw.line(screen, (128, 0, 0), (WIDTH // 2, 90), (WIDTH // 2, HEIGHT), 5)

        # Монеты
        font = pygame.font.Font(None, 50)
        text = font.render(f'{coins}$', True, 'gold')
        screen.blit(text, (WIDTH - 200, 20))

    pygame.display.flip()

pygame.quit()
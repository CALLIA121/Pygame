import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Primitives War")


class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.action = action

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
                    self.action()

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
    global startBtn, start
    print('Start')
    if not start:
        start = True
        startBtn.text = 'Заного'
    else:
        start = False
        startBtn.text = 'Готов!'


running = True
can = False
startBtn = Button('Готов!', 0, 0, 100, 50, (255, 0, 0),
                  (255, 100, 0), startGame)

buttons = [startBtn]
while running:
    print(start)
    for event in pygame.event.get():
        handle_event(event, buttons)
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    drower(screen, buttons)

    pygame.display.flip()

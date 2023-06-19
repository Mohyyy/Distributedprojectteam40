import pygame
import sys
from pygame.locals import *

pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Main Window')

class Button:
    def __init__(self, x, y, width, height, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback

    def draw(self):
        pygame.draw.rect(screen, (200, 200, 200), self.rect)
        font = pygame.font.Font(None, 32)
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.callback()

class TextBox:
    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        font = pygame.font.Font(None, 32)
        text_surface = font.render(self.text, True, (0, 0, 0))
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

def open_new_window():
    new_screen_width = 600
    new_screen_height = 400
    new_screen = pygame.display.set_mode((new_screen_width, new_screen_height))
    pygame.display.set_caption('New Window')

    new_textbox = TextBox(50, 50, new_screen_width - 100, 32)
    new_button = Button(50, 100, 100, 50, 'Submit', lambda: print('Button Clicked'))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            new_textbox.handle_event(event)
            new_button.handle_event(event)

        new_screen.fill((255, 255, 255))
        new_textbox.draw()
        new_button.draw()
        pygame.display.update()

textbox = TextBox(50, 50, screen_width - 100, 32)
button = Button(50, 100, 200, 50, 'Open New Window', open_new_window)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        textbox.handle_event(event)
        button.handle_event(event)

    screen.fill((255, 255, 255))
    textbox.draw()
    button.draw()
    pygame.display.update()

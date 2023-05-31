
import pygame
from Protocols import GameSnapshot

class Player(pygame.sprite.Sprite):
    def __init__(self, player_id: int) -> None:
        super().__init__()
        self.id = player_id
        self.sprite = pygame.image.load(f"./Sprites/Car{self.id}.png").convert()
        self.sprite = pygame.transform.scale(self.sprite, (20, 20))
        self.image = self.sprite
        self.rect = self.image.get_rect()
        self.deg = 0

    def update(self, game_input: GameSnapshot) -> None:
        pos_x, pos_y, rotation = game_input[self.id]
        if rotation != self.deg:
            self.deg = rotation
            self.image = pygame.transform.rotate(self.sprite, rotation)
            self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)

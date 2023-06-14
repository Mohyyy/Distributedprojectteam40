
from math import sin, cos, radians

class Movement:
    FORWARD = 1
    BACKWARD = -1

DEGREE = 1
SPEED = 10

class Player:
    def __init__(self, id: int) -> None:
        self.id = id
        self.x = 100
        self.y = 100 + id * 10
        self.deg = 0

    def move(self, movement: tuple) -> None:
        direction, angle = movement
        self.deg = self.deg + DEGREE * angle
        if self.deg < 0:
            self.deg += 360
        elif self.deg > 360:
            self.deg -= 360
        self.x += SPEED * cos(radians(self.deg)) * direction
        self.y -= SPEED * sin(radians(self.deg)) * direction

from enum import Enum
import pickle

class GameState(Enum):
    MainMenu = 0
    GameSetup = 1
    GamePlay = 2
    GameEnd = 3

PlayerSnapshot = tuple[int, int, int]  # x, y, deg
GameSnapshot = list[PlayerSnapshot]
Movement = list[int, int]  # Direction and Angle
Packet = tuple[GameState, int]

def getData(data: bytes) -> Packet:
    return pickle.loads(data)


def dumpData(data: Packet) -> bytes:
    return pickle.dumps(data)


SPEED = 5
DEGREE = 3

GAME_SIZE = (800, 600)
UI_SIZE = 250
WINDOW_SIZE = (GAME_SIZE[0] + UI_SIZE, GAME_SIZE[1])

CTB_HEIGHT = 500
ETB_HEIGHT = 50
BTN_HEIGHT = 50

HOST = "localhost"
PORT = 8888
MAX_PLAYERS = 4

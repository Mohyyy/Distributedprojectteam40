# Enums
from enum import Enum


class GameStatus(Enum):
    MainMenu = 0
    GameSetup = 1
    GamePlay = 2
    GameEnd = 3


# Types
PlayerSnapshotType = tuple[int, int, int]  # x, y, deg
GameSnapshotType = list[PlayerSnapshotType]
MovementType = list[int, 2]  # Direction and Angle
PacketType = tuple[GameStatus, int | GameSnapshotType]

# Helper Functions
import pickle


def load_data(data: bytes) -> PacketType:
    return pickle.loads(data)


def serialize_data(data: PacketType) -> bytes:
    return pickle.dumps(data)


# Constants
SPEED = 5
ANGLE = 3

GAME_DIMENSIONS = (800, 600)
UI_DIMENSIONS = 250
WINDOW_DIMENSIONS = (GAME_DIMENSIONS[0] + UI_DIMENSIONS, GAME_DIMENSIONS[1])

CHAT_BOX_HEIGHT = 500
ENTRY_BOX_HEIGHT = 50
BUTTON_HEIGHT = 50

HOST, PORT = "localhost", 8888
MAX_PLAYER_COUNT = 4

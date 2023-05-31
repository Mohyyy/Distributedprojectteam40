from pygame import sprite, Surface, image, transform

from Proxy import Proxy
from Player import Player
from Protocols import GAME_SIZE, Movement, GameState


class Game:
    def __init__(self, address=None) -> None:
        self.graphical_players = sprite.RenderClear()
        self.game_map = image.load("./Sprites/Map.png").convert()
        self.game_map = transform.scale(self.game_map, GAME_SIZE)
        self.state: GameState = GameState.MainMenu
        self.address = address

    def add_player(self, player_id) -> None:
        new_player = Player(player_id)
        self.graphical_players.add(new_player)

    def update(self, screen: Surface, movement: Movement) -> None:
        match self.state:
            case GameState.MainMenu:
                screen.blit(self.game_map, (0, 0))
                self.proxy = Proxy(self.address)
                self.state = GameState.GameSetup
            case GameState.GameSetup:
                if self.proxy.wait_for_other_players():
                    for i in range(len(self.proxy.latest_snapshot)):
                        self.add_player(i)
                    self.proxy.start()
                    self.state = GameState.GamePlay
            case GameState.GamePlay:
                self.graphical_players.update(self.proxy.latest_snapshot)
                self.graphical_players.clear(screen, self.game_map)
                self.graphical_players.draw(screen)
                self.proxy.move(movement)
                if not self.proxy.is_alive():
                    self.graphical_players.empty()
                    self.state = GameState.GameEnd
            case GameState.GameEnd:
                self.state = GameState.MainMenu

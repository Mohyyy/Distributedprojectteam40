from select import select
from threading import Thread
from socket import socket, AF_INET, SOCK_DGRAM, SO_REUSEADDR, SOL_SOCKET

from Protocols import (
    GameState,
    HOST,
    PORT,
    Movement,
    GameSnapshot,
    dumpData,
    getData,
)


class Proxy(Thread):
    def __init__(self, address=None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.sock = socket(AF_INET, SOCK_DGRAM)
        if address:
            self.sock.bind((HOST, address))
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        data = dumpData((GameState.GameSetup, 0))
        self.sock.sendto(data, (HOST, PORT))
        self.latest_snapshot: GameSnapshot = GameSnapshot

    def wait_for_other_players(self) -> bool:
        ready_to_read, _, _ = select([self.sock], [], [], 20 / 1000)
        if ready_to_read:
            data, _ = self.sock.recvfrom(1024)
            if data:
                state, self.latest_snapshot = getData(data)
                return True
        return False

    def move(self, movement: Movement) -> None:
        data = dumpData((GameState.GamePlay, movement))
        self.sock.sendto(data, (HOST, PORT))

    def run(self) -> None:
        duplicate_sock = self.sock.dup()
        tick_count = 0
        while tick_count < 10:
            data, _ = duplicate_sock.recvfrom(4096)
            if data:
                tick_count = 0
                packet = getData(data)
                if packet[0] is GameState.GameEnd:
                    packet[1]
                    break
                self.latest_snapshot = packet[1]
            else:
                tick_count += 1

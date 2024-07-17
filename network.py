"""Create the network to connect player data together."""

import settings as s
import socket
import pickle


# create a connected socket
class Network:
    """Network one-end connection of a player."""

    # initiator method
    def __init__(self) -> None:
        """Initialise the network."""
        self.client: socket.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )
        self.server: str = s.SERVER
        self.port: int = s.PORT
        self.address: tuple[str, int] = (self.server, self.port)
        self.player_no: str = self.connect()

    # connect users
    def connect(self):
        """Connect user and establish player number."""
        try:
            self.client.connect(self.address)  # connect based on addr
            return self.client.recv(2048).decode()

        # addr not found
        except socket.error as er_m:
            print(er_m)

    def send(self, data):
        """Send infromation between users."""
        try:
            self.client.send(str.encode(data))  # send encoded data
            return pickle.loads(self.client.recv(2048 * 2))  # receive obj data

        # data not found
        except socket.error as er_m:
            print(er_m)

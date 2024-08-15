"""Create the network to connect player data together."""

import settings as s
import pickle
import socket


# create a connected socket
class Network:
    """Network one-end connection of a player."""

    # initiator method
    def __init__(self) -> None:
        """Initialise the network."""
        self.client: socket.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )
        self.address: tuple[str, int] = (s.SERVER, s.PORT)
        self.player_no: str = self.link()

    # prompt events
    def send(self, data):
        """Send infromation between users."""
        try:
            self.client.send(str.encode(data))  # send encoded data
            return pickle.loads(self.client.recv(2048 * 2))  # receive obj data

        # data not found
        except socket.error as er_m:
            print(er_m)

    # connect users
    def link(self):
        """Connect user and establish player number."""
        try:
            self.client.connect(self.address)  # connect based on addr
            return self.client.recv(2048).decode()

        # addr not found
        except socket.error as er_m:
            print(er_m)

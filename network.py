"""Create the network to connect players together."""

import socket
import pickle


# create the network
class Network:
    """The network."""

    # initiator method
    def __init__(self):
        """Initialise the network."""
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "10.203.11.10"
        self.port = 5555
        self.addr = (self.server, self.port)

    # connect users
    def connect(self):
        """Connect users to client."""
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        """Send information between users."""
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048 * 2))
        except socket.error as e:
            print(e)

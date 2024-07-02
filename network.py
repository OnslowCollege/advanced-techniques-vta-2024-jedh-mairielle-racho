"""Create the network to connect players together."""
import settings as settings
import socket
import pickle


# create the network
class Network:
    """The network."""

    # initiator method
    def __init__(self):
        """Initialise the network."""
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = settings.SERVER
        self.port = settings.PORT
        self.addr = (self.server, self.port)
        self.player_no = self.connect()

    # connect users
    def connect(self):
        """Get player number."""
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except socket.error:
            pass

    def send(self, data):
        """Send information between users."""
        try:
            self.client.send(str.encode(data))  # send data
            return pickle.loads(self.client.recv(2048 * 2))  # receive obj data
        except socket.error as e:
            print(e)

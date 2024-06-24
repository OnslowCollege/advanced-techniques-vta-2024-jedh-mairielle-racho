"""Create the game."""


# player class to store info
class Player:
    """Create a player instance."""

    # initiator method
    def __init__(self) -> None:
        """Initialise the player."""
        # store player stats
        self.ready: bool = False  # whether player ready to start game
        self.turn: bool = False  # whether it is player's turn
        self.wins: int = 0
        self.ties: int = 0

        # store player game data
        self.hand = []


# game instance stores all game data
class Game:
    """Create a Blackjack game."""

    # initiator method
    def __init__(self, game_id: int) -> None:
        """
        Initialise the game.

        Parameters
        ----------
            game_id: id to keep track of which server to send player.

        """
        self.ready: bool = False  # if game is ready to start
        # create the players
        self.p1: Player = Player()
        self.p2: Player = Player()

    # check if players are connected
    def connected(self) -> None:
        """Check if both players are ready."""
        return self.ready

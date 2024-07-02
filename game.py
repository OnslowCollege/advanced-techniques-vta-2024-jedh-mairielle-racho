"""Create the game."""
import random


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
        self.hand: list[str] = []


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
        self.players: list[Player] = [self.p1, self.p2]

        # create the deck
        self.deck: list[str] = (  # create the deck of 52
            [str(i) for i in range(1, 11)] + ["J", "Q", "K", "A"]
        ) * 4
        random.shuffle(self.deck)  # shuffle deck

        # deal initial cards
        for i in range(2):
            self.deal_card(0)
            self.deal_card(1)

    # deal a card to a play
    def deal_card(self, player_no: int) -> None:
        """Deal a card to a player."""
        self.players[player_no].hand += self.deck[0]
        self.deck.pop(0)

    # play a round in the game
    def play_round(self, player_no: int, move) -> None:
        """Play a round of blackjack."""
        pass

    # check if players have went
    def player_turn(self) -> bool:
        """Check if players have done their turn."""
        return self.p1.turn and self.p2.turn

    # reset game
    def reset(self) -> None:
        """Reset the game."""
        pass


Game(0)
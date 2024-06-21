"""Program objects."""

import random


# the individual card object
class Card:
    """Each card."""

    # initiator method
    def __init__(self, symbol: str, value: int) -> None:
        """
        Create a card.

        Parameters
        ----------
            symbol: the card symbol
            value: the value of the card (must be chosen by user when A)

        """
        self.symbol = symbol
        self.value = value


# the deck class (can reset by replacing object)
class Deck:
    """The deck of cards used in the game."""

    # initiator method
    def __init__(self) -> None:
        """Initialise the deck."""
        self.deck: list[str] = (  # create the deck of 52
            [str(i) for i in range(1, 11)] + ["J", "Q", "K", "A"]
        ) * 4
        random.shuffle(self.deck)  # shuffle deck


# the player class
class Player:
    """Create a player to store hand."""

    # initiator method
    def __init__(self) -> None:
        """Initialise player."""
        self.hand: list[Card] = []

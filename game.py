"""Create a blackjack game."""

import random


# player class to store user info
class Player:
    """Create a player instance."""

    # initiator method
    def __init__(self) -> None:
        """Initialise the player."""
        # store player stats
        self.turn: bool = False  # indicates whether it is player's turn
        self.wins: int = 0
        self.ties: int = 0

        # store player hand
        self.hand: list[str] = []

    # total up hand
    def total(self) -> int:
        """Total up the user's hand."""
        total: int = 0
        for card in self.hand:
            # user has face card (except ace) or 10
            if card in ["10", "J", "Q", "K", "A"]:
                total += 10
            # user has ace (automatically count current best choice)
            elif card == "A":
                # ace == 1 if otherwise makes total >21
                if (total + 10) > 21:
                    total += 1
                # ace == 10
                else:
                    total += 10

            # count number card
            else:
                total += int(card)
        return total


# game instance stores all game data
class Game:
    """Create a Blackjack game."""

    # initiator method
    def __init__(self, game_id: int) -> None:
        """
        Initialise the game.

        Parameters
        ----------
            game_id: the game to send a player to when threading

        """
        self.ready: bool = False  # ready when two users have connected

        # create the players
        self.p1: Player = Player()
        self.p2: Player = Player()
        self.players: list[Player] = [self.p1, self.p2]

        # create the deck
        self.deck: list[str] = (
            [str(i) for i in range(1, 11)] + ["J", "Q", "K", "A"]
        ) * 4
        random.shuffle(self.deck)  # shuffle deck

        # deal initial 2 cards
        for i in range(2):
            self.deal_card(0)  # deal to player 1
            self.deal_card(1)  # deal to player 2

    # deal a card to a player
    def deal_card(self, player_no: int) -> None:
        """Deal a card to a player."""
        self.players[player_no].hand += self.deck[0]  # deal to hand
        self.deck.pop(0)  # remove dealt card from deck
        print(self.players[player_no].hand)

    # play a round in the game
    def play_round(self, player_no: int, move) -> None:
        """Play a round of blackjack."""
        pass

    # check if players have went
    def player_turn(self) -> bool:
        """Check if players have finished their turn."""
        return self.p1.turn and self.p2.turn

    # reset game
    def reset(self) -> None:
        """Reset the game."""
        pass

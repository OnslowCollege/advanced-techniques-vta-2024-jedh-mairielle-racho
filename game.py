"""Create a blackjack game."""

import random

# player class to store user info
class Player:
    """Create a player instance."""

    # initiator method
    def __init__(self) -> None:
        """Initialise the player."""
        # store player stats
        self.active: bool = True  # user has not stood
        self.turn: bool = True  # indicates whether it is player's turn
        self.win: bool = False

        # store player hand
        self.hand: list[str] = []
        self.total()

    # total up hand
    def total(self) -> None:
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
        self.hand_total: int = total


# game instance stores all game data
class Game:
    """Create a Blackjack game."""

    # initiator method
    def __init__(self) -> None:
        """Initialise the game."""
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
        self.players[player_no].total()
        self.check_totals(player_no)  # check total

    # check totals
    def check_totals(self, player_no: int) -> None:
        """
        Check totals of each player.

        Parameters
        ----------
            player_no: user's player number

        """
        pass

    # user chooses to hit
    def hit(self, player_no: int) -> None:
        """
        User chooses to hit, so deal them a card.

        Parameters
        ----------
            player_no: player who has chosen to hit

        """
        self.deal_card(player_no)
        self.players[player_no].turn = False

    # user chooses to stand
    def stand(self, player_no: int) -> None:
        """
        User chooses to stand, so end their turns.

        Parameters
        ----------
            player_no: player who has chosen to hit

        """
        self.players[player_no].turn = False
        self.players[player_no].active = False

    # prepare next round
    def next_round(self, player_no: int) -> None:
        """
        If users have both done their turn, do next.

        Parameters
        ----------
            player_no: user's player number

        """
        # check whether both turns have been completed
        if not any([player.turn for player in self.players]):
            for player in self.players:
                if player.active:
                    player.turn = True  # reset turn

    # reset game
    def reset(self) -> None:
        """Reset the game."""
        pass

"""Create a blackjack game."""

import random


# player class to store user info
class Player:
    """Create a player instance."""

    ACE_MAX: int = 11
    ACE_MIN: int = 1

    # initiator method
    def __init__(self) -> None:
        """Initialise the player."""
        # store player stats
        self.active: bool = True  # user has not stood
        self.turn: bool = True  # indicates whether it is player's turn
        self.win: bool = True
        self.bust: bool = False
        self.blackjack: bool = False

        # store player hand
        self.hand: list[str] = []
        self.total()

    # total up hand
    def total(self) -> None:
        """Total up the user's hand."""
        # organise hand so Aces are after, to calculate A value
        hand: list[str] = [c for c in self.hand if c != "A"]
        hand += [a for a in self.hand if a == "A"]
        total: int = 0

        for card in hand:
            # user has face card (except ace) or 10
            if card in ["10", "J", "Q", "K"]:
                total += 10
            # user has ace (automatically count current best choice)
            elif card == "A":
                # ace == 1 if otherwise makes total >21
                if (total + Player.ACE_MAX) > 21:
                    total += Player.ACE_MIN
                # ace == 11
                else:
                    total += Player.ACE_MAX

            # count number card
            else:
                total += int(card)
        self.hand_total: int = total


# game instance stores all game data
class Game:
    """Create a Blackjack game."""

    MAX: int = 21

    # initiator method
    def __init__(self) -> None:
        """Initialise the game."""
        self.ready: bool = False  # ready when two users have connected
        self.bust: bool = False
        self.blackjack: bool = False
        self.reset()  # create vars for game

    # deal a card to a player
    def deal_card(self, player_no: int) -> None:
        """Deal a card to a player."""
        self.players[player_no].hand.append(self.deck[0])  # deal to hand
        self.deck.pop(0)  # remove dealt card from deck
        self.players[player_no].total()

    # check totals
    def check_totals(self) -> None:
        """Check totals of each player."""
        for i, player in enumerate(self.players):
            # user got >21, so other player wins
            if player.hand_total > 21:
                self.bust = True
                player.bust = True
                player.win = False
                self.inactive()

            # both users got 21, so tie
            elif (
                player.hand_total == Game.MAX
                and self.players[i - 1] == Game.MAX
            ):
                self.inactive()

            # user got 21, so they win
            elif player.hand_total == Game.MAX:
                self.blackjack = True
                player.blackjack = True
                self.players[i - 1].win = False
                self.inactive()

            # both players stood before 21
            elif not any([p.active for p in self.players]):
                if player.hand_total > self.players[i - 1].hand_total:
                    self.players[
                        i - 1
                    ].win = False  # player with greater total wins
                elif player.hand_total == self.players[i - 1].hand_total:
                    player.win = False

    # disable turns
    def inactive(self) -> None:
        """Inactive as a result has occurred."""
        for i in range(2):
            self.players[i].turn = False
            self.players[i].active = False

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
    def next_round(self) -> None:
        """
        If users have both done their turn, do next.

        Parameters
        ----------
            player_no: user's player number

        """
        self.check_totals()
        # check whether both turns have been completed
        if not any([player.turn for player in self.players]):
            for player in self.players:
                if player.active:
                    player.turn = True  # reset turn

    # reset game
    def reset(self) -> None:
        """Reset the game."""
        # create the players
        self.p1: Player = Player()
        self.p2: Player = Player()
        self.players: list[Player] = [self.p1, self.p2]

        # create the deck
        self.deck: list[str] = (
            [str(i) for i in range(2, 11)] + ["J", "Q", "K", "A"]
        ) * 4
        random.shuffle(self.deck)  # shuffle deck

        # deal initial 2 cards
        for i in range(2):
            self.deal_card(0)  # deal to player 1
            self.deal_card(1)  # deal to player 2
        self.check_totals()

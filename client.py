"""
Play Blackjack with an Onslow twist.

Created by: Jedh
Date: 2024-06-07
"""
# MUST RUN SERVER BEFORE PLAYING BLACKJACK

import pygame
import settings as s
from network import Network
import sys


# create buttons
class Button:
    """Create a clickable button."""

    # initiator method
    def __init__(
        self,
        text: str,
        f_size: int,
        t_colour: str,
        t_h_colour: str,
        b_colour: str,
        b_h_colour: str,
        b_width: int,
        b_height: int,
        b_x: float,
        b_y: float,
    ) -> None:
        """
        Initialise the button.

        Parameters
        ----------
            text: button label
            f_size: font size of the text
            t_colour: non-hover text colour
            t_h_colour: hover text colour
            b_colour: non-hover button colour
            b_h_colour: hover button colour
            b_width: width of button
            b_height: height of button
            b_x: x coord of topleft
            b_y: y coord of topleft

        """
        # button specifications
        self.b_colour: str = b_colour
        self.b_h_colour: str = b_h_colour
        self.b_rect: pygame.Rect = pygame.Rect(b_x, b_y, b_width, b_height)
        self.clicked: bool = False

        # create the label
        self.label: pygame.Surface = s.s_font(f_size).render(
            text, True, t_colour
        )
        self.h_label: pygame.Surface = s.s_font(f_size).render(
            text, True, t_h_colour
        )
        self.t_rect: pygame.Rect = self.label.get_rect(
            center=(self.b_rect.centerx, self.b_rect.centery - 3)
        )

    # show button
    def show(self, surf: pygame.Surface) -> None:
        """
        Draw and use the button.

        Parameters
        ----------
            surf: the pygame.Surface to display button on

        """
        clicked: bool = False  # check button clicked

        m_pos: tuple[int, int] = pygame.mouse.get_pos()
        # based on interactions, draw button
        # mouse not hovering on button
        if not self.b_rect.collidepoint(m_pos):
            # show normal button
            pygame.draw.rect(surf, self.b_colour, self.b_rect, 0, 4)
            surf.blit(self.label, self.t_rect)

        # mouse hovering
        else:
            # show hover button
            pygame.draw.rect(surf, self.b_h_colour, self.b_rect, 0, 4)
            surf.blit(self.h_label, self.t_rect)

            # check if clicked
            if not clicked:
                for events in pygame.event.get():
                    # user has clicked
                    if events.type == pygame.MOUSEBUTTONDOWN:
                        clicked = True  # resets right after due to loop

                    if events.type == pygame.MOUSEBUTTONUP:
                        clicked = False

        self.clicked = clicked


# screen parent class
class Screen:
    """Screen base."""

    # initiator method
    def __init__(self) -> None:
        """Initialise."""
        self.clock = pygame.time.Clock()  # to define FPS
        self.run_display: bool = True

        # create display
        self.screen = pygame.display.set_mode((s.SCREEN_W, s.SCREEN_H))
        pygame.display.set_caption(s.CAPTION)
        self.surf = pygame.display.get_surface()

    # handle events
    def event_handler(self) -> None:
        """Handle user quit interaction events."""
        # quit event handler
        for event in pygame.event.get():
            # if user quits program window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # update clock ticks and display
        self.clock.tick(s.FPS)
        pygame.display.update()


# main menu screen
class MainMenu(Screen):
    """Main menu screen."""

    # initiator method
    def __init__(self) -> None:
        """Initialise main menu screen."""
        Screen.__init__(self)

        # bg image
        self.BG: pygame.Surface = pygame.image.load(
            "assets/images/main_menu.png"
        )
        self.bg_rect = self.BG.get_rect()

        # title
        self.title: pygame.Surface = s.p_font(100).render(
            "ONSLOW", True, s.D2_GREEN
        )
        self.title_rect: pygame.Rect = self.title.get_rect(
            center=(self.bg_rect.centerx, self.bg_rect.top + 120)
        )
        self.subheading: pygame.Surface = s.s_font(30).render(
            "The Blackjack", True, s.D2_GREEN
        )
        self.sub_rect: pygame.Rect = self.subheading.get_rect(
            midleft=(self.title_rect.left, self.title_rect.y + 120)
        )

        # buttons
        self.start_button: Button = Button(
            "Start game",
            30,
            s.D2_GREEN,
            s.WHITE,
            s.WHITE,
            s.RED,
            220,
            50,
            self.bg_rect.centerx - 110,
            self.bg_rect.centery + 60,
        )
        self.tutorial_button: Button = Button(
            "How to play",
            30,
            s.D2_GREEN,
            s.WHITE,
            s.WHITE,
            s.RED,
            220,
            50,
            self.bg_rect.centerx - 110,
            self.bg_rect.centery + 130,
        )

    # run screen
    def run(self) -> None:
        """Run screen."""
        while self.run_display:
            # create display
            self.surf.fill(s.WHITE)
            self.surf.blit(self.BG, self.bg_rect)
            self.surf.blit(self.title, self.title_rect)
            self.surf.blit(self.subheading, self.sub_rect)

            # display buttons
            self.start_button.show(self.surf)
            self.tutorial_button.show(self.surf)

            # when buttons are used
            if self.start_button.clicked:
                self.run_display = False
                Blackjack().run()
            if self.tutorial_button.clicked:
                print("How to play!")

            self.event_handler()  # handle quit events


# connection error screen
class ErrorConnection(Screen):
    """Show that there has been error in connection."""

    # initiator method
    def __init__(self, text: str) -> None:
        """
        Initialise the game.

        Parameters
        ----------
            text: what to show user

        """
        Screen.__init__(self)

        # connection lost screen
        self.ticks: int = pygame.time.get_ticks()
        self.c_lost_text: pygame.Surface = s.p_font(50).render(
            text, True, s.D2_GREEN
        )
        self.c_lost_subtext: pygame.Surface = s.p_font(50).render(
            "Returning to main menu", True, s.D2_GREEN
        )

        self.lost_rect: pygame.Rect = self.c_lost_text.get_rect(
            center=(s.SCREEN_W / 2, s.SCREEN_H / 2)
        )
        self.subtext_rect: pygame.Rect = self.c_lost_subtext.get_rect(
            center=(s.SCREEN_W / 2, self.lost_rect.bottom + 30)
        )

    # run screen
    def run(self) -> None:
        """Run connection lost screen."""
        while self.run_display:
            # display text
            self.surf.fill(s.WHITE)
            self.surf.blit(self.c_lost_text, self.lost_rect)
            self.surf.blit(self.c_lost_subtext, self.subtext_rect)

            current_ticks: int = pygame.time.get_ticks()
            if current_ticks >= self.ticks + 1500:
                self.run_display = False
                MainMenu().run()

            self.event_handler()  # handle quit event


# blackjack game screen
class Blackjack(Screen):
    """Start a blackjack game between players."""

    # initiator method
    def __init__(self) -> None:
        """Initialise the game."""
        Screen.__init__(self)
        self.show_results: bool = False  # when game is finished

        # set up the connected socket
        try:
            self.network: Network = Network()
            self.player_no: int = int(self.network.player_no)

            # waiting for connection screen
            self.c_text: pygame.Surface = s.p_font(50).render(
                "Waiting for connection...", True, s.D2_GREEN
            )
            self.c_rect: pygame.Rect = self.c_text.get_rect(
                center=(s.SCREEN_W / 2, s.SCREEN_H / 2)
            )

            # buttons
            self.hit_button: Button = Button(
                "Hit",
                40,
                s.WHITE,
                s.WHITE,
                s.D2_GREEN,
                s.RED,
                200,
                70,
                85,
                510,
            )
            self.stand_button: Button = Button(
                "Stand",
                40,
                s.WHITE,
                s.WHITE,
                s.D2_GREEN,
                s.RED,
                200,
                70,
                315,
                510,
            )

            # cards
            self.card_faces: list[pygame.Surfaces] = [
                pygame.image.load("assets/images/cards/face.png")
            ]
            for i in range(10):
                self.card_faces.append(
                    pygame.image.load(f"assets/images/cards/{i + 1}.png")
                )

            # waiting for other player turn
            self.w_text: pygame.Surface = s.s_font(80).render(
                "Waiting...", True, s.D1_GREEN
            )
            self.w_rect: pygame.Rect = self.w_text.get_rect(
                center=(s.SCREEN_W / 2, s.SCREEN_H - 100)
            )

            # other player stands text
            self.stand_text: pygame.Surface = s.p_font(100).render(
                "Stand", True, s.WHITE
            )
            self.stand_rect: pygame.Rect = self.stand_text.get_rect(
                center=(s.SCREEN_W / 2, s.SCREEN_H - 100)
            )
            self.stand_bg_rect: pygame.Rect = pygame.Rect(
                150, self.stand_rect.top - 10, 300, 150
            )

            # bust text
            self.bust_text: pygame.Surface = s.p_font(100).render(
                "Bust!", True, s.WHITE
            )
            self.bust_rect: pygame.Rect = self.bust_text.get_rect(
                center=(s.SCREEN_W / 2, s.SCREEN_H - 100)
            )
            self.bg_rect: pygame.Rect = pygame.Rect(
                150, self.bust_rect.top - 10, 300, 150
            )

        # Connection error, server has not started
        except TypeError:
            self.run_display = False
            ErrorConnection("Run server first...").run()

    # draw cards and total of players onto screen
    def display_cards(self) -> None:
        """Draw the cards of the players."""
        # show total of cards
        total_text: pygame.Surface = s.p_font(40).render(
            f"Total: {self.player.hand_total}", True, s.D2_GREEN
        )
        t_rect: pygame.Rect = total_text.get_rect(bottomleft=(80, 210))
        self.surf.blit(total_text, t_rect)  # show total

        for i in range(2):
            card_colour: str = s.WHITE if i == self.player_no else s.D1_GREEN
            outline_colour: str = (
                s.D1_GREEN if i == self.player_no else s.WHITE
            )

            for j, symbol in enumerate(self.game.players[i].hand):
                if i == self.player_no:
                    # player's card in front
                    c_rect: pygame.Rect = pygame.Rect(
                        (80 + 50 * j), (250 + 5 * j), 120, 200
                    )
                else:
                    # opposing player's cards at the back
                    c_rect = pygame.Rect(
                        (400 - 50 * j), (50 - 5 * j), 120, 200
                    )

                # draw cards
                pygame.draw.rect(self.surf, card_colour, c_rect, 0, 4)

                # draw card symbol for user
                if i == self.player_no:
                    if symbol in ["J", "Q", "K", "A"]:
                        index: int = 0
                    else:
                        index = int(symbol)
                    self.surf.blit(self.card_faces[index], c_rect)

                    symbol_label = s.p_font(30).render(
                        symbol, True, s.D2_GREEN
                    )
                    self.surf.blit(
                        symbol_label, (c_rect.left + 10, c_rect.top + 1)
                    )
                    self.surf.blit(
                        symbol_label, (c_rect.left + 10, c_rect.bottom - 41)
                    )

                pygame.draw.rect(self.surf, outline_colour, c_rect, 3, 4)

    # draw hit/stand buttons if user turn
    def display_buttons(self) -> None:
        """Draw buttons when user's turn."""
        # show buttons if turn
        if self.player.turn:
            self.hit_button.show(self.surf)
            if self.hit_button.clicked:
                self.network.send("hit")

            self.stand_button.show(self.surf)
            if self.stand_button.clicked:
                self.network.send("stand")

        # both users not active, show results
        elif not any([player.active for player in self.game.players]):
            self.ticks: int = pygame.time.get_ticks()  # get ticks for clock
            self.show_results = True

        # otherwise, do next round
        else:
            self.network.send("next round")
            self.surf.blit(self.w_text, self.w_rect)

    # draw other visual indicators
    def display_indicator(
        self,
        text: str,
        size: int,
        f_colour: str,
        bg_colour: str,
        width: int,
        height: int,
        centerx: float,
        centery: float,
    ) -> None:
        """
        Display other visual indicators of the game.

        Parameters
        ----------
            text: text to display
            size: font size
            f_colour: font colour
            bg_colour: colour of rect behind text
            width: width of bg rect
            height: height of bg rect
            centerx: x coord of bg centre
            centery: y coord of bg centre

        """
        # generate widgets
        bg_rect: pygame.Rect = pygame.Rect(
            centerx - (width / 2), centery - height / 2, width, height
        )
        label: pygame.Surface = s.p_font(size).render(text, True, f_colour)
        label_rect: pygame.Rect = label.get_rect(
            center=(bg_rect.centerx, bg_rect.centery)
        )

        # display
        pygame.draw.rect(self.surf, bg_colour, bg_rect, 0, 4)
        self.surf.blit(label, label_rect)

    # draw card result
    def display_card_result(self) -> None:
        """Show card result after a game."""
        # show card results of each player
        for i, player in enumerate(self.game.players):
            user: int = 0 if i == self.player_no else 1  # if cards are user's
            user_text: str = "Your" if i == self.player_no else "Opponent's"
            cards_start: float = (
                s.SCREEN_W - ((len(player.hand) + 1) * 50)
            ) / 2

            # show total of cards
            total_text: pygame.Surface = s.p_font(40).render(
                f"{user_text} Total: {player.hand_total}", True, s.D2_GREEN
            )
            t_rect: pygame.Rect = total_text.get_rect(
                center=(s.SCREEN_W / 2, 590 - 550 * user)
            )
            self.surf.blit(total_text, t_rect)  # show total

            # draw cards
            for j, symbol in enumerate(player.hand):
                c_rect: pygame.Rect = pygame.Rect(
                    (cards_start + 50 * j),
                    (t_rect.bottom + 20 if bool(user) else t_rect.top - 220),
                    120,
                    200,
                )
                if symbol in ["J", "Q", "K", "A"]:
                    index: int = 0
                else:
                    index = int(symbol)
                self.surf.blit(self.card_faces[index], c_rect)

                symbol_label = s.p_font(30).render(symbol, True, s.D2_GREEN)
                self.surf.blit(
                    symbol_label, (c_rect.left + 10, c_rect.top + 1)
                )
                self.surf.blit(
                    symbol_label, (c_rect.left + 10, c_rect.bottom - 41)
                )

                pygame.draw.rect(self.surf, s.D1_GREEN, c_rect, 3, 4)

            # draw other conditions (i.e. bust or blackjack)
            if player.bust or player.blackjack:
                if player.bust:
                    text: str = "Bust!"
                    colour: str = s.RED
                    width: int = 170
                elif player.blackjack:
                    text = "Blackjack!"
                    colour = s.L_GREEN
                    width = 180
                self.display_indicator(
                    text,
                    65,
                    s.WHITE,
                    colour,
                    width,
                    80,
                    s.SCREEN_W / 2,
                    c_rect.top + 100,
                )

    # run game
    def run(self) -> None:
        """Run blackjack game."""
        while self.run_display:
            # create display
            self.surf.fill(s.WHITE)

            try:
                # get game from connection
                self.game = self.network.send("get")  # get the user's game
                self.player = self.game.players[self.player_no]
                self.opp = self.game.players[self.player_no - 1]

                # game finished
                if self.show_results:
                    # show short card result before main result screen
                    current_ticks: int = pygame.time.get_ticks()
                    if current_ticks <= self.ticks + 2000:
                        self.display_card_result()

                    ## if both stood, go straight to results screen
                    ## otherwise, go after short result
                    else:
                        self.run_display = False
                        self.network.send("finished")

                # if two users connected, play
                elif self.game.ready:
                    self.display_cards()
                    self.display_buttons()

                    # indicate whether other player has stood
                    if not self.opp.active and self.player.active:
                        self.display_indicator(
                            "Stood",
                            40,
                            s.WHITE,
                            s.L_GREEN,
                            150,
                            50,
                            470,
                            150,
                        )

                # p1 waiting for another user, p2, to join
                else:
                    self.surf.blit(self.c_text, self.c_rect)

            except:
                if self.show_results:
                    Results(
                        self.player.hand_total,
                        self.opp.hand_total,
                        self.player.win,
                        self.opp.win,
                    ).run()

                else:
                    # other client has quit (e.g. other player lost connection)
                    # stop game and tell still connected user
                    self.run_display = False
                    ErrorConnection("Connection lost...").run()

            self.event_handler()  # handle quit events


# results screen
class Results(Screen):
    """Display the results of a blackjack game."""

    # initiator method
    def __init__(
        self, user_total: int, opp_total: int, user_win: bool, opp_win: bool
    ) -> None:
        """
        Initialise results screen.

        Parameters
        ----------
            user_total: the card total of the user
            opp_total: the card total of the opponent user
            user_win: whether the user won
            opp_win: whether the opponent won

        """
        Screen.__init__(self)

        # results menu buttons
        self.new_button: Button = Button(  # connect to a new game
            "New game",
            30,
            s.WHITE,
            s.WHITE,
            s.D2_GREEN,
            s.RED,
            280,
            55,
            s.SCREEN_W / 2 - 140,
            s.SCREEN_H / 2 + 105,
        )
        self.back_button: Button = Button(  # return to main menu
            "Back to main menu",
            30,
            s.WHITE,
            s.WHITE,
            s.D2_GREEN,
            s.RED,
            280,
            55,
            s.SCREEN_W / 2 - 140,
            s.SCREEN_H / 2 + 175,
        )

        # both players results
        self.user_total: pygame.Surface = s.s_font(40).render(
            f"You got {user_total}", True, s.D1_GREEN
        )
        self.opp_total: pygame.Surface = s.s_font(40).render(
            f"Opponent got {opp_total}", True, s.D1_GREEN
        )

        # overall result
        if user_win:  # user wins
            result: str = "won"
        elif opp_win:  # opponent wins
            result = "lost"
        else:  # tie
            result = "tie"
        self.win_result: pygame.Surface = s.p_font(70).render(
            f"You {result}!", True, s.RED
        )

        # get rects for each text
        self.user_rect: pygame.Rect = self.user_total.get_rect(
            center=(s.SCREEN_W / 2, 100)
        )
        self.opp_rect: pygame.Rect = self.opp_total.get_rect(
            center=(s.SCREEN_W / 2, self.user_rect.bottom + 40)
        )
        self.win_rect: pygame.Rect = self.win_result.get_rect(
            center=(s.SCREEN_W / 2, self.opp_rect.bottom + 70)
        )

    # run screen
    def run(self) -> None:
        """Display result."""
        while self.run_display:
            self.surf.fill(s.WHITE)

            # display result
            self.surf.blit(self.user_total, self.user_rect)
            self.surf.blit(self.opp_total, self.opp_rect)
            self.surf.blit(self.win_result, self.win_rect)

            # next action buttons
            self.new_button.show(self.surf)
            if self.new_button.clicked:
                Blackjack().run()

            self.back_button.show(self.surf)
            if self.back_button.clicked:
                self.run_display = False
                MainMenu().run()

            self.event_handler()  # handle quit events


if __name__ == "__main__":
    pygame.init()
    MainMenu().run()

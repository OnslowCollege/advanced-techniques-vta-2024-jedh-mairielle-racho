"""
Play Blackjack with an Onslow Twist.

Created by: Jedh
Date: 2024-06-17
"""

import pygame
import settings as settings
from network import Network
import pickle
import sys
from game import Game


# create buttons
class Button:
    """Create a clickable button."""

    # initiator method
    def __init__(
        self,
        text: str,
        size: int,
        t_colour: str,
        t_h_colour: str,
        b_colour: str,
        b_h_colour: str,
        b_width: int,
        b_height: int,
        b_x: int,
        b_y: int,
    ) -> None:
        """
        Initialise the button appearance.

        Parameters
        ----------
            text: the button label
            size: the font size of the button
            t_colour: the non-hover text colour
            t_h_colour: the hover text colour
            b_colour: the non-hover button colour
            b_h_colour: the hover button colour
            b_width: the width of the button
            b_height: the height of the button
            b_x: the x value of topleft
            b_y: the y value of topleft

        """
        # button specifications
        self.b_colour = b_colour
        self.b_h_colour = b_h_colour

        self.b_rect = pygame.Rect(b_x, b_y, b_width, b_height)

        # text colours
        self.text = settings.s_font(size).render(text, True, t_colour)
        self.h_text = settings.s_font(size).render(text, True, t_h_colour)
        self.t_rect = self.text.get_rect(
            center=(self.b_rect.centerx, self.b_rect.centery - 3)
        )

    # show button
    def show_button(self, surf: pygame.Surface) -> bool:
        """
        Draw and use button.

        Parameters
        ----------
            surf: the pygame.Surface to display button on
            b_pos: the coord of the topleft corner of the button
        Returns true when clicked

        """
        clicked = False
        # draw button

        m_pos = pygame.mouse.get_pos()
        # check user interactions
        # not hovering
        if not self.b_rect.collidepoint(m_pos):
            # show normal button
            pygame.draw.rect(surf, self.b_colour, self.b_rect, 0, 4)
            surf.blit(self.text, self.t_rect)

        # mouse hover
        else:
            # display hover button
            pygame.draw.rect(surf, self.b_h_colour, self.b_rect, 0, 4)
            surf.blit(self.h_text, self.t_rect)

            # check click
            if not clicked:
                for events in pygame.event.get():
                    # user has clicked
                    if events.type == pygame.MOUSEBUTTONDOWN:
                        clicked = True

                    # reset click
                    if events.type == pygame.MOUSEBUTTONUP:
                        clicked = False

        return clicked


# screen parent class
class Screen:
    """Screen base."""

    # initiator method
    def __init__(self) -> None:
        """Initialise."""
        self.clock = pygame.time.Clock()  # to define FPS
        self.run_display: bool = True

        # create display
        self.screen = pygame.display.set_mode(
            (settings.SCREEN_W, settings.SCREEN_H), pygame.RESIZABLE
        )
        pygame.display.set_caption(settings.NAME)  # name window
        self.display_surf = pygame.display.get_surface()
        self.w, self.h = pygame.display.get_surface().get_size()

    def event_handler(self) -> None:
        """Handle user-interaction events."""
        # get center
        self.w, self.h = pygame.display.get_surface().get_size()
        # update clock ticks and display
        self.clock.tick(settings.FPS)
        pygame.display.update()

        # event handler
        for event in pygame.event.get():
            # if user quits program window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def run(self) -> None:
        """Run program."""
        while self.run_display:
            self.display_surf.fill(settings.WHITE)
            self.event_handler()


# main menu screen
class MainMenu(Screen):
    """Main menu screen."""

    # initiator method
    def __init__(self) -> None:
        """Initialise main menu screen."""
        Screen.__init__(self)

        # bg image
        self.bg = pygame.image.load("assets/images/main_menu.png")

        # title
        self.title = settings.p_font(100).render(
            "ONSLOW", True, settings.D2_GREEN
        )
        self.sub = settings.s_font(30).render(
            "The Blackjack", True, settings.D2_GREEN
        )

        # buttons
        self.start_b = settings.s_font(30).render(
            "Start game", True, settings.WHITE
        )
        self.tutorial_b = settings.s_font(30).render(
            "How to play", True, settings.WHITE
        )

    # create display
    def create_display(self) -> None:
        """Create the display."""
        # bg
        self.display_surf.fill(settings.WHITE)
        bg_rect = self.bg.get_rect(center=(self.w / 2, self.h / 2))
        self.display_surf.blit(self.bg, bg_rect)

        # title
        title_rect = self.title.get_rect(
            center=(bg_rect.centerx, bg_rect.top + 120)
        )
        sub_rect = self.sub.get_rect(
            midleft=(title_rect.left, title_rect.y + 120)
        )
        self.display_surf.blit(self.title, title_rect)
        self.display_surf.blit(self.sub, sub_rect)

        # buttons
        self.s_button = Button(
            "Start game",
            30,
            settings.D2_GREEN,
            settings.WHITE,
            settings.WHITE,
            settings.RED,
            220,
            50,
            bg_rect.centerx - 110,
            bg_rect.centery + 60,
        )
        self.start = self.s_button.show_button(self.display_surf)

        self.t_button = Button(
            "How to play",
            30,
            settings.D2_GREEN,
            settings.WHITE,
            settings.WHITE,
            settings.RED,
            220,
            50,
            bg_rect.centerx - 110,
            bg_rect.centery + 130,
        )
        self.tutorial = self.t_button.show_button(self.display_surf)

    # run screen
    def run(self) -> None:
        """Run screen."""
        while self.run_display:
            # create display
            self.create_display()

            if self.start:
                self.run_display = False
                Start().run()
            if self.tutorial:
                print("How to play!")

            self.event_handler()


# run start
class Start(Screen):
    """Start game."""

    # initiator method
    def __init__(self) -> None:
        """Initialise game."""
        Screen.__init__(self)

        # set up network
        self.network = Network()
        self.player_no: int = int(self.network.player_no)
        print("You are player", self.player_no + 1)

        # waiting for connection text
        self.c_text = settings.p_font(50).render(
            "Waiting for connection...", True, settings.D2_GREEN
        )
        self.c_rect = self.c_text.get_rect(center=(300, 325))

        # connection lost text
        self.c_loss_text = settings.p_font(50).render(
            "Connection lost...", True, settings.D2_GREEN
        )
        self.c_loss_rect = self.c_loss_text.get_rect(center=(300, 325))
        self.c_loss_subtext = settings.s_font(30).render(
            "Returning to main menu", True, settings.D2_GREEN
        )
        self.l_subtext_rect = self.c_loss_subtext.get_rect(
            center=(300, self.c_loss_rect.bottom + 30)
        )

    # draw cards
    def draw_cards(self) -> None:
        """Draw the cards of the players."""
        for i in range(2):  # for both players
            # front hand is user's
            spacing: int = [0 if i == self.player_no else 1][0]
            for j, symbol in enumerate(self.game.players[i].hand):
                colour: str = [
                    settings.RED if i == self.player_no else settings.D1_GREEN
                ][0]
                c_rect: pygame.Rect = pygame.Rect(
                    (80 + 50 * j), (280 + 5 * j - 240 * spacing), 120, 200
                )
                # draw card
                pygame.draw.rect(self.display_surf, colour, c_rect, 0, 4)
                pygame.draw.rect(
                    self.display_surf, settings.D1_GREEN, c_rect, 3, 4
                )
                symbol_text = settings.p_font(30).render(
                    symbol, True, settings.D1_GREEN
                )
                symbol_rect = symbol_text.get_rect(
                    topleft=(c_rect.left + 10, c_rect.top + 1)
                )
                self.display_surf.blit(symbol_text, symbol_rect)

    # run game
    def run(self) -> None:
        """Run game."""
        while self.run_display:
            # draw GUI background
            self.display_surf.fill(settings.WHITE)

            # attempt to connect 2 clients
            try:
                self.game = self.network.send("get")  # get their game

                # if connection between two users has been established, play
                if self.game.ready:
                    # draw player cards
                    self.draw_cards()

                # p1 waiting for another user (p2)
                else:
                    self.display_surf.blit(self.c_text, self.c_rect)

            except:
                # other client has exited (e.g. other player lost connection)
                # so stop game and tell still connected user
                self.display_surf.blit(self.c_loss_text, self.c_loss_rect)
                self.display_surf.blit(
                    self.c_loss_subtext, self.l_subtext_rect
                )
                pygame.display.update()
                pygame.time.wait(2000)  # wait 2s before main menu
                self.run_display = False
                MainMenu().run()

            # program actions
            self.event_handler()


if __name__ == "__main__":
    pygame.init()
    MainMenu().run()

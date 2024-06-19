"""Create a screen."""

import pygame
from settings import *
from base import *


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
        self.title = p_font(100).render("ONSLOW", True, D2_GREEN)
        self.sub = p_font(30).render("The Blackjack", True, D2_GREEN)

        # buttons
        self.start_b = s_font(30).render("Start game", True, WHITE)
        self.tutorial_b = s_font(30).render("How to play", True, WHITE)

    # create display
    def create_display(self) -> None:
        """Create the display."""
        # bg
        self.display_surf.fill(WHITE)
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

    # run screen
    def run(self) -> None:
        """Run screen."""
        while self.run_display:
            # create display
            self.create_display()

            self.event_handler()

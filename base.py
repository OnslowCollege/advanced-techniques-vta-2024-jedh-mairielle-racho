"""Base classes."""

import pygame
import sys
from settings import *


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
            (SCREEN_W, SCREEN_H), pygame.RESIZABLE
        )
        pygame.display.set_caption(NAME)  # name window
        self.display_surf = pygame.display.get_surface()
        self.w, self.h = pygame.display.get_surface().get_size()

    def event_handler(self) -> None:
        """Handle user-interaction events."""
        # get center
        self.w, self.h = pygame.display.get_surface().get_size()
        # update clock ticks and display
        self.clock.tick(FPS)
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
            self.display_surf.fill(WHITE)
            self.event_handler()
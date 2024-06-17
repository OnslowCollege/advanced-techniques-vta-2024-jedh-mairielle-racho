"""
Play Blackjack with an Onslow Twist.

Created by: Jedh
Date: 2024-06-17
"""
import pygame
import sys
from settings import*

# run main
class Main:
    """Main program."""

    def __init__(self) -> None:
        """Initialise."""
        pygame.init()
        self.clock = pygame.time.Clock()  # to define FPS
        self.run_display: bool = True

        # create display
        pygame.display.set_caption("Blackjack")  # name window
        self.screen = pygame.display.set_mode(
            (SCREEN_W, SCREEN_H), pygame.RESIZABLE
        )
        self.display_surf = pygame.display.get_surface()

    def event_handler(self) -> None:
        """Handle user-interaction events."""
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


if "__name__" == "__main__":
    # run program
    main = Main()
    main.run()

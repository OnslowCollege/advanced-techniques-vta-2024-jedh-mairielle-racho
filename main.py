"""
Play Blackjack with an Onslow Twist.

Created by: Jedh
Date: 2024-06-17
"""
import pygame
from settings import*

# run main
class Main:
    """Main program."""

    def __init__(self) -> None:
        """Initialise."""
        pygame.init()
        self.run: bool = True

        # create display
        self.screen = pygame.display.setmode((SCREEN_W, SCREEN_H),
        pygame.RESIZABLE)
        pygame.display.set_caption("Blackjack")  # name window

    def event_handler(self) -> None:
        """Handle user-interaction events."""
        pygame.display.update()
        for event in pygame.event.get():
            # if user quits program window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def run(self) -> None:
        while self.run == True:
            

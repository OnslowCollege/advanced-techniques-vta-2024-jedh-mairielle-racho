"""Program settings."""
import pygame

# screen
SCREEN_W: int = 480
SCREEN_H: int = 800

# screen
class Screen:
    """Screen parent class."""

    def __init__(self) -> None:
        """Initialise."""
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

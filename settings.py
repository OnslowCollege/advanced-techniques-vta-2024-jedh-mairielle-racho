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
        self.
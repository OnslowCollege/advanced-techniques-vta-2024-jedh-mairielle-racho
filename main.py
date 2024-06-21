"""
Play Blackjack with an Onslow Twist.

Created by: Jedh
Date: 2024-06-17
"""
import pygame
from screens import *
from settings import*

# run main
class Main:
    """Main program."""

    # initiator method
    def __init__(self) -> None:
        """Initialise."""
        pygame.init()
        self.main_menu = MainMenu()

    # run program
    def run(self) -> None:
        """Run the program."""
        self.main_menu.run()


if __name__ == "__main__":
    # run program
    main = Main()
    main.run()

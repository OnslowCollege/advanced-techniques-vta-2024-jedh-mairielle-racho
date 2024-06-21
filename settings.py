"""Program settings."""
import pygame

# name
NAME: str = "Onslow the Blackjack"

# screen
SCREEN_W: int = 600
SCREEN_H: int = 650

# framerate
FPS: int = 60

# colours
WHITE: str = "#f7f6f6"
L_GREEN: str = "#7ec4a0"
D1_GREEN: str = "#266b63"
D2_GREEN: str = "#163e39"
RED: str = "#b63110"

# font
def p_font(size: int) -> pygame.font.Font:
    """Get the primary font."""
    return pygame.font.Font("assets/font/coolvetica rg.otf", size)


def s_font(size: int) -> pygame.font.Font:
    """Get secondary font."""
    return pygame.font.Font("assets/font/MusticaPro-SemiBold.otf", size)

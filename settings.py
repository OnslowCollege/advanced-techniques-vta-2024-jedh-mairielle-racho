"""Program settings."""

import pygame

# server settings
# school ip: 10.47.40.56
# home ip: 192.168.68.153 / 192.168.1.122
SERVER: str = "10.47.40.56"
PORT: int = 1234

# client window title
CAPTION: str = "Onslow the Blackjack"

# screen specifications
SCREEN_W: int = 600
SCREEN_H: int = 650
FPS: int = 60  # frame rate

# colours
WHITE: str = "#f7f6f6"
L_GREEN: str = "#7ec4a0"
D1_GREEN: str = "#266b63"
D2_GREEN: str = "#163e39"
RED: str = "#b63110"


# font
def p_font(size: int) -> pygame.font.Font:  # primary font
    """Initialise the primary font."""
    return pygame.font.Font("assets/font/coolvetica rg.otf", size)


def s_font(size: int) -> pygame.font.Font:  # secondary font
    """Initialise the secondary font."""
    return pygame.font.Font("assets/font/MusticaPro-SemiBold.otf", size)

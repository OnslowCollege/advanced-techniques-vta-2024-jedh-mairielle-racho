"""Program settings."""
import pygame

# screen
SCREEN_W: int = 500
SCREEN_H: int = 500

# framerate
FPS: int = 60

# colours
WHITE: str = "#f7f6f6"
L_GREEN: str = "#7ec4a0"
D1_GREEN: str = "#266b63"
D2_GREEN: str = "163e39"
RED: str = "#b63110"

# font
def p_font(size: int) -> pygame.font.Font:
    """Get the primary font."""
    return pygame.font.Font("assets/font/Makasih.ttf", size)

def s_font(size: int) -> pygame.font.Font:
    """Get secondary font."""
    return pygame.font.Font("assets/font/TangoSans.ttf", size)

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


# button class
class Button:
    """Create a clickable button."""

    # initiator method
    def __init__(
        self,
        text: str,
        size: int,
        t_colour: str,
        t_h_colour: str,
        b_colour: str,
        b_h_colour: str,
        b_width: int,
        b_height: int,
        b_x: int,
        b_y: int,
    ) -> None:
        """
        Initialise the button appearance.

        Parameters
        ----------
            text: the button label
            size: the font size of the button
            t_colour: the non-hover text colour
            t_h_colour: the hover text colour
            b_colour: the non-hover button colour
            b_h_colour: the hover button colour
            b_width: the width of the button
            b_height: the height of the button
            b_x: the x value of topleft
            b_y: the y value of topleft

        """
        # button specifications
        self.b_colour = b_colour
        self.b_h_colour = b_h_colour

        self.b_rect = pygame.Rect(b_x, b_y, b_width, b_height)

        # text colours
        self.text = s_font(size).render(text, True, t_colour)
        self.h_text = s_font(size).render(text, True, t_h_colour)
        self.t_rect = self.text.get_rect(
            center=(self.b_rect.centerx, self.b_rect.centery)
        )

    # show button
    def show_button(self, surf: pygame.Surface) -> bool:
        """
        Draw and use button.

        Parameters
        ----------
            surf: the pygame.Surface to display button on
            b_pos: the coord of the topleft corner of the button
        Returns true when clicked
        """
        clicked = False
        # draw button

        m_pos = pygame.mouse.get_pos()
        # check user interactions
        # not hovering
        if not self.b_rect.collidepoint(m_pos):
            # show normal button
            pygame.draw.rect(surf, self.b_colour, self.b_rect, 0, 4)
            surf.blit(self.text, self.t_rect)

        # mouse hover
        else:
            # display hover button
            pygame.draw.rect(surf, self.b_h_colour, self.b_rect, 0, 4)
            surf.blit(self.h_text, self.t_rect)

            # check click
            if not clicked:
                for events in pygame.event.get():
                    # user has clicked
                    if events.type == pygame.MOUSEBUTTONDOWN:
                        clicked = True

                    # reset click
                    if events.type == pygame.MOUSEBUTTONUP:
                        clicked = False

        return clicked

import pygame
import sys

pygame.init()

SCREEN = pygame.display.set_mode((1440, 850))

default_background = pygame.image.load("CadenceRushBackground.png").convert()


class Button():
    """Button class to easily create buttons for my program and automatically """

    def __init__(self, image, pos, text_input, font, base_colour, hovering_colour):
        """Initializes the components of the button"""
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.text_input = text_input
        self.font = font
        self.base_colour = base_colour
        self.hovering_colour = hovering_colour
        self.text = self.font.render(self.text_input, True, self.base_colour)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
    
    def update(self, screen):
        """Draws the button image and/or text onto the screen."""
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        """Checks if the player's mouse click is within the button."""
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        """Changes the text color if the mouse is hovering over the button."""
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_colour)
        else:
            self.text = self.font.render(self.text_input, True, self.base_colour)


def get_font(size):
    """Returns the custom font along with the size that was inputted."""
    return pygame.font.Font("assets/font.ttf", size)

def main_menu():
    """Handles the main menu screen."""
    pygame.display.set_caption("Menu")

    while True:
        SCREEN.blit(default_background, (-50, 0))
        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(100).render("Main Menu", True, "#ffffff")
        menu_rect = menu_text.get_rect(center=(720, 150))
        SCREEN.blit(menu_text, menu_rect)

        play_button = Button(image=None, pos=(720, 350), text_input="PLAY", font=get_font(50), base_colour="#d7fcd4", hovering_colour="#ffffff")
        options_button = Button(image=None, pos=(720, 500), text_input="OPTIONS", font=get_font(50), base_colour="#d7fcd4", hovering_colour="#ffffff")
        quit_button = Button(image=None, pos=(720, 650), text_input="QUIT", font=get_font(50), base_colour="#d7fcd4", hovering_colour="#ffffff")

        for button in [play_button, options_button, quit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    start_game()
                if options_button.checkForInput(menu_mouse_pos):
                    options()
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

main_menu()
pygame.quit()



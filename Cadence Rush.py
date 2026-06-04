import pygame

pygame.init()

SCREEN = pygame.display.set_mode((1440, 850))

default_background = pygame.image.load("CadenceRushBackground.png").convert()

running = True


class Button():
    def __init__(self, image, pos, text_input, font, base_colour, hovering_colour):
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


def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def main_menu():
    pygame.display.set_caption("Menu")
    global running

    while running:
        SCREEN.blit(default_background, (-50, 0))

        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(100).render("Main Menu", True, "#ffffff")
        menu_rect = menu_text.get_rect(center=(640, 100))



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

main_menu()
pygame.quit()



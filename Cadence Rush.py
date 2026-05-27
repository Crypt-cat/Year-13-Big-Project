import pygame

pygame.init()

screen = pygame.display.set_mode((1440, 850))

background = pygame.image.load("CadenceRushBackground.png").convert()

running = True
while running:

    screen.blit(background, (-50, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()



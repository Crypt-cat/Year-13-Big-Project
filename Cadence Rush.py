import pygame
import sys

pygame.init()

SCREEN = pygame.display.set_mode((1440, 850))
clock = pygame.time.Clock()

default_background = pygame.image.load("Year-13-Big-project/assets/CadenceRushBackground.png").convert()

outline_up  = pygame.transform.scale(pygame.image.load("Year-13-Big-project/assets/Arrow_Outline_1.png").convert_alpha(), (80, 80))
outline_left  = pygame.transform.scale(pygame.image.load("Year-13-Big-project/assets/Arrow_Outline_2.png").convert_alpha(), (80, 80))
outline_down    = pygame.transform.scale(pygame.image.load("Year-13-Big-project/assets/Arrow_Outline_3.png").convert_alpha(), (80, 80))
outline_right = pygame.transform.scale(pygame.image.load("Year-13-Big-project/assets/Arrow_Outline_4.png").convert_alpha(), (80, 80))

note_up  = pygame.transform.scale(pygame.image.load("Year-13-Big-project/assets/Arrow_Colour_1.png").convert_alpha(), (80, 80))
note_left  = pygame.transform.scale(pygame.image.load("Year-13-Big-project/assets/Arrow_Colour_2.png").convert_alpha(), (80, 80))
note_down    = pygame.transform.scale(pygame.image.load("Year-13-Big-project/assets/Arrow_Colour_3.png").convert_alpha(), (80, 80))
note_right = pygame.transform.scale(pygame.image.load("Year-13-Big-project/assets/Arrow_Colour_4.png").convert_alpha(), (80, 80))

receptor_images = {0: outline_left, 1: outline_down, 2: outline_up, 3: outline_right}
note_images     = {0: note_left,     1: note_down,     2: note_up,     3: note_right}

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
        if self.image != self.text:
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
    return pygame.font.Font("Year-13-Big-project/assets/font.ttf", size)

CHART_OFFSET = 1400

NIGHT_OF_NIGHTS_CHART = []

start_intro = 0 + CHART_OFFSET
for i in range(24):
    lane = i % 4 if (i // 4) % 2 == 0 else 3 - (i % 4)
    NIGHT_OF_NIGHTS_CHART.append([start_intro + int(i * 333.33), lane])

start_verse = int(24 * 333.33) + 500 + CHART_OFFSET
for i in range(16):
    t_base = start_verse + int(i * 666.66)
    NIGHT_OF_NIGHTS_CHART.append([t_base, 0])
    NIGHT_OF_NIGHTS_CHART.append([t_base + 166, 1])
    NIGHT_OF_NIGHTS_CHART.append([t_base + 333, 2])

start_pre = start_verse + int(16 * 666.66)
for i in range(12):
    t_base = start_pre + int(i * 333.33)
    if i % 2 == 0:
        NIGHT_OF_NIGHTS_CHART.append([t_base, 0])
        NIGHT_OF_NIGHTS_CHART.append([t_base, 3])
    else:
        NIGHT_OF_NIGHTS_CHART.append([t_base, 1])
        NIGHT_OF_NIGHTS_CHART.append([t_base, 2])

start_drop = start_pre + int(12 * 333.33)
stair_pattern = [0, 1, 2, 3, 2, 1, 0, 1, 2, 3, 2, 1, 0, -1, 3, -1]
for i in range(64):
    t = start_drop + int(i * 166.66)
    lane = stair_pattern[i % len(stair_pattern)]
    if lane != -1:
        NIGHT_OF_NIGHTS_CHART.append([t, lane])

def start_game():
    pygame.display.set_caption("Cadence Rush")

    lane_x_positions = [520, 620, 720, 820]
    receptor_y = 700
    scroll_speed = 0.5 
    
    counts = {"MAX": 0, "300": 0, "200": 0, "100": 0, "50": 0, "MISS": 0}
    score = 0
    combo = 0
    max_combo = 0
    total_notes_played = 0
    accuracy = 100.0

    chart_notes = list(NIGHT_OF_NIGHTS_CHART)
    active_notes = []
    
    start_time = pygame.time.get_ticks()
    back_button = Button(image=None, pos=(100, 50), text_input="BACK", font=get_font(30), base_colour="#ffffff", hovering_colour="#00ff00")

    while True:
        SCREEN.fill("black")
        mouse_pos = pygame.mouse.get_pos()
        
        current_time = pygame.time.get_ticks() - start_time - 3000

        for lane_idx, x_pos in enumerate(lane_x_positions):
            SCREEN.blit(receptor_images[lane_idx], (x_pos, receptor_y))
        
        if current_time > 0:
            while chart_notes and chart_notes[0][0] <= current_time + 1500:
                spawned = chart_notes.pop(0)
                active_notes.append({"hit_time": spawned[0], "lane": spawned[1]})

        for note in active_notes[:]:
            time_difference = note["hit_time"] - current_time
            note_y = receptor_y - (time_difference * scroll_speed)

            if -80 <= note_y <= 850:
                SCREEN.blit(note_images[note["lane"]], (lane_x_positions[note["lane"]], note_y))

            if time_difference < -133: 
                counts["MISS"] += 1
                total_notes_played += 1
                combo = 0
                active_notes.remove(note)

        if total_notes_played > 0:
            numerator = 300 * (counts["MAX"] + counts["300"]) + 200 * counts["200"] + 100 * counts["100"] + 50 * counts["50"]
            denominator = 300 * total_notes_played
            accuracy = (numerator / denominator) * 100

        acc_str = f"ACC: {accuracy:.2f}%"
        stat_str = f"MAX:{counts['MAX']}  300:{counts['300']}  200:{counts['200']}  100:{counts['100']}  50:{counts['50']}  MISS:{counts['MISS']}"
        score_str = f"SCORE: {score:07d}"
        combo_str = f"{combo}x COMBO"
        
        SCREEN.blit(get_font(25).render(acc_str, True, "#ffffff"), (1100, 40))
        SCREEN.blit(get_font(18).render(stat_str, True, "#aaaaaa"), (250, 40))
        SCREEN.blit(get_font(30).render(score_str, True, "#ffffff"), (1000, 780))
        SCREEN.blit(get_font(30).render(combo_str, True, "#ffffff"), (50, 780))
        

        if -3000 <= current_time <= 500:
            if current_time < 0:
                ready_seconds = abs(current_time) // 1000 + 1
            else:
                ready_seconds = 0

            ready_text = get_font(60).render(str(ready_seconds), True, "#ff0000")
            SCREEN.blit(ready_text, (695, 350))

        back_button.changeColor(mouse_pos)
        back_button.update(SCREEN)
                   
        pressed_lane = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN and back_button.checkForInput(mouse_pos):
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a: pressed_lane = 0
                elif event.key == pygame.K_s: pressed_lane = 1
                elif event.key == pygame.K_k: pressed_lane = 2
                elif event.key == pygame.K_l: pressed_lane = 3

                if pressed_lane is not None:
                    for note in active_notes:
                        if note["lane"] == pressed_lane:
                            diff = abs(note["hit_time"] - current_time)

                            if diff <= 16:
                                counts["MAX"] += 1
                                score += 320
                            elif diff <= 46:
                                counts["300"] += 1
                                score += 300
                            elif diff <= 79:
                                counts["200"] += 1
                                score += 200
                            elif diff <= 109:
                                counts["100"] += 1
                                score += 100
                            elif diff <= 133:
                                counts["50"] += 1
                                score += 50
                            else:
                                continue

                            combo += 1
                            if combo > max_combo:
                                max_combo = combo

                            total_notes_played += 1
                            active_notes.remove(note)
                            break

        pygame.display.flip()
        clock.tick(60)


def options():
    pygame.display.set_caption("Options")

    back_button = Button(image=None, pos=(720, 600), text_input="BACK", font=get_font(40), base_colour="#ffffff", hovering_colour="#00ff00")
    
    options_text = get_font(60).render("Options", True, "#ffffff")
    options_rect = options_text.get_rect(center=(720, 300))
    
    while True:
        SCREEN.fill("black")
        SCREEN.blit(options_text, options_rect)
        mouse_pos = pygame.mouse.get_pos()
        
        back_button.changeColor(mouse_pos)
        back_button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkForInput(mouse_pos):
                    return
                    
        pygame.display.flip()

def main_menu():
    """Handles the main menu screen."""
    pygame.display.set_caption("Menu")

    menu_text = get_font(100).render("Cadence Rush", True, "#ffffff")
    menu_rect = menu_text.get_rect(center=(720, 150))

    play_button = Button(image=None, pos=(720, 350), text_input="PLAY", font=get_font(50), base_colour="#ffffff", hovering_colour="#00ff00")
    options_button = Button(image=None, pos=(720, 500), text_input="OPTIONS", font=get_font(50), base_colour="#ffffff", hovering_colour="#00ff00")
    quit_button = Button(image=None, pos=(720, 650), text_input="QUIT", font=get_font(50), base_colour="#ffffff", hovering_colour="#00ff00")

    while True:
        SCREEN.blit(default_background, (-50, 0))
        SCREEN.blit(menu_text, menu_rect)
        menu_mouse_pos = pygame.mouse.get_pos()

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
                    pygame.display.set_caption("Menu")
                if options_button.checkForInput(menu_mouse_pos):
                    options()
                    pygame.display.set_caption("Menu")
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()
            
        pygame.display.flip()
        clock.tick(60)

main_menu()
pygame.quit()
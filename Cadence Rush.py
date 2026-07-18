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
    """Button class to easily create buttons for my program and automatically."""

    def __init__(self, image, pos, text_input, font, base_colour, hovering_colour):
        """Initializes the components of the button."""
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

    def changeColour(self, position):
        """Changes the text colour if the mouse is hovering over the button."""
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

    hit_indicators = []

    JUDGEMENT_COLOURS = {
        "MAX!": "#00ffff",   
        "300":  "#00ff00",   
        "200":  "#ffff00",   
        "100":  "#ffaa00",  
        "50":   "#ff5500",   
        "MISS": "#ff0000"    
    }

    chart_notes = list(NIGHT_OF_NIGHTS_CHART)
    active_notes = []
    
    start_time = pygame.time.get_ticks()

    is_paused = False
    pause_time_offset = 0 
    pause_start_ticks = 0

    resume_button = Button(image=None, pos=(720, 420), text_input="RESUME", font=get_font(40), base_colour="#ffffff", hovering_colour="#00ff00")
    menu_button = Button(image=None, pos=(720, 520), text_input="MAIN MENU", font=get_font(40), base_colour="#ffffff", hovering_colour="#ff0000")

    while True:
        SCREEN.blit(default_background, (-50, 0))
        mouse_pos = pygame.mouse.get_pos()
        
        current_ticks = pygame.time.get_ticks()

        if not is_paused:
            current_time = current_ticks - start_time - 3000 - pause_time_offset

        pygame.draw.rect(SCREEN, (0, 0, 0), (490, 0, 440, 850))

        for lane_idx, x_pos in enumerate(lane_x_positions):
            SCREEN.blit(receptor_images[lane_idx], (x_pos, receptor_y))

        if current_time > 0 and not is_paused:
            while chart_notes and chart_notes[0][0] <= current_time + 1500:
                spawned = chart_notes.pop(0)
                active_notes.append({"hit_time": spawned[0], "lane": spawned[1]})

        for note in active_notes[:]:
            time_difference = note["hit_time"] - current_time
            note_y = receptor_y - (time_difference * scroll_speed)

            if -80 <= note_y <= 850:
                SCREEN.blit(note_images[note["lane"]], (lane_x_positions[note["lane"]], note_y))

            if not is_paused and time_difference < -133: 
                counts["MISS"] += 1
                total_notes_played += 1
                combo = 0

                indicator_x = lane_x_positions[note["lane"]] + 40
                hit_indicators.append({"text": "MISS", "colour": JUDGEMENT_COLOURS["MISS"], "x": indicator_x, "y": 620, "spawn_time": current_ticks})

                active_notes.remove(note)

        for indicator in hit_indicators[:]:
            elapsed = current_ticks - indicator["spawn_time"]
            
            if elapsed > 400:
                hit_indicators.remove(indicator)
                continue

            float_y = indicator["y"] - (elapsed * 0.08)
            
            alpha = max(0, 255 - int((elapsed / 400) * 255))

            font_surface = get_font(24).render(indicator["text"], True, indicator["colour"])
            alpha_surface = pygame.Surface(font_surface.get_size(), pygame.SRCALPHA)
            alpha_surface.blit(font_surface, (0, 0))
            alpha_surface.set_alpha(alpha)

            rect = alpha_surface.get_rect(center=(indicator["x"], float_y))
            SCREEN.blit(alpha_surface, rect)

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

        if -3000 <= current_time <= 500 and not is_paused:
            if current_time < 0:
                ready_seconds = abs(current_time) // 1000 + 1
            else:
                ready_seconds = 0

            ready_text = get_font(60).render(str(ready_seconds), True, "#ff0000")
            SCREEN.blit(ready_text, (695, 350))

        if is_paused:
            overlay = pygame.Surface((1440, 850), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            SCREEN.blit(overlay, (0, 0))

            pause_title = get_font(80).render("PAUSED", True, "#ff00ff")
            pause_rect = pause_title.get_rect(center=(720, 280))
            SCREEN.blit(pause_title, pause_rect)

            resume_button.changeColour(mouse_pos)
            resume_button.update(SCREEN)
            menu_button.changeColour(mouse_pos)
            menu_button.update(SCREEN)

        pressed_lane = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if is_paused and event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.checkForInput(mouse_pos):
                    is_paused = False
                    pause_time_offset += (current_ticks - pause_start_ticks)
                if menu_button.checkForInput(mouse_pos):
                    pygame.event.clear()
                    return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not is_paused:
                        is_paused = True
                        pause_start_ticks = current_ticks
                    else:
                        is_paused = False
                        pause_time_offset += (current_ticks - pause_start_ticks)

                if not is_paused:
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
                                    rating = "MAX!"
                                elif diff <= 46:
                                    counts["300"] += 1
                                    score += 300
                                    rating = "300"
                                elif diff <= 79:
                                    counts["200"] += 1
                                    score += 200
                                    rating = "200"
                                elif diff <= 109:
                                    counts["100"] += 1
                                    score += 100
                                    rating = "100"
                                elif diff <= 133:
                                    counts["50"] += 1
                                    score += 50
                                    rating = "50"
                                else:
                                    continue

                                indicator_x = lane_x_positions[pressed_lane] + 40
                                hit_indicators.append({"text": rating, "colour": JUDGEMENT_COLOURS[rating], "x": indicator_x, "y": 620, "spawn_time": current_ticks})

                                combo += 1
                                if combo > max_combo:
                                    max_combo = combo

                                total_notes_played += 1
                                active_notes.remove(note)
                                break

        pygame.display.flip()
        clock.tick(60)

def instructions_page():
    """Displays the Instructions."""
    pygame.display.set_caption("How to Play")

    title_text = get_font(60).render("HOW TO PLAY", True, "#00ff00")
    title_rect = title_text.get_rect(center=(720, 80))

    lines = [
        "CONTROLS:",
        "• Lane 1 (Left):   Key 'A'",
        "• Lane 2 (Down):   Key 'S'",
        "• Lane 3 (Up):     Key 'K'",
        "• Lane 4 (Right):  Key 'L'",
        "",
        "SCORING:",
        "• MAX: 320 Points   • 300: 300 Points",
        "• 200: 200 Points   • 100: 100 Points",
        "• 50:  50 Points    • MISS: 0 Points",
        "",
        "PAUSE/EXIT GAME: Press 'ESC' mid-level",
        "",
        "AIM:",
        "Hit the notes and build up your combo.",
        "Aim for high accuracy and get the best possible score!"
    ]

    back_button = Button(image=None, pos=(180, 65), text_input="BACK", font=get_font(40), base_colour="#ffffff", hovering_colour="#00ff00")

    while True:
        SCREEN.blit(default_background, (-50, 0))

        overlay = pygame.Surface((1280, 800), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        SCREEN.blit(overlay, (80, 25))

        SCREEN.blit(title_text, title_rect)
        mouse_pos = pygame.mouse.get_pos()

        for idx, line in enumerate(lines):
            text_render = get_font(20).render(line, True, "#ffffff")
            SCREEN.blit(text_render, (160, 130 + (idx * 42)))

        back_button.changeColour(mouse_pos)
        back_button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkForInput(mouse_pos):
                    return

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
        
        back_button.changeColour(mouse_pos)
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

    menu_text = get_font(100).render("Cadence Rush", True, "#00fbff")
    menu_rect = menu_text.get_rect(center=(720, 110))

    play_button = Button(image=None, pos=(720, 320), text_input="PLAY", font=get_font(50), base_colour="#ffffff", hovering_colour="#00ff00")
    options_button = Button(image=None, pos=(720, 430), text_input="OPTIONS", font=get_font(50), base_colour="#ffffff", hovering_colour="#00ff00")
    instructions_button = Button(image=None, pos=(720, 540), text_input="INSTRUCTIONS", font=get_font(50), base_colour="#ffffff", hovering_colour="#00ff00")
    quit_button = Button(image=None, pos=(720, 650), text_input="QUIT", font=get_font(50), base_colour="#ffffff", hovering_colour="#ff0000")

    while True:
        SCREEN.blit(default_background, (-50, 0))
        SCREEN.blit(menu_text, menu_rect)
        menu_mouse_pos = pygame.mouse.get_pos()

        for button in [play_button, options_button, instructions_button, quit_button]:
            button.changeColour(menu_mouse_pos)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    start_game()

                    while pygame.mouse.get_pressed()[0]:
                        pygame.event.pump()
                    pygame.event.clear()

                    pygame.display.set_caption("Menu")
                if options_button.checkForInput(menu_mouse_pos):
                    options()
                    pygame.display.set_caption("Menu")
                if instructions_button.checkForInput(menu_mouse_pos):
                    instructions_page()
                    pygame.display.set_caption("Menu")
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()
            
        pygame.display.flip()
        clock.tick(60)

main_menu()
pygame.quit()
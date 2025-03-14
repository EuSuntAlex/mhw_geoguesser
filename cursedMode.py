import pygame
import sys
import os
import random
import math
from pinpoint import points, zones  

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)  # color for glow

font = pygame.font.Font(resource_path("./fonts/Familiar Pro-Bold.otf"), 25)
logo = pygame.image.load(resource_path("./ui/Logo Cropped.png"))
single_image = pygame.image.load(resource_path("./ui/cursedMode.png"))  # load single.png image
single_image = pygame.transform.scale(single_image, (244, 97))  # scale image to 244x97
back_map_img = pygame.image.load(resource_path("./ui/backMap.png"))
back_map_hover_img = pygame.image.load(resource_path("./ui/backMapHover.png"))
history_img = pygame.image.load(resource_path("./ui/history.png"))
history_red = pygame.image.load(resource_path("./ui/History Red.png"))
history_green = pygame.image.load(resource_path("./ui/History Green.png"))
submit_img = pygame.image.load(resource_path("./ui/sub.png"))
submit_hover_img = pygame.image.load(resource_path("./ui/subHighlight.png"))
clear_img = pygame.image.load(resource_path("./ui/clear.png"))
clear_hover_img = pygame.image.load(resource_path("./ui/clearHighlight.png"))
valky_img = pygame.image.load(resource_path("./ui/valky.png"))
valky_img =  pygame.transform.scale(valky_img, (64, 64))

MAPS_FOLDER = resource_path("maps")
maps = [f for f in os.listdir(MAPS_FOLDER) if f.endswith(('.jpg', '.png'))]
maps.sort()

def open_map(map_name):
    return pygame.image.load(resource_path(os.path.join("maps", map_name)))

def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def draw_text(surface, text, font, color, x, y, shadow_color=None, shadow_offset=2):
    if shadow_color:
        text_surface = font.render(text, True, shadow_color)
        surface.blit(text_surface, (x + shadow_offset, y + shadow_offset))
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

def wrap_text(text, font, max_width):
    if font.render(text, True, WHITE).get_width() <= max_width:
        return [text]  # text fits on a single line
    
    words = text.split(" ")
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + " " + word if current_line else word
        if font.render(test_line, True, WHITE).get_width() <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    
    if len(lines) > 2:
        lines = [" ".join(lines[:len(lines)//2]), " ".join(lines[len(lines)//2:])]
    return lines[:2]  # return at most two lines

def draw_button(surface, rect, text, texture, texture_hover, hover=False):
    if hover:
        surface.blit(texture_hover, rect.topleft)  # display hover texture
    else:
        surface.blit(texture, rect.topleft)  # display normal texture
    
    lines = wrap_text(text, font, rect.width - 20)  # adjust space for padding
    
    total_height = len(lines) * font.get_height()  # total height of the text
    y_offset = (rect.height - total_height) // 2  # vertical centering
    
    y_offset -= font.get_height() // 2
    y_offset -= 9
    
    for line in lines:
        text_surface = font.render(line, True, WHITE)
        text_rect = text_surface.get_rect(center=(rect.centerx, rect.centery + y_offset))
        surface.blit(text_surface, text_rect)
        y_offset += font.get_height()  # move to the next line

def draw_text_in_box(surface, text, color, x, y, line_spacing=10):

    font = pygame.font.Font(resource_path("./fonts/Familiar Pro-Bold.otf"), 27)
    box_width = 230  
    box_height = 300  

    words = text.split(" ")  
    lines = []  
    current_line = "" 

    for word in words:
        test_line = current_line + " " + word if current_line else word
        test_width, _ = font.size(test_line)  

        if test_width <= box_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    current_y = y  
    for line in lines:
        if current_y + font.get_height() > y + box_height:
            break 

        text_surface = font.render(line, True, color)
        surface.blit(text_surface, (x, current_y))

        current_y += font.get_height() + line_spacing

def draw_history(surface, history, WIDTH, HEIGHT):
    history_x = WIDTH * 0.01  # x position of the history_img
    history_y = HEIGHT * 0.13 + logo.get_height()  # y position of the history_img
    
    # draw background image for history
    surface.blit(history_img, (history_x, history_y))

    # iterate through the history list and display each result
    for i, (score, correct) in enumerate(history):
        # choose the appropriate image (history_green or history_red)
        history_item_image = history_green if correct == 1 else history_red

        # calculate y position for each history item
        item_y = history_y + 10 + i * (36 + 5) + 85 # 36 is the height of history_green/red image, 5 is the spacing

        # draw history_green/red image
        surface.blit(history_item_image, (history_x + 2, item_y))  # slightly adjust x position

        # add text "Round X: Score Y"
        text = f"{i + 1}: {int(score)}"
        draw_text(surface, text, font, WHITE, history_x + 10, item_y + 4, shadow_color=BLACK)



def cursed_mode():
    screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    WIDTH, HEIGHT = screen.get_size()  
    valky_y = HEIGHT * 0.357
    valky_x = WIDTH * 0.908
    valky_text = "Valky has cursed you, your game and this run. You shall not receive any blessings."
    # load images for back button
    back_btn_img_zones = pygame.image.load(resource_path("./ui/Back To Menu.png"))  # image for the first page
    back_btn_img_platforms = pygame.image.load(resource_path("./ui/BackBtn.png"))  # image for the platforms page
    back_btn_img_zones_hover = pygame.image.load(resource_path("./ui/Back_to_menu_hover.png"))  # hover for the first page
    back_btn_img_platforms_hover = pygame.image.load(resource_path("./ui/Back_Hover.png"))  # hover for the platforms page
    back_btn_img_zones = pygame.transform.scale(back_btn_img_zones, (243, 97))  # resize images
    back_btn_img_platforms = pygame.transform.scale(back_btn_img_platforms, (243, 97))
    back_btn_img_zones_hover = pygame.transform.scale(back_btn_img_zones_hover, (243, 97))
    back_btn_img_platforms_hover = pygame.transform.scale(back_btn_img_platforms_hover, (243, 97))
    
    # load textures for zone/location buttons
    button_texture = pygame.image.load(resource_path("./ui/Single Button.png"))
    button_texture_hover = pygame.image.load(resource_path("./ui/Single Button Hover.png"))
    button_texture = pygame.transform.scale(button_texture, (260, 80))  # resize texture
    button_texture_hover = pygame.transform.scale(button_texture_hover, (260, 80))  # resize hover texture

    # load textures for "Yes" and "No" buttons
    yes_texture = pygame.image.load(resource_path("./ui/yes.png"))
    yes_texture_hover = pygame.image.load(resource_path("./ui/yes_hover.png"))
    no_texture = pygame.image.load(resource_path("./ui/no.png"))
    no_texture_hover = pygame.image.load(resource_path("./ui/no_hover.png"))

    # resize textures for "Yes" and "No" buttons
    yes_texture = pygame.transform.scale(yes_texture, (81, 32))
    yes_texture_hover = pygame.transform.scale(yes_texture_hover, (81, 32))
    no_texture = pygame.transform.scale(no_texture, (81, 32))
    no_texture_hover = pygame.transform.scale(no_texture_hover, (81, 32))

    # load images for UI
    right_ui_split = pygame.image.load(resource_path("./ui/rightUISplit.png"))
    right_ui = pygame.image.load(resource_path("./ui/rightUI.png"))
    score_screen = pygame.image.load(resource_path("./ui/cursed_end.png"))

    # resize UI images
    right_ui_split = pygame.transform.scale(right_ui_split, (243, 644))  # specified size
    right_ui = pygame.transform.scale(right_ui, (243, 644))  # specified size

    sure_image = pygame.image.load(resource_path("./ui/sure.png"))
    sure_image = pygame.transform.scale(sure_image, (298, 98))  # resize to 298x98
    
    # basic variables
    game_state = {
        "numar_puncte_harta": 1,
        "zone_posibile": list(zones.keys()),
        "platforme_posibile": [],
        "scor_multiplier": 1,
        "locatii_extra": 0,
        "scor_bonus": 0,
        "elimina_platforme_gresite": False,
        "timer_powerup": 0,
        "sari_locatie": False,
        "diametru": 10,
        "total_rounds": 10,  # total number of rounds (initially 10)
        "wrong_guesses": 0,  # number of consecutive wrong guesses
        "correct_guesses": 0,  # number of consecutive correct rounds
    }

    # list for round history
    history = []

    background = pygame.image.load(resource_path("./ui/caca.png"))
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    pygame.display.set_caption("Geoguessr Mode")
    
    running = True
    show_zones = True
    show_platforms = False
    show_map = False
    selected_zone = None
    selected_platform = None
    user_clicks = []  # user points
    score = 0
    current_round = 0
    used_points = []
    show_feedback = False
    correct_location = None
    correct_point = None
    user_location = None
    user_coords = None
    show_confirmation = False

    def next_round():
        nonlocal current_round, current_point, initial_image, selected_zone, selected_platform, user_clicks, show_feedback, correct_location, correct_point, user_location, user_coords, show_zones, show_platforms, show_map, running

        current_round += 1
        if current_round >= game_state["total_rounds"]:  
            running = False
        else:
            current_point = get_random_point()
            if current_point:
                # loads img 1344x756
                initial_image = pygame.image.load(resource_path(os.path.join("geoPhotos", current_point["images"])))
                initial_image = pygame.transform.smoothscale(initial_image, (1344, 756))  # Scalare la 1344x756
                selected_zone = None
                selected_platform = None
                user_clicks = []
                show_feedback = False
                correct_location = None
                correct_point = None
                user_location = None
                user_coords = None
                show_zones = True
                show_platforms = False
                show_map = False
            else:
                print("No more Locations!")
                running = False
    
    def get_random_point():
        available_points = [p for p in points if p not in used_points]
        if not available_points:
            return None
        point = random.choice(available_points)
        used_points.append(point)
        return point
    
    current_point = get_random_point()
    
    if current_point:
        initial_image = pygame.image.load(resource_path(os.path.join("geoPhotos", current_point["images"])))
        initial_image = pygame.transform.smoothscale(initial_image, (1344, 756))  # Scalare la 1344x756
    else:
        initial_image = None
    right_ui_x = WIDTH * 0.862  
    right_ui_y = HEIGHT * 0.133  
    while running:
        screen.fill(WHITE)
        screen.blit(background, (0, 0))
        screen.blit(logo, (0, HEIGHT * 0.0275))
        screen.blit(single_image, (WIDTH * 0.01, HEIGHT * 0.0275 + logo.get_height())) 

        draw_history(screen, history, WIDTH, HEIGHT)

        screen.blit(right_ui, (right_ui_x, right_ui_y))
        screen.blit(valky_img,(valky_x,valky_y))  
        draw_text_in_box(screen, valky_text, WHITE, WIDTH * 0.9118 - 88, valky_y + 150)

        if initial_image:
            screen.blit(initial_image, (WIDTH // 2 - initial_image.get_width() // 2, 30))

        if show_zones:
            num_columns = 5 
            button_height = 80 
            button_spacing = 20
            
            button_width = 260 
            
            start_x = (WIDTH - (num_columns * (button_width + button_spacing))) // 2
            start_y = HEIGHT - 200 

            buttons = []
            for i, zone in enumerate(game_state["zone_posibile"]):
                row = i // num_columns
                col = i % num_columns
                if row >= 2: 
                    break
                button = pygame.Rect(
                    start_x + col * (button_width + button_spacing),
                    start_y + row * (button_height + button_spacing),
                    button_width, button_height
                )
                buttons.append((button, zone))
                hover = button.collidepoint(pygame.mouse.get_pos())  #hover check
                draw_button(screen, button, zone, button_texture, button_texture_hover, hover)
            
            back_button = pygame.Rect(int(WIDTH * 0.862), int(HEIGHT * 0.0275), 243, 97) 
            back_button_hover = back_button.collidepoint(pygame.mouse.get_pos())  
            if back_button_hover:
                screen.blit(back_btn_img_zones_hover, back_button.topleft)  
            else:
                screen.blit(back_btn_img_zones, back_button.topleft)
                
        elif show_platforms:
            if selected_zone:
                platforms = zones[selected_zone]
                
                button_width = 260 
                button_height = 80  
                button_spacing = 20  
                
                total_buttons = len(platforms)
                total_width = total_buttons * button_width + (total_buttons - 1) * button_spacing
                
                start_x = (WIDTH - total_width) // 2
                start_y = HEIGHT - 150  
                
                buttons = []
                for i, platform in enumerate(platforms):
                    button = pygame.Rect(
                        start_x + i * (button_width + button_spacing),
                        start_y,
                        button_width, button_height
                    )
                    
                    if platform:
                        button_text = f"{selected_zone} {platform}"
                    else:
                        button_text = selected_zone
                    buttons.append((button, button_text))
                    hover = button.collidepoint(pygame.mouse.get_pos())  
                    draw_button(screen, button, button_text, button_texture, button_texture_hover, hover)
                
                back_button = pygame.Rect(int(WIDTH * 0.862), int(HEIGHT * 0.0275), 243, 97)  
                back_button_hover = back_button.collidepoint(pygame.mouse.get_pos())  
                if back_button_hover:
                    screen.blit(back_btn_img_platforms_hover, back_button.topleft)  
                else:
                    screen.blit(back_btn_img_platforms, back_button.topleft)
        elif show_map:
            if selected_platform:
                map_screen = open_map(selected_platform + ".jpg") 
                map_screen = pygame.transform.smoothscale(map_screen, (WIDTH, HEIGHT))
                screen.blit(map_screen, (0, 0))
                
                if user_clicks:
                    for click in user_clicks:
                        pygame.draw.circle(screen, RED, click, 5)
                    if show_feedback and correct_point:
                        pygame.draw.circle(screen, GREEN, correct_point, game_state["diametru"])
                        closest_click = min(user_clicks, key=lambda click: distance(click, correct_point))
                        pygame.draw.line(screen, GREEN, closest_click, correct_point, 2)
                
                clear_button = pygame.Rect(WIDTH - 300, HEIGHT - 100, 264, 84)
                draw_button(screen, clear_button, "", clear_img, clear_hover_img, clear_button.collidepoint(pygame.mouse.get_pos()))
                
                submit_button = pygame.Rect(WIDTH - 300, HEIGHT - 200, 264, 84)
                draw_button(screen, submit_button, "", submit_img, submit_hover_img, submit_button.collidepoint(pygame.mouse.get_pos()))
            
            # Butonul de back
            back_button = pygame.Rect(int(WIDTH * 0.862), int(HEIGHT * 0.0275), 243, 97)
            back_button_hover = back_button.collidepoint(pygame.mouse.get_pos())  
            if back_button_hover:
                screen.blit(back_map_hover_img, back_button.topleft) 
            else:
                screen.blit(back_map_img, back_button.topleft)
        
        
        if not show_map:
            # calculate the x position for the score text based on its length
            score_text = f"Score: {int(score)}"
            text_width = font.size(score_text)[0]
            score_x = WIDTH * 0.902 - (text_width - font.size("Score: 0")[0]) * 0.7  # adjust x position based on text length
            draw_text(screen, score_text, font, WHITE, score_x, HEIGHT * 0.165, shadow_color=BLACK)
            draw_text(screen, f"Round: {current_round + 1}/{game_state['total_rounds']}", font, WHITE, WIDTH * 0.89, HEIGHT * 0.269, shadow_color=BLACK)
        
        if show_feedback:
            feedback_text = f"Your choice: {user_location} ({user_coords}) | Correct: {correct_location} ({correct_point})"
            draw_text(screen, feedback_text, font, BLACK, 20, HEIGHT - 100, shadow_color=WHITE)

        if show_confirmation:
            sure_rect = sure_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(sure_image, sure_rect.topleft)
            
            yes_button = pygame.Rect(sure_rect.x + 50, sure_rect.y + 50, 81, 32)
            no_button = pygame.Rect(sure_rect.x + 170, sure_rect.y + 50, 81, 32)

            draw_button(screen, yes_button, "", yes_texture, yes_texture_hover, yes_button.collidepoint(pygame.mouse.get_pos()))
            draw_button(screen, no_button, "", no_texture, no_texture_hover, no_button.collidepoint(pygame.mouse.get_pos()))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if show_confirmation:
                    if yes_button.collidepoint(event.pos):
                        from main import main_menu 
                        main_menu()
                    elif no_button.collidepoint(event.pos):
                        show_confirmation = False
                elif back_button.collidepoint(event.pos): 
                    if show_zones:
                        show_confirmation = True  
                    elif show_platforms:
                        show_platforms = False
                        show_zones = True
                    elif show_map:
                        show_map = False
                        show_platforms = True
                elif show_zones:
                    for button, zone in buttons:
                        if button.collidepoint(event.pos):
                            selected_zone = zone
                            show_zones = False
                            show_platforms = True
                elif show_platforms:
                    for button, platform in buttons:
                        if button.collidepoint(event.pos):
                            selected_platform = platform
                            show_platforms = False
                            show_map = True
                elif show_map:
                    if clear_button.collidepoint(event.pos):
                        user_clicks = []
                    elif submit_button.collidepoint(event.pos) and len(user_clicks) == game_state["numar_puncte_harta"]:
                        if selected_platform == current_point["location"]:
                            correct_x = int(current_point["correct"][0] * (WIDTH / 1920))
                            correct_y = int(current_point["correct"][1] * (HEIGHT / 1080))
                            correct_point = (correct_x, correct_y)
                            
                            # closest point
                            closest_click = min(user_clicks, key=lambda click: distance(click, correct_point))
                            dist = distance(closest_click, correct_point)
                            
                            # score calculation
                            if dist <= game_state["diametru"]:
                                round_score = 5000
                            else:
                                round_score = max(0, 5000 - dist * 7) 
                            
                            score += int(round(round_score * game_state["scor_multiplier"])) + game_state["scor_bonus"]
                            show_feedback = True
                            correct_location = current_point["location"]
                            user_location = selected_platform
                            user_coords = closest_click

                            history.append((round_score, 1))  

                            draw_text(screen, f"Points gained: {int(round(round_score * game_state["scor_multiplier"])) + game_state["scor_bonus"]}", font, GREEN, WIDTH // 2, HEIGHT // 2, shadow_color=BLACK)
                            pygame.display.update()
                            pygame.time.wait(1000)  

                            pygame.draw.circle(screen, GREEN, correct_point, game_state["diametru"])
                            pygame.draw.line(screen, GREEN, closest_click, correct_point, 2)
                            pygame.display.update()
                            pygame.time.wait(1000)

                            game_state["correct_guesses"] += 1
                        else:
                            correct_x = int(current_point["correct"][0] * (WIDTH / 1920))
                            correct_y = int(current_point["correct"][1] * (HEIGHT / 1080))
                            correct_point = (correct_x, correct_y)
                            correct_location = current_point["location"]

                            draw_text(screen, "Wrong Location!", font, RED, WIDTH // 2, HEIGHT // 2, shadow_color=BLACK)
                            pygame.display.update()
                            pygame.time.wait(1000) 

                            show_feedback = True
                            user_location = selected_platform
                            user_coords = user_clicks

                            history.append((0, 0))  

                            game_state["correct_guesses"] = 0
                            game_state["wrong_guesses"] += 1
                        
                        next_round()  
                    elif back_button.collidepoint(event.pos):
                        show_map = False
                        show_platforms = True
                    else:
                        if len(user_clicks) < game_state["numar_puncte_harta"]:
                            user_clicks.append(event.pos)
        
        pygame.display.update()

    screen.blit(score_screen,(0,0))
    draw_text(screen, f"Final Score: {int(score)}", font, WHITE, WIDTH // 2, HEIGHT // 2, shadow_color=BLACK)
    pygame.display.update()
    pygame.time.wait(2500)
    from main import main_menu
    main_menu()  

if __name__ == "__main__":
    cursed_mode()
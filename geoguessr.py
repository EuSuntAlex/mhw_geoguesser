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

font = pygame.font.Font(None, 40)

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

def draw_button(surface, rect, color, text, hover=False):
    shadow_rect = pygame.Rect(rect.x + 5, rect.y + 5, rect.width, rect.height)
    pygame.draw.rect(surface, (0, 0, 0, 100), shadow_rect, border_radius=10)
    if hover:
        hover_color = (
            min(color[0] + 20, 255),  
            min(color[1] + 20, 255),
            min(color[2] + 20, 255))
        pygame.draw.rect(surface, hover_color, rect, border_radius=10)
    else:
        pygame.draw.rect(surface, color, rect, border_radius=10)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

def geoguessr_mode():
    screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    WIDTH, HEIGHT = screen.get_size()  

    background = pygame.image.load(resource_path("easy_background.webp"))
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    pygame.display.set_caption("Geoguessr Mode")
    
    running = True
    show_zones = True
    show_platforms = False
    show_map = False
    selected_zone = None
    selected_platform = None
    user_click = None
    score = 0
    total_rounds = 10
    current_round = 0
    used_points = []
    show_feedback = False
    correct_location = None
    correct_point = None
    user_location = None
    user_coords = None
    show_confirmation = False
    
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
        aspect_ratio = initial_image.get_width() / initial_image.get_height()
        new_height = int(HEIGHT * 0.7)  
        new_width = int(new_height * aspect_ratio)
        initial_image = pygame.transform.smoothscale(initial_image, (new_width, new_height))
    else:
        initial_image = None
    
    while running:
        screen.fill(WHITE)
        screen.blit(background, (0, 0))
        
        if initial_image:
            screen.blit(initial_image, (WIDTH // 2 - initial_image.get_width() // 2, 30))
        
        if show_zones:
            num_columns = 5 
            button_height = 50
            button_spacing = 20
            
            max_text_width = max(font.size(zone)[0] for zone in zones.keys())
            button_width = max(max_text_width + 40, 200)  
            
            start_x = (WIDTH - (num_columns * (button_width + button_spacing))) // 2
            start_y = HEIGHT - 200 

            buttons = []
            for i, zone in enumerate(zones.keys()):
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
                draw_button(screen, button, BLUE, zone, button.collidepoint(pygame.mouse.get_pos()))
            
            # Butonul de back
            back_button = pygame.Rect(20, 20, 100, 50)
            draw_button(screen, back_button, RED, "Back", back_button.collidepoint(pygame.mouse.get_pos()))
        elif show_platforms:
            if selected_zone:
                num_columns = 2
                button_height = 50
                button_spacing = 20
                
                
                platforms = zones[selected_zone]
                
               
                max_text_width = max(font.size(f"{selected_zone} {platform}" if platform else selected_zone)[0] for platform in platforms)
                button_width = max(max_text_width + 40, 200)  
                
                start_x = (WIDTH - (num_columns * (button_width + button_spacing))) // 2
                start_y = HEIGHT - 150 

                buttons = []
                for i, platform in enumerate(platforms):
                    row = i // num_columns
                    col = i % num_columns
                    button = pygame.Rect(
                        start_x + col * (button_width + button_spacing),
                        start_y + row * (button_height + button_spacing),
                        button_width, button_height
                    )
                    
                    if platform:
                        button_text = f"{selected_zone} {platform}"
                    else:
                        button_text = selected_zone
                    buttons.append((button, button_text))
                    draw_button(screen, button, BLUE, button_text, button.collidepoint(pygame.mouse.get_pos()))
                
                # Butonul de back
                back_button = pygame.Rect(20, 20, 100, 50)
                draw_button(screen, back_button, RED, "Back", back_button.collidepoint(pygame.mouse.get_pos()))
        elif show_map:
            if selected_platform:
                map_screen = open_map(selected_platform + ".jpg") 
                map_screen = pygame.transform.smoothscale(map_screen, (WIDTH, HEIGHT))
                screen.blit(map_screen, (0, 0))
                
                if user_click:
                    pygame.draw.circle(screen, RED, user_click, 10)
                    if show_feedback and correct_point:
                        pygame.draw.circle(screen, GREEN, correct_point, 10)
                        pygame.draw.line(screen, GREEN, user_click, correct_point, 2)
                
                clear_button = pygame.Rect(WIDTH - 200, HEIGHT - 100, 150, 50)
                draw_button(screen, clear_button, BLUE, "Clear choice", clear_button.collidepoint(pygame.mouse.get_pos()))
                
                submit_button = pygame.Rect(WIDTH - 200, HEIGHT - 50, 150, 50)
                draw_button(screen, submit_button, GREEN, "Submit", submit_button.collidepoint(pygame.mouse.get_pos()))
            
            # Butonul de back
            back_button = pygame.Rect(20, 20, 100, 50)
            draw_button(screen, back_button, RED, "Back", back_button.collidepoint(pygame.mouse.get_pos()))
        
        draw_text(screen, f"Score: {int(score)}", font, WHITE, WIDTH - 250, 20, shadow_color=BLACK)
        draw_text(screen, f"Round: {current_round + 1}/{total_rounds}", font, WHITE, WIDTH - 250, 60, shadow_color=BLACK)
        
        if show_feedback:
            feedback_text = f"Your choice: {user_location} ({user_coords}) | Correct: {correct_location} ({correct_point})"
            draw_text(screen, feedback_text, font, BLACK, 20, HEIGHT - 100, shadow_color=WHITE)
        
        if show_confirmation:
            confirmation_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 100)
            pygame.draw.rect(screen, WHITE, confirmation_rect)
            pygame.draw.rect(screen, BLACK, confirmation_rect, 2)
            draw_text(screen, "Are you sure?", font, BLACK, confirmation_rect.x + 50, confirmation_rect.y + 20, shadow_color=WHITE)
            
            yes_button = pygame.Rect(confirmation_rect.x + 50, confirmation_rect.y + 50, 80, 30)
            draw_button(screen, yes_button, GREEN, "Yes", yes_button.collidepoint(pygame.mouse.get_pos()))
            
            no_button = pygame.Rect(confirmation_rect.x + 170, confirmation_rect.y + 50, 80, 30)
            draw_button(screen, no_button, RED, "No", no_button.collidepoint(pygame.mouse.get_pos()))
        
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
                elif show_zones:
                    for button, zone in buttons:
                        if button.collidepoint(event.pos):
                            selected_zone = zone
                            show_zones = False
                            show_platforms = True
                    if back_button.collidepoint(event.pos):
                        show_confirmation = True
                elif show_platforms:
                    for button, platform in buttons:
                        if button.collidepoint(event.pos):
                            selected_platform = platform
                            show_platforms = False
                            show_map = True
                    if back_button.collidepoint(event.pos):
                        show_platforms = False
                        show_zones = True
                elif show_map:
                    if clear_button.collidepoint(event.pos):
                        user_click = None
                    elif submit_button.collidepoint(event.pos) and user_click:
                        if selected_platform == current_point["location"]:
                            correct_x = int(current_point["correct"][0] * (WIDTH / 1920))
                            correct_y = int(current_point["correct"][1] * (HEIGHT / 1080))
                            correct_point = (correct_x, correct_y)
                            dist = distance(user_click, correct_point)
                            round_score = max(0, 5000 - dist)
                            score += int(round(round_score))
                            show_feedback = True
                            correct_location = current_point["location"]
                            user_location = selected_platform
                            user_coords = user_click

                            draw_text(screen, f"Points gained: {int(round(round_score))}", font, GREEN, WIDTH // 2, HEIGHT // 2, shadow_color=BLACK)
                            pygame.display.update()
                            pygame.time.wait(1000)  

                            pygame.draw.circle(screen, GREEN, correct_point, 10)
                            pygame.draw.line(screen, GREEN, user_click, correct_point, 2)
                            pygame.display.update()
                            pygame.time.wait(1000)
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
                            user_coords = user_click
                        
                        current_round += 1
                        if current_round >= total_rounds:
                            print(f"Game Over! Final Score: {int(score)}")
                            running = False
                        else:
                            current_point = get_random_point()
                            if current_point:
                                initial_image = pygame.image.load(resource_path(os.path.join("geoPhotos", current_point["images"])))
                                aspect_ratio = initial_image.get_width() / initial_image.get_height()
                                new_height = int(HEIGHT * 0.7) 
                                new_width = int(new_height * aspect_ratio)
                                initial_image = pygame.transform.smoothscale(initial_image, (new_width, new_height))
                                selected_zone = None
                                selected_platform = None
                                user_click = None
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
                    elif back_button.collidepoint(event.pos):
                        show_map = False
                        show_platforms = True
                    else:
                        user_click = event.pos
        
        pygame.display.update()

    screen.fill(BLACK)
    draw_text(screen, f"Final Score: {int(score)}", font, WHITE, WIDTH // 2, HEIGHT // 2, shadow_color=BLACK)
    pygame.display.update()
    pygame.time.wait(2000)
    from main import main_menu
    main_menu()  

if __name__ == "__main__":
    geoguessr_mode()
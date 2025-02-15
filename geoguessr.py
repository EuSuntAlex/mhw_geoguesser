import pygame
import sys
import os
import random
import math
from pinpoint import points

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

font = pygame.font.Font(None, 40)

MAPS_FOLDER = "maps"
maps = [f for f in os.listdir(MAPS_FOLDER) if f.endswith(('.jpg', '.png'))]
maps.sort()

def open_map(map_name):
    return pygame.image.load(os.path.join(MAPS_FOLDER, map_name))

def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def geoguessr_mode():
    screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    WIDTH, HEIGHT = screen.get_size()  

    background = pygame.image.load("easy_background.webp")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    pygame.display.set_caption("Geoguessr Mode")
    
    running = True
    show_maps = False
    selected_map = None
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
    
    def get_random_point():
        available_points = [p for p in points if p not in used_points]
        if not available_points:
            return None
        point = random.choice(available_points)
        used_points.append(point)
        return point
    
    current_point = get_random_point()
    
    if current_point:
        initial_image = pygame.image.load(os.path.join("geoPhotos", current_point["images"]))
        initial_image = pygame.transform.scale(initial_image, (int(WIDTH * 0.8), int(HEIGHT * 0.8)))
    else:
        initial_image = None
    
    while running:
        screen.fill(WHITE)
        screen.blit(background, (0, 0))
        
        if not show_maps:
            if initial_image:
                screen.blit(initial_image, (WIDTH // 2 - initial_image.get_width() // 2, 30))
            else:
                no_more_text = font.render("No more Locations!", True, BLACK)
                screen.blit(no_more_text, (WIDTH // 2 - no_more_text.get_width() // 2, HEIGHT // 2))
            
            maps_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 50)
            pygame.draw.rect(screen, BLUE, maps_button, border_radius=5)
            maps_text = font.render("Maps", True, WHITE)
            screen.blit(maps_text, (maps_button.x + 60, maps_button.y + 10))
            
            back_button = pygame.Rect(20, 20, 200, 50)
            pygame.draw.rect(screen, RED, back_button, border_radius=5)
            back_text = font.render("Back", True, WHITE)
            screen.blit(back_text, (back_button.x + 20, back_button.y + 10))
        else:
            if selected_map is None:
                num_columns = 2
                button_height = 50
                button_spacing = 20
                
                max_text_width = max(font.size(map_name.split('.')[0])[0] for map_name in maps)
                button_width = max_text_width + 20
                
                start_x = (WIDTH - (num_columns * (button_width + button_spacing))) // 2
                start_y = 100

                buttons = []
                for i, map_name in enumerate(maps):
                    row = i // num_columns
                    col = i % num_columns
                    button = pygame.Rect(
                        start_x + col * (button_width + button_spacing),
                        start_y + row * (button_height + button_spacing),
                        button_width, button_height
                    )
                    buttons.append((button, map_name))
                    if show_feedback and map_name.split('.')[0] == correct_location:
                        pygame.draw.rect(screen, GREEN, button, border_radius=5)
                    else:
                        pygame.draw.rect(screen, BLUE, button, border_radius=5)
                    text = font.render(map_name.split('.')[0], True, WHITE)
                    screen.blit(text, (button.x + 10, button.y + 10))
            else:
                map_screen = open_map(selected_map)
                map_screen = pygame.transform.scale(map_screen, (WIDTH, HEIGHT))
                screen.blit(map_screen, (0, 0))
                
                if user_click:
                    pygame.draw.circle(screen, RED, user_click, 10)
                    if show_feedback and correct_point:
                        pygame.draw.circle(screen, GREEN, correct_point, 10)
                        pygame.draw.line(screen, GREEN, user_click, correct_point, 2)
                
                clear_button = pygame.Rect(WIDTH - 200, HEIGHT - 100, 150, 50)
                pygame.draw.rect(screen, BLUE, clear_button, border_radius=5)
                clear_text = font.render("Clear choice", True, WHITE)
                screen.blit(clear_text, (clear_button.x + 10, clear_button.y + 10))
                
                submit_button = pygame.Rect(WIDTH - 200, HEIGHT - 50, 150, 50)
                pygame.draw.rect(screen, GREEN, submit_button, border_radius=5)
                submit_text = font.render("Submit", True, WHITE)
                screen.blit(submit_text, (submit_button.x + 30, submit_button.y + 10))
            
            back_button = pygame.Rect(20, 20, 100, 50)
            pygame.draw.rect(screen, RED, back_button, border_radius=5)
            back_text = font.render("Back", True, WHITE)
            screen.blit(back_text, (back_button.x + 20, back_button.y + 10))
        
        score_text = font.render(f"Score: {int(score)}", True, WHITE)
        screen.blit(score_text, (WIDTH - 250, 20))
        round_text = font.render(f"Round: {current_round + 1}/{total_rounds}", True, WHITE)
        screen.blit(round_text, (WIDTH - 250, 60))
        
        if show_feedback:
            feedback_text = font.render(
                f"Your choice: {user_location} ({user_coords}) | Correct: {correct_location} ({correct_point})",
                True, BLACK
            )
            screen.blit(feedback_text, (20, HEIGHT - 100))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not show_maps:
                    if maps_button.collidepoint(event.pos):
                        show_maps = True
                    elif back_button.collidepoint(event.pos):
                        from main import main_menu 
                        main_menu()
                else:
                    if back_button.collidepoint(event.pos):
                        if selected_map is not None:
                            selected_map = None
                        else:
                            show_maps = False
                    elif selected_map is None:
                        num_columns = 2
                        button_height = 50
                        button_spacing = 20
                        
                        max_text_width = max(font.size(map_name.split('.')[0])[0] for map_name in maps)
                        button_width = max_text_width + 20
                        
                        start_x = (WIDTH - (num_columns * (button_width + button_spacing))) // 2
                        start_y = 100

                        for i, map_name in enumerate(maps):
                            row = i // num_columns
                            col = i % num_columns
                            button = pygame.Rect(
                                start_x + col * (button_width + button_spacing),
                                start_y + row * (button_height + button_spacing),
                                button_width, button_height
                            )
                            if button.collidepoint(event.pos):
                                selected_map = map_name
                    else:
                        if clear_button.collidepoint(event.pos):
                            user_click = None
                        elif submit_button.collidepoint(event.pos) and user_click:
                            if selected_map.split('.')[0] == current_point["location"]:
                                correct_x = int(current_point["correct"][0] * (WIDTH / 1920))
                                correct_y = int(current_point["correct"][1] * (HEIGHT / 1080))
                                correct_point = (correct_x, correct_y)
                                dist = distance(user_click, correct_point)
                                round_score = max(0, 5000 - dist)
                                score += int(round(round_score))
                                show_feedback = True
                                correct_location = current_point["location"]
                                user_location = selected_map.split('.')[0]
                                user_coords = user_click
                                pygame.draw.circle(screen, GREEN, correct_point, 10)
                                pygame.draw.line(screen, GREEN, user_click, correct_point, 2)
                                pygame.display.update()
                                pygame.time.wait(2000)
                            else:
                                print("Wrong Location! 0 points.")
                                show_feedback = True
                                correct_location = current_point["location"]
                                user_location = selected_map.split('.')[0]
                                user_coords = user_click
                            
                            current_round += 1
                            if current_round >= total_rounds:
                                print(f"Game Over! Final Score: {int(score)}")
                                running = False
                            else:
                                current_point = get_random_point()
                                if current_point:
                                    initial_image = pygame.image.load(os.path.join("geoPhotos", current_point["images"]))
                                    initial_image = pygame.transform.scale(initial_image, (int(WIDTH * 0.8), int(HEIGHT * 0.5)))
                                    selected_map = None
                                    user_click = None
                                    show_feedback = False
                                    correct_location = None
                                    correct_point = None
                                    user_location = None
                                    user_coords = None
                                    show_maps = False 
                                else:
                                    print("No more Locations!")
                                    running = False
                        else:
                            user_click = event.pos
        
        pygame.display.update()

    screen.fill(WHITE)
    final_score_text = font.render(f"Final Score: {int(score)}", True, BLACK)
    screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2))
    pygame.display.update()
    pygame.time.wait(3000)  

if __name__ == "__main__":
    geoguessr_mode()
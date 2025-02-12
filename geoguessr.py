import pygame
import sys
import os
import random
import math
from pinpoint import points 

pygame.init()

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Font
font = pygame.font.Font(None, 40)

MAPS_FOLDER = "maps"
maps = [f for f in os.listdir(MAPS_FOLDER) if f.endswith(('.jpg', '.png'))]
maps.sort() 

def open_map(map_name):
    return pygame.image.load(os.path.join(MAPS_FOLDER, map_name))

def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Main function
def geoguessr_mode():
    screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    WIDTH, HEIGHT = screen.get_size()  
    pygame.display.set_caption("Geoguessr Mode")
    
    running = True
    show_maps = False  # control for displaying the list of maps
    selected_map = None
    user_click = None  # user click coordinates
    lives = 3  # number of lives
    score = 0  # players score
    used_points = []  # list to keep track of used points
    
    # Load life icon
    life_icon = pygame.image.load("hp.png")  
    life_icon = pygame.transform.scale(life_icon, (30, 30)) 
    

    def get_random_point():
        available_points = [p for p in points if p not in used_points]
        if not available_points:
            return None
        point = random.choice(available_points)
        used_points.append(point)
        return point
    
    current_point = get_random_point()
    image_stage = 0  # current image stage (0, 1, or 2)
    
    if current_point:
        initial_image = pygame.image.load(os.path.join("geoPhotos", current_point["images"][image_stage]))
        initial_image = pygame.transform.scale(initial_image, (int(WIDTH * 0.8), int(HEIGHT * 0.5)))
    else:
        initial_image = None
    
    while running:
        screen.fill(WHITE)
        
        if not show_maps:
            if initial_image:
                
                screen.blit(initial_image, (WIDTH // 2 - initial_image.get_width() // 2, 20))
            else:
             
                no_more_text = font.render("No more Locations!", True, BLACK)
                screen.blit(no_more_text, (WIDTH // 2 - no_more_text.get_width() // 2, HEIGHT // 2))
            
            # maps button
            maps_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 50)
            pygame.draw.rect(screen, BLUE, maps_button, border_radius=5)
            maps_text = font.render("Maps", True, WHITE)
            screen.blit(maps_text, (maps_button.x + 60, maps_button.y + 10))
            
            # back  button
            back_button = pygame.Rect(20, 20, 200, 50)
            pygame.draw.rect(screen, RED, back_button, border_radius=5)
            back_text = font.render("Back", True, WHITE)
            screen.blit(back_text, (back_button.x + 20, back_button.y + 10))
        else:
            if selected_map is None:
                #  list of maps in a grid
                num_columns = 2 
                button_height = 50
                button_spacing = 20
                
                # maximum width needed for the buttons
                max_text_width = max(font.size(map_name[:-4])[0] for map_name in maps)
                button_width = max_text_width + 20 
                
                # starting position for the grid
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
                    pygame.draw.rect(screen, BLUE, button, border_radius=5)
                    text = font.render(map_name[:-4], True, WHITE)
                    screen.blit(text, (button.x + 10, button.y + 10))
            else:
                #  map and the user chosen point
                map_screen = open_map(selected_map)
                map_screen = pygame.transform.scale(map_screen, (WIDTH, HEIGHT))
                screen.blit(map_screen, (0, 0))
                
                if user_click:
                    pygame.draw.circle(screen, RED, user_click, 10)
                
                # clear  button
                clear_button = pygame.Rect(WIDTH - 200, HEIGHT - 100, 150, 50)
                pygame.draw.rect(screen, BLUE, clear_button, border_radius=5)
                clear_text = font.render("Clear choice", True, WHITE)
                screen.blit(clear_text, (clear_button.x + 10, clear_button.y + 10))
                
                # sub button
                submit_button = pygame.Rect(WIDTH - 200, HEIGHT - 50, 150, 50)
                pygame.draw.rect(screen, GREEN, submit_button, border_radius=5)
                submit_text = font.render("Submit", True, WHITE)
                screen.blit(submit_text, (submit_button.x + 30, submit_button.y + 10))
            
            # back button
            back_button = pygame.Rect(20, 20, 100, 50)
            pygame.draw.rect(screen, RED, back_button, border_radius=5)
            back_text = font.render("Back", True, WHITE)
            screen.blit(back_text, (back_button.x + 20, back_button.y + 10))
        
        #lives and score
        for i in range(lives):
            screen.blit(life_icon, (WIDTH - 100 - i * 40, 20))
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (WIDTH - 150, 70))
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not show_maps:
                    # if the  map button was clicked
                    if maps_button.collidepoint(event.pos):
                        show_maps = True
                    # if the bacv button was clicked
                    elif back_button.collidepoint(event.pos):
                        from main import main_menu 
                        main_menu()
                else:
                    # if the bac button was clicked
                    if back_button.collidepoint(event.pos):
                        if selected_map is not None:
                            selected_map = None  #back to the map listt
                        else:
                            show_maps = False  # back to the initial screen
                    elif selected_map is None:
                        # if a map was clicked
                        num_columns = 2
                        button_height = 50
                        button_spacing = 20
                        
                        # maximum width needed for the buttons
                        max_text_width = max(font.size(map_name[:-4])[0] for map_name in maps)
                        button_width = max_text_width + 20  # Add padding
                        
                        # starting position for the grid
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
                        # if the buttons on the map were clicked
                        if clear_button.collidepoint(event.pos):
                            user_click = None  # Clear the chosen point
                        elif submit_button.collidepoint(event.pos) and user_click:
                            # if the user's click is within 25 pixels of the correct point
                            correct_point = current_point["correct"]
                            if distance(user_click, correct_point) <= 25:
                                print("Correct Answer!")
                                if image_stage == 0:
                                    score += 2  # +2 points for correct answer on first try
                                else:
                                    score += 1  # +1 point for correct answer on second or third try
                                current_point = get_random_point()
                                if current_point:
                                    initial_image = pygame.image.load(os.path.join("geoPhotos", current_point["images"][0]))
                                    initial_image = pygame.transform.scale(initial_image, (int(WIDTH * 0.8), int(HEIGHT * 0.5)))
                                    image_stage = 0
                                else:
                                    print("No more Locations!")
                                    running = False
                            else:
                                print("Wrong Answer!")
                                image_stage += 1
                                if image_stage >= len(current_point["images"]):
                                    lives -= 1
                                    if lives == 0:
                                        print("Game Over! You've lost all lives.")
                                        running = False
                                    else:
                                        current_point = get_random_point()
                                        if current_point:
                                            initial_image = pygame.image.load(os.path.join("geoPhotos", current_point["images"][0]))
                                            initial_image = pygame.transform.scale(initial_image, (int(WIDTH * 0.8), int(HEIGHT * 0.5)))
                                            image_stage = 0
                                        else:
                                            print("No more Locations!")
                                            running = False
                                else:
                                    initial_image = pygame.image.load(os.path.join("geoPhotos", current_point["images"][image_stage]))
                                    initial_image = pygame.transform.scale(initial_image, (int(WIDTH * 0.8), int(HEIGHT * 0.5)))
                        else:
                            # Place a point on the map
                            user_click = event.pos
        
        pygame.display.update()

if __name__ == "__main__":
    geoguessr_mode()
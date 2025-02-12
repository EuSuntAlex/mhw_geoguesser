import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Font
font = pygame.font.Font(None, 40)

# Load maps from the "maps" folder
MAPS_FOLDER = "maps"
maps = [f for f in os.listdir(MAPS_FOLDER) if f.endswith(('.jpg', '.png'))]
maps.sort()  # Sort maps alphabetically

# Function to open a map
def open_map(map_name):
    return pygame.image.load(os.path.join(MAPS_FOLDER, map_name))

# Main function
def geoguessr_mode():
    screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    WIDTH, HEIGHT = screen.get_size()  
    pygame.display.set_caption("Geoguessr Mode")
    
    running = True
    show_maps = False  # Control for displaying the list of maps
    selected_map = None
    user_click = None  # user click coordinates
    
    # Initial image
    initial_image = pygame.image.load("elder.jpg")  # E HARDCODAT AICI
    initial_image = pygame.transform.scale(initial_image, (int(WIDTH * 0.8), int(HEIGHT * 0.5)))
    
    while running:
        screen.fill(WHITE)
        
        if not show_maps:
            # Display the initial image
            screen.blit(initial_image, (WIDTH // 2 - initial_image.get_width() // 2, 20))
            
            # "Maps" button
            maps_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 50)
            pygame.draw.rect(screen, BLUE, maps_button, border_radius=5)
            maps_text = font.render("Maps", True, WHITE)
            screen.blit(maps_text, (maps_button.x + 60, maps_button.y + 10))
            
            # "Back to Main Menu" button
            back_button = pygame.Rect(20, 20, 200, 50)
            pygame.draw.rect(screen, RED, back_button, border_radius=5)
            back_text = font.render("Back", True, WHITE)
            screen.blit(back_text, (back_button.x + 20, back_button.y + 10))
        else:
            if selected_map is None:
                # Display the list of maps
                for i, map_name in enumerate(maps):
                    button = pygame.Rect(WIDTH // 2 - 100, 100 + i * 60, 200, 50)
                    pygame.draw.rect(screen, BLUE, button, border_radius=5)
                    text = font.render(map_name, True, WHITE)
                    screen.blit(text, (button.x + 10, button.y + 10))
            else:
                # Display the map and the user's chosen point
                map_screen = open_map(selected_map)
                map_screen = pygame.transform.scale(map_screen, (WIDTH, HEIGHT))
                screen.blit(map_screen, (0, 0))
                
                if user_click:
                    pygame.draw.circle(screen, RED, user_click, 10)
                
                # "Clear choice" button
                clear_button = pygame.Rect(WIDTH - 200, HEIGHT - 100, 150, 50)
                pygame.draw.rect(screen, BLUE, clear_button, border_radius=5)
                clear_text = font.render("Clear choice", True, WHITE)
                screen.blit(clear_text, (clear_button.x + 10, clear_button.y + 10))
                
                # "Submit" button
                submit_button = pygame.Rect(WIDTH - 200, HEIGHT - 50, 150, 50)
                pygame.draw.rect(screen, GREEN, submit_button, border_radius=5)
                submit_text = font.render("Submit", True, WHITE)
                screen.blit(submit_text, (submit_button.x + 30, submit_button.y + 10))
            
            # "Back" button
            back_button = pygame.Rect(20, 20, 100, 50)
            pygame.draw.rect(screen, RED, back_button, border_radius=5)
            back_text = font.render("Back", True, WHITE)
            screen.blit(back_text, (back_button.x + 20, back_button.y + 10))
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not show_maps:
                    # if the "Maps" button was clicked
                    if maps_button.collidepoint(event.pos):
                        show_maps = True
                    # if the "Back to Main Menu" button was clicked
                    elif back_button.collidepoint(event.pos):
                        from main import main_menu 
                        main_menu()
                else:
                    # if the "Back" button was clicked
                    if back_button.collidepoint(event.pos):
                        if selected_map is not None:
                            selected_map = None  # Go back to the map list
                        else:
                            show_maps = False  # Go back to the initial screen
                    elif selected_map is None:
                        # if a map was clicked
                        for i, map_name in enumerate(maps):
                            button = pygame.Rect(WIDTH // 2 - 100, 100 + i * 60, 200, 50)
                            if button.collidepoint(event.pos):
                                selected_map = map_name
                    else:
                        # if the buttons on the map were clicked
                        if clear_button.collidepoint(event.pos):
                            user_click = None  # Clear the chosen point
                        elif submit_button.collidepoint(event.pos) and user_click:
                            print(f"Selected map: {selected_map}, Clicked at: {user_click}")
                            # Add logic for checking the answer here
                        else:
                            # Place a point on the map
                            user_click = event.pos
        
        pygame.display.update()

if __name__ == "__main__":
    geoguessr_mode()
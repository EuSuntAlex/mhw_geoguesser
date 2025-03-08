import pygame
import sys
import easy_mode
import geoguessr
import howToPlay
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
WIDTH, HEIGHT = screen.get_size()  

background_image = pygame.image.load(resource_path("background.png"))
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

profile_pics = [pygame.image.load(resource_path(f"pfp/img{i+1}.jpg")) for i in range(7)]
profile_pics = [pygame.transform.scale(img, (50, 50)) for img in profile_pics]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
DARK_BLUE = (50, 100, 160)

font = pygame.font.Font(resource_path("./fonts/Familiar Pro-Bold.otf"), 30)
button_font = pygame.font.Font(None, 40)
desc_font = pygame.font.Font(None, 30)  

def draw_text(text, font, color, surface, x, y, centered=False):
    text_surface = font.render(text, True, color)
    if centered:
        text_rect = text_surface.get_rect(center=(x, y))
    else:
        text_rect = text_surface.get_rect(midleft=(x, y))
    surface.blit(text_surface, text_rect)

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
    text_surface = button_font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

button_width, button_height = 250, 60  # Butoane mai mari
start_button = pygame.Rect(WIDTH//2 - button_width//2, HEIGHT//2 - 150, button_width, button_height)
easy_button = pygame.Rect(WIDTH//2 - button_width//2, HEIGHT//2 - 50, button_width, button_height)
how_to_play_button = pygame.Rect(WIDTH//2 - button_width//2, HEIGHT//2 + 50, button_width, button_height)
cool_people_button = pygame.Rect(WIDTH//2 - button_width//2, HEIGHT//2 + 150, button_width, button_height)
exit_button = pygame.Rect(WIDTH//2 - button_width//2, HEIGHT//2 + 250, button_width, button_height)
back_button = pygame.Rect(WIDTH//2 - button_width//2, HEIGHT - 100, button_width, button_height)



def cool_people_screen():
    global WIDTH, HEIGHT, screen
    running = True
    cool_image = pygame.image.load(resource_path("cool.png"))
    cool_image = pygame.transform.scale(cool_image, (WIDTH, HEIGHT))
    while running:
        screen.blit(pygame.transform.scale(cool_image, (WIDTH, HEIGHT)), (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
            if event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    running = False

    
        
        draw_button(screen, back_button, BLUE, "Back", back_button.collidepoint(pygame.mouse.get_pos()))
        
        pygame.display.update()

def main_menu():
    global WIDTH, HEIGHT, screen
    running = True
    while running:
        screen.blit(pygame.transform.scale(background_image, (WIDTH, HEIGHT)), (0, 0))
        
        draw_button(screen, start_button, BLUE, "Start Game", start_button.collidepoint(pygame.mouse.get_pos()))
        draw_button(screen, easy_button, BLUE, "Speed Run Mode", easy_button.collidepoint(pygame.mouse.get_pos()))
        draw_button(screen, cool_people_button, BLUE, "Cool People", cool_people_button.collidepoint(pygame.mouse.get_pos()))
        draw_button(screen, how_to_play_button, BLUE, "How to Play", how_to_play_button.collidepoint(pygame.mouse.get_pos()))
        draw_button(screen, exit_button, BLUE, "Exit", exit_button.collidepoint(pygame.mouse.get_pos()))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
            if event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                
                start_button.center = (WIDTH // 2, HEIGHT // 2 - 150)
                easy_button.center = (WIDTH // 2, HEIGHT // 2 - 50)
                how_to_play_button.center = (WIDTH // 2, HEIGHT // 2 + 50)
                cool_people_button.center = (WIDTH // 2, HEIGHT // 2 + 150)
                exit_button.center = (WIDTH // 2, HEIGHT // 2 + 250)
                back_button.center = (WIDTH // 2, HEIGHT - 100)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    geoguessr.geoguessr_mode()
                if easy_button.collidepoint(event.pos):
                    easy_mode.easy_mode()
                if cool_people_button.collidepoint(event.pos):
                    cool_people_screen()
                if how_to_play_button.collidepoint(event.pos):
                    howToPlay.how_to_play(screen, WIDTH, HEIGHT)
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        
        pygame.display.update()

main_menu()
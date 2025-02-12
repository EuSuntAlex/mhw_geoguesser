import pygame
import sys
import easy_mode

pygame.init()


WIDTH, HEIGHT = 1280, 720  
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("MH World GeoGuessr")

# Background
background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
# D:\Steam\userdata\121717891\760\remote\582010\screenshots
# PFP IMG
profile_pics = [pygame.image.load(f"img{i+1}.jpg") for i in range(6)]
profile_pics = [pygame.transform.scale(img, (50, 50)) for img in profile_pics]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
DARK_BLUE = (50, 100, 160)

# Font
font = pygame.font.Font(None, 60)
button_font = pygame.font.Font(None, 40)
desc_font = pygame.font.Font(None, 30)  

def draw_text(text, font, color, surface, x, y, centered=False):
    text_obj = font.render(text, True, color)
    if centered:
        text_rect = text_obj.get_rect(center=(x, y))
    else:
        text_rect = text_obj.get_rect(midleft=(x, y))
    surface.blit(text_obj, text_rect)

# Bttns
button_width, button_height = 200, 60
start_button = pygame.Rect(WIDTH//2 - button_width//2, HEIGHT//2 - 100, button_width, button_height)
easy_button = pygame.Rect(WIDTH//2 - button_width//2, HEIGHT//2, button_width, button_height)
cool_people_button = pygame.Rect(WIDTH//2 - button_width//2, HEIGHT//2 + 100, button_width, button_height)
exit_button = pygame.Rect(WIDTH//2 - button_width//2, HEIGHT//2 + 200, button_width, button_height)
back_button = pygame.Rect(WIDTH//2 - button_width//2, HEIGHT - 100, button_width, button_height)

# Person Data
cool_people_data = [
    {"name": "Vycery", "desc": "The GOAT of Monster Hunter: https://www.twitch.tv/vycery"},
    {"name": "Gaudium", "desc": "Very cool designer and musician! ko-fi.com/gaudium017"},
    {"name": "Himekoes", "desc": "Kpop lover that also streams! https://www.twitch.tv/himekoes"},
    {"name": "Maurani", "desc": "Safi hunter: https://www.twitch.tv/maurani_mh"},
    {"name": "j1nx_vn", "desc": "Variety streamer!: https://www.twitch.tv/j1nx_vn"},
    {"name": "IlIIllIIIlll aka barcode", "desc": "Lovely person with a chill stream: https://www.twitch.tv/iliilliiillliil"},
]
special_thanks = [
    "Special thanks to:",
    "Stoopy",
    "Pistol",
    "Stanley",
    "Valky",
    "Virz",
    "AOE_Kurvy",
    "for being awesome"
]

def cool_people_screen():
    global WIDTH, HEIGHT, screen
    running = True
    while running:
        screen.blit(pygame.transform.scale(background_image, (WIDTH, HEIGHT)), (0, 0))
        draw_text("Cool People", font, WHITE, screen, WIDTH // 2, HEIGHT // 10, centered=True)
        
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
        
        # Desenează lista de persoane pe partea stângă
        x_offset = WIDTH // 10
        y_offset = HEIGHT // 5
        for i, person in enumerate(cool_people_data):
            # Iconiță
            screen.blit(profile_pics[i], (x_offset, y_offset + i * 100))
            # Nume
            draw_text(person["name"], button_font, WHITE, screen, x_offset + 70, y_offset + i * 100)
            # Descriere
            draw_text(person["desc"], desc_font, WHITE, screen, x_offset + 70, y_offset + i * 100 + 30)
        
        # Desenează "Special thanks" pe partea dreaptă (pe coloană)
        thanks_x = WIDTH * 3 // 4
        thanks_y = HEIGHT // 5
        for line in special_thanks:
            draw_text(line, button_font, WHITE, screen, thanks_x, thanks_y, centered=True)
            thanks_y += 40  # Spațiu între linii
        
        # Desenează butonul "Back"
        pygame.draw.rect(screen, BLUE, back_button, border_radius=10)
        draw_text("Back", button_font, WHITE, screen, back_button.centerx, back_button.centery, centered=True)
        
        pygame.display.update()

def main_menu():
    global WIDTH, HEIGHT, screen
    running = True
    while running:
        screen.blit(pygame.transform.scale(background_image, (WIDTH, HEIGHT)), (0, 0))
        draw_text("MH World GeoGuessr", font, BLACK, screen, WIDTH // 2, HEIGHT // 10, centered=True)
        
        # Desenează butoanele
        pygame.draw.rect(screen, BLUE, start_button, border_radius=10)
        pygame.draw.rect(screen, BLUE, easy_button, border_radius=10)
        pygame.draw.rect(screen, BLUE, cool_people_button, border_radius=10)
        pygame.draw.rect(screen, BLUE, exit_button, border_radius=10)
        
        # Desenează textul butoanelor centrat
        draw_text("Start Game", button_font, WHITE, screen, start_button.centerx, start_button.centery, centered=True)
        draw_text("Start Easy Game", button_font, WHITE, screen, easy_button.centerx, easy_button.centery, centered=True)
        draw_text("Cool People", button_font, WHITE, screen, cool_people_button.centerx, cool_people_button.centery, centered=True)
        draw_text("Exit", button_font, WHITE, screen, exit_button.centerx, exit_button.centery, centered=True)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
            if event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                # Recalculează poziția butoanelor
                start_button.center = (WIDTH // 2, HEIGHT // 2 - 100)
                easy_button.center = (WIDTH // 2, HEIGHT // 2)
                cool_people_button.center = (WIDTH // 2, HEIGHT // 2 + 100)
                exit_button.center = (WIDTH // 2, HEIGHT // 2 + 200)
                back_button.center = (WIDTH // 2, HEIGHT - 100)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    print("Start Game pressed")
                if easy_button.collidepoint(event.pos):
                    print("Start Easy Game pressed")
                if cool_people_button.collidepoint(event.pos):
                    cool_people_screen()
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        
        pygame.display.update()

main_menu()
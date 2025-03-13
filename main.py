import pygame
import sys
import easy_mode
import geoguessr
import howToPlay
import os
import cursedMode

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

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
DARK_BLUE = (50, 100, 160)

font = pygame.font.Font(resource_path("./fonts/Familiar Pro-Bold.otf"), 30)
button_font = pygame.font.Font(None, 40)
desc_font = pygame.font.Font(None, 30)  

bless_img = pygame.image.load(resource_path("./ui/bless.png"))
bless_hover_img = pygame.image.load(resource_path("./ui/blessHighlight.png"))
cursed_img = pygame.image.load(resource_path("./ui/cursed.png"))
cursed_hover_img = pygame.image.load(resource_path("./ui/cursedHighlight.png"))
speed_img = pygame.image.load(resource_path("./ui/speed.png"))
speed_hover_img = pygame.image.load(resource_path("./ui/speedHighlight.png"))
how_img = pygame.image.load(resource_path("./ui/how.png"))
how_hover_img = pygame.image.load(resource_path("./ui/howHighlight.png"))
cool_img = pygame.image.load(resource_path("./ui/cool.png"))  
cool_hover_img = pygame.image.load(resource_path("./ui/coolHighlight.png"))
back_btn_img = pygame.image.load(resource_path("./ui/backBtn.png"))
back_btn_hover_img = pygame.image.load(resource_path("./ui/Back_Hover.png"))
exit_img = pygame.image.load(resource_path("./ui/exit.png"))
exit_hover_img = pygame.image.load(resource_path("./ui/exitHighlight.png"))

button_width, button_height = 266, 86  
bless_img = pygame.transform.scale(bless_img, (button_width, button_height))
bless_hover_img = pygame.transform.scale(bless_hover_img, (button_width, button_height))
cursed_img = pygame.transform.scale(cursed_img, (button_width, button_height))
cursed_hover_img = pygame.transform.scale(cursed_hover_img, (button_width, button_height))
speed_img = pygame.transform.scale(speed_img, (button_width, button_height))
speed_hover_img = pygame.transform.scale(speed_hover_img, (button_width, button_height))
how_img = pygame.transform.scale(how_img, (button_width, button_height))
how_hover_img = pygame.transform.scale(how_hover_img, (button_width, button_height))
cool_img = pygame.transform.scale(cool_img, (button_width, button_height))
cool_hover_img = pygame.transform.scale(cool_hover_img, (button_width, button_height))
exit_img = pygame.transform.scale(exit_img, (button_width, button_height))
exit_hover_img = pygame.transform.scale(exit_hover_img, (button_width, button_height))

bless_button = pygame.Rect(WIDTH//2 - button_width//2, HEIGHT//2 - 270, button_width, button_height)
cursed_button = pygame.Rect(WIDTH//2 - button_width//2, HEIGHT//2 - 170, button_width, button_height)
speed_button = pygame.Rect(WIDTH//2 - button_width//2, HEIGHT//2 - 70, button_width, button_height)
how_button = pygame.Rect(WIDTH//2 - button_width//2, HEIGHT//2 + 30, button_width, button_height)
cool_button = pygame.Rect(WIDTH//2 - button_width//2, HEIGHT//2 + 130, button_width, button_height)
exit_button = pygame.Rect(WIDTH//2 - button_width//2, HEIGHT//2 + 230, button_width, button_height)

def draw_button(surface, rect, texture, texture_hover, hover=False):

    if hover:
        surface.blit(texture_hover, rect.topleft)  
    else:
        surface.blit(texture, rect.topleft)  

def cool_people_screen():
    global WIDTH, HEIGHT, screen
    running = True
    cool_image = pygame.image.load(resource_path("./cool.png"))
    cool_image = pygame.transform.scale(cool_image, (WIDTH, HEIGHT)) 

    back_button = pygame.Rect(WIDTH//2 - button_width//2, HEIGHT - 130, button_width, button_height)

    while running:
        screen.fill(BLACK)  # might delete this
        
        screen.blit(cool_image, (0, 0)) 

        draw_button(screen, back_button, back_btn_img, back_btn_hover_img, back_button.collidepoint(pygame.mouse.get_pos()))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
            if event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                back_button.center = (WIDTH // 2, HEIGHT - 100)
                cool_image = pygame.transform.scale(cool_image, (WIDTH, HEIGHT))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    running = False  # exit the cool_people_screen and return to the main menu
        
        pygame.display.update()

def main_menu():
    global WIDTH, HEIGHT, screen
    running = True
    while running:
        screen.blit(pygame.transform.scale(background_image, (WIDTH, HEIGHT)), (0, 0))
        draw_button(screen, bless_button, bless_img, bless_hover_img, bless_button.collidepoint(pygame.mouse.get_pos()))
        draw_button(screen, cursed_button, cursed_img, cursed_hover_img, cursed_button.collidepoint(pygame.mouse.get_pos()))
        draw_button(screen, speed_button, speed_img, speed_hover_img, speed_button.collidepoint(pygame.mouse.get_pos()))
        draw_button(screen, how_button, how_img, how_hover_img, how_button.collidepoint(pygame.mouse.get_pos()))
        draw_button(screen, cool_button, cool_img, cool_hover_img, cool_button.collidepoint(pygame.mouse.get_pos()))
        draw_button(screen, exit_button, exit_img, exit_hover_img, exit_button.collidepoint(pygame.mouse.get_pos()))
        
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
                if bless_button.collidepoint(event.pos):
                    geoguessr.geoguessr_mode()
                if cursed_button.collidepoint(event.pos):
                    cursedMode.cursed_mode()
                if speed_button.collidepoint(event.pos):
                    easy_mode.easy_mode()
                if how_button.collidepoint(event.pos):
                    howToPlay.first_page(screen, WIDTH, HEIGHT)
                if cool_button.collidepoint(event.pos):
                    cool_people_screen()
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        
        pygame.display.update()

main_menu()
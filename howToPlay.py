import pygame
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def how_to_play(screen, WIDTH, HEIGHT):
    background_image = pygame.image.load(resource_path("rulz.jpg"))
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (70, 130, 180)
    DARK_BLUE = (50, 100, 160)

    font = pygame.font.Font(None, 60)
    button_font = pygame.font.Font(None, 40)
    desc_font = pygame.font.Font(None, 30)

    back_button = pygame.Rect(WIDTH // 2 - 125, HEIGHT - 100, 250, 60)

    instructions = [
        "How To Play Standard Mode:",
        "1. Select a zone and platform.",
        "2. Click on the map to guess the location.",
        "3. Earn points based on accuracy.",
        "4. If you didn't guess the correct zone or platform, you will not receive points!",
        "",
        "",
        "How To Play Speed Run Mode:",
        "1. You will start with 15 seconds",
        "2. If you guess correctly on your first try you will get 2 points and 3 seconds back",
        "3. If you guess correctly on your 2nd/3rd try, you will get 1 point and 1 second back",
        "4. You lose when the time is up or if you have accumulated 3 wrong guesses."
    ]

    running = True
    while running:
        screen.blit(background_image, (0, 0))

        y_offset = HEIGHT // 4  # Adjusted to start from a lower position
        for line in instructions:
            draw_text(line, desc_font, WHITE, screen, WIDTH // 2, y_offset, centered=True)
            y_offset += 40

        draw_button(screen, back_button, BLUE, "Back", button_font, back_button.collidepoint(pygame.mouse.get_pos()))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    running = False

        pygame.display.update()

def draw_text(text, font, color, surface, x, y, centered=False):
    text_surface = font.render(text, True, color)
    if centered:
        text_rect = text_surface.get_rect(center=(x, y))
    else:
        text_rect = text_surface.get_rect(midleft=(x, y))
    surface.blit(text_surface, text_rect)

def draw_button(surface, rect, color, text, button_font, hover=False):
    
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (70, 130, 180)
    DARK_BLUE = (50, 100, 160)
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
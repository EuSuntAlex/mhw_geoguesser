import pygame
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# define colors globally
WHITE = (255, 255, 255)

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
    
    y_offset -= font.get_height() // 2  # fine adjustment for perfect centering
    y_offset -= 9
    
    for line in lines:
        text_surface = font.render(line, True, WHITE)
        text_rect = text_surface.get_rect(center=(rect.centerx, rect.centery + y_offset))
        surface.blit(text_surface, text_rect)
        y_offset += font.get_height()  # move to the next line

def first_page(screen, WIDTH, HEIGHT):
    # load background image
    background_image = pygame.image.load(resource_path("./ui/rulz.png"))
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    # load fonts
    global font
    font = pygame.font.Font(resource_path("./fonts/Familiar Pro-Bold.otf"), 25)

    # load button textures
    left_texture = pygame.image.load(resource_path("./ui/left.png"))
    left_hover_texture = pygame.image.load(resource_path("./ui/leftHighlight.png"))
    right_texture = pygame.image.load(resource_path("./ui/right.png"))
    right_hover_texture = pygame.image.load(resource_path("./ui/rightHighlight.png"))

    # define button rectangles
    button_width, button_height = 200, 80
    left_button = pygame.Rect(160 + WIDTH // 4 - button_width // 2, HEIGHT - 95, button_width, button_height)
    right_button = pygame.Rect(3 * WIDTH // 4 - button_width // 2, HEIGHT - 95, button_width, button_height)

    running = True
    while running:
        # draw background
        screen.blit(background_image, (0, 0))

        # draw buttons
        draw_button(screen, left_button, "", left_texture, left_hover_texture, left_button.collidepoint(pygame.mouse.get_pos()))
        draw_button(screen, right_button, "", right_texture, right_hover_texture, right_button.collidepoint(pygame.mouse.get_pos()))

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if left_button.collidepoint(event.pos):
                    from main import main_menu  # go back to main menu
                    main_menu()
                    return
                elif right_button.collidepoint(event.pos):
                    second_page(screen, WIDTH, HEIGHT)  # go to second page
                    return

        # update display
        pygame.display.update()

def second_page(screen, WIDTH, HEIGHT):
    # load background image
    background_image = pygame.image.load(resource_path("./ui/rulz2.png"))
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    # load fonts
    global font
    font = pygame.font.Font(resource_path("./fonts/Familiar Pro-Bold.otf"), 25)

    # load button textures
    left_texture = pygame.image.load(resource_path("./ui/left.png"))
    left_hover_texture = pygame.image.load(resource_path("./ui/leftHighlight.png"))

    # define button rectangle
    button_width, button_height = 200, 80
    left_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT - 95, button_width, button_height)

    running = True
    while running:
        # draw background
        screen.blit(background_image, (0, 0))

        # draw button
        draw_button(screen, left_button,"", left_texture, left_hover_texture, left_button.collidepoint(pygame.mouse.get_pos()))

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if left_button.collidepoint(event.pos):
                    first_page(screen, WIDTH, HEIGHT)  # go back to first page
                    return

        # update display
        pygame.display.update()

# example usage
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    WIDTH, HEIGHT = screen.get_size()
    first_page(screen, WIDTH, HEIGHT)
    pygame.quit()
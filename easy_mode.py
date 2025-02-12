import pygame
import sys
import random
import loc

def easy_mode():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    WIDTH, HEIGHT = screen.get_size()  
    pygame.display.set_caption("Easy Mode")
    
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (70, 130, 180)
    
    # Font
    font = pygame.font.Font(None, 40)
    
    target = random.choice(loc.locations)
    image_stage = 0
    img_path = "./locations/" + target["images"][image_stage]
    img = pygame.image.load(img_path)
    
    options = target["options"]
    random.shuffle(options)
    
    running = True
    while running:
        WIDTH, HEIGHT = screen.get_size()
        img_scaled = pygame.transform.scale(img, (int(WIDTH * 0.8), int(HEIGHT * 0.75)))
        screen.fill(WHITE)
        
        # center img
        img_rect = img_scaled.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(img_scaled, img_rect.topleft)
        
        # Butoane 
        button_width, button_height = 250, 50
        button_spacing = 20
        buttons = []
        start_x = WIDTH // 4
        start_y = HEIGHT - 150
        
        for i in range(2):  # 2 rows
            for j in range(3):  # 3 col
                idx = i * 3 + j
                if idx < len(options):
                    button_rect = pygame.Rect(start_x + j * (button_width + button_spacing), 
                                              start_y + i * (button_height + button_spacing),
                                              button_width, button_height)
                    buttons.append(button_rect)
        
        # Desenare butoane
        for i, button in enumerate(buttons):
            pygame.draw.rect(screen, BLUE, button, border_radius=5)
            text_surface = font.render(options[i], True, WHITE)
            text_rect = text_surface.get_rect(center=button.center)
            screen.blit(text_surface, text_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button.collidepoint(event.pos):
                        selected_option = options[i]
                        if selected_option == target["correct"]:
                            print("Correct Answer!")
                            running = False
                        else:
                            print("Wrong Answer!")
                            options.pop(i)
                            if options:
                                image_stage = min(image_stage + 1, len(target["images"]) - 1)
                                img_path = "./locations/" + target["images"][image_stage]
                                img = pygame.image.load(img_path)
        
        pygame.display.update()
    
if __name__ == "__main__":
    easy_mode()

import pygame
import sys
import random

def easy_mode():
    pygame.init()
    WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Easy Mode")
    
   
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (70, 130, 180)
    
    # Font
    font = pygame.font.Font(None, 40)
    
    # imagini
    images = [
        {"small": "image1_small.jpg", "medium": "image1_medium.jpg", "large": "image1_large.jpg", "correct": "Option A"},
        {"small": "image2_small.jpg", "medium": "image2_medium.jpg", "large": "image2_large.jpg", "correct": "Option C"},
    ]
    
    current_image = random.choice(images)
    image_stage = "small"
    img = pygame.image.load(current_image[image_stage])
    img = pygame.transform.scale(img, (WIDTH // 2, HEIGHT // 2))
    
    options = ["Option A", "Option B", "Option C", "Option D", "Option E", "Option F"]
    random.shuffle(options)
    
    # But
    button_width, button_height = 200, 50
    buttons = [pygame.Rect(WIDTH//2 - button_width//2, HEIGHT//2 + i * 60, button_width, button_height) for i in range(6)]
    
    running = True
    while running:
        screen.fill(WHITE)
        screen.blit(img, (WIDTH // 4, HEIGHT // 6))
        
        # Drawe but
        for i, option in enumerate(options):
            pygame.draw.rect(screen, BLUE, buttons[i], border_radius=5)
            text_surface = font.render(option, True, WHITE)
            text_rect = text_surface.get_rect(center=buttons[i].center)
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
                        if selected_option == current_image["correct"]:
                            print("Correct Answer!")
                            running = False
                        else:
                            print("Wrong Answer!")
                            options.pop(i)  # wrong thing
                            buttons.pop(i)  # yeet button
                            if image_stage == "small":
                                image_stage = "medium"
                            elif image_stage == "medium":
                                image_stage = "large"
                            img = pygame.image.load(current_image[image_stage])
                            img = pygame.transform.scale(img, (WIDTH // 2, HEIGHT // 2))
                            
        pygame.display.update()
    
if __name__ == "__main__":
    easy_mode()

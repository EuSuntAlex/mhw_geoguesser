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
    RED = (255, 0, 0)
    
    # Font
    font = pygame.font.Font(None, 40)
    
    
    heart_img = pygame.image.load("hp.png")  
    heart_img = pygame.transform.scale(heart_img, (50, 50))  
    
    running = True
    score = 0  
    lives = 3  
    
    while running:
        target = random.choice(loc.locations)
        image_stage = 0
        img_path = "./locations/" + target["images"][image_stage]
        img = pygame.image.load(img_path)
        
        options = target["options"]
        random.shuffle(options)
        
        attempts = 0  
        
        while True:
            WIDTH, HEIGHT = screen.get_size()
            img_scaled = pygame.transform.scale(img, (int(WIDTH * 0.8), int(HEIGHT * 0.75)))
            screen.fill(WHITE)
            
            
            img_rect = img_scaled.get_rect(center=(WIDTH // 2, HEIGHT // 2.5))  
            screen.blit(img_scaled, img_rect.topleft)
            
            # Butoane 
            button_width, button_height = 250, 50
            button_spacing = 20
            buttons = []
            start_x = WIDTH // 4
            start_y = HEIGHT - 200  
            
            for i in range(2):  # 2 rows
                for j in range(3):  # 3 col
                    idx = i * 3 + j
                    if idx < len(options):
                        button_rect = pygame.Rect(start_x + j * (button_width + button_spacing), 
                                                  start_y + i * (button_height + button_spacing),
                                                  button_width, button_height)
                        buttons.append(button_rect)
            
            #  butoane
            for i, button in enumerate(buttons):
                pygame.draw.rect(screen, BLUE, button, border_radius=5)
                text_surface = font.render(options[i], True, WHITE)
                text_rect = text_surface.get_rect(center=button.center)
                screen.blit(text_surface, text_rect)
            
            # Afișare scor
            score_text = font.render(f"Score: {score}", True, BLACK)
            screen.blit(score_text, (WIDTH - 150, 70))  
            
            
            for i in range(lives):
                screen.blit(heart_img, (20 + i * 50, 20))
            
            # Buton exit
            exit_button = pygame.Rect(WIDTH - 120, 20, 80, 40) 
            pygame.draw.rect(screen, RED, exit_button, border_radius=5)
            exit_text = font.render("Exit", True, WHITE)
            exit_text_rect = exit_text.get_rect(center=exit_button.center)
            screen.blit(exit_text, exit_text_rect)
            
            selected_option = None  # 
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if exit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                    for i, button in enumerate(buttons):
                        if button.collidepoint(event.pos):
                            selected_option = options[i]
                            if selected_option == target["correct"]:
                                print("Correct Answer!")
                                if attempts == 0:
                                    score += 2  
                                else:
                                    score += 1  
                                break 
                            else:
                                print("Wrong Answer!")
                                attempts += 1  
                                if attempts >= 3:  
                                    lives -= 1  
                                    if lives == 0:  
                                        print("Game Over! You've lost all lives.")
                                        running = False
                                        break
                                    else:
                                        print("You've lost a life! Moving to a new location.")
                                        break  
                                else:
                                    options.pop(i)
                                    if options:
                                        image_stage = min(image_stage + 1, len(target["images"]) - 1)
                                        img_path = "./locations/" + target["images"][image_stage]
                                        img = pygame.image.load(img_path)
            
            pygame.display.update()
            if not running:
                break
            if selected_option is not None and (attempts >= 3 or selected_option == target["correct"]):
                break  
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    easy_mode()
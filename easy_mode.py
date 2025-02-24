import pygame
import sys
import random
import loc
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def draw_text(surface, text, font, color, x, y, shadow_color=None, shadow_offset=2):
    if shadow_color:
        text_surface = font.render(text, True, shadow_color)
        surface.blit(text_surface, (x + shadow_offset, y + shadow_offset))
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

def easy_mode():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    WIDTH, HEIGHT = screen.get_size()  
    pygame.display.set_caption("Easy Mode")
    
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (70, 130, 180)
    RED = (255, 0, 0)
    
    font = pygame.font.Font(None, 40)
    
    background = pygame.image.load(resource_path("geo_bckg.png"))
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))  
    
    timesup_image = pygame.image.load(resource_path("timesup.jpg"))
    timesup_image = pygame.transform.scale(timesup_image, (WIDTH, HEIGHT))  
    
    running = True
    score = 0  
    used_locations = []
    timer = 15000  
    start_time = pygame.time.get_ticks()  
    
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
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)
    
    while running:
        if len(used_locations) == len(loc.locations):
            print("No more locations!")
            running = False
            break
        
        target = random.choice(loc.locations)
        while target in used_locations:
            target = random.choice(loc.locations)
        used_locations.append(target)
        
        img_path = target["images"][0]
        img = pygame.image.load(resource_path(img_path))
        
        options = target["options"]
        random.shuffle(options)
        
        attempts = 0  
        zoom_factor = 3.0  
        
        while True:
            WIDTH, HEIGHT = screen.get_size()
            
            img_width = int(WIDTH * 0.8 * zoom_factor)
            img_height = int(HEIGHT * 0.75 * zoom_factor)
            img_scaled = pygame.transform.smoothscale(img, (img_width, img_height))
            
            screen.blit(background, (0, 0))
            
            img_rect = img_scaled.get_rect(center=(WIDTH // 2, HEIGHT // 2.5))  
            screen.blit(img_scaled, img_rect.topleft)
            
            back_button = pygame.Rect(20, HEIGHT - 120, 200, 50)
            draw_button(screen, back_button, RED, "Back", back_button.collidepoint(pygame.mouse.get_pos()))
            
            button_width, button_height = 250, 50
            button_spacing = 20
            buttons = []
            start_x = WIDTH // 4
            start_y = HEIGHT - 200  
            
            for i in range(2):  
                for j in range(3):  
                    idx = i * 3 + j
                    if idx < len(options):
                        button_rect = pygame.Rect(start_x + j * (button_width + button_spacing), 
                                                  start_y + i * (button_height + button_spacing),
                                                  button_width, button_height)
                        buttons.append(button_rect)
            
            for i, button in enumerate(buttons):
                draw_button(screen, button, BLUE, options[i], button.collidepoint(pygame.mouse.get_pos()))
            
            exit_button = pygame.Rect(WIDTH - 120, 20, 80, 40) 
            draw_button(screen, exit_button, RED, "Exit", exit_button.collidepoint(pygame.mouse.get_pos()))
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - start_time
            remaining_time = max(0, timer - elapsed_time)
            minutes = remaining_time // 60000
            seconds = (remaining_time % 60000) // 1000            
            draw_text(screen, f"Score: {score}", font, WHITE, WIDTH - 150, 70, shadow_color=BLACK)
            draw_text(screen, f"Time: {minutes:02}:{seconds:02}", font, WHITE, WIDTH - 170, 110, shadow_color=BLACK)
            

            
            if remaining_time <= 0:
                
                screen.blit(timesup_image, (0, 0))
                draw_text(screen,  f"Time is up! Score: {score}", font, WHITE, WIDTH // 2, HEIGHT // 2, shadow_color=BLACK)
                pygame.display.update()
                pygame.time.wait(2000)
                from main import main_menu 
                main_menu()
                return
            
            selected_option = None  
            
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
                    elif back_button.collidepoint(event.pos):
                        from main import main_menu 
                        main_menu() 
                    for i, button in enumerate(buttons):
                        if button.collidepoint(event.pos):
                            selected_option = options[i]
                            if selected_option == target["correct"]:
                                if attempts == 0:
                                    score += 2  
                                    timer += 3000 
                                else:
                                    score += 1  
                                    timer += 2000  
                                break  
                            else:
                                attempts += 1  
                                timer -= 1000  
                                
                                pygame.draw.rect(screen, RED, button, border_radius=5)
                                text_surface = font.render(options[i], True, WHITE)
                                text_rect = text_surface.get_rect(center=button.center)
                                screen.blit(text_surface, text_rect)
                                pygame.display.update()
                                pygame.time.wait(240)
                                
                                zoom_factor = max(1.0, zoom_factor - 1) 
                                
                                if attempts >= 3:  
                                    screen.blit(timesup_image, (0, 0))
                                    draw_text(screen, f"Game Over! Score: {score}.", font, WHITE, WIDTH // 2, HEIGHT // 2, shadow_color=BLACK)
                                    pygame.display.update()
                                    pygame.time.wait(1500) 
                                    from main import main_menu 
                                    main_menu()
                                    break
                                else:
                                    options.pop(i)

            
            pygame.display.update()
            if not running:
                break
            if selected_option is not None and (attempts >= 3 or selected_option == target["correct"]):
                break  
    
    if len(used_locations) == len(loc.locations):
        screen.blit(timesup_image, (0, 0))
        draw_text(screen, f"Final Score: {score}", font, WHITE, WIDTH // 2, HEIGHT // 2, shadow_color=BLACK)
        pygame.display.update()
        pygame.time.wait(2000)
        from main import main_menu 
        main_menu() 
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    easy_mode()
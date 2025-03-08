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
    logo = pygame.image.load(resource_path("./ui/Logo Cropped.png"))
    single_image = pygame.image.load(resource_path("./ui/speedrun.png"))
    right_panel = pygame.image.load(resource_path("./ui/scoreTime.png"))
    back_image = pygame.image.load(resource_path("./ui/Back To Menu.png"))
    back_image_hover = pygame.image.load(resource_path("./ui/Back_to_menu_hover.png"))
    button_texture = pygame.image.load(resource_path("./ui/Single Button.png"))
    button_texture_hover = pygame.image.load(resource_path("./ui/Single Button Hover.png"))
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (70, 130, 180)
    RED = (255, 0, 0)
    
    font = pygame.font.Font(resource_path("./fonts/Familiar Pro-Bold.otf"), 29)
    
    background = pygame.image.load(resource_path("ui/caca.png"))
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))  
    
    timesup_image = pygame.image.load(resource_path("timesup.jpg"))
    timesup_image = pygame.transform.scale(timesup_image, (WIDTH, HEIGHT))  
    
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
        
        y_offset -= font.get_height() // 2  
        y_offset -= 9
        
        for line in lines:
            text_surface = font.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(rect.centerx, rect.centery + y_offset))
            surface.blit(text_surface, text_rect)
            y_offset += font.get_height()  # move to the next line

    running = True
    score = 0  
    used_locations = []
    timer = 15000  
    start_time = pygame.time.get_ticks()  
    
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
        
        # scale image to 1920x1080 before cropping
        img = pygame.transform.smoothscale(img, (1920, 1080))
        
        options = target["options"]
        random.shuffle(options)
        
        attempts = 0  
        
        # initial crop and scale
        crop_size = 500  # start with 500x500
        img_scaled = pygame.transform.smoothscale(
            img.subsurface((img.get_width() // 2 - crop_size // 2, img.get_height() // 2 - crop_size // 2, crop_size, crop_size)),
            (1344, 756)
        )
        
        while True:
            WIDTH, HEIGHT = screen.get_size()
            
            screen.blit(background, (0, 0))
            screen.blit(logo, (0, HEIGHT * 0.0275))
            screen.blit(single_image, (WIDTH * 0.01, HEIGHT * 0.0275 + logo.get_height())) 
            screen.blit(right_panel, (WIDTH * 0.863, HEIGHT * 0.133))
            
            # display the processed image
            img_rect = img_scaled.get_rect(center=(WIDTH // 2, HEIGHT // 2.647))  
            screen.blit(img_scaled, img_rect.topleft)
            
            # back button
            back_button = pygame.Rect(int(WIDTH * 0.862), int(HEIGHT * 0.0275), 243, 97) 
            back_button_hover = back_button.collidepoint(pygame.mouse.get_pos())  
            if back_button_hover:
                screen.blit(back_image_hover, back_button.topleft)  
            else:
                screen.blit(back_image, back_button.topleft)
            
            # option buttons
            button_width, button_height = 260, 80
            button_spacing = 20
            buttons = []
            start_x = WIDTH // 4
            start_y = HEIGHT - 235  
            
            for i in range(2):  
                for j in range(3):  
                    idx = i * 3 + j
                    if idx < len(options):
                        button_rect = pygame.Rect(start_x + j * (button_width + button_spacing), 
                                                  start_y + i * (button_height + button_spacing),
                                                  button_width, button_height)
                        buttons.append(button_rect)
            
            for i, button in enumerate(buttons):
                draw_button(screen, button, options[i], button_texture, button_texture_hover, button.collidepoint(pygame.mouse.get_pos()))
            

            
            # display score and time
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - start_time
            remaining_time = max(0, timer - elapsed_time)
            minutes = remaining_time // 60000
            seconds = (remaining_time % 60000) // 1000            
            draw_text(screen, f"Score: {score}", font, WHITE, WIDTH - 197, 174, shadow_color=BLACK)
            draw_text(screen, f"Time: {minutes:02}:{seconds:02}", font, WHITE, WIDTH - 222, 288, shadow_color=BLACK)
            
            # check if time is up
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
                    if back_button.collidepoint(event.pos):
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
                                
                                # update crop size for zoom-out effect
                                if attempts == 1:
                                    crop_size = 800  # zoom out to 800x800
                                elif attempts == 2:
                                    # after 2 wrong attempts, show the full image scaled to 1344x756
                                    img_scaled = pygame.transform.smoothscale(img, (1344, 756))
                                    pygame.display.update()
                                    continue  # skip the rest of the loop to avoid cropping errors
                                
                                # ensure crop size doesn't exceed image dimensions
                                crop_size = min(crop_size, img.get_width(), img.get_height())
                                
                                # recrop and rescale the image
                                img_scaled = pygame.transform.smoothscale(
                                    img.subsurface((img.get_width() // 2 - crop_size // 2, img.get_height() // 2 - crop_size // 2, crop_size, crop_size)),
                                    (1344, 756)
                                )
                                
                                pygame.draw.rect(screen, RED, button, border_radius=5)
                                text_surface = font.render(options[i], True, WHITE)
                                text_rect = text_surface.get_rect(center=button.center)
                                screen.blit(text_surface, text_rect)
                                pygame.display.update()
                                pygame.time.wait(240)
                                
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
    
    from main import main_menu 
    main_menu() 

if __name__ == "__main__":
    easy_mode()
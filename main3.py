import pygame
import sys

pygame.init()

#dimensiunile ecranului
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

#ferestre joc
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Treasure Hunt cu Pitici")

# Setarea ratei de cadre
clock = pygame.time.Clock()

# Culoare butoane control
button_color = (128, 28, 28) # Maro-vișiniu
button_hover_color = (85, 53, 29)  # Varianta mai închisă pentru hover
button_text_color = (255, 255, 255)  # Text alb pentru butoane
button_border_color = (255, 228, 181)  # Culoare crem-galbui pentru rame

# Încărcarea imaginilor
start_map_image = pygame.image.load('coperta.png')
start_map_image = pygame.transform.scale(start_map_image, (screen_width, screen_height))

customize_map_image = pygame.image.load('coperta.png')
customize_map_image = pygame.transform.scale(customize_map_image, (screen_width, screen_height))

login_background_image = pygame.image.load('coperta.png')
login_background_image = pygame.transform.scale(login_background_image, (screen_width, screen_height))

# Fundal pentru mesaje
message_bg_image = pygame.image.load('message_bg.png').convert_alpha()

# Font medieval
try:
    medieval_font = pygame.font.Font('MedievalSharp-Book.ttf', 30)
except FileNotFoundError:
    print("Fontul MedievalSharp-Book.ttf nu a fost găsit. Se va folosi fontul implicit.")
    medieval_font = pygame.font.SysFont('Arial', 30)

# Funcție pentru a desena harta
def draw_map(is_start_page=True):
    if is_start_page:
        screen.blit(start_map_image, (0, 0))
    else:
        translucent_surface = pygame.Surface((screen_width, screen_height))
        translucent_surface.set_alpha(180)
        translucent_surface.blit(customize_map_image, (0, 0))
        screen.blit(translucent_surface, (0, 0))

# Funcție pentru a crea un buton
def draw_button(text, x, y, width, height, color, hover_color, border_color, font_size=30):
    font = pygame.font.Font('MedievalSharp-Book.ttf', font_size)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if x + width > mouse_x > x and y + height > mouse_y > y:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))  # hover
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))  # normală

    pygame.draw.rect(screen, border_color, (x, y, width, height), 3)  # Rama butonului

    text_surface = font.render(text, True, button_text_color)
    screen.blit(text_surface, (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))

# Funcție pentru a desena un mesaj cu fundal
def draw_message(text, x, y, width, height):
    message_bg = pygame.transform.scale(message_bg_image, (width, height))
    screen.blit(message_bg, (x, y))

    text_surface = medieval_font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))

# Funcție pentru meniul de start
def start_game(player):
    in_game = True
    while in_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fundalul paginii
        draw_map(is_start_page=True)

        # Butoane numerotate
        button_width = 100
        button_height = 50
        button_spacing = 20
        start_x = screen_width // 2 - (3 * button_width + 2 * button_spacing) // 2
        start_y = screen_height // 2 - button_height // 2

        for i in range(6):
            x = start_x + (button_width + button_spacing) * (i % 3)
            y = start_y + (button_height + button_spacing) * (i // 3)
            draw_button(str(i + 1), x, y, button_width, button_height, button_color, button_hover_color, button_border_color)

        # Butonul de „Înapoi”
        draw_button('Înapoi', 10, 10, 150, 50, button_color, button_hover_color, button_border_color)

        # Verificăm click pe butoane
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            # Verificăm dacă s-a apăsat pe unul dintre butoanele numerotate
            for i in range(6):
                x = start_x + (button_width + button_spacing) * (i % 3)
                y = start_y + (button_height + button_spacing) * (i // 3)
                if x <= mouse_x <= x + button_width and y <= mouse_y <= y + button_height:
                    open_page(i + 1)  # Deschidem pagina corespunzătoare butonului
            # Verificăm dacă s-a apăsat pe butonul „Înapoi”
            if 10 <= mouse_x <= 160 and 10 <= mouse_y <= 60:
                return

        pygame.display.update()
        clock.tick(60)

# Funcție pentru a deschide o pagină nouă
def open_page(page_number):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fundalul paginii
        screen.blit(start_map_image, (0, 0))

        # Mesaj care indică pagina curentă
        draw_message(f"Pagina {page_number}", screen_width // 2 - 150, screen_height // 2 - 50, 300, 100)

        # Butonul de „Înapoi”
        draw_button('Înapoi', 10, 10, 150, 50, button_color, button_hover_color, button_border_color)

        # Verificăm click pe butonul „Înapoi”
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if 10 <= mouse_x <= 160 and 10 <= mouse_y <= 60:
                return  # Înapoi la pagina anterioară

        pygame.display.update()
        clock.tick(60)
    in_game = True
    while in_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fundalul paginii
        draw_map(is_start_page=True)

        # Butoane numerotate
        button_width = 100
        button_height = 50
        button_spacing = 20
        start_x = screen_width // 2 - (3 * button_width + 2 * button_spacing) // 2
        start_y = screen_height // 2 - button_height // 2

        for i in range(6):
            x = start_x + (button_width + button_spacing) * (i % 3)
            y = start_y + (button_height + button_spacing) * (i // 3)
            draw_button(str(i + 1), x, y, button_width, button_height, button_color, button_hover_color, button_border_color)

        # Butonul de „Înapoi”
        draw_button('Înapoi', 10, 10, 150, 50, button_color, button_hover_color, button_border_color)

        # Verificăm click pe butoane
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            # Verificăm dacă s-a apăsat pe unul dintre butoanele numerotate
            for i in range(6):
                x = start_x + (button_width + button_spacing) * (i % 3)
                y = start_y + (button_height + button_spacing) * (i // 3)
                if x <= mouse_x <= x + button_width and y <= mouse_y <= y + button_height:
                    open_page(i + 1)  # Deschidem pagina corespunzătoare butonului
            # Verificăm dacă s-a apăsat pe butonul „Înapoi”
            if 10 <= mouse_x <= 160 and 10 <= mouse_y <= 60:
                return

        pygame.display.update()
        clock.tick(60)
    in_game = True
    while in_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fundalul paginii
        draw_map(is_start_page=True)

        # Butoane numerotate
        button_width = 100
        button_height = 50
        button_spacing = 20
        start_x = screen_width // 2 - (3 * button_width + 2 * button_spacing) // 2
        start_y = screen_height // 2 - button_height // 2

        for i in range(6):
            x = start_x + (button_width + button_spacing) * (i % 3)
            y = start_y + (button_height + button_spacing) * (i // 3)
            draw_button(str(i + 1), x, y, button_width, button_height, button_color, button_hover_color, button_border_color)

        # Butonul de „Înapoi”
        draw_button('Înapoi', 10, 10, 150, 50, button_color, button_hover_color, button_border_color)

        # Verificăm click pe butoane
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            # Verificăm dacă s-a apăsat pe unul dintre butoanele numerotate
            for i in range(6):
                x = start_x + (button_width + button_spacing) * (i % 3)
                y = start_y + (button_height + button_spacing) * (i // 3)
                if x <= mouse_x <= x + button_width and y <= mouse_y <= y + button_height:
                    print(f"Apăsat butonul {i + 1}")
            # Verificăm dacă s-a apăsat pe butonul „Înapoi”
            if 10 <= mouse_x <= 160 and 10 <= mouse_y <= 60:
                return

        pygame.display.update()
        clock.tick(60)
    in_game = True
    while in_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Harta de start
        draw_map(is_start_page=True)

        # Butonul de „Înapoi”
        draw_button('Înapoi', 10, 10, 150, 50, button_color, button_hover_color, button_border_color)
        # Butonul de „Minimizare”
        draw_button('Minimize', screen_width - 110, 10, 100, 40, button_color, button_hover_color, button_border_color, font_size=20)
        # Butonul de „Închidere”
        draw_button('Închidere', screen_width - 110, screen_height - 50, 100, 40, button_color, button_hover_color, button_border_color, font_size=20)

        # Verificăm click pe butoane
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if 10 <= mouse_x <= 160 and 10 <= mouse_y <= 60:
                return
            if screen_width - 110 <= mouse_x <= screen_width - 10 and 10 <= mouse_y <= 50:
                pygame.display.iconify()
            if screen_width - 110 <= mouse_x <= screen_width - 10 and screen_height - 50 <= mouse_y <= screen_height - 10:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)

# Meniul de login
def login_page():
    login = True
    username = ""
    password = ""
    active_input = None  # None, "username", or "password"

    font = pygame.font.Font('MedievalSharp-Book.ttf', 30)

    while login:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Verificăm dacă s-a apăsat pe butonul "Login"
                if screen_width // 2 - 150 <= mouse_x <= screen_width // 2 + 150 and screen_height // 2 + 150 <= mouse_y <= screen_height // 2 + 230:
                    print(f"Username: {username}, Password: {password}")  # Înlocuiește cu logica de autentificare
                    return
                # Verificăm dacă s-a apăsat pe butonul "Înapoi"
                elif 10 <= mouse_x <= 160 and 10 <= mouse_y <= 60:
                    return  # Înapoi la meniul principal
                # Verificăm dacă s-a apăsat pe câmpul de utilizator
                elif screen_width // 2 - 150 <= mouse_x <= screen_width // 2 + 150 and screen_height // 2 - 100 <= mouse_y <= screen_height // 2 - 50:
                    active_input = "username"
                # Verificăm dacă s-a apăsat pe câmpul de parolă
                elif screen_width // 2 - 150 <= mouse_x <= screen_width // 2 + 150 and screen_height // 2 <= mouse_y <= screen_height // 2 + 50:
                    active_input = "password"
                else:
                    active_input = None
            elif event.type == pygame.KEYDOWN and active_input:
                if event.key == pygame.K_BACKSPACE:
                    if active_input == "username":
                        username = username[:-1]
                    elif active_input == "password":
                        password = password[:-1]
                else:
                    if active_input == "username":
                        username += event.unicode
                    elif active_input == "password":
                        password += event.unicode

        # Fundalul paginii de login
        screen.blit(login_background_image, (0, 0))

        # Desenăm câmpurile de input
        username_color = (200, 200, 200) if active_input == "username" else (255, 255, 255)
        password_color = (200, 200, 200) if active_input == "password" else (255, 255, 255)

        pygame.draw.rect(screen, username_color, (screen_width // 2 - 150, screen_height // 2 - 100, 300, 50))
        pygame.draw.rect(screen, password_color, (screen_width // 2 - 150, screen_height // 2, 300, 50))
        pygame.draw.rect(screen, (0, 0, 0), (screen_width // 2 - 150, screen_height // 2 - 100, 300, 50), 2)
        pygame.draw.rect(screen, (0, 0, 0), (screen_width // 2 - 150, screen_height // 2, 300, 50), 2)

        # Text pentru câmpuri
        username_surface = font.render(username, True, (0, 0, 0))
        password_surface = font.render("*" * len(password), True, (0, 0, 0))
        screen.blit(username_surface, (screen_width // 2 - 140, screen_height // 2 - 90))
        screen.blit(password_surface, (screen_width // 2 - 140, screen_height // 2 + 10))

        # Etichete
        draw_message("Nume utilizator:", screen_width // 2 - 150, screen_height // 2 - 150, 300, 30)
        draw_message("Parolă:", screen_width // 2 - 150, screen_height // 2 - 50, 300, 30)

        # Butoane
        draw_button('Login', screen_width // 2 - 150, screen_height // 2 + 150, 300, 80, button_color, button_hover_color, button_border_color)
        draw_button('Înapoi', 10, 10, 150, 50, button_color, button_hover_color, button_border_color)

        pygame.display.update()
        clock.tick(60)
        
# Pagina cu reguli
def rules_page():
    rules = True
    while rules:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))  # Fundal negru pentru reguli
        draw_message('Aici vor fi regulile jocului...', screen_width // 4, screen_height // 4, screen_width // 2, screen_height // 2)

        draw_button('Înapoi', 10, 10, 150, 50, button_color, button_hover_color, button_border_color)

        # Verificăm click pe butoane
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if 10 <= mouse_x <= 160 and 10 <= mouse_y <= 60:
                return  # Înapoi la meniul principal

        pygame.display.update()
        clock.tick(60)

# Pagina de personalizare a piticului
def customize_dwarf():
    customize = True
    while customize:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))  # Fundal negru pentru personalizare pitic
        draw_message('Aici poți personaliza piticul...', screen_width // 4, screen_height // 4, screen_width // 2, screen_height // 2)

        draw_button('Înapoi', 10, 10, 150, 50, button_color, button_hover_color, button_border_color)

        # Verificăm click pe butoane
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if 10 <= mouse_x <= 160 and 10 <= mouse_y <= 60:
                return  # Înapoi la meniul principal

        pygame.display.update()
        clock.tick(60)

# Meniul principal
def main_menu():
    menu = True
    # Define the Player class
    class Player:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.width = 50
            self.height = 50
            self.color = (0, 255, 0)  # Green
    
        def draw(self, surface):
            pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
    
    player = Player(screen_width // 2 - 75, screen_height - 200)
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Imaginea de fundal
        screen.blit(login_background_image, (0, 0))

        # Butoane în poziții diferite
        draw_button('Start', screen_width // 2 - 250, screen_height // 2 - 50, 500, 120, button_color, button_hover_color, button_border_color, font_size=50)
        draw_button('Login', 100, screen_height - 200, 150, 50, button_color, button_hover_color, button_border_color)
        draw_button('Rules', 100, screen_height - 100, 150, 50, button_color, button_hover_color, button_border_color)
        draw_button('Customize Dwarf', screen_width - 300, screen_height - 200, 250, 50, button_color, button_hover_color, button_border_color)

        # Butonul de „Muzică”
        draw_button('Music on/off', screen_width - 300, 200, 250, 50, button_color, button_hover_color, button_border_color)

        # Butonul de „Minimizare”
        draw_button('Minimize', screen_width - 110, 0, 100, 40, button_color, button_hover_color, button_border_color, font_size=20)
        # Butonul de „Închidere”
        draw_button('Închidere', screen_width - 110, screen_height - 50, 100, 40, button_color, button_hover_color, button_border_color, font_size=20)

        pygame.display.update()
        clock.tick(60)

        # Verificăm click pe butoane
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if screen_width // 2 - 250 <= mouse_x <= screen_width // 2 + 250 and screen_height // 2 - 50 <= mouse_y <= screen_height // 2 + 70:
                start_game(player)
            elif 100 <= mouse_x <= 250 and screen_height - 200 <= mouse_y <= screen_height - 150:
                login_page()
            elif 100 <= mouse_x <= 250 and screen_height - 100 <= mouse_y <= screen_height - 50:
                rules_page()
            elif screen_width - 300 <= mouse_x <= screen_width - 50 and screen_height - 200 <= mouse_y <= screen_height - 150:
                customize_dwarf()
            elif screen_width - 300 <= mouse_x <= screen_width - 150 and 10 <= mouse_y <= 60:
                print("Music on/off - În implementare")
            elif screen_width - 110 <= mouse_x <= screen_width - 10 and 10 <= mouse_y <= 50:
                pygame.display.iconify()
            elif screen_width - 110 <= mouse_x <= screen_width - 10 and screen_height - 50 <= mouse_y <= screen_height - 10:
                pygame.quit()
                sys.exit()

# Pornim jocul
if __name__ == "__main__":
    main_menu()
    
#Dear reader,
#When I wrote this code, only god and
#I knew how it worked.
#Now, only god knows it!

#Therefore, if you are trying to optimize
#this routine and it fails (most surely),
#please increase this counter as a
#warning for the next time:
#total_hours_wasted_here = 254
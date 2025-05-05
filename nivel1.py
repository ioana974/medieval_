import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Regatul Cronogrilor: Pădurea Cărților Pierdute")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# --- Assets Loading ---
# TODO: Replace with your actual image paths
#  Make sure you have these images in the correct directory after replacing the paths.
try:
    background_img = pygame.image.load("padure_fundal.png").convert() # Example
    pitic_img = pygame.image.load("pitic_idle_1.png").convert_alpha() # Example
    goblin_img = pygame.image.load("goblin_idle_1.png").convert_alpha() # Example
    carte_img = pygame.image.load("carte_magica.png").convert_alpha()  # Example
    sadogandul_img = pygame.image.load("sadogandul.png").convert_alpha()  # Example
    button_img = pygame.image.load("button.png").convert_alpha()       # Example, customize this
except pygame.error as e:
    print(f"Unable to load one or more images: {e}")
    sys.exit()  # Exit if critical images are missing



# Scale background
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# --- Pitic Class ---
class Pitic(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pitic_img  # Use the loaded image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.animation_frames = [pygame.image.load(f"pitic_idle_{i}.png").convert_alpha() for i in range(1, 5)] #Example animation
        self.current_frame = 0
        self.animation_speed = 5  # Lower number = faster animation
        self.animation_counter = 0
        self.direction = 1  # 1 for right, -1 for left



    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.direction = -1
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.direction = 1

        # Keep player within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

       # Animation update
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
            self.image = self.animation_frames[self.current_frame]
            if self.direction == -1:
                self.image = pygame.transform.flip(self.image, True, False) #Flip image if moving left


# --- Goblin Class ---
class Goblin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = goblin_img  # Use the loaded image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.animation_frames = [pygame.image.load(f"goblin_idle_{i}.png").convert_alpha() for i in range(1, 5)] #Example animation change numbers as needed
        self.current_frame = 0
        self.animation_speed = 7  # adjust speed as needed
        self.animation_counter = 0
        self.direction = 1 #1 for right, -1 for left
        self.max_walk = 50 # How far the goblin walks before changing direction
        self.start_x = x

    def update(self):
        # Basic back and forth movement
        self.rect.x += self.speed * self.direction
        if self.rect.x > self.start_x + self.max_walk:
            self.direction = -1
        elif self.rect.x < self.start_x - self.max_walk:
            self.direction = 1

        # Goblin animation
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
            self.image = self.animation_frames[self.current_frame]
            if self.direction == -1:
                self.image = pygame.transform.flip(self.image, True, False)


# --- Carte Class ---
class Carte(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = carte_img  # Use the loaded image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# --- Sadogandul Class --- (NPC)
class Sadogandul(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = sadogandul_img # The loaded image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.talking = False
        self.font = pygame.font.Font(None, 24) # Load a font (None means default font)
        self.dialogue = [
            "Bine ai venit, mic pitic!",
            "Goblinul Cenzurii a furat cărțile!",
            "Recuperează-le pentru mine!",
            "Îți voi povesti despre Sadoveanu...",
             "Apăsați tasta E pentru a continua" #Added a prompt to guide dialogue
        ]
        self.current_line = 0

    def update(self):
        pass # No movement, just static NPC

    def start_dialogue(self):
        self.talking = True
        self.current_line = 0

    def next_line(self):
        self.current_line += 1
        if self.current_line >= len(self.dialogue):
            self.talking = False
            self.current_line = 0 # Reset for next interaction

    def draw_dialogue(self, screen):
        if self.talking:
            text_surface = self.font.render(self.dialogue[self.current_line], True, BLACK) #Render the current line in black text
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))# Position the text box
            screen.blit(text_surface, text_rect)


# --- Button Class for Quiz ---
class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, text, text_color, action=None):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.font = pygame.font.Font(None, 24) # Use pygame font
        self.text_surface = self.font.render(text, True, text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        self.action = action

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text_surface, self.text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
# --- Game Logic Variables ---
score = 0
game_state = "playing" # Possible states: "playing", "dialogue", "quiz", "level_complete"
collected_books = 0
required_books = 3 # Set a number of books to collect to complete the level, adjust as needed.

# --- Sprite Groups ---
all_sprites = pygame.sprite.Group()
goblin_group = pygame.sprite.Group()
carte_group = pygame.sprite.Group()

# --- Create Objects ---
pitic = Pitic(50, SCREEN_HEIGHT - 100)
all_sprites.add(pitic)

# Example Goblin placement.  Adjust coordinates
goblin1 = Goblin(200, SCREEN_HEIGHT - 100)
goblin2 = Goblin(400, SCREEN_HEIGHT - 100)
goblin_group.add(goblin1, goblin2)
all_sprites.add(goblin1, goblin2)

# Example Carte placement. Adjust coordinates
carte1 = Carte(150, SCREEN_HEIGHT - 200)
carte2 = Carte(350, SCREEN_HEIGHT - 250)
carte3 = Carte(550, SCREEN_HEIGHT -150)

carte_group.add(carte1, carte2, carte3)
all_sprites.add(carte1, carte2, carte3)

#Create Sadogandul
sadogandul = Sadogandul(650, SCREEN_HEIGHT - 100) # Adjust coordinates as needed
all_sprites.add(sadogandul)


# --- Quiz Function ---
def start_quiz():
    global game_state
    game_state = "quiz"

# Quiz Data (Example)
quiz_data = {
    "question": "Care revistă literară importantă a fost publicată în perioada interbelică?",
    "options": ["Gândirea", "Luceafărul", "România Literară", "Convorbiri Literare"],
    "correct_answer": "Gândirea"
}

quiz_active = False
selected_answer = None
quiz_buttons = []

def create_quiz_buttons():
    global quiz_buttons
    button_width = 150
    button_height = 50
    start_x = (SCREEN_WIDTH - (button_width * len(quiz_data["options"]) + 20 * (len(quiz_data["options"]) - 1))) // 2
    y = 450  # Adjust the vertical position as needed
    for i, option in enumerate(quiz_data["options"]):
        x = start_x + i * (button_width + 20)  # 20 is the spacing between buttons
        button = Button(x, y, button_width, button_height, BLUE, option, WHITE, action=option)
        quiz_buttons.append(button)


def draw_quiz(screen):
    font = pygame.font.Font(None, 36)
    question_surface = font.render(quiz_data["question"], True, BLACK)
    question_rect = question_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(question_surface, question_rect)

    for button in quiz_buttons:
        button.draw(screen)

def check_answer(answer):
    global game_state, score
    if answer == quiz_data["correct_answer"]:
        print("Correct!")
        score += 10  # Award points for correct answer
        game_state = "level_complete"

    else:
        print("Incorrect!")
        game_state = "playing" # or back to dialogue, or other consequence

    reset_quiz() # Reset for the next time, if any.

def reset_quiz():
    global quiz_active, selected_answer, quiz_buttons
    quiz_active = False
    selected_answer = None
    quiz_buttons = [] # Clear out the buttons

# --- Level Complete Display ---
def show_level_complete_screen():
    font = pygame.font.Font(None, 36)
    level_complete_text = font.render("NIVEL COMPLET!", True, GREEN)
    level_complete_rect = level_complete_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))

    score_text = font.render(f"Scor: {score}", True, GREEN)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    next_level_text = font.render("Apasa SPACE pentru a continua", True, GREEN)
    next_level_rect = next_level_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

    screen.blit(level_complete_text, level_complete_rect)
    screen.blit(score_text, score_rect)
    screen.blit(next_level_text, next_level_rect)

# --- Text Narativ & History Lesson ---
story_text = [
    "NIVEL 1: Pădurea Cărților Pierdute",
    "Sadogândul, spiritul pădurii, scrie povești pe frunze.",
    "Goblinul Cenzurii a furat cărțile magice ale epocii interbelice!",
    "Ajută-l pe Sadogândul să le recupereze și să învețe istoria literară!"
]

history_lesson = [
    "Lecție: Cultura și literatura interbelică",
    "Anii 1920–1940 au fost o perioadă de efervescență culturală în România.",
    "Scriitori ca Tudor Arghezi, Lucian Blaga, Hortensia Papadat-Bengescu, Camil Petrescu au definit epoca.",
    "Mihail Sadoveanu, unul dintre cei mai prolifici autori, scria romane de inspirație istorică și rurală.",
    "Au apărut reviste literare importante precum *Gândirea*, *Viața Românească*, *Contimporanul*.",
    "Aceste publicații au reflectat curente moderne, tradiționaliste, simboliste și avangardiste."
]

def display_text(screen, text_list, x, y, color=BLACK):
    font = pygame.font.Font(None, 24)
    line_spacing = 30  # Space between lines
    for i, line in enumerate(text_list):
        text_surface = font.render(line, True, color)
        text_rect = text_surface.get_rect(topleft=(x, y + i * line_spacing))
        screen.blit(text_surface, text_rect)

# --- Main Game Loop ---
running = True
clock = pygame.time.Clock()

while running:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_state == "dialogue":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e: # Advance dialogue with E key press
                    sadogandul.next_line()
                    if not sadogandul.talking:  # Dialogue over? Start quiz.
                        start_quiz()
                        create_quiz_buttons() # Create buttons when quiz starts
        elif game_state == "quiz":
             if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for button in quiz_buttons:
                    if button.is_clicked(mouse_pos):
                        check_answer(button.action)
        elif game_state == "level_complete":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    #TODO: Implement Level Progression.  For now, reset.
                    game_state = "playing"
                    collected_books = 0
                    # Reset Player Position, Goblin positions, Book positions...
                    pitic.rect.x = 50
                    pitic.rect.y = SCREEN_HEIGHT - 100
                    goblin1.rect.x = 200
                    goblin1.start_x = 200
                    goblin2.rect.x = 400
                    goblin2.start_x = 400
                    # Reposition books
                    carte1.rect.x = 150
                    carte1.rect.y = SCREEN_HEIGHT - 200
                    carte2.rect.x = 350
                    carte2.rect.y = SCREEN_HEIGHT - 250
                    carte3.rect.x = 550
                    carte3.rect.y = SCREEN_HEIGHT - 150
                    #Re-add the books to the group
                    carte_group.add(carte1,carte2,carte3)

    # --- Game Logic ---
    if game_state == "playing":
        pitic.update()
        goblin_group.update()

        # Check for book collection
        book_collisions = pygame.sprite.spritecollide(pitic, carte_group, True) # True = book disappears
        if book_collisions:
            collected_books += len(book_collisions)
            print(f"Books collected: {collected_books}")

        # Check for dialogue trigger
        if pygame.sprite.collide_rect(pitic, sadogandul):
            game_state = "dialogue"
            sadogandul.start_dialogue()


        if collected_books >= required_books:

            # Only initiate dialogue if not already happening
            if game_state != "dialogue": #Avoid infinite loop

            #if game_state !="level_complete" :
                start_quiz()
                create_quiz_buttons()
    # --- Drawing ---
    screen.blit(background_img, (0, 0))  # Draw background

    # Draw all sprites
    for sprite in all_sprites:
        screen.blit(sprite.image, sprite.rect)

    #Score display
    font = pygame.font.Font(None, 24)
    score_text = font.render(f"Cărți recuperate: {collected_books}/{required_books}", True, BLACK)
    screen.blit(score_text, (10, 10))  # Position the score

    # Dialogue Display
    if game_state == "dialogue":
         sadogandul.draw_dialogue(screen)


    # Quiz Display
    if game_state == "quiz":
        draw_quiz(screen)

    # Level Complete Display
    if game_state == "level_complete":
        show_level_complete_screen()

    pygame.display.flip() # Update the display
    clock.tick(60) # Limit frame rate to 60 FPS

pygame.quit()
sys.exit()
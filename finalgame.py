import pygame
import os

pygame.init()

# Display variables
PINK = (255, 192, 203)
BLUE = (0, 153, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pet Sim")
FPS = 30
CLOCK = pygame.time.Clock()

# Initial factor levels
HUNGER_LEVEL = 100
SLEEP_LEVEL = 100
HAPPINESS_LEVEL = 100

# Cat properties
CAT_HEIGHT = 150
CAT_WIDTH = 150

# For rendering concatenations
HUNGER_LEVEL_CONCATENATE = "HUNGER LEVEL = "
SLEEP_LEVEL_CONCATENATE = "SLEEP LEVEL = "
HAPPINESS_LEVEL_CONCATENATE = "HAPPINESS LEVEL = "

# Rendering welcome text and controls and warnings
FONT = pygame.font.Font('freesansbold.ttf', 24)
WELCOME_TEXT = FONT.render('This is MIKI!', True, BLUE, WHITE)
HUNGER_OK_TEXT = FONT.render('MIKI is well fed, YAY!', True, BLUE, WHITE)
HUNGER_LOW_TEXT = FONT.render('Please feed Miki!', True, YELLOW, BLACK)
HUNGER_DEAD_TEXT = FONT.render('Miki is dead!', True, RED, BLACK)
SLEEP_OK_TEXT = FONT.render('MIKI is not sleepy, YAY!', True, BLUE, WHITE)
SLEEP_LOW_TEXT = FONT.render('MIKI is very sleepy', True, YELLOW, BLACK)
SLEEP_DEAD_TEXT = FONT.render('Miki is dead!', True, RED, BLACK)
HAPPINESS_OK_TEXT = FONT.render('MIKI is happy!', True, BLUE, WHITE)
HAPPINESS_LOW_TEXT = FONT.render('MIKI is sad :(', True, YELLOW, BLACK)
HAPPINESS_DEAD_TEXT = FONT.render('Miki is dead!', True, RED, BLACK)
TEXT_RECT = WELCOME_TEXT.get_rect()
TEXT_RECT.center = (400, 20)
HUNGER_WARNING_TEXT_RECT = HUNGER_OK_TEXT.get_rect()
HUNGER_WARNING_TEXT_RECT.center = (150, 140)
SLEEP_WARNING_TEXT_RECT = SLEEP_OK_TEXT.get_rect()
SLEEP_WARNING_TEXT_RECT.center = (150, 180)
HAPPINESS_WARNING_TEXT_RECT = HAPPINESS_OK_TEXT.get_rect()
HAPPINESS_WARNING_TEXT_RECT.center = (150, 220)
PETTING_CON_TEXT = FONT.render('TOUCH cat to pet', True, BLUE, WHITE)
PETTING_CON_TEXT_RECT = PETTING_CON_TEXT.get_rect()
PETTING_CON_TEXT_RECT.center = (680, 400)
FEEDING_CON_TEXT = FONT.render('Press A to feed', True, BLUE, WHITE)
FEEDING_CON_TEXT_RECT = FEEDING_CON_TEXT.get_rect()
FEEDING_CON_TEXT_RECT.center = (680, 430)
SLEEPING_CON_TEXT = FONT.render('Press S to put to sleep', True, BLUE, WHITE)
SLEEPING_CON_TEXT_RECT = SLEEPING_CON_TEXT.get_rect()
SLEEPING_CON_TEXT_RECT.center = (660, 460)
COMFORT_TEXT = FONT.render('Its ok! It wasnt your fault. You tried your best', True, BLUE, WHITE)
COMFORT_TEXT_RECT = COMFORT_TEXT.get_rect()
COMFORT_TEXT_RECT.center = (300, 500)

# Rendering factor levels
HUNGER_LVL_TEXT = FONT.render(HUNGER_LEVEL_CONCATENATE + str(int(HUNGER_LEVEL)), True, BLUE, WHITE)
HUNGER_LVL_TEXT_RECT = HUNGER_LVL_TEXT.get_rect()
HUNGER_LVL_TEXT_RECT.center = (120, 20)
SLEEP_LVL_TEXT = FONT.render(SLEEP_LEVEL_CONCATENATE + str(int(SLEEP_LEVEL)), True, BLUE, WHITE)
SLEEP_LVL_TEXT_RECT = SLEEP_LVL_TEXT.get_rect()
SLEEP_LVL_TEXT_RECT.center = (120, 50)
HAPPINESS_LVL_TEXT = FONT.render(HAPPINESS_LEVEL_CONCATENATE + str(int(HAPPINESS_LEVEL)), True, BLUE, WHITE)
HAPPINESS_LVL_TEXT_RECT = HAPPINESS_LVL_TEXT.get_rect()
HAPPINESS_LVL_TEXT_RECT.center = (120, 80)

# Image variables
CAT_IMAGE = pygame.image.load(os.path.join('Assets', 'Cat picture.png'))
CAT_SCALED = pygame.transform.scale(CAT_IMAGE, (CAT_WIDTH, CAT_HEIGHT))
TOMBSTONE_IMAGE = pygame.image.load(os.path.join('Assets', 'Tombstone picture.png'))
TOMBSTONE_SCALED = pygame.transform.scale(TOMBSTONE_IMAGE, (CAT_WIDTH, CAT_HEIGHT))  # They are both the same size

# Sound variables
pygame.mixer.init()
MEOW_SOUND = pygame.mixer.Sound(os.path.join("Assets", "petting_meow.mp3"))
SLEEP_SOUND = pygame.mixer.Sound(os.path.join("Assets", "sleep_sound.mp3"))
HUNGRY_SOUND = pygame.mixer.Sound(os.path.join("Assets", "hungry_meow.mp3"))

last_sleep_press_time = 0  # Initialize last sleep press time


# Function to update hunger factor
def update_hunger_factor(elapsed_time):
    global HUNGER_LEVEL
    minutes_passed = elapsed_time / 60
    HUNGER_LEVEL = max(0, HUNGER_LEVEL - minutes_passed * 50)


# Function to update sleepiness factor
def update_sleepiness_factor(elapsed_time):
    global SLEEP_LEVEL, last_sleep_press_time
    minutes_passed = elapsed_time / 60
    if pygame.key.get_pressed()[pygame.K_s] and pygame.time.get_ticks() - last_sleep_press_time >= 60000:
        SLEEP_LEVEL = min(100, SLEEP_LEVEL + 50)
        last_sleep_press_time = pygame.time.get_ticks()
    else:
        SLEEP_LEVEL = max(0, SLEEP_LEVEL - minutes_passed * 40)


# Function to update happiness factor
def update_happiness_factor(elapsed_time):
    global HAPPINESS_LEVEL
    minutes_passed = elapsed_time / 60
    HAPPINESS_LEVEL = max(0, HAPPINESS_LEVEL - minutes_passed * 60)  # Adjust the decrease rate as needed


# Function to handle keyboard events for feeding cat and resetting sleepiness
def handle_keyboard_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                update_hunger_on_keypress()
            elif event.key == pygame.K_s and pygame.time.get_ticks() - last_sleep_press_time >= 60000:  # So that the cat cant sleep twice in 60 seconds
                update_sleepiness_on_keypress()
    return True


# Function to handle updating hunger level on key press
def update_hunger_on_keypress():
    global HUNGER_LEVEL
    HUNGER_LEVEL = min(100, HUNGER_LEVEL + 1)


# Function to handle updating sleepiness level on key press
def update_sleepiness_on_keypress():
    global SLEEP_LEVEL, last_sleep_press_time
    SLEEP_LEVEL = 100
    last_sleep_press_time = pygame.time.get_ticks()
    SLEEP_SOUND.play()


# Function to handle petting the cat and increasing happiness
def pet_cat():
    global HAPPINESS_LEVEL
    HAPPINESS_LEVEL = min(100, HAPPINESS_LEVEL + 5)  # Increase happiness by 5


# Function to check if Miki is dead
def check_miki_dead(countdown_timer):
    if countdown_timer <= 0 or HUNGER_LEVEL <= 0 or SLEEP_LEVEL <= 0 or HAPPINESS_LEVEL <= 0:
        return True
    else:
        return False


# Window function
def draw_window(countdown_timer, mouse_pos):
    global HUNGER_LVL_TEXT, HUNGER_LVL_TEXT_RECT, WELCOME_TEXT

    WIN.fill(PINK)
    if check_miki_dead(countdown_timer):
        WIN.blit(TOMBSTONE_SCALED, (400, 250))
        if countdown_timer <= 0:
            WIN.blit(HUNGER_DEAD_TEXT, HUNGER_WARNING_TEXT_RECT)
            WIN.blit(SLEEP_DEAD_TEXT, SLEEP_WARNING_TEXT_RECT)
            WIN.blit(HAPPINESS_DEAD_TEXT, HAPPINESS_WARNING_TEXT_RECT)
            WIN.blit(COMFORT_TEXT, COMFORT_TEXT_RECT)  # Display comfort text when Miki dies
        else:
            if HUNGER_LEVEL <= 0:
                WIN.blit(HUNGER_DEAD_TEXT, HUNGER_WARNING_TEXT_RECT)
                WIN.blit(SLEEP_DEAD_TEXT, SLEEP_WARNING_TEXT_RECT)
                WIN.blit(HAPPINESS_DEAD_TEXT, HAPPINESS_WARNING_TEXT_RECT)
                WIN.blit(COMFORT_TEXT, COMFORT_TEXT_RECT)  # Display comfort text when Miki dies
            if SLEEP_LEVEL <= 0:
                WIN.blit(SLEEP_DEAD_TEXT, SLEEP_WARNING_TEXT_RECT)
                WIN.blit(HUNGER_DEAD_TEXT, HUNGER_WARNING_TEXT_RECT)
                WIN.blit(HAPPINESS_DEAD_TEXT, HAPPINESS_WARNING_TEXT_RECT)
                WIN.blit(COMFORT_TEXT, COMFORT_TEXT_RECT)  # Display comfort text when Miki dies
            if HAPPINESS_LEVEL <= 0:
                WIN.blit(HAPPINESS_DEAD_TEXT, HAPPINESS_WARNING_TEXT_RECT)
                WIN.blit(SLEEP_DEAD_TEXT, SLEEP_WARNING_TEXT_RECT)
                WIN.blit(HUNGER_DEAD_TEXT, HUNGER_WARNING_TEXT_RECT)
                WIN.blit(COMFORT_TEXT, COMFORT_TEXT_RECT)  # Display comfort text when Miki dies
    else:
        if HUNGER_LEVEL <= 0:
            WIN.blit(TOMBSTONE_SCALED, (400, 250))
            WIN.blit(HUNGER_DEAD_TEXT, HUNGER_WARNING_TEXT_RECT)
        else:
            WIN.blit(CAT_SCALED, (400, 250))
            if HUNGER_LEVEL < 50:
                WIN.blit(HUNGER_LOW_TEXT, HUNGER_WARNING_TEXT_RECT)
            else:
                WIN.blit(HUNGER_OK_TEXT, HUNGER_WARNING_TEXT_RECT)
        if SLEEP_LEVEL <= 0:
            WIN.blit(TOMBSTONE_SCALED, (400, 250))
            WIN.blit(SLEEP_DEAD_TEXT, SLEEP_WARNING_TEXT_RECT)
        else:
            if SLEEP_LEVEL < 50:
                WIN.blit(SLEEP_LOW_TEXT, SLEEP_WARNING_TEXT_RECT)
            else:
                WIN.blit(SLEEP_OK_TEXT, SLEEP_WARNING_TEXT_RECT)
        if HAPPINESS_LEVEL <= 0:
            WIN.blit(TOMBSTONE_SCALED, (400, 250))
            WIN.blit(HAPPINESS_DEAD_TEXT, HAPPINESS_WARNING_TEXT_RECT)
        else:
            if HAPPINESS_LEVEL < 50:
                WIN.blit(HAPPINESS_LOW_TEXT, HAPPINESS_WARNING_TEXT_RECT)
            else:
                WIN.blit(HAPPINESS_OK_TEXT, HAPPINESS_WARNING_TEXT_RECT)
        WIN.blit(WELCOME_TEXT, TEXT_RECT)
        WIN.blit(PETTING_CON_TEXT, PETTING_CON_TEXT_RECT)
        WIN.blit(FEEDING_CON_TEXT, FEEDING_CON_TEXT_RECT)
        WIN.blit(SLEEPING_CON_TEXT, SLEEPING_CON_TEXT_RECT)
        HUNGER_LVL_TEXT = FONT.render(HUNGER_LEVEL_CONCATENATE + str(int(HUNGER_LEVEL)), True, BLUE, WHITE)
        HUNGER_LVL_TEXT_RECT = HUNGER_LVL_TEXT.get_rect()
        HUNGER_LVL_TEXT_RECT.center = (120, 20)
        WIN.blit(HUNGER_LVL_TEXT, HUNGER_LVL_TEXT_RECT)
        SLEEP_LVL_TEXT = FONT.render(SLEEP_LEVEL_CONCATENATE + str(int(SLEEP_LEVEL)), True, BLUE, WHITE)
        SLEEP_LVL_TEXT_RECT = SLEEP_LVL_TEXT.get_rect()
        SLEEP_LVL_TEXT_RECT.center = (120, 50)
        WIN.blit(SLEEP_LVL_TEXT, SLEEP_LVL_TEXT_RECT)
        HAPPINESS_LVL_TEXT = FONT.render(HAPPINESS_LEVEL_CONCATENATE + str(int(HAPPINESS_LEVEL)), True, BLUE, WHITE)
        HAPPINESS_LVL_TEXT_RECT = HAPPINESS_LVL_TEXT.get_rect()
        HAPPINESS_LVL_TEXT_RECT.center = (150, 80)
        WIN.blit(HAPPINESS_LVL_TEXT, HAPPINESS_LVL_TEXT_RECT)
        timer_text = FONT.render(f"Time Left: {countdown_timer // 60:02}:{countdown_timer % 60:02}", True, BLUE, WHITE)
        WIN.blit(timer_text, (600, 10))
        cat_rect = CAT_SCALED.get_rect(topleft=(400, 250))
        if cat_rect.collidepoint(mouse_pos):
            MEOW_SOUND.play()
            pet_cat()  # Pet the cat when the mouse cursor is over it


# Main function
def main():
    countdown_timer = 600
    run = True
    while run:
        CLOCK.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = CLOCK.get_time() / 1000
        countdown_timer = max(0, countdown_timer - elapsed_time)
        update_hunger_factor(elapsed_time)
        update_sleepiness_factor(elapsed_time)
        update_happiness_factor(elapsed_time)
        run = handle_keyboard_events()
        draw_window(int(countdown_timer), mouse_pos)
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()

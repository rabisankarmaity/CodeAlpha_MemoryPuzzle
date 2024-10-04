import pygame
import random
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 700  # Adjust the height for the header
HEADER_HEIGHT = 100  # Space for the header with the timer
GRID_SIZE = 4  # 4x4 grid
CARD_SIZE = WIDTH // GRID_SIZE
FPS = 30
FONT = pygame.font.Font(None, 36)
BUTTON_FONT = pygame.font.Font(None, 40)
TIME_LIMIT = 60  # Game time limit in seconds

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 205, 50)
BORDER_COLOR = (0, 0, 0)  # Black border color for cards
CARD_BORDER_WIDTH = 5
BACKGROUND_COLOR = (173, 216, 230)  # Light blue background for the board
HEADER_BACKGROUND_COLOR = (135, 206, 250)  # Sky blue background for the header
WIN_COLOR = (128, 0, 128)  # Purple for winning message
LOSS_COLOR = (255, 0, 0)   # Red for loss (time up) message
BUTTON_COLOR = (30, 144, 255)  # Blue for the "Play Again" button
BUTTON_HOVER_COLOR = (65, 105, 225)  # Darker blue on hover
BUTTON_TEXT_COLOR = WHITE
BUTTON_SHADOW_COLOR = (0, 0, 139)  # Dark blue shadow

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Memory Puzzle Game')

# Load card images (using random colors for simplicity)
CARD_BACK = pygame.Surface((CARD_SIZE, CARD_SIZE))
CARD_BACK.fill(GREEN)

def initialize_cards():
    # Load and shuffle the cards
    cards = [pygame.Surface((CARD_SIZE, CARD_SIZE)) for _ in range(GRID_SIZE**2 // 2)]
    for i, card in enumerate(cards):
        card.fill((random.randint(50, 200), random.randint(50, 200), random.randint(50, 200)))
    
    # Duplicate and shuffle cards
    cards *= 2
    random.shuffle(cards)
    return cards

# Game state variables
flipped = []
matched = []
cards = initialize_cards()
start_time = time.time()
elapsed_time = 0  # Initialize elapsed time

# Button rectangle
button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 60)

def draw_header(time_left, message="", message_color=BLACK):
    # Draw the header (timer and messages) area
    pygame.draw.rect(screen, HEADER_BACKGROUND_COLOR, (0, 0, WIDTH, HEADER_HEIGHT))
    
    # Draw the timer
    timer_surface = FONT.render(f"Time Left: {time_left}s", True, BLACK)
    screen.blit(timer_surface, (10, 10))
    
    # Draw game messages (if any)
    if message:
        message_surface = FONT.render(message, True, message_color)
        screen.blit(message_surface, (WIDTH // 2 - 50, HEADER_HEIGHT // 2))

def draw_board():
    padding = 10  # Spacing between cards
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            idx = i * GRID_SIZE + j
            x, y = j * CARD_SIZE + padding // 2, i * CARD_SIZE + padding // 2 + HEADER_HEIGHT
            if idx in flipped or idx in matched:
                # Draw the card with a border
                pygame.draw.rect(screen, BORDER_COLOR, (x, y, CARD_SIZE - padding, CARD_SIZE - padding), CARD_BORDER_WIDTH)
                screen.blit(cards[idx], (x + CARD_BORDER_WIDTH // 2, y + CARD_BORDER_WIDTH // 2))
            else:
                # Draw the card back with a border
                pygame.draw.rect(screen, BORDER_COLOR, (x, y, CARD_SIZE - padding, CARD_SIZE - padding), CARD_BORDER_WIDTH)
                screen.blit(CARD_BACK, (x + CARD_BORDER_WIDTH // 2, y + CARD_BORDER_WIDTH // 2))

def draw_button(hovered=False):
    # Draw the shadow for the button
    pygame.draw.rect(screen, BUTTON_SHADOW_COLOR, (button_rect.x + 5, button_rect.y + 5, button_rect.width, button_rect.height), border_radius=10)
    
    # Draw the actual button
    button_color = BUTTON_HOVER_COLOR if hovered else BUTTON_COLOR
    pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
    
    # Render and center the text
    button_text = BUTTON_FONT.render("Play Again", True, BUTTON_TEXT_COLOR)
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)

def get_card_at_pos(pos):
    padding = 10
    x, y = pos
    if y < HEADER_HEIGHT:
        return None  # Ignore clicks in the header area
    row = (y - HEADER_HEIGHT) // (CARD_SIZE + padding // 2)
    col = x // (CARD_SIZE + padding // 2)
    return row * GRID_SIZE + col

def check_for_match():
    if len(flipped) == 2:
        idx1, idx2 = flipped
        if cards[idx1] == cards[idx2]:
            matched.extend(flipped)
        flipped.clear()

def reset_game():
    global flipped, matched, cards, start_time, elapsed_time
    flipped = []
    matched = []
    cards = initialize_cards()
    start_time = time.time()
    elapsed_time = 0

def main():
    global start_time, elapsed_time
    clock = pygame.time.Clock()
    running = True
    game_over = False
    player_won = False
    message_color = BLACK  # Default message color
    show_button = False  # Button will be shown after game ends
    
    while running:
        screen.fill(BACKGROUND_COLOR)  # Set background for the game
        
        # If the player has not won yet, calculate the time left
        if not player_won:
            elapsed_time = time.time() - start_time
        time_left = max(TIME_LIMIT - int(elapsed_time), 0)

        # Draw the header section with a dynamic message
        if player_won:
            draw_header(time_left, "You Win!", WIN_COLOR)
            show_button = True
        elif game_over:
            draw_header(time_left, "Time's Up!", LOSS_COLOR)
            show_button = True
        else:
            draw_header(time_left)

        # Draw the card grid
        draw_board()

        # Check if the player has won
        if len(matched) == GRID_SIZE**2 and not player_won:
            player_won = True
            message_color = WIN_COLOR
            pygame.display.flip()
            pygame.time.wait(2000)
            game_over = True  # Stop the game after win

        # Check if time is up and player hasn't won
        if time_left == 0 and not player_won:
            game_over = True
            message_color = LOSS_COLOR

        # Draw the "Play Again" button if the game is over
        if show_button:
            mouse_pos = pygame.mouse.get_pos()
            hovered = button_rect.collidepoint(mouse_pos)
            draw_button(hovered)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over and not player_won:
                    if len(flipped) < 2:
                        idx = get_card_at_pos(pygame.mouse.get_pos())
                        if idx is not None and idx not in flipped and idx not in matched:
                            flipped.append(idx)
                elif show_button and button_rect.collidepoint(event.pos):
                    # If the "Play Again" button is clicked, reset the game
                    reset_game()
                    player_won = False
                    game_over = False
                    show_button = False
                
        check_for_match()
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if True:
    main()

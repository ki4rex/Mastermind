import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRID_ROWS = 10  # Number of guesses allowed
GRID_COLS = 4   # Number of pegs per guess
PEG_RADIUS = 20
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (128, 0, 128)]  # Red, Green, Blue, Yellow, Orange, Purple
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND_COLOR = (240, 240, 240)

# Screen Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mastermind")

# Font
font = pygame.font.SysFont('Arial', 24)

# Functions to calculate feedback
def calculate_feedback(secret, guess):
    black_pegs = 0
    white_pegs = 0
    secret_copy = secret[:]
    guess_copy = guess[:]

    # First pass: check for black pegs (correct color and position)
    for i in range(len(secret)):
        if guess[i] == secret[i]:
            black_pegs += 1
            secret_copy[i] = None  # Mark this peg as used
            guess_copy[i] = None

    # Second pass: check for white pegs (correct color but wrong position)
    for i in range(len(guess)):
        if guess_copy[i] is not None:
            for j in range(len(secret)):
                if guess_copy[i] == secret_copy[j]:
                    white_pegs += 1
                    secret_copy[j] = None  # Mark this peg as used
                    break

    return black_pegs, white_pegs

# Game class
class MastermindGame:
    def __init__(self):
        self.secret_code = random.sample(COLORS, GRID_COLS)  # Random 4-color secret code
        self.guesses = []
        self.feedback = []
        self.current_guess = []

    def reset_game(self):
        self.secret_code = random.sample(COLORS, GRID_COLS)
        self.guesses = []
        self.feedback = []
        self.current_guess = []

    def add_guess(self, color):
        if len(self.current_guess) < GRID_COLS:
            self.current_guess.append(color)

    def submit_guess(self):
        if len(self.current_guess) == GRID_COLS:
            self.guesses.append(self.current_guess)
            black_pegs, white_pegs = calculate_feedback(self.secret_code, self.current_guess)
            self.feedback.append((black_pegs, white_pegs))
            self.current_guess = []  # Reset for next guess
            if black_pegs == GRID_COLS:
                return True  # Game won
        return False  # Game continues

# Function to display the splash screen
def display_splash_screen():
    splash_screen = True
    while splash_screen:
        screen.fill(BLACK)

        # Display game title and rules
        title_text = font.render("Mastermind", True, WHITE)
        rules_text = font.render("Rules of the Game:", True, WHITE)
        rule1_text = font.render("1. Guess the secret color sequence.", True, WHITE)
        rule2_text = font.render("2. Each guess is followed by feedback.", True, WHITE)
        rule3_text = font.render("3. Black pegs = correct color and position.", True, WHITE)
        rule4_text = font.render("4. White pegs = correct color, wrong position.", True, WHITE)
        rule5_text = font.render("5. You have 10 guesses to solve the puzzle.", True, WHITE)
        start_text = font.render("Press any key or click to start.", True, WHITE)

        # Position the text
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))
        screen.blit(rules_text, (50, 150))
        screen.blit(rule1_text, (50, 180))
        screen.blit(rule2_text, (50, 210))
        screen.blit(rule3_text, (50, 240))
        screen.blit(rule4_text, (50, 270))
        screen.blit(rule5_text, (50, 300))
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT - 100))

        pygame.display.flip()

        # Wait for user to click or press a key
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False  # Exit the program
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                splash_screen = False  # Exit splash screen

    return True

# Pygame loop
def main():
    # Display the splash screen with rules
    if not display_splash_screen():
        return  # Exit if user closes the splash screen

    game = MastermindGame()
    running = True
    game_won = False
    clock = pygame.time.Clock()

    while running:
        screen.fill(BACKGROUND_COLOR)

        # Draw guesses and feedback
        for i, guess in enumerate(game.guesses):
            for j, color in enumerate(guess):
                pygame.draw.circle(screen, color, (50 + j * 60, 50 + i * 60), PEG_RADIUS)

            # Draw feedback (black and white pegs)
            black_pegs, white_pegs = game.feedback[i]
            pygame.draw.circle(screen, BLACK, (350, 50 + i * 60), 10)  # Black pegs
            pygame.draw.circle(screen, WHITE, (375, 50 + i * 60), 10)  # White pegs
            for _ in range(black_pegs):
                pygame.draw.circle(screen, BLACK, (350 + _ * 20, 50 + i * 60), 10)
            for _ in range(white_pegs):
                pygame.draw.circle(screen, WHITE, (375 + _ * 20, 50 + i * 60), 10)

        # Draw the current guess
        for i, color in enumerate(game.current_guess):
            pygame.draw.circle(screen, color, (50 + i * 60, 350), PEG_RADIUS)

        # Color selection interface
        for i, color in enumerate(COLORS):
            pygame.draw.rect(screen, color, (50 + i * 100, 420, 80, 50))
            pygame.draw.rect(screen, BLACK, (50 + i * 100, 420, 80, 50), 2)

        # Check for win condition
        if game_won:
            win_text = font.render("You Win!", True, (0, 255, 0))
            screen.blit(win_text, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y > 420:  # If clicked on color selection
                    index = (x - 50) // 100
                    if 0 <= index < len(COLORS):
                        game.add_guess(COLORS[index])
                elif y < 400 and len(game.current_guess) == GRID_COLS:  # Submit guess if row is filled
                    game_won = game.submit_guess()
                    if game_won:
                        win_text = font.render("You Win!", True, (0, 255, 0))
                        screen.blit(win_text, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
    pygame.quit()

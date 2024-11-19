# Import necessary modules
import pygame  # For creating the game window and handling game logic
import sys     # For handling system-specific functionalities like exiting the game
import random  # For randomizing the apple's position

# Initialize Pygame
pygame.init()

# Screen dimensions
SW, SH = 800, 800  # Screen width and height

# Block size (used for grid and snake/food dimensions)
BLOCK_SIZE = 50

# Font setup for score display
FONT = pygame.font.Font("font.ttf", BLOCK_SIZE * 2)

# Set up the game screen and window title
screen = pygame.display.set_mode((SW, SH))
pygame.display.set_caption("Snake!")  # Game title
clock = pygame.time.Clock()           # Clock to control game frame rate

# Snake class to handle the snake's position, movement, and collisions
class Snake:
    def __init__(self):
        # Initialize snake's starting position and movement direction
        self.x, self.y = BLOCK_SIZE, BLOCK_SIZE  # Initial position of the snake's head
        self.xdir = 1                            # Movement direction (1 block to the right)
        self.ydir = 0                            # No vertical movement
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)  # Head of the snake
        self.body = [pygame.Rect(self.x - BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]  # Initial body segment
        self.dead = False  # Status flag for whether the snake is "dead"

    def update(self):
        global apple

        # Check for collisions with the snake's body or the screen boundaries
        for square in self.body:
            if self.head.x == square.x and self.head.y == square.y:
                self.dead = True  # Collision with body
            if self.head.x not in range(0, SW) or self.head.y not in range(0, SH):
                self.dead = True  # Collision with screen edges

        # Reset the snake if it dies
        if self.dead:
            # Reset snake's position, direction, and body
            self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
            self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
            self.body = [pygame.Rect(self.x - BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
            self.xdir = 1
            self.ydir = 0
            self.dead = False
            apple = Apple()  # Spawn a new apple

        # Update the snake's body and head position
        self.body.append(self.head)  # Add the current head to the body
        for i in range(len(self.body) - 1):
            # Move body segments to follow the segment ahead
            self.body[i].x, self.body[i].y = self.body[i + 1].x, self.body[i + 1].y
        self.head.x += self.xdir * BLOCK_SIZE  # Move head in the x direction
        self.head.y += self.ydir * BLOCK_SIZE  # Move head in the y direction
        self.body.remove(self.head)  # Remove the duplicate head at the tail

# Apple class to handle the food for the snake
class Apple:
    def __init__(self):
        # Randomize apple's position within the grid
        self.x = int(random.randint(0, SW) / BLOCK_SIZE) * BLOCK_SIZE
        self.y = int(random.randint(0, SH) / BLOCK_SIZE) * BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)  # Represent the apple as a rectangle

    def update(self):
        # Draw the apple on the screen
        pygame.draw.rect(screen, "orange", self.rect)

# Function to draw the grid lines on the screen
def drawGrid():
    for x in range(0, SW, BLOCK_SIZE):
        for y in range(0, SH, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, "#3c3c3b", rect, 1)  # Draw grid lines with a light gray color

# Initial score display setup
score = FONT.render("1", True, "white")  # Initial score text
score_rect = score.get_rect(center=(SW / 2, SH / 20))  # Position the score at the top center of the screen

# Initialize the game grid, snake, and apple
drawGrid()
snake = Snake()
apple = Apple()

# Game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # Close the game window
            sys.exit()
        if event.type == pygame.KEYDOWN:
            # Change the snake's direction based on arrow key inputs
            if event.key == pygame.K_DOWN:
                snake.ydir = 1
                snake.xdir = 0
            elif event.key == pygame.K_UP:
                snake.ydir = -1
                snake.xdir = 0
            elif event.key == pygame.K_RIGHT:
                snake.ydir = 0
                snake.xdir = 1
            elif event.key == pygame.K_LEFT:
                snake.ydir = 0
                snake.xdir = -1

    # Update the snake's position and check for collisions
    snake.update()

    # Clear the screen
    screen.fill('black')
    
    # Redraw the grid
    drawGrid()

    # Update and draw the apple
    apple.update()

    # Update and draw the score
    score = FONT.render(f"{len(snake.body) + 1}", True, "white")
    screen.blit(score, score_rect)

    # Draw the snake
    pygame.draw.rect(screen, "green", snake.head)  # Draw the head
    for square in snake.body:
        pygame.draw.rect(screen, "green", square)  # Draw each body segment

    # Check if the snake eats the apple
    if snake.head.x == apple.x and snake.head.y == apple.y:
        # Add a new body segment at the tail and spawn a new apple
        snake.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
        apple = Apple()

    # Refresh the display
    pygame.display.update()
    clock.tick(5)  # Limit the frame rate to 5 FPS

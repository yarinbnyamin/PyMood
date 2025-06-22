import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_RADIUS = 10
SAFE_ZONE_RADIUS = 30
SIGNAL_INTERVAL = 2000  # milliseconds

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 150, 255)
DARK_GRAY = (30, 30, 30)

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sanctuary Signal")

# Clock
clock = pygame.time.Clock()

# Player and Safe Zone positions
player_pos = [WIDTH // 2, HEIGHT // 2]
safe_zone = [random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)]

# Timing
last_signal_time = 0

# Game loop
running = True
font = pygame.font.SysFont(None, 36)

while running:
    dt = clock.tick(60)
    current_time = pygame.time.get_ticks()

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= 3
    if keys[pygame.K_RIGHT]:
        player_pos[0] += 3
    if keys[pygame.K_UP]:
        player_pos[1] -= 3
    if keys[pygame.K_DOWN]:
        player_pos[1] += 3

    # Draw background
    screen.fill(DARK_GRAY)

    # Draw Safe Zone (only when player reaches it)
    dist = math.hypot(player_pos[0] - safe_zone[0], player_pos[1] - safe_zone[1])
    if dist < SAFE_ZONE_RADIUS:
        pygame.draw.circle(screen, BLUE, safe_zone, SAFE_ZONE_RADIUS)
        msg = font.render("You found the Safe Zone", True, WHITE)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 20))
    else:
        # Show direction pulse every few seconds
        if current_time - last_signal_time > SIGNAL_INTERVAL:
            last_signal_time = current_time
            pygame.draw.line(screen, BLUE, player_pos, safe_zone, 2)

    # Draw player
    pygame.draw.circle(screen, WHITE, player_pos, PLAYER_RADIUS)

    # Update display
    pygame.display.flip()

pygame.quit()

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
TIME_LIMIT = 15000  # 15 seconds to reach safe zone

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
round_start_time = pygame.time.get_ticks()

# Movement and dash
NORMAL_SPEED = 3
DASH_SPEED = 6

# Game state
running = True
font = pygame.font.SysFont(None, 36)
show_game_over = False


def reset_safe_zone():
    global safe_zone, round_start_time
    safe_zone[0] = random.randint(50, WIDTH - 50)
    safe_zone[1] = random.randint(50, HEIGHT - 50)
    round_start_time = pygame.time.get_ticks()


while running:
    dt = clock.tick(60)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Time and distance checks
    time_elapsed = current_time - round_start_time
    dist = math.hypot(player_pos[0] - safe_zone[0], player_pos[1] - safe_zone[1])

    if time_elapsed > TIME_LIMIT and dist >= SAFE_ZONE_RADIUS:
        show_game_over = True

    # Movement
    keys = pygame.key.get_pressed()
    speed = DASH_SPEED if keys[pygame.K_SPACE] else NORMAL_SPEED

    if keys[pygame.K_LEFT]:
        player_pos[0] -= speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += speed
    if keys[pygame.K_UP]:
        player_pos[1] -= speed
    if keys[pygame.K_DOWN]:
        player_pos[1] += speed

    # Keep player within bounds
    player_pos[0] = max(PLAYER_RADIUS, min(WIDTH - PLAYER_RADIUS, player_pos[0]))
    player_pos[1] = max(PLAYER_RADIUS, min(HEIGHT - PLAYER_RADIUS, player_pos[1]))

    # Drawing
    screen.fill(DARK_GRAY)

    if show_game_over:
        msg = font.render("Game Over", True, RED)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 20))
    else:
        if dist < SAFE_ZONE_RADIUS:
            pygame.draw.circle(screen, BLUE, safe_zone, SAFE_ZONE_RADIUS)
            msg = font.render("Safe! New Zone...", True, WHITE)
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 20))
            pygame.display.flip()
            pygame.time.delay(1000)
            reset_safe_zone()
            continue
        elif current_time - last_signal_time > SIGNAL_INTERVAL:
            last_signal_time = current_time
            pygame.draw.line(screen, BLUE, player_pos, safe_zone, 2)

    # Draw player
    pygame.draw.circle(screen, WHITE, player_pos, PLAYER_RADIUS)

    # Draw time left
    time_left = max(0, (TIME_LIMIT - time_elapsed) // 1000)
    timer_msg = font.render(f"Time Left: {time_left}s", True, WHITE)
    screen.blit(timer_msg, (10, 10))

    pygame.display.flip()

pygame.quit()

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
ZOMBIE_COUNT = 5
ZOMBIE_SPEED = 1.2
PLAYER_MAX_HEALTH = 100
ZOMBIE_DAMAGE = 10
KNOCKBACK_DISTANCE = 15

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 150, 255)
YELLOW = (255, 255, 0)
DARK_GRAY = (30, 30, 30)
GREEN = (0, 255, 0)

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sanctuary Signal - Zombie Mode")

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

# Zombies
zombies = []


def spawn_zombies():
    return [
        [random.randint(0, WIDTH), random.randint(0, HEIGHT)]
        for _ in range(ZOMBIE_COUNT)
    ]


zombies = spawn_zombies()

# Game state
running = True
font = pygame.font.SysFont(None, 36)
show_game_over = False
locked_safe_zone = False
player_health = PLAYER_MAX_HEALTH


# Functions
def reset_safe_zone():
    global safe_zone, round_start_time, zombies, locked_safe_zone, player_pos
    safe_zone = [random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)]
    round_start_time = pygame.time.get_ticks()
    zombies = spawn_zombies()
    locked_safe_zone = False
    player_pos = [WIDTH // 2, HEIGHT // 2]


# Game loop
while running:
    dt = clock.tick(60)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Time and distance checks
    time_elapsed = current_time - round_start_time
    dist_to_safe = math.hypot(
        player_pos[0] - safe_zone[0], player_pos[1] - safe_zone[1]
    )

    if time_elapsed > TIME_LIMIT:
        if dist_to_safe < SAFE_ZONE_RADIUS and locked_safe_zone:
            zombies = []  # Clear zombies after surviving the round
            pygame.time.delay(1000)
            reset_safe_zone()
            continue
        else:
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

    # Lock the door manually when inside the safe zone
    if keys[pygame.K_e] and dist_to_safe < SAFE_ZONE_RADIUS:
        locked_safe_zone = True

    # Keep player within bounds
    player_pos[0] = max(PLAYER_RADIUS, min(WIDTH - PLAYER_RADIUS, player_pos[0]))
    player_pos[1] = max(PLAYER_RADIUS, min(HEIGHT - PLAYER_RADIUS, player_pos[1]))

    # Move zombies toward the player
    for zombie in zombies:
        dx, dy = player_pos[0] - zombie[0], player_pos[1] - zombie[1]
        distance = math.hypot(dx, dy)
        if distance != 0:
            zombie[0] += ZOMBIE_SPEED * dx / distance
            zombie[1] += ZOMBIE_SPEED * dy / distance

        # Check collision with player
        if distance < PLAYER_RADIUS + 8:
            player_health -= ZOMBIE_DAMAGE
            # Knockback
            knock_dx = -KNOCKBACK_DISTANCE * dx / distance
            knock_dy = -KNOCKBACK_DISTANCE * dy / distance
            zombie[0] += knock_dx
            zombie[1] += knock_dy

            # Clamp zombie back inside screen
            zombie[0] = max(0, min(WIDTH, zombie[0]))
            zombie[1] = max(0, min(HEIGHT, zombie[1]))

    if player_health <= 0:
        show_game_over = True

    # Drawing
    screen.fill(DARK_GRAY)

    if show_game_over:
        msg = font.render("Game Over", True, RED)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 20))
    else:
        # Safe Zone Visuals
        if locked_safe_zone:
            pygame.draw.circle(screen, YELLOW, safe_zone, SAFE_ZONE_RADIUS)
        else:
            pygame.draw.circle(screen, BLUE, safe_zone, SAFE_ZONE_RADIUS)

        # Signal pulse
        if current_time - last_signal_time > SIGNAL_INTERVAL:
            last_signal_time = current_time
            pygame.draw.line(screen, BLUE, player_pos, safe_zone, 2)

        # Draw zombies
        for zombie in zombies:
            pygame.draw.circle(screen, RED, (int(zombie[0]), int(zombie[1])), 8)

        # Draw player
        pygame.draw.circle(screen, WHITE, player_pos, PLAYER_RADIUS)

        # Draw time left
        time_left = max(0, (TIME_LIMIT - time_elapsed) // 1000)
        timer_msg = font.render(f"Time Left: {time_left}s", True, WHITE)
        screen.blit(timer_msg, (10, 10))

        # Draw health bar
        pygame.draw.rect(screen, RED, (10, 50, 200, 20))
        pygame.draw.rect(
            screen, GREEN, (10, 50, max(0, 200 * player_health / PLAYER_MAX_HEALTH), 20)
        )
        health_text = font.render("Health", True, WHITE)
        screen.blit(health_text, (220, 45))

        if dist_to_safe < SAFE_ZONE_RADIUS and not locked_safe_zone:
            hint = font.render("Press E to lock the door!", True, WHITE)
            screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 40))

    pygame.display.flip()

pygame.quit()

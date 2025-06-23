import pygame
import random
import math


def main():
    pygame.init()

    # Constants
    WIDTH, HEIGHT = 800, 600
    PLAYER_RADIUS = 10
    SAFE_ZONE_RADIUS = 30
    SIGNAL_INTERVAL = 2000
    TIME_LIMIT = 15000
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

    # Screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Safe Zone - Zombie Survival")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    # Game State Variables
    player_pos = [WIDTH // 2, HEIGHT // 2]
    safe_zone = [random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)]
    last_signal_time = 0
    round_start_time = pygame.time.get_ticks()
    zombies = []
    running = True
    show_game_over = False
    locked_safe_zone = False
    player_health = PLAYER_MAX_HEALTH
    hold_start_time = 0
    lock_held = False
    health_pickups = []
    paused = False
    score = 0
    zombie_count = 5

    def spawn_zombies(n):
        return [[random.randint(0, WIDTH), random.randint(0, HEIGHT)] for _ in range(n)]

    def reset_safe_zone():
        nonlocal safe_zone, round_start_time, zombies, locked_safe_zone, score, health_pickups, zombie_count
        safe_zone = [random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)]
        round_start_time = pygame.time.get_ticks()
        zombie_count = 5 + score * 2
        zombies.extend(spawn_zombies(zombie_count))
        locked_safe_zone = False
        score += 1
        health_pickups.append(
            [random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)]
        )

    def reset_game():
        nonlocal player_pos, safe_zone, last_signal_time, round_start_time, zombies, running
        nonlocal show_game_over, locked_safe_zone, player_health, score, hold_start_time, lock_held, health_pickups
        nonlocal zombie_count, paused
        player_pos = [WIDTH // 2, HEIGHT // 2]
        safe_zone = [random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)]
        last_signal_time = 0
        round_start_time = pygame.time.get_ticks()
        score = 0
        zombie_count = 5 + score * 2
        zombies = spawn_zombies(zombie_count)
        running = True
        show_game_over = False
        locked_safe_zone = False
        player_health = PLAYER_MAX_HEALTH
        hold_start_time = 0
        lock_held = False
        health_pickups = [
            [random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)]
        ]
        paused = False

    # Initial state
    reset_game()

    while running:
        dt = clock.tick(60)
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if (
                show_game_over
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_r
            ):
                reset_game()
            if paused and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_r:
                    reset_game()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            paused = True

        if paused:
            screen.fill(DARK_GRAY)
            pause_text = font.render("Paused", True, YELLOW)
            cont_text = font.render("Press C to Continue, R to Restart", True, WHITE)
            screen.blit(
                pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 40)
            )
            screen.blit(
                cont_text, (WIDTH // 2 - cont_text.get_width() // 2, HEIGHT // 2)
            )
            pygame.display.flip()
            continue

        if show_game_over:
            screen.fill(DARK_GRAY)
            msg = font.render("Game Over", True, RED)
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 20))
            restart_msg = font.render("Press R to Restart", True, WHITE)
            screen.blit(
                restart_msg,
                (WIDTH // 2 - restart_msg.get_width() // 2, HEIGHT // 2 + 30),
            )
            pygame.display.flip()
            continue

        time_elapsed = current_time - round_start_time
        dist_to_safe = math.hypot(
            player_pos[0] - safe_zone[0], player_pos[1] - safe_zone[1]
        )

        if time_elapsed > TIME_LIMIT:
            if dist_to_safe < SAFE_ZONE_RADIUS and locked_safe_zone:
                zombies.clear()
                reset_safe_zone()
            else:
                show_game_over = True

        speed = 6 if keys[pygame.K_SPACE] else 3

        if not (locked_safe_zone and dist_to_safe < SAFE_ZONE_RADIUS):
            if keys[pygame.K_LEFT]:
                player_pos[0] -= speed
            if keys[pygame.K_RIGHT]:
                player_pos[0] += speed
            if keys[pygame.K_UP]:
                player_pos[1] -= speed
            if keys[pygame.K_DOWN]:
                player_pos[1] += speed

        if keys[pygame.K_e] and dist_to_safe < SAFE_ZONE_RADIUS:
            if not lock_held:
                if hold_start_time == 0:
                    hold_start_time = current_time
                elif current_time - hold_start_time >= 1000:
                    locked_safe_zone = not locked_safe_zone
                    hold_start_time = 0
                    lock_held = True
        else:
            hold_start_time = 0
            lock_held = False

        player_pos[0] = max(PLAYER_RADIUS, min(WIDTH - PLAYER_RADIUS, player_pos[0]))
        player_pos[1] = max(PLAYER_RADIUS, min(HEIGHT - PLAYER_RADIUS, player_pos[1]))

        for zombie in zombies:
            dx, dy = player_pos[0] - zombie[0], player_pos[1] - zombie[1]
            distance = math.hypot(dx, dy)
            dist_to_zone = math.hypot(
                zombie[0] - safe_zone[0], zombie[1] - safe_zone[1]
            )

            if locked_safe_zone and dist_to_zone < SAFE_ZONE_RADIUS:
                knock_dx = (
                    -KNOCKBACK_DISTANCE * (safe_zone[0] - zombie[0]) / dist_to_zone
                )
                knock_dy = (
                    -KNOCKBACK_DISTANCE * (safe_zone[1] - zombie[1]) / dist_to_zone
                )
                zombie[0] += knock_dx
                zombie[1] += knock_dy
                continue

            if distance != 0:
                zombie[0] += 1.2 * dx / distance
                zombie[1] += 1.2 * dy / distance

            if distance < PLAYER_RADIUS + 8:
                if not (locked_safe_zone and dist_to_safe < SAFE_ZONE_RADIUS):
                    player_health -= ZOMBIE_DAMAGE
                knock_dx = -KNOCKBACK_DISTANCE * dx / distance
                knock_dy = -KNOCKBACK_DISTANCE * dy / distance
                zombie[0] += knock_dx
                zombie[1] += knock_dy
                zombie[0] = max(0, min(WIDTH, zombie[0]))
                zombie[1] = max(0, min(HEIGHT, zombie[1]))

        for pickup in health_pickups[:]:
            if (
                math.hypot(player_pos[0] - pickup[0], player_pos[1] - pickup[1])
                < PLAYER_RADIUS + 8
            ):
                player_health = min(PLAYER_MAX_HEALTH, player_health + 20)
                health_pickups.remove(pickup)

        if player_health <= 0:
            show_game_over = True

        screen.fill(DARK_GRAY)

        if dist_to_safe < SAFE_ZONE_RADIUS:
            zone_color = YELLOW if locked_safe_zone else BLUE
            pygame.draw.circle(screen, zone_color, safe_zone, SAFE_ZONE_RADIUS)

        if current_time - last_signal_time > SIGNAL_INTERVAL:
            last_signal_time = current_time
            pygame.draw.line(screen, BLUE, player_pos, safe_zone, 2)

        for zombie in zombies:
            pygame.draw.circle(screen, RED, (int(zombie[0]), int(zombie[1])), 8)

        for pickup in health_pickups:
            pygame.draw.circle(screen, GREEN, (int(pickup[0]), int(pickup[1])), 6)

        pygame.draw.circle(screen, WHITE, player_pos, PLAYER_RADIUS)

        time_left = max(0, (TIME_LIMIT - time_elapsed) // 1000)
        screen.blit(font.render(f"Time Left: {time_left}s", True, WHITE), (10, 10))

        pygame.draw.rect(screen, RED, (10, 50, 200, 20))
        pygame.draw.rect(
            screen, GREEN, (10, 50, max(0, 200 * player_health / PLAYER_MAX_HEALTH), 20)
        )
        screen.blit(font.render("Health", True, WHITE), (220, 45))

        screen.blit(font.render(f"Score: {score}", True, WHITE), (WIDTH - 150, 10))

        if dist_to_safe < SAFE_ZONE_RADIUS:
            screen.blit(
                font.render("Hold E to lock/unlock (1s)", True, WHITE),
                (WIDTH // 2 - 150, HEIGHT - 40),
            )
            if hold_start_time > 0:
                bar_length = 100
                progress = min(1.0, (current_time - hold_start_time) / 1000.0)
                pygame.draw.rect(
                    screen,
                    WHITE,
                    (WIDTH // 2 - bar_length // 2, HEIGHT - 20, bar_length, 10),
                    1,
                )
                pygame.draw.rect(
                    screen,
                    GREEN,
                    (
                        WIDTH // 2 - bar_length // 2,
                        HEIGHT - 20,
                        int(bar_length * progress),
                        10,
                    ),
                )

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

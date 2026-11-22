import pygame
import random
from pathlib import Path

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("❊ 𝔣𝔯𝔬𝔰𝔱𝔟𝔦𝔱𝔢 ❊")

clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms", 30)
small_font = pygame.font.SysFont("comicsansms", 20)

IMG_DIR = Path(__file__).resolve().parent / "imgs"

def load_sprite(filename, size):
    image = pygame.image.load(str(IMG_DIR / filename)).convert_alpha()
    return pygame.transform.smoothscale(image, size)

player_img = load_sprite("player.png", (65, 90))
frostling_img = load_sprite("frostling.png", (60, 65))
frostfang_img = load_sprite("frostfang.png", (50, 65))
boss_img = load_sprite("jack frost.png", (110, 150))

running = True
dt = 0

player_pos = pygame.Vector2(400, 300)
player_speed = 300
player_health = 5
damage_cooldown = 0

facing = pygame.Vector2(1, 0)
fireballs = []
fireball_speed = 400

enemies = []
spawn_timer = 2.0
spawn_interval = 2.0
max_enemies = 3

level = 1
enemies_defeated = 0
total_defeated = 0
enemies_per_level = 5

boss_spawned = False
game_over = False
victory = False

def spawn_enemy(enemy_type, x, y):
    if enemy_type == "frostling":
        speed = 175
        health = 1

    elif enemy_type == "frostfang":
        speed = 0
        health = 2

    elif enemy_type == "frostking":
        speed = 70
        health = 20

    else:
        return

    enemy = {
        "type": enemy_type,
        "pos": pygame.Vector2(x, y),
        "speed": speed,
        "health": health,
        "timer": 1.0,
        "attacked": False,
        "vulnerable": False,
        "crystal_timer": 3.0,
        "dash_timer": 3.0,
        "dash_state": "chase",
        "dash_direction": pygame.Vector2(),
        "dash_target": pygame.Vector2(),
        "dash_duration": 0.0
    }

    enemies.append(enemy)

def restart_game():
    global player_pos, player_health, damage_cooldown
    global game_over, victory, spawn_timer, dt, facing
    global level, enemies_defeated, total_defeated, boss_spawned

    player_pos = pygame.Vector2(400, 300)
    player_health = 5
    damage_cooldown = 0

    game_over = False
    victory = False

    dt = 0
    facing = pygame.Vector2(1, 0)

    fireballs.clear()
    enemies.clear()

    level = 1
    enemies_defeated = 0
    total_defeated = 0
    boss_spawned = False

    spawn_timer = spawn_interval
    spawn_enemy("frostling", 650, 200)

def damage_player(amount=1):
    global player_health, damage_cooldown, game_over

    if damage_cooldown > 0 or game_over or victory:
        return

    player_health = max(0, player_health - amount)
    damage_cooldown = 1.0

    print("Player HP:", player_health)

    if player_health <= 0:
        game_over = True
        print("Game Over!")

def defeat_enemy(enemy):
    global enemies_defeated, total_defeated
    global level, victory, spawn_timer

    if enemy in enemies:
        enemies.remove(enemy)

    total_defeated += 1

    if enemy["type"] == "frostking":
        victory = True
        print("YOU DEFEATED THE FROST KING!")
        return

    enemies_defeated += 1
    print("Enemies defeated:", enemies_defeated)

    if enemies_defeated >= enemies_per_level and level < 10:
        level += 1
        enemies_defeated = 0

        enemies.clear()
        fireballs.clear()
        spawn_timer = 0

        print("Level up!", level)

spawn_enemy("frostling", 650, 200)

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r and (game_over or victory):
                restart_game()

            elif event.key == pygame.K_SPACE and not game_over and not victory:
                fireballs.append([
                    player_pos.copy(),
                    facing.copy()
                ])

    if victory:
        screen.fill("midnightblue")

        win_text = font.render(
            "YOU DEFEATED THE FROST KING!",
            True,
            "cyan"
        )

        restart_text = font.render(
            "Press R to restart",
            True,
            "white"
        )

        stats_text = small_font.render(
            f"Total enemies defeated: {total_defeated}",
            True,
            "white"
        )

        screen.blit(win_text, win_text.get_rect(center=(400, 230)))
        screen.blit(restart_text, restart_text.get_rect(center=(400, 300)))
        screen.blit(stats_text, stats_text.get_rect(center=(400, 350)))

        pygame.display.flip()
        dt = clock.tick(60) / 1000
        continue

    if game_over:
        screen.fill("black")

        game_over_text = font.render(
            "GAME OVER!",
            True,
            "white"
        )

        restart_text = font.render(
            "Press R to restart",
            True,
            "white"
        )

        stats_text = small_font.render(
            f"You defeated {total_defeated} enemies",
            True,
            "white"
        )

        screen.blit(game_over_text, game_over_text.get_rect(center=(400, 230)))
        screen.blit(restart_text, restart_text.get_rect(center=(400, 300)))
        screen.blit(stats_text, stats_text.get_rect(center=(400, 350)))

        pygame.display.flip()
        dt = clock.tick(60) / 1000
        continue

    keys = pygame.key.get_pressed()

    movement = pygame.Vector2(0, 0)

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        movement.y -= 1

    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        movement.y += 1

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        movement.x -= 1

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        movement.x += 1

    if movement.length_squared() > 0:
        movement = movement.normalize()
        facing = movement.copy()
        player_pos += movement * player_speed * dt

    player_pos.x = max(23, min(777, player_pos.x))
    player_pos.y = max(23, min(577, player_pos.y))

    damage_cooldown = max(0, damage_cooldown - dt)

    spawn_timer -= dt

    if spawn_timer <= 0:

        if level == 10:

            if not boss_spawned:
                enemies.clear()
                fireballs.clear()

                spawn_enemy("frostking", 400, 100)
                boss_spawned = True

        elif len(enemies) < max_enemies:

            x = random.randint(50, 750)
            y = random.randint(50, 550)

            if level <= 3:
                enemy_type = "frostling"

            elif level <= 6:
                enemy_type = "frostfang"

            else:
                enemy_type = random.choice([
                    "frostling",
                    "frostfang"
                ])

            spawn_enemy(enemy_type, x, y)

        spawn_timer = spawn_interval

    for enemy in enemies[:]:

        enemy_type = enemy["type"]

        if enemy_type == "frostling":

            direction = player_pos - enemy["pos"]

            if direction.length_squared() > 0:
                direction = direction.normalize()
                enemy["pos"] += direction * enemy["speed"] * dt

        elif enemy_type == "frostfang":

            enemy["timer"] -= dt

            if enemy["timer"] <= 0 and not enemy["attacked"]:

                enemy["attacked"] = True
                enemy["timer"] = 0.5

                attack_rect = pygame.Rect(
                    int(enemy["pos"].x - 60),
                    int(enemy["pos"].y - 40),
                    120,
                    80
                )

                if attack_rect.collidepoint(player_pos):
                    damage_player()

            elif enemy["attacked"] and enemy["timer"] <= 0:
                enemy["vulnerable"] = True

            if enemy["vulnerable"]:

                enemy["crystal_timer"] -= dt

                if enemy["crystal_timer"] <= 0:
                    enemies.remove(enemy)
                    continue

        elif enemy_type == "frostking":

            phase_two = enemy["health"] <= 10

            chase_speed = 110 if phase_two else 70
            dash_speed = 650 if phase_two else 450
            dash_cooldown = 2.0 if phase_two else 3.0
            warning_time = 0.4 if phase_two else 0.8

            state = enemy["dash_state"]

            if state == "chase":

                direction = player_pos - enemy["pos"]

                if direction.length_squared() > 0:
                    direction = direction.normalize()
                    enemy["pos"] += direction * chase_speed * dt

                enemy["dash_timer"] -= dt

                if enemy["dash_timer"] <= 0:

                    enemy["dash_state"] = "warning"
                    enemy["dash_timer"] = warning_time

                    enemy["dash_target"] = player_pos.copy()

                    dash_direction = player_pos - enemy["pos"]

                    if dash_direction.length_squared() > 0:
                        enemy["dash_direction"] = dash_direction.normalize()
                    else:
                        enemy["dash_direction"] = pygame.Vector2(1, 0)

            elif state == "warning":

                enemy["dash_timer"] -= dt

                if enemy["dash_timer"] <= 0:

                    enemy["dash_state"] = "dashing"
                    enemy["dash_duration"] = 0.35

            elif state == "dashing":

                enemy["pos"] += (
                    enemy["dash_direction"] * dash_speed * dt
                )

                enemy["dash_duration"] -= dt

                if enemy["dash_duration"] <= 0:

                    enemy["dash_state"] = "chase"
                    enemy["dash_timer"] = dash_cooldown

            enemy["pos"].x = max(40, min(760, enemy["pos"].x))
            enemy["pos"].y = max(50, min(550, enemy["pos"].y))

    for enemy in enemies:

        if enemy["type"] == "frostling":

            if player_pos.distance_to(enemy["pos"]) < 45:
                damage_player()

        elif enemy["type"] == "frostfang":

            if enemy["vulnerable"]:

                if player_pos.distance_to(enemy["pos"]) < 43:
                    damage_player()

        elif enemy["type"] == "frostking":

            if player_pos.distance_to(enemy["pos"]) < 60:
                damage_player()

    for fireball in fireballs:
        fireball[0] += fireball[1] * fireball_speed * dt

    for fireball in fireballs[:]:

        if (
            fireball[0].x < -8 or
            fireball[0].x > 808 or
            fireball[0].y < -8 or
            fireball[0].y > 608
        ):
            fireballs.remove(fireball)

    for enemy in enemies[:]:

        for fireball in fireballs[:]:

            if enemy not in enemies:
                break

            distance = fireball[0].distance_to(enemy["pos"])

            if enemy["type"] == "frostking":
                hit_radius = 55

            elif enemy["type"] == "frostfang":
                hit_radius = 38

            else:
                hit_radius = 38

            can_hit = (
                enemy["type"] != "frostfang"
                or enemy["vulnerable"]
            )

            if distance < hit_radius and can_hit:

                fireballs.remove(fireball)
                enemy["health"] -= 1

                if enemy["health"] <= 0:
                    defeat_enemy(enemy)

                break

    screen.fill("lightsteelblue4")

    screen.blit(
        player_img,
        player_img.get_rect(center=player_pos)
    )

    for fireball in fireballs:
        pygame.draw.circle(
            screen,
            "orange",
            fireball[0],
            8
        )

    for enemy in enemies:

        pos = enemy["pos"]

        if enemy["type"] == "frostling":

            screen.blit(
                frostling_img,
                frostling_img.get_rect(center=pos)
            )

        elif enemy["type"] == "frostfang":

            warning_rect = pygame.Rect(
                int(pos.x - 60),
                int(pos.y - 40),
                120,
                80
            )

            if enemy["vulnerable"]:

                screen.blit(
                    frostfang_img,
                    frostfang_img.get_rect(center=pos)
                )

            elif enemy["attacked"]:

                pygame.draw.rect(
                    screen,
                    "cyan",
                    warning_rect
                )

            else:

                pygame.draw.rect(
                    screen,
                    "yellow",
                    warning_rect,
                    3
                )

        elif enemy["type"] == "frostking":

            screen.blit(
                boss_img,
                boss_img.get_rect(center=pos)
            )

            if enemy["health"] <= 10:

                pygame.draw.circle(
                    screen,
                    "mediumpurple",
                    (int(pos.x), int(pos.y)),
                    65,
                    3
                )

            if enemy["dash_state"] == "warning":

                target = enemy["dash_target"]

                pygame.draw.line(
                    screen,
                    "yellow",
                    pos,
                    target,
                    4
                )

    hp_text = font.render(
        f"HP: {player_health}/5",
        True,
        "white"
    )

    level_text = font.render(
        f"Level: {level}",
        True,
        "white"
    )

    screen.blit(hp_text, (20, 20))
    screen.blit(level_text, (20, 60))

    if level < 10:

        progress_text = small_font.render(
            f"Defeated: {enemies_defeated}/{enemies_per_level}",
            True,
            "white"
        )

        screen.blit(progress_text, (20, 105))

    if level == 10:

        for enemy in enemies:

            if enemy["type"] == "frostking":

                boss_text = small_font.render(
                    "FROST KING",
                    True,
                    "white"
                )

                screen.blit(
                    boss_text,
                    boss_text.get_rect(center=(400, 20))
                )

                pygame.draw.rect(
                    screen,
                    "black",
                    (250, 45, 300, 20)
                )

                bar_width = int(
                    300 * enemy["health"] / 20
                )

                bar_color = (
                    "mediumpurple"
                    if enemy["health"] <= 10
                    else "deepskyblue"
                )

                pygame.draw.rect(
                    screen,
                    bar_color,
                    (250, 45, bar_width, 20)
                )

                break

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()

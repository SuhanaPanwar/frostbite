import pygame
import random
import asyncio

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("❊ 𝔣𝔯𝔬𝔰𝔱𝔟𝔦𝔱𝔢 ❊")

running = True
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms", 30)

player_img = pygame.image.load("imgs/player.png").convert_alpha()
frostling_img = pygame.image.load("imgs/frostling.png").convert_alpha()
frostfang_img = pygame.image.load("imgs/frostfang.png").convert_alpha()
boss_img = pygame.image.load("imgs/jack frost.png").convert_alpha()

player_img = pygame.transform.smoothscale(player_img, (65, 90))
frostling_img = pygame.transform.smoothscale(frostling_img, (60, 65))
frostfang_img = pygame.transform.smoothscale(frostfang_img, (50, 65))
boss_img = pygame.transform.smoothscale(boss_img, (110, 150))

player_pos = pygame.Vector2(400, 300)

player_speed = 300
dt = 0

player_health = 5
damage_cooldown = 0
victory = False
game_over = False

fireballs = []
fireball_speed = 400
facing = pygame.Vector2(1, 0)

enemies = []
spawn_timer = 2.0
spawn_interval = 2.0
max_enemies = 3
level = 1
boss_spawned = False
enemies_defeated = 0
total_defeated = 0
enemies_per_level = 5

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

    enemy = {
        "type": enemy_type,
        "pos": pygame.Vector2(x, y),
        "speed": speed,
        "health": health,
        "timer": 1.0,
        "attacked": False,
        "vulnerable": False,
        "crystal_timer": 3.0
    }

    enemies.append(enemy)

def restart_game():
    global player_pos, player_health, damage_cooldown, game_over, spawn_timer, dt, facing, level, total_defeated, enemies_defeated, boss_spawned

    player_pos = pygame.Vector2(400, 300)
    player_health = 5
    damage_cooldown = 0
    game_over = False
    dt = 0
    facing = pygame.Vector2(1,0)

    fireballs.clear()
    enemies.clear()

    spawn_timer = spawn_interval
    spawn_enemy("frostling", 650, 200)

    level = 1
    enemies_defeated = 0
    total_defeated = 0

spawn_enemy("frostling", 650, 200)

if victory:
    screen.fill("midnightblue")

    win_text = font.render("YOU DEFEATED THE FROST KING!", True, "cyan")
    screen.blit(win_text, (95, 250))

    restart_text = font.render("Press R to restart", True, "white")
    screen.blit(restart_text, (240, 310))

    pygame.display.flip()
    clock.tick(60)
    continue

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE and not game_over:
                fireballs.append([player_pos.copy(), facing.copy()])

            if event.key == pygame.K_r and (game_over or victory):
                restart_game()
                boss_spawned = False

    if game_over:
        screen.fill("black")
        game_over_text = font.render("Game Over!", True, "white")
        restart_text = font.render("Press [r] to restart", True, "white") 
        stats_text = font.render(f"You defeated: {total_defeated} enemies", True, "white")
        screen.blit(game_over_text, (310, 250))
        screen.blit(restart_text, (240, 300))
        screen.blit(stats_text, (220, 200))
        pygame.display.flip()
        clock.tick(60)
        continue

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_pos.y -= player_speed * dt
        facing = pygame.Vector2(0, -1)
    
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_pos.y += player_speed * dt
        facing = pygame.Vector2(0, 1)

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_pos.x -= player_speed * dt
        facing = pygame.Vector2(-1, 0)

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_pos.x += player_speed * dt
        facing = pygame.Vector2(1, 0)

    if player_pos.x < 23:
        player_pos.x = 23

    if player_pos.x > 777:
         player_pos.x = 777

    if player_pos.y < 23:
         player_pos.y = 23

    if player_pos.y > 577:
         player_pos.y = 577  

    spawn_timer -= dt

    if spawn_timer <= 0:

        if level == 10 and not boss_spawned:
            enemies.clear()
            spawn_enemy("frostking", 400, 100)
            boss_spawned = True

        elif level < 10 and len(enemies) < max_enemies:
            x = random.randint(50, 750)
            y = random.randint(50, 550)

            if level <= 3:
                enemy_type = "frostling"

            elif level <= 6:
                enemy_type = "frostfang"

            elif level <= 9:
                enemy_type = random.choice(["frostling", "frostfang"])

            else:
                enemy_type = "frostking"

            spawn_enemy(enemy_type, x, y)

            if enemy_type == "frostking":
                boss_spawned = True

        spawn_timer = spawn_interval

    for enemy in enemies:
        direction = player_pos - enemy["pos"]

        if direction.length() > 0:
            direction = direction.normalize()
            enemy["pos"] += direction * enemy["speed"] * dt

    for enemy in enemies:
        if enemy["type"] == "frostfang":

            enemy["timer"] -= dt

            if enemy["timer"] <= 0 and not enemy["attacked"]:
                enemy["attacked"] = True
                enemy["timer"] = 0.5

                attack_rect = pygame.Rect(
                    enemy["pos"].x - 60,
                    enemy["pos"].y - 40,
                    120,
                    80
                )

                if attack_rect.collidepoint(player_pos):
                    player_health = max(0, player_health - 1)
                    print("Frost Fang hit! HP:", player_health)

                    if player_health == 0:
                        game_over = True

            elif enemy["attacked"] and enemy["timer"] <= 0:
                enemy["vulnerable"] = True

    for enemy in enemies[:]:

        if enemy["type"] == "frostfang" and enemy["vulnerable"]:
            enemy["crystal_timer"] -= dt

            if enemy["crystal_timer"] <= 0:
                enemies.remove(enemy)

    damage_cooldown -= dt

    for enemy in enemies:
        if ((enemy["type"] != "frostfang" and player_pos.distance_to(enemy["pos"]) < 45) or (enemy["type"] == "frostfang" and enemy["vulnerable"] and player_pos.distance_to(enemy["pos"]) < 43)):
            if damage_cooldown <= 0:
                player_health -= 1
                damage_cooldown = 1.0
                print("Player HP:", player_health)

            if player_health <= 0 and not game_over:
                player_health = 0
                print("Game Over!")
                game_over = True

    for fireball in fireballs:
        fireball[0] += fireball[1] *fireball_speed * dt

    for fireball in fireballs[:]:
        if (fireball[0].x < -8 or fireball[0].x > 808 or
            fireball[0].y < -8 or fireball[0].y > 608):
            fireballs.remove(fireball)

    for enemy in enemies[:]:

        for fireball in fireballs[:]:
            if (fireball[0].distance_to(enemy["pos"]) < 38 and (enemy["type"] != "frostfang" or enemy["vulnerable"])):
                fireballs.remove(fireball)
                enemy["health"] -= 1

                if enemy["health"] <= 0:
                    enemies.remove(enemy)

                if enemy["type"] == "frostking":
                    victory = True

                    enemies_defeated += 1
                    total_defeated += 1
                    print("Enemy destroyed!")
                    print("Enemies defeated: ", enemies_defeated)

                    if enemies_defeated >= enemies_per_level and level < 10:
                        level += 1
                        enemies_defeated = 0
                        print("Level up!", level)

                break

    screen.fill("lightsteelblue4")

    hp_text = font.render(f"HP: {player_health}/5", True, "white")
    screen.blit(hp_text, (20,20))

    level_text = font.render(f"Level: {level}", True, "white")
    screen.blit(level_text, (20, 60))

    screen.blit(player_img, player_img.get_rect(center=player_pos))

    for fireball in fireballs:
        pygame.draw.circle(screen, "orange", fireball[0], 8)

    for enemy in enemies:
        pos = enemy["pos"]

        if enemy["type"] == "frostling":
            screen.blit(frostling_img, frostling_img.get_rect(center=pos))

        elif enemy["type"] == "frostfang":
            warning_rect = pygame.Rect(
                int(pos.x - 60),
                int(pos.y - 40),
                120,
                80
            )

            if enemy["vulnerable"]:
                screen.blit(frostfang_img, frostfang_img.get_rect(center=pos))

            elif enemy["attacked"]:
                pygame.draw.rect(screen, "cyan", warning_rect)

            else:
                pygame.draw.rect(screen, "yellow", warning_rect, 3)

        elif enemy["type"] == "frostking":
            screen.blit(boss_img, boss_img.get_rect(center=pos))

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
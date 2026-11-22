import pygame
import random

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("❊ 𝔣𝔯𝔬𝔰𝔱𝔟𝔦𝔱𝔢 ❊")

running = True
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms", 30)

player_pos = pygame.Vector2(400, 300)

player_speed = 300
dt = 0

player_health = 5
damage_cooldown = 0
game_over = False

fireballs = []
fireball_speed = 400
facing = pygame.Vector2(1, 0)

enemies = []
spawn_timer = 2.0
spawn_interval = 2.0
max_enemies = 3

def spawn_enemy(enemy_type, x, y):

    enemy = {
        "type": enemy_type,
        "pos": pygame.Vector2(x, y),
        "speed": 175,
        "health": 1
    }

    enemies.append(enemy)

def restart_game():
    global player_pos, player_health, damage_cooldown, game_over, spawn_timer, dt, facing

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

spawn_enemy("frostling", 650, 200)

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE and not game_over:
                fireballs.append([player_pos.copy(), facing.copy()])

            if event.key == pygame.K_r and game_over:
                restart_game()

    if game_over:
        screen.fill("black")
        game_over_text = font.render("Game Over!", True, "white")
        restart_text = font.render("Press [r] to restart", True, "white") 
        screen.blit(game_over_text, (310, 250))
        screen.blit(restart_text, (240, 300))
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

        if len(enemies) < max_enemies:
            x = random.randint(50, 750)
            y = random.randint(50, 550)

            spawn_enemy("frostling", x, y)

        spawn_timer = spawn_interval

    for enemy in enemies:
        direction = player_pos - enemy["pos"]

        if direction.length() > 0:
            direction = direction.normalize()
            enemy["pos"] += direction * enemy["speed"] * dt

    damage_cooldown -= dt

    for enemy in enemies:
        if player_pos.distance_to(enemy["pos"]) < 45:
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
            if fireball[0].distance_to(enemy["pos"]) < 38:
                fireballs.remove(fireball)
                enemy["health"] -= 1

                if enemy["health"] <= 0:
                    enemies.remove(enemy)
                    print("Enemy destroyed!")

                break

    screen.fill("lightsteelblue4")

    hp_text = font.render(f"HP: {player_health}/5", True, "white")
    screen.blit(hp_text, (20,20))

    pygame.draw.circle(screen, "lightsalmon4", player_pos, 23)

    for fireball in fireballs:
        pygame.draw.circle(screen, "orange", fireball[0], 8)

    for enemy in enemies:
        pos = enemy["pos"]

        pygame.draw.polygon(screen, "lightskyblue", [
            (pos.x - 25, pos.y),
            (pos.x + 15, pos.y - 15),
            (pos.x + 15, pos.y + 15)
        ])

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
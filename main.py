import pygame
import random

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("❊ 𝔣𝔯𝔬𝔰𝔱𝔟𝔦𝔱𝔢 ❊")

running = True
clock = pygame.time.Clock()

player_pos = pygame.Vector2(400, 300)

player_speed = 300
dt = 0

fireballs = []
fireball_speed = 400
facing = pygame.Vector2(1, 0)

ice_pos = pygame.Vector2(650, 200)
ice_speed = 180
ice_alive = True
ice_respawn_timer = 0

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                fireballs.append([player_pos.copy(), facing.copy()])

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

    if ice_alive:
        ice_direction = player_pos - ice_pos

        if ice_direction.length() > 0:
            ice_direction = ice_direction.normalize()
            ice_pos += ice_direction * ice_speed * dt

    for fireball in fireballs:
        fireball[0] += fireball[1] *fireball_speed * dt

    for fireball in fireballs[:]:
        if (fireball[0].x < -8 or fireball[0].x > 808 or
            fireball[0].y < -8 or fireball[0].y > 608):
            fireballs.remove(fireball)

    if ice_alive:
        for fireball in fireballs[:]:
            if fireball[0].distance_to(ice_pos) < 38:
                fireballs.remove(fireball)
                ice_alive = False
                ice_respawn_timer = 1.0
                print("Ice shard destroyed!")
                break

    if not ice_alive:
        ice_respawn_timer -= dt

        if ice_respawn_timer <= 0:
            ice_pos = pygame.Vector2(
            random.randint(50, 750),
            random.randint(50, 550)
            )

            ice_alive = True

    screen.fill("lightsteelblue4")
    pygame.draw.circle(screen, "lightsalmon4", player_pos, 23)

    for fireball in fireballs:
        pygame.draw.circle(screen, "orange", fireball[0], 8)

    if ice_alive:
        pygame.draw.polygon(screen, "lightskyblue", [
            (ice_pos.x - 25, ice_pos.y),
            (ice_pos.x + 15, ice_pos.y - 15),
            (ice_pos.x + 15, ice_pos.y + 15)
    ])

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
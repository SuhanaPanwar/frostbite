import pygame

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

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                fireballs.append([player_pos(), facing.copy()])
    
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

    for fireball in fireballs:
        fireball.x += fireball_speed * dt

    screen.fill("lightsteelblue4")
    pygame.draw.circle(screen, "lightsalmon4", player_pos, 23)

    for fireball in fireballs:
        pygame.draw.circle(screen, "orange", fireball, 8)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
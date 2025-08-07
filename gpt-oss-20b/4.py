# напиши программу на Python, которая показывает мяч, подпрыгивающий внутри вращающегося  шестиугольника. На мяч должны влиять гравитация и трение, и он должен реалистично отскакивать от вращающихся стен


import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
CENTER = (WIDTH // 2, HEIGHT // 2)
FPS = 60

g = 0.5  # гравитация
friction = 0.999  # воздушное трение
restitution = 0.9  # упругость

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# шар
ball_radius = 15
ball_pos = pygame.Vector2(CENTER[0], CENTER[1] - 100)
ball_vel = pygame.Vector2(2, 0)

# шестиугольник
hex_radius = 250
angle = 0

# расчёт вершин в полярных координатах
def get_hexagon_vertices(center, radius, angle_deg):
    verts = []
    for i in range(6):
        theta = math.radians(angle_deg + i * 60)
        x = center[0] + radius * math.cos(theta)
        y = center[1] + radius * math.sin(theta)
        verts.append(pygame.Vector2(x, y))
    return verts

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))

    angle += 1  # скорость вращения
    verts = get_hexagon_vertices(CENTER, hex_radius, angle)

    # отрисовка шестиугольника
    pygame.draw.polygon(screen, (255, 255, 255), [(v.x, v.y) for v in verts], 2)

    # физика
    ball_vel.y += g
    ball_vel *= friction
    ball_pos += ball_vel

    # столкновение с гранями
    for i in range(6):
        a = verts[i]
        b = verts[(i + 1) % 6]
        edge = b - a
        normal = pygame.Vector2(-edge.y, edge.x).normalize()
        # расстояние от центра шара до грани
        dist = (ball_pos - a).dot(normal)
        if dist < ball_radius:
            # если шар движется внутрь стены
            if ball_vel.dot(normal) < 0:
                ball_pos += normal * (ball_radius - dist)
                # отражение
                ball_vel = ball_vel - 2 * ball_vel.dot(normal) * normal * restitution
                # трение вдоль грани
                tangent = pygame.Vector2(normal.y, -normal.x)
                ball_vel -= tangent * (1 - restitution) * ball_vel.dot(tangent)

    # отрисовка шара
    pygame.draw.circle(screen, (255, 0, 0), (int(ball_pos.x), int(ball_pos.y)), ball_radius)

    pygame.display.flip()
    clock.tick(FPS)

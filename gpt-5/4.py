# напиши программу на Python, которая показывает мяч, подпрыгивающий внутри вращающегося  шестиугольника. На мяч должны влиять гравитация и трение, и он должен реалистично отскакивать от вращающихся стен


import math
import pygame
from pygame.math import Vector2

# ---------------- ПАРАМЕТРЫ ----------------
WIDTH, HEIGHT = 800, 800
CENTER = Vector2(WIDTH / 2, HEIGHT / 2)

HEX_RADIUS = 300.0             # радиус (до вершин) шестиугольника
HEX_OMEGA = 0.6                # угловая скорость шестиугольника (рад/с), + против часовой
REST_COEFF = 0.82              # коэффициент реституции (упругости)
FRICTION_COEFF = 0.28          # коэффициент трения (Кулона) в касании
GRAVITY = Vector2(0, 1200.0)   # гравитация (px/s^2)
SLOP = 0.5                     # "люфт" при коррекции проникновения (px)
POS_CORR_FACTOR = 1.0          # коэффициент "выдавливания" при пересечении
BALL_RADIUS = 14.0
BALL_MASS = 1.0

PHYS_DT = 1.0 / 240.0          # фиксированный шаг физики
FPS_CAP = 120                  # ограничение кадров отрисовки

# -------------- ВСПОМОГАТЕЛЬНОЕ --------------
def clamp(x, a, b):
    return max(a, min(b, x))

def rotate_point(p: Vector2, angle: float) -> Vector2:
    ca = math.cos(angle)
    sa = math.sin(angle)
    return Vector2(ca * p.x - sa * p.y, sa * p.x + ca * p.y)

def regular_hex_vertices(center: Vector2, radius: float, angle: float):
    # шестиугольник с "острым" верхом (pointy), можно сдвинуть фазу по желанию
    verts = []
    for i in range(6):
        a = angle + i * (2 * math.pi / 6.0)
        verts.append(center + Vector2(math.cos(a), math.sin(a)) * radius)
    return verts

def closest_point_on_segment(c: Vector2, a: Vector2, b: Vector2):
    ab = b - a
    ab_len2 = ab.length_squared()
    if ab_len2 == 0.0:
        return a, 0.0
    t = (c - a).dot(ab) / ab_len2
    t = clamp(t, 0.0, 1.0)
    p = a + ab * t
    return p, t

def wall_point_velocity_at(p_world: Vector2, center: Vector2, omega: float) -> Vector2:
    # скорость точки стенки из-за вращения ω: v = ω × r (в 2D: (-ω*y, ω*x))
    r = p_world - center
    return Vector2(-omega * r.y, omega * r.x)

# -------------- ОСНОВНАЯ ЛОГИКА СТОЛКНОВЕНИЙ --------------
def solve_collisions(ball_pos: Vector2, ball_vel: Vector2, radius: float, mass: float,
                     hex_center: Vector2, verts, omega: float):
    # Перебор всех 6 рёбер (как отрезков)
    for i in range(6):
        a = verts[i]
        b = verts[(i + 1) % 6]

        # Ближайшая точка на ребре к центру мяча
        p, _ = closest_point_on_segment(ball_pos, a, b)
        n = ball_pos - p
        dist = n.length()

        # Проникновение круга в стенку
        penetration = radius - dist
        if penetration > 0.0:
            # Нормаль от точки касания к центру мяча (направление "выдавливания")
            if dist > 1e-8:
                n_hat = n / dist
            else:
                # редкий случай: центр упал точно на точку/вершину
                # ориентируем нормаль от центра шестиугольника к мячу
                vtmp = (ball_pos - hex_center)
                if vtmp.length_squared() < 1e-12:
                    n_hat = Vector2(0, -1)  # что-нибудь стабильноe
                else:
                    n_hat = vtmp.normalize()

            # Коррекция позиции (выдавливаем мяч из стенки)
            correction = n_hat * (penetration + SLOP) * POS_CORR_FACTOR
            ball_pos += correction

            # Скорость точки стенки (она движется из-за вращения)
            v_wall = wall_point_velocity_at(p, hex_center, omega)

            # Относительная скорость в точке контакта
            v_rel = ball_vel - v_wall

            # Нормальная составляющая
            vn = v_rel.dot(n_hat)

            # Упругое отражение (импульс по нормали) — только если движемся "в стенку"
            if vn < 0.0:
                jn = -(1.0 + REST_COEFF) * vn * mass
                ball_vel += (jn / mass) * n_hat

            # Трение (по касательной) — действует пока есть контакт
            # Направление касательной
            tangent = v_rel - vn * n_hat
            vt = tangent.length()
            if vt > 1e-6:
                t_hat = tangent / vt
                # Импульс трения, ограниченный конусом трения (Кулон)
                jt_free = -vt * mass                  # "затянуть" скольжение до нуля
                max_jt = FRICTION_COEFF * abs((-(1.0 + REST_COEFF) * vn * mass) if vn < 0 else mass * 0.0 + mass * 0.0)
                # Небольшой трюк: если нормального импульса не было (vn>=0), ограничим трение мягче:
                if vn >= 0:
                    max_jt = FRICTION_COEFF * mass * 50.0  # слабое трение при "проскальзывании" в контакте
                jt = clamp(jt_free, -max_jt, max_jt)
                ball_vel += (jt / mass) * t_hat

    return ball_pos, ball_vel

# -------------- ВИЗУАЛИЗАЦИЯ И ЦИКЛ --------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Мяч в вращающемся шестиугольнике (гравитация + трение)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 16)

    # Состояние
    ball_pos = CENTER + Vector2(0, -HEX_RADIUS * 0.5)
    ball_vel = Vector2(220.0, 0.0)

    angle = 0.0    # текущий угол шестиугольника
    omega = HEX_OMEGA

    accumulator = 0.0
    running = True

    while running:
        # Обработка событий
        dt_frame = clock.tick(FPS_CAP) / 1000.0
        accumulator += dt_frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                # Небольшое управление скоростью вращения
                elif event.key == pygame.K_LEFT:
                    omega -= 0.2
                elif event.key == pygame.K_RIGHT:
                    omega += 0.2
                elif event.key == pygame.K_SPACE:
                    ball_pos = CENTER + Vector2(0, -HEX_RADIUS * 0.5)
                    ball_vel = Vector2(220.0, 0.0)

        # Фиксированные шаги физики
        substeps = 0
        while accumulator >= PHYS_DT:
            substeps += 1
            accumulator -= PHYS_DT

            # Обновляем угол
            angle += omega * PHYS_DT

            # Интеграция (Semi-implicit Euler)
            ball_vel += GRAVITY * PHYS_DT
            ball_pos += ball_vel * PHYS_DT

            # Геометрия шестиугольника в текущий момент
            verts = regular_hex_vertices(CENTER, HEX_RADIUS, angle)

            # Столкновения с вращающимися стенками (с учетом их скорости)
            ball_pos, ball_vel = solve_collisions(
                ball_pos, ball_vel, BALL_RADIUS, BALL_MASS, CENTER, verts, omega
            )

            # На всякий случай мягко удерживаем в окне (если вдруг вылетит численно)
            if not (-1000 < ball_pos.x < WIDTH + 1000) or not (-1000 < ball_pos.y < HEIGHT + 1000):
                ball_pos = CENTER
                ball_vel = Vector2(0, 0)

            # Брейк на случай "спайка" времени
            if substeps > 600:
                accumulator = 0.0
                break

        # Рендер
        screen.fill((18, 18, 22))
        verts_draw = regular_hex_vertices(CENTER, HEX_RADIUS, angle)
        pygame.draw.polygon(screen, (60, 140, 210), [(v.x, v.y) for v in verts_draw], width=4)

        pygame.draw.circle(screen, (240, 95, 80), (ball_pos.x, ball_pos.y), BALL_RADIUS)

        # UI-подсказки
        info1 = f"omega = {omega:.2f} rad/s   e = {REST_COEFF:.2f}   mu = {FRICTION_COEFF:.2f}"
        info2 = "LEFT/RIGHT — изменить вращение, SPACE — сбросить мяч, ESC — выход"
        text1 = font.render(info1, True, (210, 210, 210))
        text2 = font.render(info2, True, (150, 150, 150))
        screen.blit(text1, (10, 10))
        screen.blit(text2, (10, 32))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
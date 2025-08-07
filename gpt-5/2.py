# напиши программу на Python, которая показывает мяч, подпрыгивающий внутри вращающегося  шестиугольника. На мяч должны влиять гравитация и трение, и он должен реалистично отскакивать от вращающихся стен

import math
import sys
import pygame as pg
from pygame.math import Vector2 as Vec

# ----------------- Параметры сцены -----------------
W, H = 900, 900
CENTER = Vec(W / 2, H / 2)
R_POLY = 320          # радиус описанной окружности шестиугольника
SIDES = 6             # число сторон (шестиугольник)

# ----------------- Параметры физики ----------------
g = 1400.0            # гравитация (пикс/с^2), вниз по экрану
air_drag = 0.35       # коэффициент «воздушного» трения (1/с), экспоненциальное затухание
restitution = 0.86    # коэффициент реституции (упругость отскока)
friction_mu = 0.28    # коэффициент трения при ударе (Кулона)
omega = 0.85          # угловая скорость вращения полигона (рад/с), + — против часовой (геометрически)

# ----------------- Параметры мяча ------------------
ball_r = 16.0
ball_pos = CENTER + Vec(0, -R_POLY * 0.55)  # старт внутри полигона
ball_vel = Vec(240.0, 0.0)                  # начальная скорость

# Рендер
BG = (15, 18, 22)
WALL = (70, 110, 150)
BALL = (230, 95, 95)
TEXT = (210, 210, 210)

def perp(v: Vec) -> Vec:
    # Перпендикуляр (для 2D: z-вектор единичный), v_perp = omega x r
    return Vec(-v.y, v.x)

def regular_polygon(center: Vec, radius: float, n: int, angle: float):
    # Вершины правильного n-угольника с углом поворота angle
    verts = []
    for i in range(n):
        a = angle + 2.0 * math.pi * i / n
        verts.append(center + Vec(math.cos(a), math.sin(a)) * radius)
    return verts

def resolve_circle_vs_segment(pos: Vec, vel: Vec, radius: float,
                              a: Vec, b: Vec, center: Vec, omega: float,
                              restitution: float, mu: float):
    """
    Разрешает столкновение окружности с отрезком a-b.
    Учитывает скорость точки стены из-за вращения полигона вокруг center.
    Возвращает (pos, vel, collided: bool)
    """
    e = b - a
    len2 = e.length_squared()
    if len2 == 0.0:
        return pos, vel, False

    # Ближайшая точка q на отрезке к центру шара
    t = (pos - a).dot(e) / len2
    t = max(0.0, min(1.0, t))
    q = a + e * t

    delta = pos - q
    dist = delta.length()

    if dist >= radius:
        return pos, vel, False

    # Нормаль в точке контакта (от стены к шару)
    if dist > 1e-8:
        n = delta / dist
    else:
        # редкий вырожденный случай — ориентируем нормаль от ближайшего края к центру шара
        n = (pos - center)
        if n.length_squared() == 0:
            n = Vec(0, -1)
        else:
            n = n.normalize()

    # Скорость точки стены (т.к. стена — часть вращающегося жёсткого тела)
    r = q - center
    v_wall = perp(r) * omega

    # Относительная скорость в точке контакта
    v_rel = vel - v_wall
    v_rel_n = v_rel.dot(n)

    if v_rel_n < 0.0:
        # Импульс по нормали (стенка бесконечно тяжёлая)
        Jn = -(1.0 + restitution) * v_rel_n
        vel += Jn * n

        # Трение (Кулона) по касательной
        vt_vec = v_rel - v_rel_n * n
        vt = vt_vec.length()
        if vt > 1e-6:
            t_hat = vt_vec / vt
            # Нужный импульс, чтобы погасить vt: Jt_need = vt (масса=1)
            # Ограничиваем Jt <= mu * Jn (Кулон)
            Jt = min(mu * Jn, vt)
            vel -= Jt * t_hat

    # Исправление проникновения (positional correction)
    penetration = radius - dist
    pos += n * (penetration + 0.001)

    return pos, vel, True

def main():
    pg.init()
    screen = pg.display.set_mode((W, H))
    pg.display.set_caption("Bouncing ball in rotating hexagon (gravity + friction)")
    clock = pg.time.Clock()
    font = pg.font.SysFont("consolas", 18)

    theta = 0.0
    pos = ball_pos.copy()
    vel = ball_vel.copy()

    running = True
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    running = False
                # Немного управления параметрами на лету
                elif e.key == pg.K_LEFT:
                    # медленнее вращение
                    globals()['omega'] -= 0.1
                elif e.key == pg.K_RIGHT:
                    # быстрее вращение
                    globals()['omega'] += 0.1
                elif e.key == pg.K_UP:
                    globals()['restitution'] = min(0.98, globals()['restitution'] + 0.02)
                elif e.key == pg.K_DOWN:
                    globals()['restitution'] = max(0.0, globals()['restitution'] - 0.02)
                elif e.key == pg.K_1:
                    globals()['friction_mu'] = max(0.0, globals()['friction_mu'] - 0.02)
                elif e.key == pg.K_2:
                    globals()['friction_mu'] = min(1.0, globals()['friction_mu'] + 0.02)

        # Шаг времени
        dt = clock.tick(120) / 1000.0
        dt = min(dt, 1/60)  # ограничим скачки dt
        substeps = 2        # для устойчивости при быстрых столкновениях
        sdt = dt / substeps

        for _ in range(substeps):
            # Обновляем поворот полигона
            theta += omega * sdt

            # Интеграция (semi-implicit Euler)
            vel.y += g * sdt

            # Воздушное трение как экспоненциальное затухание
            if air_drag > 0.0:
                damp = math.exp(-air_drag * sdt)
                vel *= damp

            pos += vel * sdt

            # Текущие вершины шестиугольника
            verts = regular_polygon(CENTER, R_POLY, SIDES, theta)

            # Столкновения с каждой гранью
            collided_any = False
            for i in range(SIDES):
                a = verts[i]
                b = verts[(i + 1) % SIDES]
                pos, vel, collided = resolve_circle_vs_segment(
                    pos, vel, ball_r, a, b, CENTER, omega, restitution, friction_mu
                )
                collided_any = collided_any or collided

            # Подстраховка: если вдруг улетели наружу (крайне редко), направим внутрь
            if not collided_any:
                # Проверим минимальную дистанцию до сторон
                min_dist = float("inf")
                push_n = None
                push_q = None
                for i in range(SIDES):
                    a = verts[i]
                    b = verts[(i + 1) % SIDES]
                    e = b - a
                    len2 = e.length_squared()
                    if len2 == 0.0:
                        continue
                    t = (pos - a).dot(e) / len2
                    t = max(0.0, min(1.0, t))
                    q = a + e * t
                    d = (pos - q).length()
                    if d < min_dist:
                        min_dist = d
                        push_q = q
                if push_q is not None and min_dist < ball_r * 0.7:
                    n = (pos - push_q)
                    if n.length_squared() > 1e-8:
                        n = n.normalize()
                        pos += n * (ball_r - min_dist + 0.001)

        # Рендер
        screen.fill(BG)
        verts = regular_polygon(CENTER, R_POLY, SIDES, theta)
        pg.draw.polygon(screen, WALL, verts, width=5)
        pg.draw.circle(screen, BALL, (int(pos.x), int(pos.y)), int(ball_r))

        # Инфо
        info1 = f"omega: {omega:+.2f} rad/s   g: {g:.0f}   e(restitution): {restitution:.2f}   mu: {friction_mu:.2f}"
        info2 = "Controls: LEFT/RIGHT = omega, UP/DOWN = restitution, 1/2 = friction mu, ESC = quit"
        surf1 = font.render(info1, True, TEXT)
        surf2 = font.render(info2, True, TEXT)
        screen.blit(surf1, (12, 12))
        screen.blit(surf2, (12, 36))

        pg.display.flip()

    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main()
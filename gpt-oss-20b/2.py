# Напиши  симуляцию: жёлтый шар движется внутри вращающейся фигуры. Учитывай физику движения (гравитация, трение, упругие/неупругие столкновения), предотвратить выход шара за пределы. Ввод — параметры: форма (кол‑во сторон, радиус), скорость вращения, начальная позиция и скорость шара. Вывод — анимация. Код — в одном файле, минимум зависимостей. Упор на точность физики и устойчивость 

import sys
import math
import argparse
import time
try:
    import tkinter as tk
except ImportError:
    print("tkinter is required. On Linux: sudo apt-get install python3-tk")
    sys.exit(1)

def parse_args():
    p = argparse.ArgumentParser(description='Simulate a ball in a rotating polygon container')
    p.add_argument('--sides', type=int, default=6, help='Number of sides of the polygon')
    p.add_argument('--radius', type=float, default=200, help='Radius of the circumscribed circle')
    p.add_argument('--omega', type=float, default=0.5, help='Angular speed (rad/s)')
    p.add_argument('--x0', type=float, default=0, help='Initial x position relative to center')
    p.add_argument('--y0', type=float, default=-100, help='Initial y position relative to center')
    p.add_argument('--vx0', type=float, default=100, help='Initial x velocity')
    p.add_argument('--vy0', type=float, default=0, help='Initial y velocity')
    return p.parse_args()

class Ball:
    def __init__(self, x, y, vx, vy, r=10, mass=1.0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self.mass = mass
        self.restitution = 0.9  # coefficient of restitution
        self.friction = 0.01    # air friction coefficient

    def update(self, dt, g=500):
        self.vy += g * dt
        # linear drag
        self.vx *= (1 - self.friction * dt)
        self.vy *= (1 - self.friction * dt)
        self.x += self.vx * dt
        self.y += self.vy * dt

class RotatingPolygon:
    def __init__(self, sides, radius, omega, cx, cy):
        self.sides = sides
        self.radius = radius
        self.omega = omega
        self.cx = cx
        self.cy = cy
        self.angle = 0.0

    def vertices(self):
        verts = []
        for i in range(self.sides):
            theta = self.angle + 2 * math.pi * i / self.sides
            x = self.cx + self.radius * math.cos(theta)
            y = self.cy + self.radius * math.sin(theta)
            verts.append((x, y))
        return verts

    def update(self, dt):
        self.angle += self.omega * dt

    def collide_ball(self, ball):
        verts = self.vertices()
        n = len(verts)
        for i in range(n):
            x1, y1 = verts[i]
            x2, y2 = verts[(i + 1) % n]
            # edge vector
            ex, ey = x2 - x1, y2 - y1
            # normal (outward) = rotate edge by 90deg
            nx, ny = ey, -ex
            # normalize
            dist = math.hypot(nx, ny)
            if dist == 0: continue
            nx /= dist; ny /= dist
            # point to ball
            dx, dy = ball.x - x1, ball.y - y1
            # signed distance
            d = dx * nx + dy * ny
            if d < ball.r:
                # projection onto edge
                proj = dx * ex + dy * ey
                if 0 <= proj <= ex * ex + ey * ey:
                    # collision
                    # move out
                    overlap = ball.r - d
                    ball.x += nx * overlap
                    ball.y += ny * overlap
                    # reflect velocity
                    vdotn = ball.vx * nx + ball.vy * ny
                    ball.vx -= (1 + ball.restitution) * vdotn * nx
                    ball.vy -= (1 + ball.restitution) * vdotn * ny

class Simulation:
    def __init__(self, args):
        self.args = args
        self.width = int(2 * (args.radius + 50))
        self.height = int(2 * (args.radius + 50))
        self.root = tk.Tk()
        self.root.title("Rotating Polygon Simulation")
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg='white')
        self.canvas.pack()
        cx, cy = self.width / 2, self.height / 2
        self.poly = RotatingPolygon(args.sides, args.radius, args.omega, cx, cy)
        self.ball = Ball(cx + args.x0, cy + args.y0, args.vx0, args.vy0)
        self.poly_id = None
        self.ball_id = None
        self.last_time = time.time()
        self.dt = 1/60

    def draw(self):
        verts = self.poly.vertices()
        coords = []
        for x, y in verts:
            coords.extend([x, y])
        if self.poly_id:
            self.canvas.coords(self.poly_id, *coords)
        else:
            self.poly_id = self.canvas.create_polygon(*coords, outline='black', fill='', width=2)
        x, y, r = self.ball.x, self.ball.y, self.ball.r
        if self.ball_id:
            self.canvas.coords(self.ball_id, x-r, y-r, x+r, y+r)
        else:
            self.ball_id = self.canvas.create_oval(x-r, y-r, x+r, y+r, fill='yellow', outline='')

    def step(self):
        now = time.time()
        dt = self.dt
        self.poly.update(dt)
        self.ball.update(dt)
        self.poly.collide_ball(self.ball)
        self.draw()
        self.root.after(int(dt*1000), self.step)

    def run(self):
        self.step()
        self.root.mainloop()

if __name__ == '__main__':
    args = parse_args()
    sim = Simulation(args)
    sim.run()

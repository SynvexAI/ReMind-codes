import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Параметры симуляции
num_bodies = 50
G = 1.0  # Гравитационная постоянная
dt = 0.01 # Шаг времени
iterations = 500

# Начальные условия
np.random.seed(42)  # Для воспроизводимости
positions = np.random.rand(num_bodies, 2) * 2 - 1  # Случайные позиции от -1 до 1
velocities = np.random.rand(num_bodies, 2) * 0.1 - 0.05 # Случайные скорости
masses = np.random.rand(num_bodies) * 5 + 1 # Случайные массы от 1 до 6

# Функция для вычисления сил гравитации
def calculate_forces(positions, masses):
    num_bodies = len(positions)
    forces = np.zeros_like(positions)
    for i in range(num_bodies):
        for j in range(i + 1, num_bodies):
            r = positions[j] - positions[i]
            distance = np.linalg.norm(r)
            force_magnitude = G * masses[i] * masses[j] / (distance**2 + 0.1)  # Добавлено 0.1 для предотвращения деления на ноль
            force = force_magnitude * (r / distance)
            forces[i] += force
            forces[j] -= force
    return forces

# Функция для обновления позиций и скоростей
def update(frame):
    global positions, velocities

    forces = calculate_forces(positions, masses)

    # Обновление скоростей и позиций (численное интегрирование)
    velocities += (forces / masses[:, np.newaxis]) * dt
    positions += velocities * dt

    # Ограничение мира (тела отталкиваются от стенок)
    positions[positions > 1] = 1
    positions[positions < -1] = -1
    velocities[positions > 0.99] *= -0.5
    velocities[positions < -0.99] *= -0.5

    # Обновление точек на графике
    scatter.set_offsets(positions)
    return scatter,


# Настройка графика
fig, ax = plt.subplots()
ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-1.1, 1.1)
ax.set_aspect(equal)
scatter = ax.scatter(positions[:, 0], positions[:, 1], s=masses*10, color=blue) # Размер точек зависит от массы
ax.set_facecolor("black") # Черный фон
fig.patch.set_facecolor(black) # Черный фон для всего окна
ax.tick_params(axis=x, colors=white)
ax.tick_params(axis=y, colors=white)
ax.spines[bottom].set_color(white)
ax.spines[top].set_color(white)
ax.spines[left].set_color(white)
ax.spines[right].set_color(white)
ax.set_title("N-body Simulation", color=white)

# Создание анимации
ani = animation.FuncAnimation(fig, update, blit=True, frames=iterations, repeat=True)

# Сохранение анимации (опционально, требует установленного ffmpeg или imagemagick)
# ani.save("n_body_simulation.gif", writer=imagemagick, fps=60)

plt.show()

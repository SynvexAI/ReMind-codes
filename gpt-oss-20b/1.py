#Напиши код для гинерации лабиринта


import random
from typing import List, Tuple

# ────────────────────────  МОДУЛЬ ГЕНЕРАЦИИ ЛАБИРИНТА  ──────────────────────── #

def generate_maze(width: int, height: int) -> List[List[int]]:
    """
    Создаёт лабиринт размерами width × height.
    Размеры должны быть нечетными (чтобы вокруг была «оболочка» стен).
    Возвращает двумерный список списков:
        0 – проход
        1 – стена
    """
    # --- Проверка входных параметров ---------------------------------------
    if width < 3 or height < 3:
        raise ValueError("Размеры лабиринта должны быть >= 3")
    if width % 2 == 0:   # делаем нечётным, чтобы вокруг был бортик стен
        width += 1
    if height % 2 == 0:
        height += 1

    # --- Инициализация поля стенами -----------------------------------------
    maze = [[1] * width for _ in range(height)]

    # --- Стартовая точка (должна быть в нечётном индексе) -------------------
    start_x, start_y = 1, 1
    maze[start_y][start_x] = 0

    # --- Список направлений: (dx, dy)
    directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]

    # --- Итеративный DFS с использованием стека --------------------------------
    stack: List[Tuple[int, int]] = [(start_x, start_y)]
    while stack:
        x, y = stack[-1]

        # Находим все «соседние» непокрашенные клетки (на 2 шага от текущей)
        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < width-1 and 0 < ny < height-1:
                if maze[ny][nx] == 1:          # пока «сосед» – стена
                    neighbors.append((nx, ny))

        if not neighbors:
            stack.pop()   # откатываемся назад, если в текущей ячейке нет новых соседей
            continue

        # Выбираем случайного соседа и «выкапываем» путь к нему
        nx, ny = random.choice(neighbors)
        maze[ny][nx] = 0          # открываем соседнюю клетку
        maze[y + (ny-y)//2][x + (nx-x)//2] = 0   # убираем стену между ними

        stack.append((nx, ny))    # переходим к новому «активному» узлу

    return maze


def print_maze(maze: List[List[int]]) -> None:
    """
    Печатает лабиринт в консоли. 0 → пробел, 1 → █
    """
    wall = "█"
    passage = " "
    for row in maze:
        print("".join(wall if cell else passage for cell in row))


# ────────────────────────  ПРИМЕР ИСПОЛЬЗОВАНИЯ  ──────────────────────── #

if __name__ == "__main__":
    w, h = 21, 15          # любые нечётные размеры ≥3
    m = generate_maze(w, h)
    print_maze(m)

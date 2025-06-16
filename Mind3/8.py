import random

def generate_maze(width, height):
    """
    Генерирует лабиринт используя алгоритм Recursive Backtracker.

    Args:
        width: Ширина лабиринта (количество ячеек). Должна быть нечетной.
        height: Высота лабиринта (количество ячеек). Должна быть нечетной.

    Returns:
        Двумерный список, представляющий лабиринт.  
        '#': Стена
        ' ': Пустое пространство
    """

    # Проверка на нечетность размеров (необходимо для алгоритма)
    if width % 2 == 0:
        width += 1
    if height % 2 == 0:
        height += 1

    maze = [['#' for _ in range(width)] for _ in range(height)]  # Заполняем всё стенами

    def carve_path(x, y):
        """
        Рекурсивная функция для прокладки пути в лабиринте.
        """
        maze[y][x] = ' '  # Отмечаем текущую ячейку как проход

        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]  # Возможные направления (шаг 2, чтобы между стенами оставались стены)
        random.shuffle(directions)  # Перемешиваем направления для случайности

        for dx, dy in directions:
            nx, ny = x + dx, y + dy  # Вычисляем координаты следующей ячейки

            # Проверяем, что следующая ячейка находится в пределах лабиринта и является стеной
            if 0 < nx < width - 1 and 0 < ny < height - 1 and maze[ny][nx] == '#':
                maze[y + dy // 2][x + dx // 2] = ' '  # Пробиваем стену между текущей и следующей ячейками
                carve_path(nx, ny)  # Рекурсивно вызываем себя для следующей ячейки

    # Начинаем генерацию с произвольной нечетной ячейки
    start_x, start_y = 1, 1
    carve_path(start_x, start_y)

    return maze


def print_maze(maze):
    """
    Выводит лабиринт в консоль.
    """
    for row in maze:
        print(''.join(row))


# Пример использования
width = 21  # Ширина лабиринта
height = 15 # Высота лабиринта

maze = generate_maze(width, height)
print_maze(maze)

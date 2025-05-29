def mandelbrot(cols, rows):
    for row in range(rows):
        for col in range(cols):
            c = complex(-2 + (col / cols) * 3, -1 + (row / rows) * 2)
            z = 0
            for i in range(20):  # Количество итераций (больше - лучше детализация, но дольше)
                z = z * z + c
                if abs(z) > 2:
                    break
            if abs(z) <= 2:
                print("*", end="") # Или можно использовать другие символы
            else:
                print(" ", end="") # Пустое пространство
        print()

mandelbrot(80, 40) # Размеры изображения

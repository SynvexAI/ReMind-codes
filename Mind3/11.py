def fibonacci(n):
  """Генерирует список чисел Фибоначчи до n-го элемента."""
  fib_list = []
  a, b = 0, 1
  while len(fib_list) < n:
    fib_list.append(a)
    a, b = b, a + b
  return fib_list

# Пример использования
num_elements = 10
fibonacci_sequence = fibonacci(num_elements)
print(f"Первые {num_elements} чисел Фибоначчи: {fibonacci_sequence}")

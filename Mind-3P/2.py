# Напиши генератор кода на Python
import random

def generate_code(length=8, characters="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"):
  """
  Генерирует случайный код заданной длины, используя указанные символы.

  Args:
    length: Длина генерируемого кода. По умолчанию 8.
    characters: Строка символов, которые могут быть использованы в коде.
                По умолчанию используются буквы (в верхнем и нижнем регистре) и цифры.

  Returns:
    Случайный код в виде строки.
  """

  if not isinstance(length, int) or length <= 0:
    raise ValueError("Длина должна быть положительным целым числом.")

  if not isinstance(characters, str) or not characters:
    raise ValueError("Строка символов не может быть пустой.")

  code = ''.join(random.choice(characters) for _ in range(length))
  

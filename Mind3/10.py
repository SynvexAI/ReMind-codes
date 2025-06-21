import random
import string

def generate_password(length=12):
    """Генерирует случайный пароль заданной длины.

    Args:
        length: Длина пароля (по умолчанию 12).

    Returns:
        Случайный пароль в виде строки.
    """

    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

if __name__ == "__main__":
    password_length = int(input("Введите желаемую длину пароля: "))
    new_password = generate_password(password_length)
    print("Сгенерированный пароль:", new_password)

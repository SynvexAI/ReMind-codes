import random

def print_board(board):
    """Выводит игровое поле."""
    print("-------------")
    for i in range(3):
        print("|", board[i][0], "|", board[i][1], "|", board[i][2], "|")
        print("-------------")

def get_player_move(board, player):
    """Запрашивает у игрока ввод хода и проверяет его."""
    while True:
        try:
            row = int(input(f"Игрок {player}, введите номер строки (0-2): "))
            col = int(input(f"Игрок {player}, введите номер столбца (0-2): "))
            if row < 0 or row > 2 or col < 0 or col > 2:
                print("Неверный ввод! Номер строки и столбца должен быть от 0 до 2.")
            elif board[row][col] != " ":
                print("Эта клетка уже занята!")
            else:
                return row, col
        except ValueError:
            print("Неверный ввод! Введите число.")

def check_win(board, player):
    """Проверяет, есть ли победитель."""
    # Проверка по горизонтали
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] == player:
            return True
    # Проверка по вертикали
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] == player:
            return True
    # Проверка по диагонали
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False

def check_tie(board):
    """Проверяет, есть ли ничья."""
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                return False  # Есть свободные клетки, игра не окончена
    return True  # Нет свободных клеток, ничья

def play_tic_tac_toe():
    """Основная функция игры."""
    board = [[" " for _ in range(3)] for _ in range(3)]  # Создание пустого поля
    player = "X"
    game_over = False

    print("Добро пожаловать в игру крестики-нолики!")
    print_board(board)

    while not game_over:
        row, col = get_player_move(board, player)
        board[row][col] = player
        print_board(board)

        if check_win(board, player):
            print(f"Игрок {player} победил!")
            game_over = True
        elif check_tie(board):
            print("Ничья!")
            game_over = True
        else:
            # Смена игрока
            player = "O" if player == "X" else "X"

if __name__ == "__main__":
    play_tic_tac_toe()

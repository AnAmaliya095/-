def print_board(board):
    """Выводит текущее состояние игрового поля."""
    print("\n   1   2   3")
    for i in range(3):
        print(f"{i+1}  {board[i][0]} | {board[i][1]} | {board[i][2]}")
        if i < 2:
            print("  -----------")

def check_winner(board, player):
    """Проверяет, выиграл ли игрок (X или O)."""
    # Проверяем строки, столбцы и диагонали
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):  # строка
            return True
        if all(board[j][i] == player for j in range(3)):  # столбец
            return True
    if board[0][0] == board[1][1] == board[2][2] == player:  # диагональ \
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:  # диагональ /
        return True
    return False

def is_full(board):
    """Проверяет, заполнено ли поле (ничья)."""
    return all(board[i][j] != ' ' for i in range(3) for j in range(3))

def get_move(player):
    """Запрашивает у игрока координаты хода и проверяет их корректность."""
    while True:
        try:
            move = input(f"Игрок {player}, введите координаты (строка и столбец, например '1 2'): ").strip()
            row, col = map(int, move.split())
            if 1 <= row <= 3 and 1 <= col <= 3:
                return row - 1, col - 1  # перевод в индексы 0..2
            else:
                print("Координаты должны быть от 1 до 3. Попробуйте снова.")
        except ValueError:
            print("Введите два числа через пробел (например, '1 2'). Попробуйте снова.")

def main():
    # Инициализация пустого поля 3x3
    board = [[' ' for _ in range(3)] for _ in range(3)]
    current_player = 'X'  # первый ход — X

    print("Добро пожаловать в Крестики‑нолики!")
    print_board(board)

    while True:
        # Получаем ход игрока
        row, col = get_move(current_player)

        # Проверяем, что клетка свободна
        if board[row][col] != ' ':
            print("Эта клетка уже занята! Выберите другую.")
            continue

        # Ставим символ игрока
        board[row][col] = current_player
        print_board(board)

        # Проверяем победу
        if check_winner(board, current_player):
            print(f"\nИгрок {current_player} победил! Поздравляем!")
            break

        # Проверяем ничью
        if is_full(board):
            print("\nНичья! Поле заполнено.")
            break

        # Передаем ход другому игроку
        current_player = 'O' if current_player == 'X' else 'X'

if __name__ == "__main__":
    main()

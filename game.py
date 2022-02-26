# Write your code here
def print_chess_board():
    number_of_borders = len(chess_board[0]) * (_len + 1) + 3
    print(" " + number_of_borders * "-")
    for i, x in reversed(list(enumerate(chess_board, 1))):
        print(f'{i}| {" ".join(x)} |')
    print(" " + number_of_borders * "-")
    lista = [str(x) for x in range(1, len(chess_board[0]) + 1)]
    print(4 * " " + '  '.join(lista) if _len > 1 else 3 * " " + ' '.join(lista))


def validation(type_):
    while True:
        if type_ == "board":
            position = input("Enter your board dimensions:").split()
        else:
            position = input("Enter the knight's starting position:").split()
        try:
            if len(position) != 2 or position[0].isalpha() or position[1].isalpha() or int(position[0]) <= 0 or int(
                    position[1]) <= 0:
                print("Invalid dimensions!")
            else:
                return position
        except IndexError:
            print("Invalid dimensions!")


def isSafe(x, y):
    if 0 <= x < int(board_size[0]) and 0 <= y < int(board_size[1]) and chess_board[y][x] == _len * "_":
        return True
    return False


def possibilities(coords):
    coords_to_clean = []
    check_end = []
    for x in possible_moves:
        new_coord = [coords[0] + x[0], coords[1] + x[1]]
        if 0 <= new_coord[0] < int(board_size[0]) and 0 <= new_coord[1] < int(
                board_size[1]) and new_coord not in prev_move_int:
            n_of_moves = check_moves(new_coord, possible_moves)
            check_end.append(n_of_moves)
            chess_board[new_coord[1]][new_coord[0]] = format_inside(str(n_of_moves))
            coords_to_clean.append([new_coord[1], new_coord[0]])
    if not check_end:
        return check_end
    else:
        return coords_to_clean


def check_moves(coords, moves):
    if not moves:
        return 0
    x = coords[0] + moves[0][0]
    y = coords[1] + moves[0][1]

    if 0 <= x < int(board_size[0]) and 0 <= y < int(board_size[1]) and chess_board[y][x].strip() != "X" and \
            chess_board[y][x].strip() != "*":
        return 1 + check_moves(coords, moves[1:])
    else:
        return 0 + check_moves(coords, moves[1:])


def clean_board(coords_to_clean, last_move):
    for x in coords_to_clean:
        chess_board[x[0]][x[1]] = _len * "_"
    chess_board[last_move[1]][last_move[0]] = format_inside("*")


def format_inside(str_used):
    return (_len - 1) * " " + str_used if _len > 1 else str_used


def knight_move(knight_position):
    while True:
        knight_x, knight_y = [int(x) for x in knight_position]
        if knight_x > int(board_size[0]) or knight_y > int(board_size[1]):
            print("Invalid position!")
        elif knight_x <= 0 or knight_y <= 0:
            print("Invalid position!")
        else:
            knight_coords = [knight_x - 1, knight_y - 1]
            chess_board[knight_coords[1]][knight_coords[0]] = format_inside("X")
            game_status = possibilities(knight_coords)
            prev_move_str.append([str(knight_x), str(knight_y)])
            prev_move_int.append([knight_coords[0], knight_coords[1]])
            print_chess_board()
            clean_board(game_status, knight_coords)
            if not game_status:
                return game_status
            else:
                return game_status


def check_solusion(curr_x, curr_y, possible_moves, pos):
    if pos - 1 == int(board_size[0]) * int(board_size[1]):
        return True
    for move in possible_moves:
        new_x = curr_x + move[0]
        new_y = curr_y + move[1]
        if isSafe(new_x, new_y):
            chess_board[new_y][new_x] = (
                (_len - 1) * " " + str(pos) if len(str(pos)) == 1 else str(pos)) if _len > 1 else str(pos)
            if check_solusion(new_x, new_y, possible_moves, pos + 1):
                return True
            # Backtracking
            chess_board[new_y][new_x] = _len * "_"
    return False


possible_moves = [[2, 1], [2, -1], [1, 2], [1, -2], [-2, 1], [-2, -1], [-1, 2], [-1, -2]]
square_number = 1
board_size = validation("board")
prev_move_str = []
prev_move_int = []
_len = len(str(int(board_size[0]) * int(board_size[0])))
chess_board = [[_len * "_" for y in range(int(board_size[0]))] for x in range(int(board_size[1]))]
knight_position = validation("knight")

while True:
    question = input("Do you want to try the puzzle? (y/n):")
    chess_board[int(knight_position[1]) - 1][int(knight_position[0]) - 1] = " " + str(square_number)
    square_number += 1
    solusion = check_solusion(int(knight_position[0]) - 1, int(knight_position[1]) - 1, possible_moves,
                              square_number)

    if question == "y":
        if solusion:
            break
        else:
            print("No solution exists!")
            exit()
    elif question == "n":
        if solusion:
            print("\nHere's the solution!")
            print_chess_board()
            exit()
        else:
            print("No solution exists!")
            exit()
    else:
        print("Invalid input!")

chess_board = [[_len * "_" for y in range(int(board_size[0]))] for x in range(int(board_size[1]))]
game_status = knight_move(knight_position)

while True:
    next_move = input("Enter your next move:").split()

    if next_move not in prev_move_str and [int(next_move[1]) - 1, int(next_move[0]) - 1] in game_status:
        game_status = knight_move(next_move)
        square_number += 1
    else:
        print("Invalid move!", end=" ")
    if square_number == int(board_size[0]) * int(board_size[1]):
        print("What a great tour! Congratulations!")
        break
    if not game_status:
        print("No more possible moves!")
        print(f"Your knight visited {square_number - 1} squares!")
        break

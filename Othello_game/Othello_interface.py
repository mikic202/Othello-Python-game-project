from Othello_io import write_board_to_file, write_result_to_file
from Othello_board import Board, IncorectSizeError
from Othello_consts import first_colour, second_colour, possible_value
from tabulate import tabulate


class TooManyIncorectTriesError(TypeError):
    pass


def start_interface():
    """
    function used at the start of the game
    gives user choice of gamemode board size
    and if player vs computer function is chosen also gives colour choice
    """
    possible_game_types = ['1', '2', '3']
    color = None
    print('Welcome to Othello\nChose game type\n')
    print('1 - player vs player\n2 - player vs computer\n3 - computer vs computer')
    game_type = input('Your choice: ')
    while game_type not in possible_game_types:
        game_type = input('Previous choice incorect\nChose again: ')
    is_size_corect = False
    while not is_size_corect:
        try:
            board = board_size_choice()
            is_size_corect = True
        except(IncorectSizeError) as er:
            print(er)
            is_size_corect = False
        except(TypeError) as er:
            print(er)
            is_size_corect = False
    if game_type == '2':
        color = input(f'chose {first_colour} - black or {second_colour} - white colour: ')
        while color != first_colour and color != second_colour:
            color = input(f'chose {first_colour} - black or {second_colour} - white colour: ')
    print('you can open Game_board.txt file to see the board')
    return int(game_type), board, color


def board_size_choice():
    """
    function that gives user choice of board size
    """
    board_size_x = int(input('Chose even boards x dimensions between 8 and 30: '))
    board_size_y = int(input('Chose even boards y dimensions between 8 and 30: '))
    return Board((board_size_x, board_size_y))


def display_board(board_values, size):
    """
    function that shows user curent board and saves it to the Game_board.txt file
    """
    with open('Game_board.txt', 'w')as file_handle:
        write_board_to_file(board_values, size, file_handle)
        size_x, size_y = size
    table = list()
    for row in range(size_y):
        line = board_values[row*size_x:(row+1)*size_x]
        table.append(line)
    print(tabulate(table))


def players_choice(max_index, color):
    """
    function that accepts index of space chosen by player
    """
    max_tries = 5
    chosen_space = (input(f'{color} playing, chose spaces from {possible_value}1 to {possible_value}{max_index}: '))
    chosen_space = chosen_space.strip()
    tries = 1
    while check_index(chosen_space, max_index) and tries < max_tries:
        print('chosen index incorect, try again')
        chosen_space = (input(f'{color} playing, chose spaces from {possible_value}1 to {possible_value}{max_index}: '))
        chosen_space = chosen_space.strip()
        tries += 1
    if tries >= max_tries:
        raise TooManyIncorectTriesError
    return chosen_space


def display_result(board: Board):
    """
    function displays final board and results
    """
    display_board(board.board_values(), board.size())
    with open('Game_board.txt', 'a')as file_handle:
        write_result_to_file(board, file_handle)
    score, result = calculate_result(board)
    print(score+"\n"+result)


def calculate_result(board: Board):
    """
    function calculates result on given board
    """
    black_spaces = white_spaces = 0
    for space in board.board_values():
        if space == first_colour:
            black_spaces += 1
        elif space == second_colour:
            white_spaces += 1
    score = f'white: {white_spaces:3}  black: {black_spaces:3}'
    if white_spaces > black_spaces:
        result = 'White won!'
    elif white_spaces < black_spaces:
        result = 'Black won!'
    else:
        result = 'Tie'
    return score, result


def check_index(chosen, max_index):
    """
    function checks if index is in given range
    """
    try:
        if int(chosen[1:]) > max_index:
            return True
    except Exception:
        return True

from Othello_board import Board
from Othello_consts import first_colour, second_colour


def write_board_to_file(board_values, size, file_handle):
    """
    function used to write curent board to file
    """
    size_x, size_y = size
    for row in range(size_y):
        line = board_values[row*size_x:(row+1)*size_x]
        file_handle.write(str(line) + '\n')


def write_result_to_file(board: Board, file_handle):
    """
    function used to write final results to file
    """
    white_spaces = 0
    black_spaces = 0
    for space in board.board_values():
        if space == first_colour:
            black_spaces += 1
        elif space == second_colour:
            white_spaces += 1
    file_handle.write(f'white: {white_spaces}  black: {black_spaces}\n')
    if white_spaces > black_spaces:
        file_handle.write('White won!')
    elif white_spaces < black_spaces:
        file_handle.write('Black won!')
    else:
        file_handle.write('Tie')

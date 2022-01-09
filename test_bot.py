from Othello_board import Board
from Othello_bot import BOT
from Othello_consts import first_colour, second_colour


def test_init():
    board = Board((8, 8))
    bot = BOT(board, first_colour)
    assert bot.board() == board
    assert bot.colour() == first_colour
    assert bot.weights() == [-2, 0, 2, 3, 2, 3, 2]


def test_count_spaces_played():
    board = Board((8, 8))
    bot = BOT(board, first_colour)
    assert bot._count_spaces_played(board) == 4


def test_evaluate_move():
    previous_board = Board((8, 8))
    board = Board((8, 8))
    board_values = [
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', 'b', '#', '#', '#', '#', '#',
        '#', '#', '#', 'w', '#', '#', '#', '#',
        '#', '#', '#', 'w', 'b', 'b', 'b', '#',
        '#', '#', 'w', 'b', 'w', 'w', '#', '#',
        '#', '#', '#', 'w', 'w', '#', 'b', '#',
        '#', '#', '#', '#', 'b', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#']
    board.set_board_values(board_values)
    bot = BOT(previous_board, first_colour)
    assert bot.evaluate_move(board) == -2*10 + 2*1


def test_chose_move():
    board = Board((8, 8))
    board_value = [
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', 'w', '#', '#', '#', '#', '#',
        '#', '#', '#', 'w', 'w', 'w', 'w', 'w',
        '#', '#', '#', 'w', 'b', 'b', 'b', '#',
        '#', '#', 'w', 'w', 'w', 'w', 'w', 'w',
        '#', '#', 'w', 'w', 'w', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#']
    board.set_board_values(board_value)
    bot = BOT(board, second_colour)
    chosen_space = bot.chose_move(board)
    assert chosen_space.place_on_board() == (7, 3)


def test_chose_move_tow_possible():
    board = Board((8, 8))
    board_value = [
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', 'w', '#', '#', '#', '#', '#',
        '#', '#', '#', 'w', 'w', '#', 'w', 'w',
        '#', '#', '#', 'w', 'b', 'b', 'b', '#',
        '#', '#', 'w', 'w', 'w', 'w', 'w', 'w',
        '#', '#', 'w', 'w', 'w', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#']
    board.set_board_values(board_value)
    bot = BOT(board, second_colour)
    chosen_space = bot.chose_move(board)
    assert chosen_space.place_on_board() == (5, 2)

from Othello_board import Board
from Othello_main import change_spaces, format_board_file, play, computer_move
from Othello_bot import BOT
from Othello_consts import first_colour, empty_value
from io import StringIO


def test_change_spaces_typical():
    board = Board((8, 8))
    line = [board.board()[0], board.board()[1], board.board()[2], board.board()[3], board.board()[4]]
    space_num = [1, 3, 2]
    change_spaces(first_colour, line, space_num)
    assert board.board()[0].value() == empty_value
    assert board.board()[1].value() == first_colour
    assert board.board()[2].value() == first_colour
    assert board.board()[3].value() == first_colour
    assert board.board()[4].value() == empty_value


def test_change_spaces_one_None_left():
    board = Board((8, 8))
    line = [board.board()[0], board.board()[1], board.board()[2], board.board()[3], board.board()[4]]
    space_num = [None, 3, 2]
    change_spaces(first_colour, line, space_num)
    assert board.board()[0].value() == empty_value
    assert board.board()[1].value() == empty_value
    assert board.board()[2].value() == first_colour
    assert board.board()[3].value() == first_colour
    assert board.board()[4].value() == empty_value


def test_change_spaces_one_None_right():
    board = Board((8, 8))
    line = [board.board()[0], board.board()[1], board.board()[2], board.board()[3], board.board()[4]]
    space_num = [1, None, 2]
    change_spaces(first_colour, line, space_num)
    assert board.board()[0].value() == empty_value
    assert board.board()[1].value() == first_colour
    assert board.board()[2].value() == first_colour
    assert board.board()[3].value() == empty_value
    assert board.board()[4].value() == empty_value


def test_format_board_file_typical():
    board = Board((8, 8))
    expected_board = [
        ['#', '#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', '#', 'w', 'b', '#', '#', '#'],
        ['#', '#', '#', 'b', 'w', '#', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#', '#']]
    assert format_board_file(board) == expected_board


def test_play_typical(monkeypatch):
    board = Board((8, 8))
    expected_board = [
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', 'b', '#', '#', '#', '#',
        '#', '#', '#', 'b', 'b', '#', '#', '#',
        '#', '#', '#', 'b', 'w', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#']
    fake_input = StringIO('p1\n')
    monkeypatch.setattr('sys.stdin', fake_input)
    play(board, first_colour)
    assert board.board_values() == expected_board


def test_computer_move_typical(monkeypatch):
    board = Board((8, 8))
    expected_board = [
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', 'b', '#', '#', '#', '#',
        '#', '#', 'b', 'w', 'b', '#', '#', '#',
        '#', '#', '#', 'b', 'b', 'b', '#', '#',
        '#', '#', '#', '#', 'b', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#']
    new_board = [
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', 'b', '#', '#', '#', '#',
        '#', '#', 'b', 'w', 'b', '#', '#', '#',
        '#', '#', '#', 'b', 'w', '#', '#', '#',
        '#', '#', '#', '#', 'b', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#']
    board.set_board_values(new_board)
    fake_input = StringIO('p1\n')
    monkeypatch.setattr('sys.stdin', fake_input)
    computer_move(board, first_colour, BOT(board, first_colour))
    assert board.board_values() == expected_board

from Othello_game.Othello_board import Board
from Othello_game.Othello_io import write_board_to_file, write_result_to_file
from io import StringIO


def test_write_board_to_file():
    filehandle = StringIO()
    board_values = ['1', '2', '3', '4', '5', '6']
    write_board_to_file(board_values, (3, 2), filehandle)
    expected = "['1', '2', '3']\n['4', '5', '6']\n"
    assert expected == filehandle.getvalue()


def test_write_result_to_file_black_won():
    filehandle = StringIO()
    board = Board((8, 8))
    fake_board = [
        'b', 'b', 'b', 'w', 'b', 'w', 'b', 'b',
        'b', 'b', 'b', 'w', 'b', 'w', 'b', 'b',
        'b', 'b', 'b', 'w', 'b', 'w', 'b', 'b',
        'b', 'b', 'b', 'w', 'b', 'w', 'b', 'b',
        'b', 'b', 'b', 'w', 'b', 'w', 'b', 'b',
        'b', 'b', 'b', 'w', 'b', 'w', 'b', 'b',
        'b', 'b', 'b', 'w', 'b', 'w', 'b', 'b',
        'b', 'b', 'b', 'w', 'b', 'w', 'b', 'b']
    board.set_board_values(fake_board)
    write_result_to_file(board, filehandle)
    expected = 'white: 16  black: 48\nBlack won!'
    assert expected == filehandle.getvalue()


def test_write_result_to_file_white_won():
    filehandle = StringIO()
    board = Board((8, 8))
    fake_board = [
        'w', 'w', 'b', 'w', 'b', 'w', 'w', 'b',
        'w', 'w', 'b', 'w', 'b', 'w', 'w', 'b',
        'w', 'w', 'b', 'w', 'b', 'w', 'w', 'b',
        'w', 'w', 'b', 'w', 'b', 'w', 'w', 'b',
        'w', 'w', 'b', 'w', 'b', 'w', 'w', 'b',
        'w', 'w', 'b', 'w', 'b', 'w', 'w', 'b',
        'w', 'w', 'b', 'w', 'b', 'w', 'w', 'b',
        'w', 'w', 'b', 'w', 'b', 'w', 'w', 'b']
    board.set_board_values(fake_board)
    write_result_to_file(board, filehandle)
    expected = 'white: 40  black: 24\nWhite won!'
    assert expected == filehandle.getvalue()


def test_write_result_to_file_tie():
    filehandle = StringIO()
    board = Board((8, 8))
    fake_board = [
        'w', 'w', 'b', 'b', 'b', 'w', 'w', 'b',
        'w', 'w', 'b', 'b', 'b', 'w', 'w', 'b',
        'w', 'w', 'b', 'b', 'b', 'w', 'w', 'b',
        'w', 'w', 'b', 'b', 'b', 'w', 'w', 'b',
        'w', 'w', 'b', 'b', 'b', 'w', 'w', 'b',
        'w', 'w', 'b', 'b', 'b', 'w', 'w', 'b',
        'w', 'w', 'b', 'b', 'b', 'w', 'w', 'b',
        'w', 'w', 'b', 'b', 'b', 'w', 'w', 'b']
    board.set_board_values(fake_board)
    write_result_to_file(board, filehandle)
    expected = 'white: 32  black: 32\nTie'
    assert expected == filehandle.getvalue()

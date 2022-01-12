from Othello_game.Othello_board import Board
from Othello_game.Othello_interface import TooManyIncorectTriesError, players_choice, start_interface, check_index, calculate_result
from io import StringIO
import pytest


def test_players_choice_typical(monkeypatch):
    fake_input = StringIO('p2\n')
    monkeypatch.setattr('sys.stdin', fake_input)
    assert players_choice(4, 'w') == 'p2'


def test_players_choice_too_many_incorect_tries(monkeypatch):
    fake_input = StringIO('p6\np7\np8\np9\np8\np6')
    monkeypatch.setattr('sys.stdin', fake_input)
    with pytest.raises(TooManyIncorectTriesError):
        players_choice(4, 'w')


def test_players_choice_input_with_space(monkeypatch):
    fake_input = StringIO('  p2 \n')
    monkeypatch.setattr('sys.stdin', fake_input)
    assert players_choice(4, 'w') == 'p2'


def test_start_interfejs_player_vs_player_8x8_board(monkeypatch):
    fake_input = StringIO('1\n8\n8\n')
    monkeypatch.setattr('sys.stdin', fake_input)
    choice, board, colour = start_interface()
    assert colour is None
    assert choice == 1
    assert board.size() == (8, 8)


def test_start_interfejs_player_vs_computer_10x10_board(monkeypatch):
    fake_input = StringIO('2\n10\n10\nb\n')
    monkeypatch.setattr('sys.stdin', fake_input)
    choice, board, colour = start_interface()
    assert colour == 'b'
    assert choice == 2
    assert board.size() == (10, 10)


def test_check_index_corect():
    assert check_index('p4', 6) is None


def test_check_index_incorect():
    assert check_index('p10', 4)


def test_calculate_score_typical():
    board = Board((8, 8))
    board_to_calculate = [
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', 'b', '#', '#', '#', '#',
        '#', '#', 'b', 'w', 'b', '#', '#', '#',
        '#', '#', '#', 'b', 'w', '#', '#', '#',
        '#', '#', '#', '#', 'b', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#']
    board.set_board_values(board_to_calculate)
    assert calculate_result(board) == ('white:   2  black:   5', 'Black won!')


def test_calculate_score_tie():
    board = Board((8, 8))
    assert calculate_result(board) == ('white:   2  black:   2', 'Tie')

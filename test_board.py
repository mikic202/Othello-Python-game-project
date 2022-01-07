from Othello_board import Board
from Othello_consts import IncorectSizeError, first_colour, second_colour, empty_value, possible_value
import pytest

from Othello_space import Space


def test_board_init():
    board = Board((8, 8))
    expected_board = [
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', 'w', 'b', '#', '#', '#',
        '#', '#', '#', 'b', 'w', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#']
    assert board.board_values() == expected_board
    assert board.size() == (8, 8)


def test_board_init_too_small_size():
    with pytest.raises(IncorectSizeError):
        Board((3, 3))


def test_board_init_too_big_size():
    with pytest.raises(IncorectSizeError):
        Board((63, 33))


def test_board_init_size_not_even_numbers():
    with pytest.raises(IncorectSizeError):
        Board((13, 23))


def test_board_find_posible_spaces_playing_white():
    board = Board((8, 8))
    expected_board = [
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', 'p', 'p', 'p', '#', '#',
        '#', '#', 'p', 'w', 'b', 'p', '#', '#',
        '#', '#', 'p', 'b', 'w', 'p', '#', '#',
        '#', '#', 'p', 'p', 'p', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#']
    board.find_possible_spaces('w')
    w = board.board_values()
    assert w == expected_board


def test_board_find_posible_spaces_playing_black():
    board = Board((8, 8))
    expected_board = [
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', 'p', 'p', 'p', '#', '#', '#',
        '#', '#', 'p', 'w', 'b', 'p', '#', '#',
        '#', '#', 'p', 'b', 'w', 'p', '#', '#',
        '#', '#', '#', 'p', 'p', 'p', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#']
    board.find_possible_spaces('b')
    b = board.board_values()
    assert b == expected_board


def test_board_find_bossible_spaces_complex_situation():
    board = Board((8, 8))
    expected_board = [
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', 'p', 'p', 'p', '#', '#', '#',
        '#', '#', 'p', 'w', 'p', '#', '#', '#',
        '#', 'p', 'p', 'w', 'b', 'b', 'b', '#',
        '#', 'p', 'w', 'b', 'w', 'w', 'p', '#',
        '#', 'p', 'p', 'w', 'w', 'p', 'p', '#',
        '#', '#', 'p', 'p', 'b', 'p', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#']
    fake_board = [
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', 'w', '#', '#', '#', '#',
        '#', '#', '#', 'w', 'b', 'b', 'b', '#',
        '#', '#', 'w', 'b', 'w', 'w', '#', '#',
        '#', '#', '#', 'w', 'w', '#', '#', '#',
        '#', '#', '#', '#', 'b', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#']
    board.set_board_values(fake_board)
    board.find_possible_spaces('b')
    b = board.board_values()
    assert b == expected_board


def test_vertical_line_function():
    board = Board((8, 8))
    fake_board = [
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', 'w', '#', '#', '#', '#',
        '#', '#', '#', 'w', 'b', 'b', 'b', '#',
        '#', '#', 'w', 'b', 'w', 'w', '#', '#',
        '#', '#', '#', 'w', 'w', '#', '#', '#',
        '#', '#', '#', '#', 'b', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#']
    board.set_board_values(fake_board)
    expected = ['#', '#', 'w', 'w', 'b', 'w', '#', '#']
    line = board._vertical_line(3)
    values = [space.value() for space in line]
    assert values == expected


def test_horizontal_line_function():
    board = Board((8, 8))
    fake_board = [
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', 'w', '#', '#', '#', '#',
        '#', '#', '#', 'w', 'b', 'b', 'b', '#',
        '#', '#', 'w', 'b', 'w', 'w', '#', '#',
        '#', '#', '#', 'w', 'w', '#', '#', '#',
        '#', '#', '#', '#', 'b', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#']
    board.set_board_values(fake_board)
    expected = ['#', '#', 'w', 'b', 'w', 'w', '#', '#']
    line = board._horizontal_line(4)
    values = [space.value() for space in line]
    assert values == expected


def test_diagonal_line_positive_function():
    board = Board((8, 8))
    fake_board = [
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', 'w', '#', '#', '#', '#',
        '#', '#', '#', 'w', 'b', 'b', 'b', '#',
        '#', '#', 'w', 'b', 'w', 'w', '#', '#',
        '#', '#', '#', 'w', 'w', '#', '#', '#',
        '#', '#', '#', '#', 'b', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#']
    board.set_board_values(fake_board)
    expected = ['#', '#', 'w', '#', '#', '#']
    line = board._diagonal_line_positive(33)
    values = [space.value() for space in line]
    assert values == expected


def test_diagonal_line_positive_function_upper_right_corner():
    board = Board((8, 8))
    fake_board = [
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', 'w', '#', '#', '#', '#',
        '#', '#', '#', 'w', 'b', 'b', 'b', '#',
        '#', '#', 'w', 'b', 'w', 'w', '#', '#',
        '#', '#', '#', 'w', 'w', '#', '#', '#',
        '#', '#', '#', '#', 'b', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#']
    board.set_board_values(fake_board)
    expected = ['#', '#', '#', 'b', 'b', '#', '#', '#']
    line = board._diagonal_line_positive(7)
    values = [space.value() for space in line]
    assert values == expected


def test_diagonal_line_positive_function_close_to_right_border():
    board = Board((8, 8))
    fake_board = [
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', 'w', '#', '#', '#', '#',
        '#', '#', '#', 'w', 'b', 'b', 'b', '#',
        '#', '#', 'w', 'b', 'w', 'w', '#', '#',
        '#', '#', '#', 'w', 'w', '#', '#', '#',
        '#', '#', '#', '#', 'b', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#']
    board.set_board_values(fake_board)
    expected = ['#', 'b', 'w', 'w', '#', '#']
    line = board._diagonal_line_positive(23)
    values = [space.value() for space in line]
    assert values == expected


def test_diagonal_line_positive_function_upper_left_corner():
    board = Board((8, 8))
    fake_board = [
        'w', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', 'w', '#', '#', '#', '#',
        '#', '#', '#', 'w', 'b', 'b', 'b', '#',
        '#', '#', 'w', 'b', 'w', 'w', '#', '#',
        '#', '#', '#', 'w', 'w', '#', '#', '#',
        '#', '#', '#', '#', 'b', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#']
    board.set_board_values(fake_board)
    expected = ['w']
    line = board._diagonal_line_positive(0)
    values = [space.value() for space in line]
    assert values == expected


def test_diagonal_line_negative_function():
    board = Board((8, 8))
    fake_board = [
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', 'w', '#', '#', '#', '#',
        '#', '#', '#', 'w', 'b', 'b', 'b', '#',
        '#', '#', 'w', 'b', 'w', 'w', '#', '#',
        '#', '#', '#', 'w', 'w', '#', '#', '#',
        '#', '#', '#', '#', 'b', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#']
    board.set_board_values(fake_board)
    expected = ['#', '#', 'w', 'w', 'b', '#']
    line = board._diagonal_line_negative(34)
    values = [space.value() for space in line]
    assert values == expected


def test_diagonal_line_negative_function_upper_left_corner():
    board = Board((8, 8))
    fake_board = [
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', 'w', '#', '#', '#', '#',
        '#', '#', '#', 'w', 'b', 'b', 'b', '#',
        '#', '#', 'w', 'b', 'w', 'w', '#', '#',
        '#', '#', '#', 'w', 'w', '#', '#', '#',
        '#', '#', '#', '#', 'b', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#']
    board.set_board_values(fake_board)
    expected = ['#', '#', '#', 'w', 'w', '#', '#', '#']
    line = board._diagonal_line_negative(0)
    values = [space.value() for space in line]
    assert values == expected


def test_diagonal_line_negative_function_upper_right_corner():
    board = Board((8, 8))
    fake_board = [
        '#', '#', '#', '#', '#', '#', '#', 'w',
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', 'w', '#', '#', '#', '#',
        '#', '#', '#', 'w', 'b', 'b', 'b', '#',
        '#', '#', 'w', 'b', 'w', 'w', '#', '#',
        '#', '#', '#', 'w', 'w', '#', '#', '#',
        '#', '#', '#', '#', 'b', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#']
    board.set_board_values(fake_board)
    expected = ['w']
    line = board._diagonal_line_negative(7)
    values = [space.value() for space in line]
    assert values == expected


def test_check_line_for_series_of_spaces_function_typical():
    board = Board((8, 8))
    white_space = Space((1, 1), 'w', (4, 4))
    black_space = Space((1, 2), 'b', (4, 4))
    empty_space = Space((1, 3), '#', (4, 4))
    possible_space = Space((2, 3), 'p', (4, 4))
    line_to_check = [white_space, black_space, black_space, possible_space, black_space, white_space, empty_space]
    line_to_check = board._check_line_for_series_of_spaces(line_to_check, 'b', 'w', 3)
    assert line_to_check == [0, 5]


def test_check_line_for_series_of_spaces_function_p_at_the_begining():
    board = Board((8, 8))
    white_space = Space((1, 1), 'w', (4, 4))
    black_space = Space((1, 2), 'b', (4, 4))
    empty_space = Space((1, 3), '#', (4, 4))
    possible_space = Space((2, 3), 'p', (4, 4))
    line_to_check = [possible_space, black_space, white_space, empty_space]
    line_to_check = board._check_line_for_series_of_spaces(line_to_check, 'b', 'w', 0)
    assert line_to_check == [None, 2]


def test_check_line_for_series_of_spaces_function_at_the_end():
    board = Board((8, 8))
    white_space = Space((1, 1), 'w', (4, 4))
    black_space = Space((1, 2), 'b', (4, 4))
    empty_space = Space((1, 3), '#', (4, 4))
    possible_space = Space((2, 3), 'p', (4, 4))
    line_to_check = [empty_space, white_space, black_space, black_space, possible_space]
    line_to_check = board._check_line_for_series_of_spaces(line_to_check, 'b', 'w', 4)
    assert line_to_check == [1, None]


def test_check_line_for_series_of_spaces_function_no_solution():
    board = Board((8, 8))
    white_space = Space((1, 1), 'w', (4, 4))
    black_space = Space((1, 2), 'b', (4, 4))
    empty_space = Space((1, 3), '#', (4, 4))
    possible_space = Space((2, 3), 'p', (4, 4))
    line_to_check = [black_space, black_space, possible_space, white_space, empty_space]
    line_to_check = board._check_line_for_series_of_spaces(line_to_check, 'b', 'w', 2)
    assert line_to_check == [None, None]


def test_check_line_for_series_of_spaces_function_only_black_around_w_playing():
    board = Board((8, 8))
    black_space = Space((1, 2), 'b', (4, 4))
    possible_space = Space((2, 3), 'p', (4, 4))
    line_to_check = [black_space, black_space, possible_space, black_space]
    line_to_check = board._check_line_for_series_of_spaces(line_to_check, 'b', 'w', 3)
    assert line_to_check == [None, None]


def test_check_line_for_series_of_spaces_function_only_p_in_line():
    board = Board((8, 8))
    possible_space = Space((2, 3), 'p', (4, 4))
    line_to_check = [possible_space]
    line_to_check = board._check_line_for_series_of_spaces(line_to_check, 'b', 'w', 3)
    assert line_to_check == [None, None]


def test_check_line_for_series_of_spaces_function_two_p_in_line():
    board = Board((8, 8))
    white_space = Space((1, 1), second_colour, (4, 4))
    black_space = Space((1, 2), first_colour, (4, 4))
    empty_space = Space((1, 3), empty_value, (4, 4))
    possible_space = Space((2, 3), possible_value, (4, 4))
    line = [white_space, black_space, black_space, possible_space, black_space, possible_space, white_space, empty_space]
    line = board._check_line_for_series_of_spaces(line, first_colour, second_colour, 3)
    assert line == [0, None]


def test_find_plays_start():
    board = Board((8, 8))
    board.find_plays(first_colour)
    expected_board = [
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', 'p', '#', '#', '#', '#',
        '#', '#', 'p', 'w', 'b', '#', '#', '#',
        '#', '#', '#', 'b', 'w', 'p', '#', '#',
        '#', '#', '#', '#', 'p', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#']
    b = board.board_values()
    assert b == expected_board


def test_find_plays_more_complex_situation():
    board = Board((8, 8))
    expected_board = [
        '#', 'p', '#', '#', '#', '#', '#', '#',
        '#', '#', 'b', '#', '#', '#', '#', '#',
        '#', '#', '#', 'w', 'p', 'p', 'p', 'p',
        '#', '#', 'p', 'w', 'b', 'b', 'b', 'p',
        '#', '#', 'w', 'b', 'w', 'w', '#', '#',
        '#', '#', '#', 'w', 'w', '#', 'b', '#',
        '#', '#', '#', '#', 'b', '#', '#', 'p',
        '#', '#', '#', '#', 'p', 'p', '#', '#']
    fake_board = [
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', 'b', '#', '#', '#', '#', '#',
        '#', '#', '#', 'w', '#', '#', '#', '#',
        '#', '#', '#', 'w', 'b', 'b', 'b', '#',
        '#', '#', 'w', 'b', 'w', 'w', '#', '#',
        '#', '#', '#', 'w', 'w', '#', 'b', '#',
        '#', '#', '#', '#', 'b', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#']
    board.set_board_values(fake_board)
    board.find_plays(second_colour)
    b = board.board_values()
    assert b == expected_board


def test_find_plays_no_possible_plays():
    board = Board((8, 8))
    fake_board = [
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', 'w', '#', '#', '#', '#', '#',
        '#', '#', '#', 'w', 'w', 'w', 'w', 'w',
        '#', '#', '#', '#', 'b', 'b', 'b', '#',
        '#', '#', 'w', 'w', 'w', 'w', 'w', 'w',
        '#', '#', 'w', 'w', 'w', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#']
    board.set_board_values(fake_board)
    board.find_plays(second_colour)
    b = board.board_values()
    assert b == fake_board


def test_reset_possible_typical():
    board = Board((8, 8))
    expected_board = [
        '#', '#', '#', '#', '#', '#', '#', '#',
        '#', '#', 'b', '#', '#', '#', '#', '#',
        '#', '#', '#', 'w', '#', '#', '#', '#',
        '#', '#', '#', 'w', 'b', 'b', 'b', '#',
        '#', '#', 'w', 'b', 'w', 'w', '#', '#',
        '#', '#', '#', 'w', 'w', '#', 'b', '#',
        '#', '#', '#', '#', 'b', '#', '#', '#',
        '#', '#', '#', '#', '#', '#', '#', '#']
    board.set_board_values(expected_board)
    board.find_plays(second_colour)
    board.reset_possible()
    assert board.board_values() == expected_board

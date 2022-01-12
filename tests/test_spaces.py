from Othello_game.Othello_space import Space
from Othello_game.Othello_consts import IncorectSpacePositionError, IncorectSpaceValueError
from Othello_game.Othello_consts import first_colour, second_colour, empty_value, possible_value
import pytest


def test_space_init_typical():
    board_space = Space((3, 3), 'w', (10, 10))
    assert board_space.place_on_board() == (3, 3)
    assert board_space.value() == 'w'
    assert board_space.board_size() == (10, 10)


def test_space_init_place_on_board_not_tuple():
    with pytest.raises(TypeError):
        Space(1, 'b', (10, 10))


def test_space_init_place_on_board_out_of_range():
    with pytest.raises(ValueError):
        Space((10, 13), 'w', (2, 2))


def test_space_init_value_int():
    with pytest.raises(IncorectSpaceValueError):
        Space((1, 2), 2, (4, 4))


def test_space_init_incorect_value():
    with pytest.raises(IncorectSpaceValueError):
        Space((1, 2), 'c', (4, 7))


def test_space_init_positions_out_of_range():
    with pytest.raises(IncorectSpacePositionError):
        Space((8, 20), 'b', (4, 7))


def test_set_valeu_typiypical():
    space = Space((1, 3), 'w', (4, 4))
    space.set_value('b')
    assert space.value() == 'b'


# na potrzeby testowania lista miejsc to numery
# ale w ostatecznej wersji będzie działać na innych obiektach klasy Space
def test_find_spaces_around_upper_left_corner():
    pos = Space((0, 0), 'b', (4, 4))
    num_tab = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    assert pos.find_space_around(num_tab) == [2, 5, 6]


def test_find_spaces_around_upper_right_corner():
    pos = Space((3, 0), 'b', (4, 4))
    num_tab = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    assert pos.find_space_around(num_tab) == [3, 7, 8]


def test_find_spaces_around_lower_left_corner():
    pos = Space((0, 3), 'b', (4, 4))
    num_tab = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    assert pos.find_space_around(num_tab) == [9, 10, 14]


def test_find_spaces_around_lower_right_corner():
    pos = Space((3, 3), 'b', (4, 4))
    num_tab = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    assert pos.find_space_around(num_tab) == [11, 12, 15]


def test_find_spaces_around_right_border():
    pos = Space((0, 1), 'b', (4, 4))
    num_tab = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    assert pos.find_space_around(num_tab) == [1, 2, 6, 9, 10]


def test_find_spaces_around_left_border():
    pos = Space((3, 1), 'b', (4, 4))
    num_tab = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    assert pos.find_space_around(num_tab) == [3, 4, 7, 11, 12]


def test_find_spaces_around_upper_border():
    pos = Space((1, 0), 'b', (4, 4))
    num_tab = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    assert pos.find_space_around(num_tab) == [1, 3, 5, 6, 7]


def test_find_spaces_around_lower_border():
    pos = Space((1, 3), 'b', (4, 4))
    num_tab = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    assert pos.find_space_around(num_tab) == [9, 10, 11, 13, 15]


def test_find_spaces_around_in_the_middle():
    pos = Space((1, 1), 'b', (4, 4))
    num_tab = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    assert pos.find_space_around(num_tab) == [1, 2, 3, 5, 7, 9, 10, 11]


def test_reset_if_possible_empty():
    pos = Space((1, 1), empty_value, (4, 4))
    pos.reset_if_possible()
    assert pos.value() == empty_value


def test_reset_if_possible_black():
    pos = Space((1, 1), first_colour, (4, 4))
    pos.reset_if_possible()
    assert pos.value() == first_colour


def test_reset_if_possible_white():
    pos = Space((1, 1), second_colour, (4, 4))
    pos.reset_if_possible()
    assert pos.value() == second_colour


def test_reset_if_possible_space_possible():
    pos = Space((1, 1), possible_value, (4, 4))
    pos.reset_if_possible()
    assert pos.value() == empty_value

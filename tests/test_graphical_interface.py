from Othello_game.Othello_graphical_interface import function_choice, player_function, computer_function
from Othello_game.Othello_graphical_interface import button_colour_change, OptionSpace, SpaceToPress
from Othello_game.Othello_graphical_interface import white, gray, board_size_choice, chose_delay
from Othello_game.Othello_space import Space
from Othello_game.Othello_consts import first_colour, second_colour
import pygame


def test_function_choice_pvp():
    assert function_choice(1) == (player_function, player_function)


def test_function_choice_compvcomp():
    assert function_choice(3) == (computer_function, computer_function)


def test_function_choice_pvcomp_first_colour(monkeypatch):
    def fake_colour_choice():
        return first_colour
    monkeypatch.setattr('Othello_game.Othello_graphical_interface.colour_choice', fake_colour_choice)
    assert function_choice(2) == (player_function, computer_function)


def test_function_choice_pvcomp_second_colour(monkeypatch):
    def fake_colour_choice():
        return second_colour
    monkeypatch.setattr('Othello_game.Othello_graphical_interface.colour_choice', fake_colour_choice)
    assert function_choice(2) == (computer_function, player_function)


def test_button_colour_change_first_option():
    assert button_colour_change(1) == (gray, white, white)


def test_button_colour_change_second_option():
    assert button_colour_change(2) == (white, gray, white)


def test_button_colour_change_third_option():
    assert button_colour_change(3) == (white, white, gray)


def test_board_size_choice_key_up_typical():
    key_press = {pygame.K_UP: True, pygame.K_DOWN: False, pygame.K_LEFT: False, pygame.K_RIGHT: False}
    assert board_size_choice(key_press, 8, 8) == (8, 9)


def test_board_size_choice_key_up_out_of_range():
    key_press = {pygame.K_UP: True, pygame.K_DOWN: False, pygame.K_LEFT: False, pygame.K_RIGHT: False}
    assert board_size_choice(key_press, 8, 30) == (8, 30)


def test_board_size_choice_key_down_typical():
    key_press = {pygame.K_UP: False, pygame.K_DOWN: True, pygame.K_LEFT: False, pygame.K_RIGHT: False}
    assert board_size_choice(key_press, 8, 10) == (8, 9)


def test_board_size_choice_key_down_out_of_range():
    key_press = {pygame.K_UP: False, pygame.K_DOWN: True, pygame.K_LEFT: False, pygame.K_RIGHT: False}
    assert board_size_choice(key_press, 8, 8) == (8, 8)


def test_board_size_choice_key_left_typical():
    key_press = {pygame.K_UP: False, pygame.K_DOWN: False, pygame.K_LEFT: True, pygame.K_RIGHT: False}
    assert board_size_choice(key_press, 9, 10) == (8, 10)


def test_board_size_choice_key_left_out_of_range():
    key_press = {pygame.K_UP: False, pygame.K_DOWN: False, pygame.K_LEFT: True, pygame.K_RIGHT: False}
    assert board_size_choice(key_press, 8, 8) == (8, 8)


def test_board_size_choice_key_right_typical():
    key_press = {pygame.K_UP: False, pygame.K_DOWN: False, pygame.K_LEFT: False, pygame.K_RIGHT: True}
    assert board_size_choice(key_press, 9, 10) == (10, 10)


def test_board_size_choice_key_tight_out_of_range():
    key_press = {pygame.K_UP: False, pygame.K_DOWN: False, pygame.K_LEFT: False, pygame.K_RIGHT: True}
    assert board_size_choice(key_press, 30, 8) == (30, 8)


def test_option_space_init():
    option = OptionSpace((100, 100), (200, 200))
    rect = option.rect
    assert isinstance(rect, pygame.Rect)
    assert rect.x, rect.y == (100, 100)
    assert rect.size == (200, 200)


def test_space_to_press_init():
    space = Space((3, 3), first_colour, (8, 8))
    space_to_press = SpaceToPress((100, 100), (200, 200), space)
    assert space_to_press.space == space


def test_chose_delay_player():
    delay = chose_delay(player_function)
    assert delay == 200


def test_chose_delay_computer():
    delay = chose_delay(computer_function)
    assert delay == 1

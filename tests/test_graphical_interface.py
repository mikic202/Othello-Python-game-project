from Othello_game.Othello_graphical_interface import function_choice, player_function, computer_function
from Othello_game.Othello_graphical_interface import button_colour_change
from Othello_game.Othello_graphical_interface import white, gray, board_size_choice
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

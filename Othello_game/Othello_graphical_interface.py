import pygame
from Othello_board import Board
from Othello_consts import possible_value, first_colour, second_colour, swap_colour
from Othello_main import change_spaces
from random import choice
from Othello_bot import BOT
import os
import sys
from Othello_interface import calculate_result
start_width, start_height = 600, 600
if __name__ == '__main__':
    WIN = pygame.display.set_mode((start_width, start_height))
pygame.display.set_caption("Othello")

pygame.init()
white = (255, 255, 255)
black = (0, 0, 0)
background = (84, 166, 92)
gray = (60, 60, 60)
blue = (53, 168, 230)
empty_space = pygame.image.load(os.path.join('Assets', 'Othello_space.png'))
fps = 40
menu_fps = 20
font = pygame.font.Font('freesansbold.ttf', 13)
title_font = pygame.font.Font('freesansbold.ttf', 32)


class OptionSpace:
    """
    class OptionSpace. Contains atributes:
        :param rect: contains rectangel, created with given position and size, representing space on board
        :type rect: Rect
    """
    def __init__(self, position, space_size) -> None:
        self.rect = pygame.Rect(position[0], position[1], space_size[0], space_size[1])


class SpaceToPress(OptionSpace):
    """
    class SpaceToPress inherits after OptionSpace. Contains atributes:
        :param space: public parameter containing Space object
        :type space: Space

        :param rect: contains rectangel, created with given position and size, representing space on board
        :type rect: Rect
    """
    def __init__(self, position, space_size, space) -> None:
        super().__init__(position, space_size)
        self.space = space


def check_quit():
    """
    function 'watching' if the game was quited using x at upper right corner
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def main_graphic():
    pygame.display.set_icon(pygame.image.load(os.path.join('Assets', 'Othello_icon.png')))
    """
    main function for game that uses graphical interface
    """
    option, size = game_start()
    first_function, second_function = function_choice(option)
    board = Board(size)
    main_game(first_function, second_function, board)
    game_end(board)
    pygame.quit()


def main_game(first_function, second_function, board: Board):
    """
    main function used for game
    """
    delay = 200
    WIN = pygame.display.set_mode((start_width, start_height+30))
    colour = first_colour
    run = True
    checked = False
    clock = pygame.time.Clock()
    comp1 = BOT(board, first_colour)
    comp2 = BOT(board, second_colour)
    while run:
        clock.tick(fps)
        check_quit()
        if not checked:
            WIN.fill(black)
            line_dict, play_pos_dict = board.find_plays(colour)
            if possible_value not in board.board_values():
                colour = swap_colour(colour)
                line_dict, play_pos_dict = board.find_plays(colour)
                if possible_value not in board.board_values():
                    break
            possible_spaces = draw_board(board)
            display_game_information(board, colour)
            pygame.display.update()
            checked = True
        mouse_press = pygame.mouse.get_pressed(3)[0]
        if (mouse_press or first_function == computer_function) and colour == first_colour:
            colour, checked = first_function(possible_spaces, line_dict, play_pos_dict, colour, board, comp1)
            pygame.time.wait(delay)
        elif (mouse_press or second_function == computer_function) and colour == second_colour:
            colour, checked = second_function(possible_spaces, line_dict, play_pos_dict, colour, board, comp2)
            pygame.time.wait(delay)


def draw_text(text, position, font_type, colour, button_size=None):
    """
    function that draws given text in given font and colour in given place on screen
    """
    text_obj = font_type.render(text, True, colour)
    width, height = font_type.size(text)
    pos_x = position[0]-width//2
    pos_y = position[1]-height//2
    if button_size is not None:
        pos_x += button_size[0]//2
        pos_y += button_size[1]//2
    WIN.blit(text_obj, (pos_x, pos_y))


def display_game_information(board: Board, colour):
    """
    this function displays game information about curent game such as:
        - colour playing
        - amount of spaces on board of each colour
    """
    width, height = pygame.display.get_surface().get_size()
    black_spac = 0
    white_spac = 0
    for value in board.board_values():
        if value == first_colour:
            black_spac += 1
        elif value == second_colour:
            white_spac += 1
    playing = f'{"White" if colour == "w" else "Black"}'
    text_scores = font.render(f'Playing: {playing} Scores: Black: {black_spac:3<}  White: {white_spac:3<}', True, white)
    WIN.blit(text_scores, (0, height-20))


def player_function(possible_spaces, line_dict, play_pos_dict, colour, board=None, bot=None):
    """
    function used when game is in player vs player or player vs computer mode
    function takes user feedback and converts it into move on board
    """
    chosen_space = None
    for posib_presed in possible_spaces:
        if posib_presed.rect.collidepoint(pygame.mouse.get_pos()):
            chosen_space = posib_presed.space
            for line, space_num in zip(line_dict[chosen_space], play_pos_dict[chosen_space]):
                change_spaces(colour, line, space_num)
            return swap_colour(colour), False
    return colour, True


def computer_function(possible_spaces, line_dict, play_pos_dict, colour, board, bot):
    """
    function used when game is in computer vs computer or player vs computer mode
    function takes space chosen by computer based on its calculations and converts
    that chosen space into move on board
    """
    size_x, size_y = board.size()
    chosen_space = bot.chose_move(board)
    if chosen_space is None:
        chosen_space = choice(list(line_dict.keys()))
    pos_x, pos_y = chosen_space.place_on_board()
    space_position_in_list = pos_y*size_x + pos_x
    chosen_space = board.board()[space_position_in_list]
    for line, space_num in zip(line_dict[chosen_space], play_pos_dict[chosen_space]):
        change_spaces(colour, line, space_num)
    return swap_colour(colour), False


def draw_board(board: Board):
    """
    function used to display board on screen
    """
    width, height = pygame.display.get_surface().get_size()
    size_x, size_y = board.size()
    space_size = min(width//size_x, (height-30)//size_y)
    empty_space_trans = pygame.transform.scale(empty_space, (space_size, space_size))
    for pos_y in range(size_y):
        for pos_x in range(size_x):
            WIN.blit(empty_space_trans, (pos_x*space_size, pos_y*space_size))
    possible_spaces = draw_space_values(board, space_size)
    draw_circle(board.size(), space_size)
    pygame.display.update()
    return possible_spaces


def draw_space_values(board: Board, space_size):
    """
    function used to display space that have value other than empty
    """
    possible_spaces = list()
    for space in board.board():
        value = set_values(space, space_size)
        if value is not None:
            possible_spaces.append(value)
    return possible_spaces


def draw_circle(size, space_size):
    """
    function draws four circles at the corners of squer created by sixteen central spaces
    """
    size_x, size_y = size
    circle_pos_x = (size_x//2-2, size_x//2+2)
    circle_pos_y = (size_y//2-2, size_y//2+2)
    for pos_x in circle_pos_x:
        for pos_y in circle_pos_y:
            pygame.draw.circle(WIN, black, (pos_x*space_size, pos_y*space_size), 2)


def set_values(space, space_size):
    """
    Displays individual space thats value is not empty
    and if value is possible returns SpaceToPress object
    """
    pos_x, pos_y = space.place_on_board()
    image_dict = {
        possible_value: os.path.join('Assets', 'Othello_space_possible.png'),
        first_colour: os.path.join('Assets', 'Othello_black.png'),
        second_colour: os.path.join('Assets', 'Othello_white.png')}
    if space.value() in image_dict.keys():
        space_value = pygame.image.load(image_dict[space.value()])
        space_value_transform = pygame.transform.scale(space_value, (space_size, space_size))
        WIN.blit(space_value_transform, (pos_x*space_size, pos_y*space_size))
        if space.value() == possible_value:
            return SpaceToPress((pos_x*space_size, pos_y*space_size), (space_size, space_size), space)


def game_start():
    """
    Function that creates starting menu and monitors users choices
    """
    x_value, y_value = (8, 8)
    clock = pygame.time.Clock()
    playervsplayer_pos = (30, 300)
    playervscomp_pos = (210, 300)
    compvscomp_pos = (390, 300)
    start_pos = (210, 500)
    title_pos = (300, 100)
    button_size = (150, 40)
    playervsplayer = OptionSpace(playervsplayer_pos, button_size)
    playervscomp = OptionSpace(playervscomp_pos, button_size)
    compvscomp = OptionSpace(compvscomp_pos, button_size)
    start_button = OptionSpace(start_pos, button_size)
    pvp_col = white
    pvb_col = white
    bvb_col = white
    run = True
    option = 0
    while run:
        width, height = pygame.display.get_surface().get_size()
        clock.tick(menu_fps)
        WIN.fill(background)
        check_quit()
        keys_press = pygame.key.get_pressed()
        x_value, y_value = board_size_choice(keys_press, x_value, y_value)
        size_text = f'Baord Size: X{x_value - x_value % 2:2}    Y{y_value - y_value % 2:2}    '
        if pygame.mouse.get_pressed(3)[0]:
            if playervsplayer.rect.collidepoint(pygame.mouse.get_pos()):
                option = 1
            elif playervscomp.rect.collidepoint(pygame.mouse.get_pos()):
                option = 2
            elif compvscomp.rect.collidepoint(pygame.mouse.get_pos()):
                option = 3
            elif start_button.rect.collidepoint(pygame.mouse.get_pos()) and option != 0:
                return option, (x_value - x_value % 2, y_value - y_value % 2)
        pvp_col, pvb_col, bvb_col = button_colour_change(option)
        pygame.draw.rect(WIN, pvp_col, playervsplayer.rect)
        pygame.draw.rect(WIN, pvb_col, playervscomp.rect)
        pygame.draw.rect(WIN, bvb_col, compvscomp.rect)
        pygame.draw.rect(WIN, white, start_button.rect)
        draw_text('player vs player', (playervsplayer_pos[0], playervsplayer_pos[1]), font, black, button_size)  # PvP
        draw_text('player vs computer', (playervscomp_pos[0], playervscomp_pos[1]), font, black, button_size)  # Pvcomp
        draw_text('computer vs computer', (compvscomp_pos[0], compvscomp_pos[1]), font, black, button_size)  # compVcomp
        draw_text('Start', (start_pos[0], start_pos[1]), font, black, button_size)  # Start
        draw_text('Othello', (title_pos[0], title_pos[1]), title_font, black)  # title
        draw_text(size_text, (width//2, 400), font, black)  # board size
        pygame.display.update()
    pygame.quit()


def function_choice(option):
    """
    function that decides wchich functions will be used in main_game
    based on users choice
    """
    delay = 200
    if option == 1:
        return player_function, player_function
    if option == 2:
        colour_chosen = colour_choice()
        pygame.time.wait(delay)
        if colour_chosen == first_colour:
            return player_function, computer_function
        else:
            return computer_function, player_function
    if option == 3:
        return computer_function, computer_function


def colour_choice():
    """
    function that alows user to chose wchich colour he wants to play
    usefull only in player vs computer mode
    """
    button_size = (150, 40)
    WIN.fill(background)
    first_col_choice = OptionSpace((start_width//4-button_size[0]//2, 250), button_size)
    second_col_choice = OptionSpace((3*start_width//4-button_size[0]//2, 250), button_size)
    pygame.draw.rect(WIN, white, first_col_choice.rect)
    pygame.draw.rect(WIN, white, second_col_choice.rect)
    draw_text('Black', (start_width//4-button_size[0]//2, 250), font, black, button_size)
    draw_text('White', (3*start_width//4-button_size[0]//2, 250), font, black, button_size)
    pygame.display.update()
    while True:
        check_quit()
        if pygame.mouse.get_pressed(3)[0]:
            if first_col_choice.rect.collidepoint(pygame.mouse.get_pos()):
                return first_colour
            elif second_col_choice.rect.collidepoint(pygame.mouse.get_pos()):
                return second_colour


def board_size_choice(keys_press, x_value, y_value):
    """
    function that moitors user input and changes board size value depending on it
    thanks to incrementing size by one start menu can operate in 20 fps while board size increments in 10 fps
    """
    if keys_press[pygame.K_LEFT] and x_value > 8:
        x_value -= 1
    if keys_press[pygame.K_RIGHT] and x_value < 30:
        x_value += 1
    if keys_press[pygame.K_DOWN] and y_value > 8:
        y_value -= 1
    if keys_press[pygame.K_UP] and y_value < 30:
        y_value += 1
    return x_value, y_value


def button_colour_change(option):
    """
    function that changes colour of buttons depending on which is presed
    if button is presed its colour changes to gray
    """
    pvp_col = white
    pvb_col = white
    bvb_col = white
    if option == 1:
        pvp_col = gray
    elif option == 2:
        pvb_col = gray
    elif option == 3:
        bvb_col = gray
    return pvp_col, pvb_col, bvb_col


def game_end(board: Board):
    """
    game end menu
    """
    width, height = pygame.display.get_surface().get_size()
    draw_board(board)
    score, result = calculate_result(board)
    draw_text(score, (width//2, (height)//2-30), title_font, black)
    draw_text(result, (width//2, height//2), title_font, black)
    pygame.display.update()
    run = True
    while run:
        check_quit()


if __name__ == '__main__':
    main_graphic()

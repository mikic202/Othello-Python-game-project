import pygame
from Othello_board import Board
from Othello_consts import possible_value, first_colour, second_colour
from Othello_main import change_spaces
from random import choice
from Othello_bot import BOT
import os
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
delay = 250


class SpaceToPress:
    def __init__(self, position, space_size, space=None) -> None:
        self.space = space
        self.rect = pygame.Rect(position[0], position[1], space_size[0], space_size[1])


class OptionSpace(SpaceToPress):
    def __init__(self, position, space_size) -> None:
        super().__init__(position, space_size, None)


def main_graphic():
    option, size = game_start()
    first_function, second_function = function_choice(option)
    board = Board(size)
    main_game(first_function, second_function, board)
    pygame.time.wait(10)
    pygame.display.update()
    game_end(board)
    pygame.quit()


def change_colour(colour):
    if colour == first_colour:
        return second_colour
    else:
        return first_colour


def main_game(first_function, second_function, board: Board):
    WIN = pygame.display.set_mode((start_width, start_height+30))
    colour = first_colour
    run = True
    checked = False
    clock = pygame.time.Clock()
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        if not checked:
            WIN.fill(black)
            line_dict, play_pos_dict = board.find_plays(colour)
            if possible_value not in board.board_values():
                colour = change_colour(colour)
                line_dict, play_pos_dict = board.find_plays(colour)
                if possible_value not in board.board_values():
                    break
            possible_spaces = draw_board(board)
            display_game_information(board, colour)
            pygame.display.update()
            checked = True
        mouse_press = pygame.mouse.get_pressed(3)[0]
        if (mouse_press or first_function == computer_function) and colour == first_colour:
            colour, checked = first_function(possible_spaces, line_dict, play_pos_dict, colour, board)
            pygame.time.wait(delay)
        elif (mouse_press or second_function == computer_function) and colour == second_colour:
            colour, checked = second_function(possible_spaces, line_dict, play_pos_dict, colour, board)
            pygame.time.wait(delay)


def function_choice(option):
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


def player_function(possible_spaces, line_dict, play_pos_dict, colour, board):
    chosen_space = None
    for posib_presed in possible_spaces:
        if posib_presed.rect.collidepoint(pygame.mouse.get_pos()):
            chosen_space = posib_presed.space
            for line, space_num in zip(line_dict[chosen_space], play_pos_dict[chosen_space]):
                change_spaces(colour, line, space_num)
            return change_colour(colour), False
    return colour, True


def computer_function(possible_spaces, line_dict, play_pos_dict, colour, board):
    bot = BOT(board, colour)
    size_x, size_y = board.size()
    chosen_space = bot.chose_move(board)
    if chosen_space is None:
        chosen_space = choice(list(line_dict.keys()))
    pos_x, pos_y = chosen_space.place_on_board()
    space_position_in_list = pos_y*size_x + pos_x
    chosen_space = board.board()[space_position_in_list]
    for line, space_num in zip(line_dict[chosen_space], play_pos_dict[chosen_space]):
        change_spaces(colour, line, space_num)
    del bot
    return change_colour(colour), False


def draw_board(board: Board):
    width, height = pygame.display.get_surface().get_size()
    size_x, size_y = board.size()
    space_size = min(width//size_x, (height-30)//size_y)
    empty_space_trans = pygame.transform.scale(empty_space, (space_size, space_size))
    for pos_y in range(size_y):
        for pos_x in range(size_x):
            WIN.blit(empty_space_trans, (pos_x*space_size, pos_y*space_size))
    possible_spaces = list()
    for space in board.board():
        value = set_values(space, space_size)
        if value is not None:
            possible_spaces.append(value)
    draw_circle(board.size(), space_size)
    pygame.display.update()
    return possible_spaces


def draw_circle(size, space_size):
    size_x, size_y = size
    circle_pos_x = (size_x//2-2, size_x//2+2)
    circle_pos_y = (size_y//2-2, size_y//2+2)
    for pos_x in circle_pos_x:
        for pos_y in circle_pos_y:
            pygame.draw.circle(WIN, black, (pos_x*space_size, pos_y*space_size), 2)


def set_values(space, space_size):
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
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


def button_colour_change(option):
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
    width, height = pygame.display.get_surface().get_size()
    draw_board(board)
    score, result = calculate_result(board)
    draw_text(score, (width//2, (height)//2-30), title_font, black)
    draw_text(result, (width//2, height//2), title_font, black)
    pygame.display.update()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


def board_size_choice(keys_press, x_value, y_value):
    if keys_press[pygame.K_LEFT] and x_value > 8:
        x_value -= 1
    if keys_press[pygame.K_RIGHT] and x_value < 30:
        x_value += 1
    if keys_press[pygame.K_DOWN] and y_value > 8:
        y_value -= 1
    if keys_press[pygame.K_UP] and y_value < 30:
        y_value += 1
    return x_value, y_value


def display_game_information(board: Board, colour):
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


def colour_choice():
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        if pygame.mouse.get_pressed(3)[0]:
            if first_col_choice.rect.collidepoint(pygame.mouse.get_pos()):
                return first_colour
            elif second_col_choice.rect.collidepoint(pygame.mouse.get_pos()):
                return second_colour


def draw_text(text, position, font_type, colour, button_size=None):
    text_obj = font_type.render(text, True, colour)
    width, height = font_type.size(text)
    pos_x = position[0]-width//2
    pos_y = position[1]-height//2
    if button_size is not None:
        pos_x += button_size[0]//2
        pos_y += button_size[1]//2
    WIN.blit(text_obj, (pos_x, pos_y))


if __name__ == '__main__':
    # display_game_information(Board((8, 8)))
    main_graphic()
    # game_start()
    # game_end(Board((8, 8)))
    # colour_choice()

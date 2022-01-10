import pygame
from Othello_board import Board
from Othello_consts import possible_value, first_colour, second_colour
from Othello_main import change_spaces
from random import choice
from Othello_bot import BOT
import os
from Othello_interface import calculate_result
start_width, start_height = 600, 600
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
    WIN = pygame.display.set_mode((start_width, start_height+30))
    colour = first_colour
    run = True
    checked = False
    clock = pygame.time.Clock()
    board = Board(size)
    while run:
        clock.tick(fps)
        WIN.fill(black)
        # if pygame.display.get_surface().get_size() != previous_win_size:
        #     draw_board(board)
        #     pygame.display.update()
        #     previous_win_size = pygame.display.get_surface().get_size()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        if not checked:
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
    WIN = pygame.display.set_mode((start_width, start_height+30))
    game_end(board)
    pygame.quit()


def change_colour(colour):
    if colour == first_colour:
        return second_colour
    else:
        return first_colour


def function_choice(option):
    if option == 1:
        return player_function, player_function
    if option == 2:
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
    circle_pos_x = (size_x//2-2, size_x//2+2)
    circle_pos_y = (size_y//2-2, size_y//2+2)
    empty_space_trans = pygame.transform.scale(empty_space, (space_size, space_size))
    for pos_y in range(size_y):
        for pos_x in range(size_x):
            WIN.blit(empty_space_trans, (pos_x*space_size, pos_y*space_size))
            if pos_x in circle_pos_x and pos_y in circle_pos_y:
                pygame.draw.circle(WIN, black, (pos_x*space_size, pos_y*space_size), 2)
    possible_spaces = list()
    for space in board.board():
        value = set_values(space, space_size)
        if value is not None:
            possible_spaces.append(value)
    pygame.display.update()
    return possible_spaces


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
    # if space.value() == possible_value:
    #     return (pos_x*space_size, pos_y*space_size)


def game_start():
    x_value, y_value = (8, 8)
    clock = pygame.time.Clock()
    playervsplayer_pos = (30, 300)
    playervscomp_pos = (210, 300)
    compvscomp_pos = (390, 300)
    start_pos = (210, 500)
    title_pos = (300, 100)
    playervsplayer = OptionSpace(playervsplayer_pos, (150, 40))
    playervscomp = OptionSpace(playervscomp_pos, (150, 40))
    compvscomp = OptionSpace(compvscomp_pos, (150, 40))
    start_button = OptionSpace(start_pos, (150, 40))
    text_pvp = font.render('player vs player', True, black)
    text_pvb = font.render('player vs computer', True, black)
    text_bvb = font.render('computer vs computer', True, black)
    text_start = font.render('Start', True, black)
    text_title = title_font.render('Othello', True, black)
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
        text_size = font.render(f'Baord Size: X{x_value - x_value % 2:2}    Y{y_value - y_value % 2:2}', True, black)
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
        WIN.blit(text_pvp, (playervsplayer_pos[0]+22, playervsplayer_pos[1]+15))
        WIN.blit(text_pvb, (playervscomp_pos[0]+15, playervscomp_pos[1]+15))
        WIN.blit(text_bvb, (compvscomp_pos[0]+6, compvscomp_pos[1]+15))
        WIN.blit(text_start, (start_pos[0]+60, start_pos[1]+15))
        WIN.blit(text_title, (title_pos[0]-70, title_pos[1]))
        WIN.blit(text_size, (width//2 - 80, 400))
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
    text_result = title_font.render(result, True, black)
    text_scores = title_font.render(score, True, black)
    WIN.blit(text_result, (width//2 - 16*len(result)/2, height//2))
    WIN.blit(text_scores, (width//2 - 150, (height)//2-30))
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


if __name__ == '__main__':
    # display_game_information(Board((8, 8)))
    main_graphic()
    # game_start()
    # game_end(Board((8, 8)))

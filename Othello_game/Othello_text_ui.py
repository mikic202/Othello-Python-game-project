from Othello_board import Board
from Othello_bot import BOT
from random import choice
from Othello_consts import first_colour, second_colour, possible_value
from Othello_interface import display_board, display_result, start_interface, players_choice


def main():
    """
    main function used to play game using text ui
    """
    chosen_game, board, colour = start_interface()
    if chosen_game == 1:
        pvp_board = board
        first_function = play
        second_function = play
        main_user_vs_user(pvp_board, first_function, second_function)
    elif chosen_game == 3:
        bvb_board = board
        first_function = computer_move
        second_function = computer_move
        main_user_vs_user(bvb_board, first_function, second_function)
    elif chosen_game == 2 and colour == first_colour:
        pvb_board = board
        first_function = play
        second_function = computer_move
        main_user_vs_user(pvb_board, first_function, second_function)
    elif chosen_game == 2 and colour == second_colour:
        bvp_board = board
        second_function = play
        first_function = computer_move
        main_user_vs_user(bvp_board, first_function, second_function)
    return


def play(board: Board, color, bot=None):
    """
    functions that controls chosen by player move and displays board before and after
    player has chosen move
    """
    board.reset_possible()
    line_dict, play_pos_dict = board.find_plays(color)
    space_to_board = dict()
    p_index = 1
    for space in line_dict.keys():
        space_to_board[f'{possible_value}{p_index}'] = space
        max_index = p_index
        p_index += 1
    values_board = format_board_file(board)
    display_board(values_board, board.size())
    chosen_index = players_choice(max_index, color)
    chosen_space = space_to_board[chosen_index]
    for line, space_num in zip(line_dict[chosen_space], play_pos_dict[chosen_space]):
        change_spaces(color, line, space_num)
    board.reset_possible()


def change_spaces(playing, line, positions: list):
    """
    function that changes spaces to playing colour in given line between
    indexes given in position list
    """
    if positions is None:
        return
    elif positions[0] is None:
        line_to_change = line[positions[2]:positions[1]+1]
        for space in line_to_change:
            space.set_value(playing)
    elif positions[1] is None:
        line_to_change = line[positions[0]:positions[2]+1]
        for space in line_to_change:
            space.set_value(playing)
    elif positions is not None:
        line_to_change = line[positions[0]:positions[1]+1]
        for space in line_to_change:
            space.set_value(playing)


def computer_move(board: Board, color, bot):
    """
    function used when game is in computer vs computer or player vs computer mode
    function takes space chosen by computer based on its calculations and converts
    that chosen space into move on board
    """
    size_x, size_y = board.size()
    line_dict, play_pos_dict = board.find_plays(color)
    values_board = format_board_file(board)
    display_board(values_board, board.size())
    chosen_space = bot.chose_move(board)
    if chosen_space is None:
        chosen_space = choice(list(line_dict.keys()))
    pos_x, pos_y = chosen_space.place_on_board()
    space_position_in_list = pos_y*size_x + pos_x
    chosen_space = board.board()[space_position_in_list]
    for line, space_num in zip(line_dict[chosen_space], play_pos_dict[chosen_space]):
        change_spaces(color, line, space_num)
    board.reset_possible()


def format_board_file(board: Board):
    """
    function formats board values list so that there would be possible spaces with indexes
    and values
    """
    values_board = list()
    p_index = 1
    for space in board.board():
        if space.value() == possible_value:
            values_board.append(f'{possible_value}{p_index}')
            p_index += 1
        else:
            values_board.append(f'{space.value():2}')
    return values_board


def main_user_vs_user(uvu_board: Board, first_function, second_function):
    """
    main function used for playing game with given functions
    """
    is_game_ending = [False, False]
    comp1 = BOT(uvu_board, first_colour)
    comp2 = BOT(uvu_board, second_colour)
    while not all(is_game_ending):
        is_game_ending = [False, False]
        uvu_board.find_plays(first_colour)
        if possible_value in uvu_board.board_values():
            first_function(uvu_board, first_colour, comp1)
        elif possible_value not in uvu_board.board_values():
            is_game_ending[0] = True
        uvu_board.find_plays(second_colour)
        if possible_value in uvu_board.board_values():
            second_function(uvu_board, second_colour, comp2)
        elif possible_value not in uvu_board.board_values():
            is_game_ending[1] = True
    display_result(uvu_board)


if __name__ == '__main__':
    main()

from Othello_board import Board
from Othello_consts import possible_value, first_colour, second_colour, swap_colour


class BOT:
    """
        class BOT. Contains atributes:
            param _colour: informs what colour is playing
            type _colour: str

            param _board: contains Board object with curent board
            type _board: Board

            param _weights: cotains information about weights of algoritm
            type _weights: list
    """
    def __init__(self, board: Board, colour) -> None:
        self._colour = colour
        self._board = board
        if colour == first_colour:
            self._weights = [-2, 0, 2, 3, 2, 3, 2]
        elif colour == second_colour:
            self._weights = [-2, 0, 2, 3, 2, 3, 2]

    def board(self):
        """
        Returns _board param
        """
        return self._board

    def colour(self):
        """
        Returns _colour param
        """
        return self._colour

    def weights(self):
        """
        returns _weights param
        """
        return self._weights

    def evaluate_move(self, board):
        """
        function evaluating moves based on starting board,
        inputed board and weights
        """
        play_value = 0
        previous_board = self.board()
        size_x, size_y = board.size()
        second_center_ring_x = range(int(size_x/2-2), int(size_x/2+2))
        second_center_ring_y = range(int(size_y/2-2), int(size_y/2+2))
        spaces_that_are_different = list()
        for space, space_before in zip(board.board(), previous_board.board()):
            if space.value() != space_before.value():
                spaces_that_are_different.append(space)
        played = self._count_spaces_played(board)
        if played <= size_x*size_y/4:
            play_value += self._weights[0]*len(spaces_that_are_different)
        elif played <= size_x*size_y/2:
            play_value += self._weights[1]*len(spaces_that_are_different)
        else:
            play_value += self._weights[2]*len(spaces_that_are_different)
        for space in spaces_that_are_different:
            pos_x, pos_y = space.place_on_board()
            if space.value() == self.colour():
                if (pos_x == size_x/2 or pos_x == size_x/2 - 1) and (pos_y == size_y/2 or pos_y == size_y/2 - 1):
                    play_value += self._weights[3]
                elif pos_x in second_center_ring_x and pos_y in second_center_ring_y:
                    play_value += self._weights[4]
                elif (pos_x == 0 or pos_x == size_x-1) and (pos_y == 0 or pos_y == size_y-1):
                    play_value += self._weights[5]
                elif pos_x == 0 or pos_x == size_x-1 or pos_y == 0 or pos_y == size_y-1:
                    play_value += self._weights[6]
        return play_value

    def chose_move(self, board):
        """
        Function that returns space tahat was chosen by the algoritm
        as the one with the best outcome out of possible spaces
        """
        depth = 3
        best_eval, space = self._min_max_func(board, depth, -float('inf'), float('inf'), True, self.colour(), None)
        return space

    def _min_max_func(self, board: Board, depth, max_move, min_move, is_maximasing, col, space_played):
        """
        internal function used for minmax algorithm with alfa beta pruning
        """
        min_space = None
        max_space = None
        new_board = self._copy_board(board)
        new_board.find_plays(col)
        size_x, size_y = board.size()
        if depth == 0:
            return self.evaluate_move(board), space_played
        elif possible_value not in new_board.board_values():
            return self.evaluate_move(board) + 5, space_played
        if is_maximasing:
            max_eval = -float('inf')
            for space in new_board.board():
                if space.value() == possible_value:
                    pos_x, pos_y = space.place_on_board()
                    space_position_in_list = pos_y*size_x + pos_x
                    test_board = self._copy_board(new_board)
                    line_plays, line_positions = test_board.find_plays(col)
                    space = test_board.board()[space_position_in_list]
                    for line, spcae_num in zip(line_plays[space], line_positions[space]):
                        self.change_spaces(col, line, spcae_num)
                    test_board.reset_possible()
                    new_col = swap_colour(col)
                    evaluated, scor = self._min_max_func(test_board, depth-1, max_move, min_move, False, new_col, space)
                    if max_eval < evaluated:
                        max_eval = evaluated
                        max_move = evaluated
                        max_space = space
                    if(min_move <= max_move):
                        break
            return max_eval, max_space
        else:
            min_eval = float('inf')
            for space in new_board.board():
                if space.value() == possible_value:
                    pos_x, pos_y = space.place_on_board()
                    space_position_in_list = pos_y*size_x + pos_x
                    test_board = self._copy_board(new_board)
                    line_plays, line_positions = test_board.find_plays(col)
                    space = test_board.board()[space_position_in_list]
                    for line, spcae_num in zip(line_plays[space], line_positions[space]):
                        self.change_spaces(col, line, spcae_num)
                    test_board.reset_possible()
                    new_col = swap_colour(col)
                    evaluated, scor = self._min_max_func(test_board, depth-1, max_move, min_move, True, new_col, space)
                    if min_eval > evaluated:
                        min_eval = evaluated
                        min_move = evaluated
                        min_space = space
                    if(min_move <= max_move):
                        break
            return min_eval, min_space

    def _count_spaces_played(self, board: Board):
        """
        returns amount of spaces that already have pieces on them
        """
        played = 0
        for space in board.board():
            if space.value() == first_colour or space.value() == second_colour:
                played += 1
        return played

    def change_spaces(self, playing, line, positions):
        """
        Function that changes spaces that sholuld be changed in result of playing space
        Same function as in main.py but couldn't be imported from that file due to circular
        character of import
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

    def _copy_board(self, board):
        """
        internal function returning Board object identical to inputed board, but not the same adress
        """
        new_board = Board(board.size())
        new_board.set_board_values(board.board_values())
        new_board.reset_possible()
        return new_board

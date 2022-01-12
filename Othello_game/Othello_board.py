from Othello_space import Space
from Othello_consts import first_colour, second_colour, empty_value, possible_value, IncorectSizeError


class Board:
    """
    class Board. Contains atributes:
        :param _size: size of playing board
        :type _size: tuple

        :param _size_x: size of playing board in x dimensions
        :type _size_x: int

        :param _size_y: size of playing board in y dimensions
        :type _size_y: int

        :param _board: list of spaces on board from left to right
        :type _board: list
    """
    def __init__(self, size: tuple) -> None:
        self._size_check(size)
        self._size = size
        self._size_x, self._size_y = size
        self._create_board(size)

    def size(self):
        """
        Returns size of board in form of a tuple
        """
        return self._size

    def board(self):
        """
        Returnd list of spaces on board
        """
        return self._board

    def board_values(self):
        """
        Returns list of values of spaces that are on board
        """
        board_values = list()
        for space in self._board:
            board_values.append(space.value())
        return board_values

    def set_board_values(self, new_board_values):
        """
        Changes value of spaces on board to values of ne_board_values given in form of a list
        """
        for space, value in zip(self._board, new_board_values):
            space.set_value(value)

    def set_space_value(self, space, new_value):
        """
        Changes value of given space to new new_value
        """
        index_x, index_y = space
        self._board[self._size_x*(index_y-1)+index_x-2].set_value(new_value)

    def _size_check(self, size):
        """
        internal function that checks if size is odd and brtween 8 and 30
        """
        size_x, size_y = size
        if size_x < 8 or size_x > 30 or size_x % 2 != 0:
            raise IncorectSizeError('x')
        if size_y < 8 or size_y > 30 or size_y % 2 != 0:
            raise IncorectSizeError('y')

    def _create_board(self, size):
        """
        internal functino that creates starting board
        """
        size_x, size_y = size
        board = list()
        board = [Space((index_x, index_y), empty_value, size)for index_y in range(size_y) for index_x in range(size_x)]
        for space in board:
            space.find_space_around(board)
        self._board = board
        self._assign_starting_point(size)

    def _assign_starting_point(self, size):
        """
        internal function that assigns four starting pices
        """
        size_x, size_y = size
        self._board[size_x*int(size_y/2-1)+size_x//2-1].set_value(second_colour)
        self._board[size_x*int(size_y/2-1)+size_x//2].set_value(first_colour)
        self._board[size_x*int(size_y/2)+size_x//2-1].set_value(first_colour)
        self._board[size_x*int(size_y/2)+size_x//2].set_value(second_colour)

    def _find_possible_spaces(self, playing):
        """
        internal function that checks if there is pices of another colour around
        studied pice
        """
        if playing == first_colour:
            looking = second_colour
        else:
            looking = first_colour
        for space in self._board:
            if_possible = False
            for suraunding in space.space_around():
                if suraunding.value() == looking:
                    if_possible = True
            if if_possible and space.value() == empty_value:
                space.set_value(possible_value)

    def find_plays(self, playing):
        """
        function that looks for spaces wher piece of colour that is playing can be put
        """
        self._find_possible_spaces(playing)
        possible_plays = dict()
        space_line_plays = dict()
        if playing == first_colour:
            looking = second_colour
        else:
            looking = first_colour
        for space in self._board:
            if space.value() == possible_value:
                possible_plays[space] = []
                index_x, index_y = space.place_on_board()
                place_in_list = (index_y)*self._size_x + index_x

                diagonal_positive = self._diagonal_line_positive(place_in_list)
                p_pos = min(self._size_x-index_x-1, index_y)
                where_to_play = self._check_line_for_series_of_spaces(diagonal_positive, looking, playing, p_pos)
                where_to_play = self._check_where_to_play(where_to_play)
                if where_to_play is not None:
                    where_to_play.append(p_pos)
                possible_plays[space].append(where_to_play)

                diagonal_negative = self._diagonal_line_negative(place_in_list)
                p_pos = min(index_x, index_y)
                where_to_play = self._check_line_for_series_of_spaces(diagonal_negative, looking, playing, p_pos)
                where_to_play = self._check_where_to_play(where_to_play)
                if where_to_play is not None:
                    where_to_play.append(p_pos)
                possible_plays[space].append(where_to_play)

                vertical = self._vertical_line(index_x)
                where_to_play = self._check_line_for_series_of_spaces(vertical, looking, playing, index_y)
                where_to_play = self._check_where_to_play(where_to_play)
                if where_to_play is not None:
                    where_to_play.append(index_y)
                possible_plays[space].append(where_to_play)

                horizontal = self._horizontal_line(index_y)
                where_to_play = self._check_line_for_series_of_spaces(horizontal, looking, playing, index_x)
                where_to_play = self._check_where_to_play(where_to_play)
                if where_to_play is not None:
                    where_to_play.append(index_x)
                possible_plays[space].append(where_to_play)

                if self._check_if_all_plays_None(possible_plays[space]):
                    space.set_value(empty_value)
                    possible_plays.pop(space)
                    continue
                space_line_plays[space] = [diagonal_positive, diagonal_negative, vertical, horizontal]
        return space_line_plays, possible_plays

    def _diagonal_line_positive(self, space_pos_in_list):
        """
        internal function that creates list of spaces that are in diagonal line
        going form lower left corner to upper right corner and throught studied space

        """
        part_above = self._board[:space_pos_in_list+1]
        part_belov = self._board[space_pos_in_list:]
        part_above.reverse()
        diagonal_above = part_above[::self._size_x-1]
        diagonal_above = diagonal_above[1:]
        diagonal_above.reverse()
        if len(diagonal_above) > space_pos_in_list // self._size_x:
            diagonal_above = diagonal_above[1:]
        diagonal_belov = part_belov[::self._size_x-1]
        diagonal_line = diagonal_above + diagonal_belov
        if self._size_y-space_pos_in_list % self._size_x < space_pos_in_list // self._size_x + 1:
            diagonal_line.reverse()
            checked = self._check_diagonal(diagonal_line)
            checked.reverse()
            return checked
        return self._check_diagonal(diagonal_line)

    def _diagonal_line_negative(self, space_pos_in_list):
        """
        internal function that creates list of spaces that are in diagonal line
        going form upper left corner to lower right corner and throught studied space
        """
        part_above = self._board[:space_pos_in_list+1]
        part_belov = self._board[space_pos_in_list:]
        part_above.reverse()
        diagonal_above = part_above[::self._size_x+1]
        diagonal_above.reverse()
        diagonal_belov = part_belov[::self._size_x+1]
        diagonal_belov = diagonal_belov[1:]
        diagonal_line = diagonal_above + diagonal_belov
        if space_pos_in_list % self._size_x > space_pos_in_list // self._size_x + 1:
            checked = self._check_diagonal(diagonal_line)
            return checked
        diagonal_line.reverse()
        final_line = self._check_diagonal(diagonal_line)
        final_line.reverse()
        return final_line

    def _vertical_line(self, row_num):
        """
        internal function that creates list of spaces that are in the
        same row as studied space
        """
        return self._board[row_num::self._size_x]

    def _horizontal_line(self, line_num):
        """
        internal function that creates list of spaces that are
        in the same line as studied space
        """
        return self._board[line_num*self._size_x:(line_num+1)*self._size_x]

    def _check_diagonal(self, space_list):
        """
        internal function that checks if there are spaces in list which one of positions is
        different from correct ones by over one
        """
        final_line = None
        condition = 1
        for index in range(len(space_list)):
            if index != 0:
                condition = space_list[index].place_on_board()[0] - space_list[index-1].place_on_board()[0]
            if (condition != 1 and condition != -1) and final_line is None:
                final_line = space_list[:index]
        if final_line is None:
            final_line = space_list
        return final_line

    def _check_line_for_series_of_spaces(self, line, looking, playing, p_pos):
        """
        internal function that serches for plays that will change at least one pice
        """
        line = self._split_line(line, p_pos)
        result = list()
        line[0].reverse()
        for part in line:
            is_in_line = False
            index_to_play = None
            for space in part:
                if space.value() == looking:
                    is_in_line = True
                elif space.value() != looking and not is_in_line or (space.value() != playing and is_in_line):
                    break
                elif space.value() == playing and is_in_line:
                    index_to_play = part.index(space)
                    break
            result.append(index_to_play)
        if result[0] is not None:
            result[0] = len(line[0])-result[0]-1
        if result[1] is not None:
            result[1] = len(line[0])+result[1]+1
        return result

    def _split_line(self, line, p_position):
        """
        internal function that splits line into two pices,
        without p_position element
        """
        return line[:p_position], line[p_position+1:]

    def _check_where_to_play(self, where_to_play):
        """
        internal function that checks if all elements in list are None
        """
        if all(play is None for play in where_to_play):
            return None
        else:
            return where_to_play

    def reset_possible(self):
        """
        function that resets all spaces which have possible value yo empty value
        """
        for space in self._board:
            space.reset_if_possible()

    def _check_if_all_plays_None(self, plays_list):
        return all(play is None for play in plays_list)

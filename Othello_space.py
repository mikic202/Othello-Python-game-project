from Othello_consts import (
    first_colour, second_colour, possible_value, empty_value,
    IncorectSpacePositionError, IncorectSpaceValueError)


class Space:
    """
    class Space. Contains atributes:
        :param _place_on_board: spaces position x and y in board in range from 0 to board size - 1
        :type _place_on_board: tuple

        :param _value: indicates what value is in this space
        :type _vlaue: str

        :param _board_size: stores size of board containging space
        :type _board_size: tuple

        :param _spaces_around: stores inforamtion about spaces around that space
        :type _spaces_around: list of Space
    """
    def __init__(self, place_on_board: tuple, value: str, board_size: tuple) -> None:
        # place_on_board is in range o 0 to board_size-1
        self._check_place_on_board(place_on_board, board_size)
        self._place_on_board = place_on_board
        self._check_value(value)
        self._value = value
        self._board_size = board_size
        self._spaces_around = list()

    def place_on_board(self):
        """
        Returns spaces _place_on_board atribute in form of a tuple,
        that informs what is spaces place on board
        """
        return self._place_on_board

    def value(self):
        """
        Returns _value atribute contained by space in form of a str
        """
        return self._value

    def board_size(self):
        """
        Returns _board_size
        """
        return self._board_size

    def set_value(self, new_value):
        """
        Changes _value atribute of Space to new_value given at the start of function
        """
        self._check_value(new_value)
        self._value = new_value

    def _check_value(self, value):
        """
        Internal function used to check if given value is in values that space could be set to
        """
        possible_values = [first_colour, second_colour, empty_value, possible_value]
        if value not in possible_values:
            raise IncorectSpaceValueError

    def _check_place_on_board(self, place, board_size):
        """
        internal function used to check if any of spaces position in board isn't bigger than board dimensions
        """
        place_x, place_y = place
        size_x, size_y = board_size
        if place_x < 0 or place_x >= size_x:
            raise IncorectSpacePositionError('x')
        if place_y < 0 or place_y >= size_y:
            raise IncorectSpacePositionError('y')

    def space_around(self):
        """
        Function returns _spaces_around atribute which is list of Space objects
        which are next to space on board
        """
        return self._spaces_around

    def find_space_around(self, list_of_spaces):
        """
        Function reqires list of spaces that are in the board
        asigns list of Space object that are next to space on board in form of a list
        and returns that list
        """
        place_x, place_y = self._place_on_board
        size_x, size_y = self._board_size
        place_in_list = place_x + size_x * place_y
        if place_x == 0 and place_y == 0:
            self._find_spaces_around_upper_left_corner(size_x, list_of_spaces)
        elif place_x == size_x - 1 and place_y == 0:
            self._find_spaces_around_upper_right_corner(size_x, list_of_spaces)
        elif place_x == 0 and place_y == size_y - 1:
            self._find_spaces_around_lower_left_corner(size_x, size_y, list_of_spaces)
        elif place_x == size_x - 1 and place_y == size_y - 1:
            self._find_spaces_around_lower_right_corner(size_x, size_y, list_of_spaces)
        elif place_x == 0:
            self._find_spaces_around_left_border(size_x, place_in_list, list_of_spaces)
        elif place_x == size_x - 1:
            self._find_spaces_around_right_border(size_x, place_in_list, list_of_spaces)
        elif place_y == 0:
            self._find_spaces_around_upper_border(size_x, place_in_list, list_of_spaces)
        elif place_y == size_y - 1:
            self._find_spaces_around_lower_border(size_x, place_in_list, list_of_spaces)
        else:
            self._find_spaces_around_center(size_x, place_in_list, list_of_spaces)
        return self._spaces_around

    def _find_spaces_around_upper_left_corner(self, size_x, list_of_spaces):
        """
        internal function used to find Space objects next to space inboard if space is in upper left corner
        """
        self._spaces_around.append(list_of_spaces[1])
        self._spaces_around.append(list_of_spaces[size_x])
        self._spaces_around.append(list_of_spaces[size_x + 1])

    def _find_spaces_around_upper_right_corner(self, size_x, list_of_spaces):
        """
        internal function used to find Space objects next to space inboard if space is in upper right corner
        """
        self._spaces_around.append(list_of_spaces[size_x - 2])
        self._spaces_around.append(list_of_spaces[2 * size_x - 2])
        self._spaces_around.append(list_of_spaces[2 * size_x - 1])

    def _find_spaces_around_lower_left_corner(self, size_x, size_y, list_of_spaces):
        """
        internal function used to find Space objects next to space inboard if space is in lower left corner
        """
        self._spaces_around.append(list_of_spaces[(size_y - 2) * size_x])
        self._spaces_around.append(list_of_spaces[(size_y - 2) * size_x + 1])
        self._spaces_around.append(list_of_spaces[(size_y - 1) * size_x + 1])

    def _find_spaces_around_lower_right_corner(self, size_x, size_y, list_of_spaces):
        """
        internal function used to find Space objects next to space inboard if space is in lower right corner
        """
        self._spaces_around.append(list_of_spaces[(size_y - 1) * size_x - 2])
        self._spaces_around.append(list_of_spaces[(size_y - 1) * size_x - 1])
        self._spaces_around.append(list_of_spaces[size_y*size_x - 2])

    def _find_spaces_around_left_border(self, size_x, place_in_list, list_of_spaces):
        """
        internal function used to find Space objects next to space inboard if space is next to left border
        """
        self._spaces_around.append(list_of_spaces[place_in_list - size_x])
        self._spaces_around.append(list_of_spaces[place_in_list - size_x + 1])
        self._spaces_around.append(list_of_spaces[place_in_list + 1])
        self._spaces_around.append(list_of_spaces[place_in_list + size_x])
        self._spaces_around.append(list_of_spaces[place_in_list + size_x + 1])

    def _find_spaces_around_right_border(self, size_x, place_in_list, list_of_spaces):
        """
        internal function used to find Space objects next to space inboard if space is next to right border
        """
        self._spaces_around.append(list_of_spaces[place_in_list - size_x - 1])
        self._spaces_around.append(list_of_spaces[place_in_list - size_x])
        self._spaces_around.append(list_of_spaces[place_in_list - 1])
        self._spaces_around.append(list_of_spaces[place_in_list + size_x - 1])
        self._spaces_around.append(list_of_spaces[place_in_list + size_x])

    def _find_spaces_around_upper_border(self, size_x, place_in_list, list_of_spaces):
        """
        internal function used to find Space objects next to space inboard if space is next to upper border
        """
        self._spaces_around.append(list_of_spaces[place_in_list - 1])
        self._spaces_around.append(list_of_spaces[place_in_list + 1])
        self._spaces_around.append(list_of_spaces[place_in_list + size_x - 1])
        self._spaces_around.append(list_of_spaces[place_in_list + size_x])
        self._spaces_around.append(list_of_spaces[place_in_list + size_x + 1])

    def _find_spaces_around_lower_border(self, size_x, place_in_list, list_of_spaces):
        """
        internal function used to find Space objects next to space inboard if space is next to lower border
        """
        self._spaces_around.append(list_of_spaces[place_in_list - size_x - 1])
        self._spaces_around.append(list_of_spaces[place_in_list - size_x])
        self._spaces_around.append(list_of_spaces[place_in_list - size_x + 1])
        self._spaces_around.append(list_of_spaces[place_in_list - 1])
        self._spaces_around.append(list_of_spaces[place_in_list + 1])

    def _find_spaces_around_center(self, size_x, place_in_list, list_of_spaces):
        """
        internal function used to find Space objects next to space inboard if space is in center
        """
        self._spaces_around.append(list_of_spaces[place_in_list - size_x - 1])
        self._spaces_around.append(list_of_spaces[place_in_list - size_x])
        self._spaces_around.append(list_of_spaces[place_in_list - size_x + 1])
        self._spaces_around.append(list_of_spaces[place_in_list - 1])
        self._spaces_around.append(list_of_spaces[place_in_list + 1])
        self._spaces_around.append(list_of_spaces[place_in_list + size_x - 1])
        self._spaces_around.append(list_of_spaces[place_in_list + size_x])
        self._spaces_around.append(list_of_spaces[place_in_list + size_x + 1])

    def reset_if_possible(self):
        """
        function that sets spaces _value atribute if _value is equal to possible_value
        """
        if self.value() == possible_value:
            self._value = empty_value


if __name__ == '__main__':
    pos = Space((1, 2), 'b', (4, 4))
    print(pos.find_space_around([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]))

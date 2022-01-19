first_colour = 'b'
second_colour = 'w'
possible_value = 'p'
empty_value = '#'


def swap_colour(colour):
    """
    function swaping colour to opposite one
    """
    if colour == first_colour:
        return second_colour
    else:
        return first_colour

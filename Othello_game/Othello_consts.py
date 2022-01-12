first_colour = 'b'
second_colour = 'w'
possible_value = 'p'
empty_value = '#'


class IncorectSpaceValueError(ValueError):
    pass


class IncorectSpacePositionError(ValueError):
    def __init__(self, axis) -> None:
        super().__init__(f'Incorect position value on {axis} axis')


class IncorectSizeError(ValueError):
    def __init__(self, axis) -> None:
        super().__init__(f'{axis} axis size has incorect value')


class TooManyIncorectTriesError(TypeError):
    pass

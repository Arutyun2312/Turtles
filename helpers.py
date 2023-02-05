import math
import operator

import arcade

class Vector(list):
    def __new__(cls, *args):
        return super().__new__(cls, args)
    def __init__(self, *args):
        if len(args) == 0: raise Exception('Must pass something to vector')
        if len(args) == 1:
            try:
                self.__init__(*iter(args[0]))
            except TypeError:
                self.__init__(args[0], args[0])
            return
        super().__init__(args)

    def apply(self, o, func):
        if isinstance(o, (int, float)):
            o = self.__class__(*[o for _ in self])
        if len(o) != len(self): raise Exception('Must be same dimension')
        return self.__class__(*[func(left, right) for left, right in zip(self, o)])
    
    def distance_to(self, v):
        return sum((x1 - x2) ** 2 for x1, x2 in zip(self, v)) ** 0.5

    def __eq__(self, o): return o and all(left == right for left, right in zip(self, o))
    def __hash__(self): return hash(tuple(self))
    
    def __add__(self, o): return self.apply(o, operator.add)
    def __mul__(self, o): return self.apply(o, operator.mul)
    def __truediv__(self, o): return self.apply(o, operator.truediv)
    def __neg__(self): return self * -1
    def __sub__(self, o): return self + -o

class Position(Vector):
    x = property(operator.itemgetter(0))
    y = property(operator.itemgetter(1))

class Size(Vector):
    width = property(operator.itemgetter(0))
    height = property(operator.itemgetter(1))

def is_inside(location: Position, size: Size, p: Position):
    return location.x <= p.x and p.x <= location.x + size.width and location.y <= p.y and p.y <= location.y + size.height 

def grid_like_iteration(size: Size):
    for x in range(size.width):
        for y in range(size.height):
            yield Position(x, y)

def angle(position: Position):
    if position == (0, 0): return 0
    x, y = position
    return int(math.atan2(y, x) * 180 / math.pi) - 90

def in_rect(x: int, y: int, width: int, height: int, point: tuple[int, int]):
    p_x, p_y = point
    return x <= p_x and p_x <= x + width and y <= p_y and p_y <= y + height 

def is_valid_index(size: Size, position: Position):
    return in_rect(0, 0, size.width - 1, size.height - 1, tuple(position))


if 0: from main import Game

def game() -> 'Game': return arcade.window_commands.get_window()
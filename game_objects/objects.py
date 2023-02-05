import arcade
from astar import AStar
from helpers import Position

class GridObject:
    def __init__(self, sprite: arcade.Sprite, need_ground=False, can_be_eaten=False, clickable=True):
        self.sprite = sprite
        self.need_ground = need_ground
        self.can_be_eaten = can_be_eaten
        self.clickable = clickable
        self.position = Position(0, 0)
        self.direction = Position(0, 0)

class Apple(GridObject):
    def __init__(self):
        super().__init__(arcade.Sprite('media/apple.png'), True, True)

class EmptySpace(GridObject):
    def __init__(self, clickable=True):
        super().__init__(arcade.Sprite('media/grass.png'), can_be_eaten=True, clickable=clickable)

class Obstacle(GridObject):
    def __init__(self):
        super().__init__(arcade.Sprite('media/obstacle.png'))

class Turtle(GridObject):
    def __init__(self):
        super().__init__(arcade.Sprite('media/turtle.png'), True)
        self.astar: AStar = None
        self.ai = False
        self.color = arcade.color.WHITE
        self.score = 0
        self.name = f'Turtle {id(self)}'
    
    def create_astar(self):
        self.astar = AStar(self.position)


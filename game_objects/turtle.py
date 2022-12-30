import arcade
from game_objects.grid_object import GridObject

class Turtle(GridObject):
    def __init__(self, name: str):
        super().__init__(arcade.Sprite('media/turtle.png'), True, can_be_marked=False)
        self.name = name

import arcade
from game_objects.grid_object import GridObject

class Apple(GridObject):
    def __init__(self):
        super().__init__(arcade.Sprite('media/apple.png'), True, True)
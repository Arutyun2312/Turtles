import arcade
from game_objects.grid_object import GridObject

class EmptySpace(GridObject):
    def __init__(self, clickable=True):
        super().__init__(arcade.Sprite('media/grass.png'), can_be_eaten=True, clickable=clickable)
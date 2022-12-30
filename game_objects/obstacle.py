import arcade
from game_objects.grid_object import GridObject

class Obstacle(GridObject):
    def __init__(self):
        super().__init__(arcade.Sprite('media/obstacle.png'))
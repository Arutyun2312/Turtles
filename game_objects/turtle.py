import arcade
import arcade.color
from game_objects.grid_object import GridObject
from astar import AStar

class Turtle(GridObject):
    def __init__(self, name: str, color: arcade.Color = arcade.color.WHITE, ai=False):
        super().__init__(arcade.Sprite('media/turtle.png'), True)
        self.name = name
        self.astar: AStar = None
        self.color = color
        self.ai = ai
    
    def reset_astar(self, current_position: tuple[int, int], apple_position: tuple[int, int], grid: list[list[int]]):
        self.astar = AStar(current_position, apple_position, grid)

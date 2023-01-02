import arcade.gui
from game_objects.grid_object import GridObject
from game_objects.grid import Grid
from game_objects.turtle import Turtle
from game_objects.apple import Apple
from game_objects.obstacle import Obstacle

class PresetItem:
    def __init__(self, obj: GridObject, position: tuple[int, int]):
        self.obj = obj
        self.position = position
    
    @classmethod
    def multiply(self, create_obj: GridObject, *positions: tuple[int, int]):
        for pos in positions:
            yield PresetItem(create_obj(), pos)

    def setup_grid(self, grid: Grid):
        x, y = self.position
        grid.set_position(self.obj, x, y)

class Preset:
    def __init__(self, name: str, *items: PresetItem):
        self.name = name
        self.items = items

    def setup_grid(self, grid: Grid):
        for item in self.items:
            item.setup_grid(grid)

presets = [
    Preset(
        'Default', 
        PresetItem(Apple(), (5, 5)),
        PresetItem(Turtle('Turtle 1'), (1, 2)),
        PresetItem(Turtle('Turtle 2'), (6, 9)),
        *PresetItem.multiply(lambda: Obstacle(), (0, 0), (0, 2), (0, 4), (0, 6), (1, 1), (1, 3))
    ),
    Preset(
        'Hard', 
        PresetItem(Apple(), (5, 5)),
        PresetItem(Turtle('Turtle 1'), (1, 2)),
        PresetItem(Turtle('Turtle 2'), (6, 9)),
        *PresetItem.multiply(lambda: Obstacle(), (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5))
    ),
]

def create_maze_presets_ui():    
    h_box = arcade.gui.UIBoxLayout(vertical=False)

    h_box.add(child)
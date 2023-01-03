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
    def __init__(self, name: str, *items: PresetItem, size=(10, 10)):
        self.name = name
        self.items = items
        self.size = size

    def setup_grid(self, grid: Grid):
        grid.create(self.size[0], self.size[1])
        for item in self.items:
            item.setup_grid(grid)

presets = [
    Preset(
        'Easy', 
        PresetItem(Apple(), (5, 5)),
        PresetItem(Turtle('Turtle 1'), (0, 0)),
        PresetItem(Turtle('Turtle 2'), (9, 9)),
        *PresetItem.multiply(lambda: Obstacle(), (0, 1), (0, 2), (0, 4), (0, 5), (0,8), (0,9), (1,9), (1,8), (1,7), (2,7), (2,5), 
        (3,5), (2,0), (2,1), (2,3), (2,4), (4,4), (2,4), (0,4), (8,9), (7,7),(7,4), (7,5), (7,2), (6,2),
        (5,2), (4,2), (6,4), (4,6), (6,6), (6,8), (3,9), (9,1), (9,2), (9,4), (9,5), (3,9), (4,0), (5,0),
        (6,0), (7,0), (4,8), (7,3), (9,7))
    ),
     Preset(
        'Hard', 
        PresetItem(Apple(), (5, 4)),
        PresetItem(Turtle('Turtle 1'), (0, 5)),
        PresetItem(Turtle('Turtle 2'), (9, 4)),
        *PresetItem.multiply(lambda: Obstacle(), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7), (1,8),
        (8,1), (8,2), (8,3), (8,4), (8,5), (8,6), (8,7), (1,8), (2,8), (3,8), (4,8), (5,8), (6,8), (8,8),
        (1,1), (3,1), (4,1), (5,1), (6,1), (7,1), (8,1), (3,3), (4,3), (5,3), (6,3),
        (3,6), (4,6), (5,6), (6,6), (3,4), (6,4), (4,4), (8,9), (1,0), (7,6), (2,3), (0,0), (9,9)),
        size=(20, 20)
     ),
     Preset(
        'No Solution', 
        PresetItem(Apple(), (4, 4)),
        PresetItem(Turtle('Turtle 1'), (0, 9)),
        PresetItem(Turtle('Turtle 2'), (9, 0)),
        *PresetItem.multiply(lambda: Obstacle(), (4,6), (5,6), (6,6), (5,5), (5,4), (6,4), (4,5), (4,6), (6,5), (6,6),
        (0,5), (1,5), (2,5), (3,5), (4,5), (7,5), (8,5), (9,5), (5,0), (5,1), (5,2), (5,3), (5,7), (5,8), (5,9),
        (0,0), (1,1), (2,2), (3,3), (7,7), (8,8), (9,9), (1,8), (2,7), (3,6), (6,3), (7,2), (8,1), (0,3), (1,2), (2,1), (3,0),
        (7,8), (8,7), (6,9), (9,6), (0,4), (1,4), (2,4), (3,4), (8,4), (7,4), (9,4), (4,0), (4,1), (4,2), (4,3))

    ),
    Preset(
        'Medium', 
        PresetItem(Apple(), (8, 5)),
        PresetItem(Turtle('Turtle 1'), (0, 0)),
        PresetItem(Turtle('Turtle 2'), (0, 9)),
        *PresetItem.multiply(lambda: Obstacle(), (9,4), (9,5), (9,6), (7,4), (7,5), (7,6),
        (1,9), (2,8), (3,7), (1,0), (2,1), (3,2), (0,4), (0,6), (1,5), (0,2), (1,3), (4,5),
        (0,3), (1,4), (0,5), (2,4), (3,4), (0,7), (1,6), (2,5), (4,4), (5,4), (6,4),
        (5,2), (6,1), (7,0), (9,2), (9,0), (6,8), (7,8), (5,8), (4,9), (2,9), (6,5),
        (8,8), (5,5), (5,6), (2,0), (3,0), (5,0), (6,0), (3,5), (8,2))
    ),
       Preset(
        'Hard', 
        PresetItem(Apple(), (5, 5)),
        PresetItem(Turtle('Turtle 1'), (0, 0)),
        PresetItem(Turtle('Turtle 2'), (0, 9)),
        *PresetItem.multiply(lambda: Obstacle(), (0, 1))

    ),
]

def create_maze_presets_ui():    
    h_box = arcade.gui.UIBoxLayout(vertical=False)

    h_box.add(child)
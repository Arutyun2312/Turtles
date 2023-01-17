from game_objects.grid import Grid
from game_objects.grid_object import GridObject


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
        grid.set_position(self.obj, (x, y), True)

class Preset:
    def __init__(self, name: str, *items: PresetItem, size=(10, 10)):
        self.name = name
        self.items = items
        self.size = size

    def setup_grid(self, grid: Grid):
        grid.create(self.size[0], self.size[1])
        for item in self.items:
            item.setup_grid(grid)

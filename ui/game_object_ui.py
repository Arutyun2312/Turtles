from game_objects.grid_object import GridObject
from game_objects.grid import Grid
from game_objects.turtle import Turtle
from ui.turtle_ui import create_turtle_ui
import arcade.gui

def create_game_object_ui(grid: Grid, obj: GridObject):
    if isinstance(obj, Turtle):
        return create_turtle_ui(grid, obj)
    else:
        v_box = arcade.gui.UIBoxLayout()

        label = arcade.gui.UILabel(text=f'{obj.__class__.__name__}: {obj.name}', width=100)
        v_box.add(label)

        return v_box
from game_objects.empty import EmptySpace
from game_objects.grid_object import GridObject
from game_objects.grid import Grid
from game_objects.obstacle import Obstacle
from game_objects.turtle import Turtle
from ui.turtle_ui import create_turtle_ui
import arcade.gui

def create_game_object_ui(grid: Grid, obj: GridObject, on_set):
    if isinstance(obj, Turtle):
        return create_turtle_ui(grid, obj)
    else:
        v_box = arcade.gui.UIBoxLayout()

        label = arcade.gui.UILabel(text=f'{obj.__class__.__name__}: {obj.name}', width=100)
        v_box.add(label)

        apple_button = arcade.gui.UIFlatButton(width=100, text='Set Apple')
        apple_button.on_click = lambda _ : grid.set_apple_pos(grid.get_position(obj))
        v_box.add(apple_button)

        if isinstance(obj, EmptySpace):
            set_obstacle_button = arcade.gui.UIFlatButton(width=100, text='Set Obstacle')
            def on_click(_):
                grid.set_position(Obstacle(), grid.get_position(obj), True)
                on_set()
            set_obstacle_button.on_click = on_click
            v_box.add(set_obstacle_button)
        elif isinstance(obj, Obstacle):
            set_obstacle_button = arcade.gui.UIFlatButton(width=100, text='Set Empty Space')
            def on_click(_):
                grid.set_position(EmptySpace(), grid.get_position(obj), True)
                on_set()
            set_obstacle_button.on_click = on_click
            v_box.add(set_obstacle_button)

        return v_box
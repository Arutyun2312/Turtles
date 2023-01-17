from game_objects.turtle import Turtle
from game_objects.grid import Grid
import arcade.gui
import arcade

def create_turtle_ui(grid: Grid, turtle: Turtle):
    v_box = arcade.gui.UIBoxLayout()

    label = arcade.gui.UILabel(text=f'Turtle: {turtle.name}')
    v_box.add(label)

    def reset_turtle_astar():
        turtle.reset_astar(grid.get_position(turtle), grid.get_position(grid.apple) if grid.apple else None, grid.create_astar_maze())

    def select_turtle():
        if not turtle.astar: reset_turtle_astar()
        grid.target_astar = turtle.astar

    next_step_button = arcade.gui.UIFlatButton(text="Calculate next step", width=100)
    def on_click(_):
        select_turtle()
        turtle.astar.next_step()
    next_step_button.on_click = on_click
    v_box.add(next_step_button)

    all_steps_button = arcade.gui.UIFlatButton(text="Calculate all steps", width=100)
    def calculate_all_steps():
        select_turtle()
        while not turtle.astar.is_done:
            turtle.astar.next_step()
    all_steps_button.on_click = lambda _ : calculate_all_steps()
    v_box.add(all_steps_button)

    reset_astar_button = arcade.gui.UIFlatButton(text="Reset A*", width=100)
    def reset_astar():
        reset_turtle_astar()
        select_turtle() 
    reset_astar_button.on_click = lambda _ : reset_astar()
    v_box.add(reset_astar_button)

    automate_button = arcade.gui.UIFlatButton(text='Automate', width=100)
    def automate():
        if not grid.apple: return
        reset_turtle_astar()
        calculate_all_steps()
        path = iter(turtle.astar.path)
        turtle.automated = True
        def schedule(_):
            if not turtle.automated or not grid.apple:
                turtle.automated = False
                arcade.unschedule(schedule)
                automate()
                return
            try:
                x, y = next(path)
            except StopIteration:
                turtle.automated = False
                return
            grid.set_position(turtle, (x, y))
        arcade.schedule(schedule, 0.8)
    automate_button.on_click = lambda _ : automate()
    v_box.add(automate_button)

    return v_box

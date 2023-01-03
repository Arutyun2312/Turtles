from game_objects.turtle import Turtle
from game_objects.grid import Grid
from game_objects.apple import Apple
import arcade.gui

def create_turtle_ui(grid: Grid, turtle: Turtle):
    v_box = arcade.gui.UIBoxLayout()

    label = arcade.gui.UILabel(text=f'Turtle: {turtle.name}')
    v_box.add(label)

    go_up_button = arcade.gui.UIFlatButton(text="UP", width=100)
    go_up_button.on_click = lambda _ : grid.move_up(turtle)
    v_box.add(go_up_button)

    h_box = arcade.gui.UIBoxLayout(vertical=False)

    go_right_button = arcade.gui.UIFlatButton(text="LEFT", width=100)
    go_right_button.on_click = lambda _ : grid.move_left(turtle)
    h_box.add(go_right_button)

    go_left_button = arcade.gui.UIFlatButton(text="RIGHT", width=100)
    go_left_button.on_click = lambda _ : grid.move_right(turtle)
    h_box.add(go_left_button)

    v_box.add(h_box)

    go_up_button = arcade.gui.UIFlatButton(text="DOWN", width=100)
    go_up_button.on_click = lambda _ : grid.move_down(turtle)
    v_box.add(go_up_button)

    def reset_turtle_astar():
        turtle.reset_astar(grid.get_position(turtle), grid.get_position(grid.apple), grid.create_astar_maze())

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
    def on_click1(_):
        select_turtle()
        while not turtle.astar.is_done:
            turtle.astar.next_step()
    all_steps_button.on_click = on_click1
    v_box.add(all_steps_button)

    reset_astar_button = arcade.gui.UIFlatButton(text="Reset A*", width=100)
    def on_click2(_):
        reset_turtle_astar()
        select_turtle() 
    reset_astar_button.on_click = on_click2
    v_box.add(reset_astar_button)

    # calculate_button = arcade.gui.UIFlatButton(text="Calculate path", width=100)
    # def on_calculate_path(_):
    #     apple = grid.find_first(Apple)
    #     if not apple: return
    #     grid.marked = astar(grid.create_astar_maze(), grid.get_position(turtle), grid.get_position(apple))
    # calculate_button.on_click = on_calculate_path
    # v_box.add(calculate_button)

    return v_box

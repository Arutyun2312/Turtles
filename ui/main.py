import arcade 
from typing import Callable 

class MainUI:
    def __init__(self, on_up: Callable, on_down: Callable, on_right: Callable, on_left: Callable, on_calculate_path: Callable):
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout()

        go_up_button = arcade.gui.UIFlatButton(text="UP", width=100)
        go_up_button.on_click = on_up
        self.v_box.add(go_up_button)

        self.h_box = arcade.gui.UIBoxLayout(vertical=False)

        go_right_button = arcade.gui.UIFlatButton(text="LEFT", width=100)
        go_right_button.on_click = on_left
        self.h_box.add(go_right_button)

        go_left_button = arcade.gui.UIFlatButton(text="RIGHT", width=100)
        go_left_button.on_click = on_right
        self.h_box.add(go_left_button)

        self.v_box.add(self.h_box)

        go_up_button = arcade.gui.UIFlatButton(text="DOWN", width=100)
        go_up_button.on_click = on_down
        self.v_box.add(go_up_button)

        calculate_button = arcade.gui.UIFlatButton(text="Calculate path", width=100)
        calculate_button.on_click = on_calculate_path
        self.v_box.add(calculate_button)

        quit_button = arcade.gui.UIFlatButton(text="Quit", width=100)
        quit_button.on_click = lambda _ : arcade.exit()
        self.v_box.add(quit_button)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="right",
                anchor_y="center_y",
                child=self.v_box
            )
        )
    
    def draw(self):
        self.manager.draw()
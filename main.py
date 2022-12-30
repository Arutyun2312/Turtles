import arcade
import arcade.gui
from game_objects.grid import Grid
from game_objects.turtle import Turtle
from game_objects.obstacle import Obstacle
from game_objects.apple import Apple
from astar import astar

# Set constants for the screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Set the background color to white.
# For a list of named colors see:
# http://arcade.academy/arcade.color.html
# Colors can also be specified in (red, green, blue) format and
# (red, green, blue, alpha) format.

# Start the render process. This must be done before any drawing commands.

# Draw the face
# x = 300
# y = 300
# radius = 200
# arcade.draw_circle_filled(x, y, radius, arcade.color.YELLOW)

# # Draw the right eye
# x = 370
# y = 350
# radius = 20
# arcade.draw_circle_filled(x, y, radius, arcade.color.BLACK)

# # Draw the left eye
# x = 230
# y = 350
# radius = 20
# arcade.draw_circle_filled(x, y, radius, arcade.color.BLACK)

# # Draw the smile
# x = 300
# y = 280
# width = 120
# height = 100
# start_angle = 190
# end_angle = 350
# arcade.draw_arc_outline(x, y, width, height, arcade.color.BLACK, start_angle, end_angle, 10)

class MyGame(arcade.Window):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.grid = Grid(10, 10)
        turtle = Turtle('hi')
        self.grid.set_position(turtle, 1, 2)
        apple_block = [(4, 5), (6, 5), (5, 4)]
        for x, y in [(0, 0), (0, 2), (0, 4), (0, 6), (1, 1), (1, 3)] + apple_block:
            self.grid.set_position(Obstacle(), x, y)
        
        apple = Apple()
        self.grid.set_position(apple, 5, 5)

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Set background color
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the buttons
        go_up_button = arcade.gui.UIFlatButton(text="UP", width=100)
        go_up_button.on_click = lambda _ : self.grid.move_up(turtle)
        self.v_box.add(go_up_button)

        self.h_box = arcade.gui.UIBoxLayout(vertical=False)

        go_right_button = arcade.gui.UIFlatButton(text="LEFT", width=100)
        go_right_button.on_click = lambda _ : self.grid.move_left(turtle)
        self.h_box.add(go_right_button)

        go_left_button = arcade.gui.UIFlatButton(text="RIGHT", width=100)
        go_left_button.on_click = lambda _ : self.grid.move_right(turtle)
        self.h_box.add(go_left_button)

        self.v_box.add(self.h_box)

        go_up_button = arcade.gui.UIFlatButton(text="DOWN", width=100)
        go_up_button.on_click = lambda _ : self.grid.move_down(turtle)
        self.v_box.add(go_up_button)

        calculate_button = arcade.gui.UIFlatButton(text="Calculate path", width=100)
        def on_click(_):
            maze = list(map(lambda row : list(map(lambda o : bool(isinstance(o, Obstacle)), row)), self.grid.grid))
            self.grid.marked = astar(maze, self.grid.get_position(turtle), self.grid.get_position(apple))
        calculate_button.on_click = on_click
        self.v_box.add(calculate_button)

        quit_button = arcade.gui.UIFlatButton(text="Quit", width=100)
        quit_button.on_click = lambda _ : arcade.exit()
        self.v_box.add(quit_button)

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="right",
                anchor_y="center_y",
                child=self.v_box
            )
        )

    def on_click_start(self, event):
        print("Start:", event)
    
    def setup(self):
        # Set up your game here
        pass

    def on_draw(self):
        self.clear()
        arcade.start_render()
        self.manager.draw()
        self.grid.draw(20, SCREEN_HEIGHT - Grid.px_height * self.grid.height - 30)

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        pass


game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
game.setup()
arcade.run()

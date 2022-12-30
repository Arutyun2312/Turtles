import arcade
import arcade.gui
from game_objects.grid import Grid
from game_objects.turtle import Turtle
from game_objects.obstacle import Obstacle
from game_objects.apple import Apple
from astar import astar
from ui.main import MainUI

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

class MyGame(arcade.Window):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.grid = Grid(10, 10)
        turtle = Turtle('hi')
        self.grid.set_position(turtle, 1, 2)
        # apple_block = [(4, 5), (6, 5), (5, 4)]
        # Set obstacles here :)
        obstacles = [(0, 0), (0, 2), (0, 4), (0, 6), (1, 1), (1, 3)]
        for x, y in obstacles:
            self.grid.set_position(Obstacle(), x, y)
        
        apple = Apple()
        self.grid.set_position(apple, 5, 5)
        
        def on_calculate_path_click(_):
            self.grid.marked = astar(self.grid.create_astar_maze(), self.grid.get_position(turtle), self.grid.get_position(apple))

        self.mainUI = MainUI(
            lambda _ : self.grid.move_up(turtle),
            lambda _ : self.grid.move_down(turtle),
            lambda _ : self.grid.move_right(turtle),
            lambda _ : self.grid.move_left(turtle),
            on_calculate_path_click
        )
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

    def on_draw(self):
        self.clear()
        arcade.start_render()
        self.mainUI.draw()
        self.grid.draw(20, SCREEN_HEIGHT - Grid.px_height * self.grid.height - 30)

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        pass


game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()

import arcade
from game_objects.grid_object import GridObject
from game_objects.grid import Grid
from ui.main_ui import create_main_ui
from utils import in_rect
from ui.game_object_ui import create_game_object_ui
from ui.maze_presets import presets

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600

class MyGame(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.grid = Grid(10, 10)
        self.grid.offset_x = 250
        self.grid.offset_y = SCREEN_HEIGHT - Grid.px_height * self.grid.height - 30
        
        presets[1].setup_grid(self.grid)
        
        self.selectedUI: GridObject | None = None
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.create_ui()

    def on_draw(self):
        self.clear(arcade.color.DARK_BLUE_GRAY)
        self.manager.draw()
        self.grid.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        for obj_x, obj_y, obj in self.grid.objects():
            if not obj.clickable: continue
            obj_x, obj_y = self.grid.get_px_position(obj_x, obj_y)
            obj_x -= Grid.px_width / 2
            obj_y -= Grid.px_height / 2
            if not in_rect(obj_x, obj_y, Grid.px_width, Grid.px_height, (x, y)): continue
            self.selectedUI = obj
            self.create_ui()
            return

    def create_ui(self):
        self.manager.clear()
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="center_y",
                child=create_main_ui()
            )
        )
        if self.selectedUI:
            self.manager.add(
                arcade.gui.UIAnchorWidget(
                    anchor_x="right",
                    anchor_y="center_y",
                    child=create_game_object_ui(self.grid, self.selectedUI)
                )
            )

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        pass

MyGame().run()

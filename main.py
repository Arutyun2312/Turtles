import arcade
import arcade.gui
import arcade.key as Keys
from game_objects.grid_object import GridObject
from game_objects.grid import Grid
from game_objects.turtle import Turtle
from ui.main_ui import create_main_ui
from ui.maze_presets_ui import create_maze_presets_ui
from utils import in_rect
from ui.game_object_ui import create_game_object_ui
from ui.maze_presets import presets

class MyGame(arcade.Window):

    def __init__(self):
        super().__init__(1100, 850)
        self.grid = Grid()
        presets[0].setup_grid(self.grid)
        self.selectedUI: GridObject | None = None
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.create_ui()

    def on_draw(self):
        self.clear(arcade.color.DARK_BLUE_GRAY)
        self.manager.draw()

        self.grid.offset_x = 200
        self.grid.offset_y = self.height - self.grid.px_height * self.grid.height - 30
        self.grid.draw()

    def on_mouse_press(self, x, y, button, modifiers): 
        for obj_x, obj_y, obj in self.grid.objects():
            if not obj.clickable: continue
            obj_x, obj_y = self.grid.get_px_position(obj_x, obj_y)
            obj_x -= self.grid.px_width / 2
            obj_y -= self.grid.px_height / 2
            if not in_rect(obj_x, obj_y, self.grid.px_width, self.grid.px_height, (x, y)): continue
            self.selectedUI = obj
            self.create_ui()
            return

    def on_key_press(self, symbol, modifiers):
        if not isinstance(self.selectedUI, Turtle): return
        match symbol:
            case Keys.UP:
                self.grid.move_up(self.selectedUI)
            case Keys.DOWN:
                self.grid.move_down(self.selectedUI)
            case Keys.LEFT:
                self.grid.move_left(self.selectedUI)
            case Keys.RIGHT:
                self.grid.move_right(self.selectedUI)
            
        return super().on_key_press(symbol, modifiers)

    def create_ui(self):
        self.manager.clear()
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="center_y",
                child=create_main_ui()
            ) 
        )
        def on_selected():
            self.selectedUI = None
            self.create_ui()
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center",
                anchor_y="bottom",
                child=create_maze_presets_ui(self.grid, on_selected)
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

MyGame().run()

import arcade
import arcade.gui
import arcade.key as Keys
from game_objects.apple import Apple
from game_objects.grid_object import GridObject
from game_objects.grid import Grid
from ui.maze_presets_ui import create_maze_presets_ui
from utils import in_rect
from ui.game_object_ui import create_game_object_ui
from ui.maze_presets import presets

class MyGame(arcade.Window):

    def __init__(self):
        super().__init__(900, 900, 'Maze Munch')
        self.grid = Grid()
        presets[0].setup_grid(self.grid)
        self.selectedUI: GridObject | None = None
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.create_ui()
        self.step_sound = arcade.load_sound('media/step.wav')
        self.apple_sound = arcade.load_sound('media/apple.wav')
        self.wall_sound = arcade.load_sound('media/wall.wav')
        self.grid.on_move = lambda obj : (self.apple_sound.play(volume=0.2), self.grid.set_apple_pos()) if isinstance(obj, Apple) else self.step_sound.play(volume=0.2)
        self.grid.on_hit = lambda : self.wall_sound.play()
        arcade.load_sound('media/background.wav').play(volume=0.2, loop=True)

    def on_draw(self):
        self.clear(arcade.color.DARK_BLUE_GRAY)
        self.manager.draw()

        self.grid.offset_x = 50
        self.grid.offset_y = self.height - self.grid.px_height * self.grid.height - 30
        self.grid.draw()
        arcade.draw_rectangle_outline(
            self.grid.offset_x + self.grid.px_width * self.grid.width / 2, 
            self.grid.offset_y + self.grid.px_height * self.grid.height / 2, 
            self.grid.px_width * self.grid.width, 
            self.grid.px_height * self.grid.height, 
            arcade.color.BLACK, 3
        )

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
        turtle1, turtle2, *_ = list(sorted(self.grid.turtles(), key=lambda t: t.name)) + [None]
        match symbol:
            case Keys.W:
                self.grid.move_up(turtle1)
            case Keys.S:
                self.grid.move_down(turtle1)
            case Keys.A:
                self.grid.move_left(turtle1)
            case Keys.D:
                self.grid.move_right(turtle1)

            case Keys.UP:
                self.grid.move_up(turtle2)
            case Keys.DOWN:
                self.grid.move_down(turtle2)
            case Keys.LEFT: 
                self.grid.move_left(turtle2)
            case Keys.RIGHT:
                self.grid.move_right(turtle2)
            
        return super().on_key_press(symbol, modifiers)

    def create_ui(self):
        self.manager.clear()
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




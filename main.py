from random import choice
import arcade
import arcade.gui
import arcade.key as Keys
from game_objects.apple import Apple
from game_objects.empty import EmptySpace
from game_objects.grid_object import GridObject
from game_objects.grid import Grid
from game_objects.obstacle import Obstacle
from game_objects.turtle import Turtle
from ui.maze_presets_ui import create_maze_presets_ui
from utils import in_rect
from ui.game_object_ui import create_game_object_ui
from ui.maze_presets import presets

class Game(arcade.Window):

    def __init__(self):
        super().__init__(950, 850, 'Maze Munch')
        self.grid = Grid()
        presets[0].setup_grid(self.grid)
        self.block_ai = False
        self.selectedUI: GridObject | None = None
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.score: dict[str, int] = {}
        self.create_ui()
        self.step_sound = arcade.load_sound('media/step.wav')
        self.apple_sound = arcade.load_sound('media/apple.wav')
        self.wall_sound = arcade.load_sound('media/wall.wav')
        self.grid.on_move = self.on_move
        self.grid.on_hit = lambda : self.wall_sound.play()
        # arcade.load_sound('media/background.wav').play(volume=0.2, loop=True)

    def on_draw(self):
        self.clear(arcade.color.DARK_BLUE_GRAY)
        self.manager.draw()

        self.grid.offset_x = (self.width - self.grid.px_size) / 2
        self.grid.offset_y = self.height - self.grid.px_height * self.grid.height - 30
        self.grid.draw()
        arcade.draw_rectangle_outline(
            self.grid.offset_x + self.grid.px_width * self.grid.width / 2, 
            self.grid.offset_y + self.grid.px_height * self.grid.height / 2, 
            self.grid.px_width * self.grid.width, 
            self.grid.px_height * self.grid.height, 
            arcade.color.BLACK, 3
        )

    def on_move(self, old_obj: GridObject, new_obj: GridObject):
        if isinstance(old_obj, Apple):
            self.apple_sound.play(volume=0.2)
            self.grid.set_apple_pos()
        else:
            self.step_sound.play(volume=0.2)
        
        if isinstance(new_obj, Turtle) and isinstance(old_obj, Apple):
            self.score[new_obj.name] = self.score.get(new_obj.name, 0) + 1
            self.create_ui()

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
        if modifiers == Keys.MOD_SHIFT and symbol == Keys.C:
            obstacles = ((x, y) for x, y, obj in self.grid.objects() if isinstance(obj, Obstacle))
            print(', '.join(map(lambda pos: f'({pos[0]}, {pos[1]})', obstacles)))
            return
        
        if modifiers == Keys.MOD_COMMAND and symbol == Keys.R:
            self.create_ui()
            return

        if modifiers == Keys.MOD_COMMAND and symbol == Keys.N:
            pos = choice((x, y) for x, y, obj in self.grid.objects() if isinstance(obj, EmptySpace))
            return

        turtle1, turtle2, *_ = list(sorted(self.grid.turtles(), key=lambda t: t.name)) + [None]
        if symbol == Keys.W:
                self.grid.move_up(turtle1)
        elif symbol == Keys.S:
                self.grid.move_down(turtle1)
        elif symbol == Keys.A:
                self.grid.move_left(turtle1)
        elif symbol == Keys.D:
                self.grid.move_right(turtle1)
        elif symbol == Keys.UP:
                self.grid.move_up(turtle2)
        elif symbol == Keys.DOWN:
                self.grid.move_down(turtle2)
        elif symbol == Keys.LEFT:
                self.grid.move_left(turtle2)
        elif symbol == Keys.RIGHT:
                self.grid.move_right(turtle2)
            
        return super().on_key_press(symbol, modifiers)

    def create_ui(self):
        self.manager.clear()
        def on_selected():
            self.selectedUI = None
            self.score = dict(map(lambda t: (t.name, 0), self.grid.turtles()))
            self.create_ui()
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center",
                anchor_y='bottom',
                child=create_maze_presets_ui(self.grid, on_selected, self.score)
            )
        )
        if self.selectedUI:
            def on_set(): 
                self.selectedUI = None 
                self.create_ui()
            self.manager.add(
                arcade.gui.UIAnchorWidget(
                    anchor_x="right",
                    anchor_y="center_y",
                    child=create_game_object_ui(self.grid, self.selectedUI, on_set)
                )
            )
        
    def unblock(self): 
        self.block_ai = False
        arcade.unschedule(self.unblock)

    def on_update(self, delta_time: float):
        if self.block_ai: return
        if not self.selectedUI or not isinstance(self.selectedUI, Turtle) or not self.selectedUI.ai: return
        apple = self.grid.apple
        if not apple: return
        # turtle = t for t in self.grid.turtles() if t.ai 
        # turtle.reset_astar(self.grid.get_position(turtle), self.grid.get_position(apple), self.grid.create_astar_maze())
        # pos = next(turtle.astar.path, None)
        # if pos:
        #     self.grid.set_position(turtle, pos)
        #     self.block_ai = True
        #     arcade.schedule(self.unblock, 0.7)

Game().run()

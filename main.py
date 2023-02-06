from random import choice
import arcade
import arcade.gui
import arcade.key as Keys
from astar_drawer import AStarDrawer
from game_objects.objects import *
from game_objects.grid import Grid
from helpers import *
from ui.main_ui import MainUI
from ui.manager import UIManager
from ui.game_object_ui import *
import pyglet

class Game(arcade.Window):
    grid = Grid()
    floor = Grid()
    astar_drawer = AStarDrawer([grid, floor])
    selectedUI: GridObject | None = None
    block_ai = False
    step_sound = arcade.load_sound('media/step.wav')
    apple_sound = arcade.load_sound('media/apple.wav')
    wall_sound = arcade.load_sound('media/wall.wav')

    def __init__(self):
        super().__init__(850, 850, 'Maze Munch', resizable=True)
        self.grid.on_move = self.on_move
        self.grid.on_hit = self.on_hit
        self.silent = False
        self.manager = UIManager()
        self.mainUI = MainUI()
        self.old_apple_position: Position = None
        # arcade.load_sound('media/background.wav').play(volume=0.2, loop=True)
    
    @property
    def size(self): return Size(self.width, self.height)

    def on_resize(self, width: float, height: float):
        self.astar_drawer.update_positions()
        return super().on_resize(width, height)

    def on_draw(self):
        self.clear()
        if self.grid.size != self.floor.size:
            spaces = []
            for x, y in grid_like_iteration(self.grid.size):
                space = EmptySpace(False)
                space.position = Position(x, y)
                spaces.append(space)
            self.floor.create(*self.grid.size, spaces)
        self.astar_drawer.draw()
        self.floor.draw()
        self.grid.draw()
        if self.manager.current:
            arcade.draw_rectangle_filled(self.width / 2, self.height / 2, self.width, self.height, [*arcade.color.BLACK, 255 / 2])
            self.manager.draw()

    def on_hit(self):
        if self.silent: return
        self.wall_sound.play()

    def on_move(self, old_obj: GridObject, new_obj: GridObject):
        if self.silent: return
        if isinstance(old_obj, Apple):
            self.apple_sound.play(volume=0.2)
            self.grid.apple.position = choice([pos for pos in grid_like_iteration(self.grid.size) if not self.grid[pos]])
        else:
            self.step_sound.play(volume=0.2)

        if isinstance(new_obj, Turtle) and isinstance(old_obj, Apple):
            new_obj.score += 1
            if isinstance(self.manager.current, TurtleUI):
                self.manager.rerender()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.manager.current: return
        mouse_position = Position(x, y)
        for obj in self.grid:
            px_position = self.grid.node_px_position(obj.position) - self.grid.node_px_size / 2
            if not is_inside(px_position, self.grid.node_px_size, mouse_position): continue
            if isinstance(obj, Turtle):
                self.manager.push(TurtleUI(obj))
            elif isinstance(obj, Obstacle):
                self.manager.push(ObstacleUI(obj))
            return
        
        self.manager.push(EmptySpaceUI(mouse_position))

    def on_key_press(self, symbol, modifiers):
        super().on_key_press(symbol, modifiers)

        if symbol == Keys.S and modifiers == Keys.MOD_COMMAND:
            pyglet.image.get_buffer_manager().get_color_buffer().save('image.png')
            return
        
        self.manager.on_key_press(symbol, modifiers)
        if self.manager.current: return

        turtle1, turtle2, *_ = list(sorted((t for t in self.grid.turtles if not t.ai), key=lambda t: t.name)) + [None, None]
        mapped_symbol = {Keys.W: Keys.UP, Keys.S: Keys.DOWN, Keys.A: Keys.LEFT, Keys.D: Keys.RIGHT}.get(symbol, symbol)
        turtle = turtle1 if mapped_symbol == symbol else turtle2
        if turtle:
            if mapped_symbol == Keys.UP:
                self.grid.set_position(turtle, turtle.position + (0, 1))
            elif mapped_symbol == Keys.DOWN:
                self.grid.set_position(turtle, turtle.position + (0, -1))
            elif mapped_symbol == Keys.LEFT:
                self.grid.set_position(turtle, turtle.position + (-1, 0))
            elif mapped_symbol == Keys.RIGHT:
                self.grid.set_position(turtle, turtle.position + (1, 0))
        
    def unblock(self, _): 
        self.block_ai = False
        arcade.unschedule(self.unblock)

    def on_update(self, delta_time):
        if self.block_ai: return
        turtle = next((t for t in self.grid.turtles if t.ai), None)
        if not turtle: return
        if self.old_apple_position != self.grid.apple.position:
            self.old_apple_position = self.grid.apple.position
            turtle.create_astar()
        turtle.astar.all_steps(turtle.position)
        if len(turtle.astar.path) > 1:
            self.grid.set_position(turtle, turtle.astar.path[1])
        self.block_ai = True
        arcade.schedule(self.unblock, 0.5)

Game().run()

from pathlib import Path
import arcade.color as Color
from game_objects.objects import *
from ui.manager import *
import arcade.gui as gui
import json
from helpers import *

def get_name(path: Path): return path.name[:path.name.index('.')]

ext = '.maze'
maze_directory = Path('./mazes')
maze_directory.mkdir(exist_ok=True)
default_maze = maze_directory.joinpath('default.maze')

with open(default_maze, 'w') as file:
    file.write("""
{
    "apple": [2,4],
    "obstacles": [],
    "size": [5, 5],
    "turtles": [[2,2]]
}
    """)

class MainUI(UIManagerRepresent):
    def __init__(self):
        super().__init__()
        self.text_field = UITextField(width=200, text='default')
        def text_changed(name): self.opened_path = maze_directory.joinpath(f'{name}{ext}')
        self.text_field.text_changed = text_changed
        self.click_open_preset(default_maze)
        self.game.silent = True
        self.game.silent = False

    def setup_ui(self):
        box = v_stack(self.list)
        yield gui.UIAnchorWidget(child=box, anchor_x='center', anchor_y='center')
    
    @property
    def list(self):
        yield self.create_button('Stop all ai', self.click_stop_all_ai)
        if self.opened_path:
            yield self.create_label(f'Opened Maze: {self.opened_path.name}')
        yield h_stack(
            self.sizer('Width', 0), 
            self.sizer('Height', 1)
        )
        if self.opened_path:
            yield h_stack(
                [self.text_field.with_space_around(bg_color=Color.WHITE)],
                [self.create_button('Save', self.click_save)]
            )
        yield gui.UISpace(height=50)
        yield self.create_label('Available mazes')
        for path in maze_directory.iterdir():
            if path.is_file() and ext in path.name:
                def create_click(path): 
                    return lambda: self.click_open_preset(path)
                yield self.create_button(f'Open: {get_name(path)}', create_click(path), 300)

    def sizer(self, name: str, i: int):
        def change(by: int): 
            self.game.grid.size[i] += by
            self.refresh()
        yield self.create_label(f'{name}: {self.game.grid.size[i]}')
        yield self.create_button('-', lambda: change(-1), width=50)
        yield self.create_button('+', lambda: change(1), width=50)
    
    def click_open_preset(self, path: Path):
        with open(path) as file:
            size, objects = json.load(file, object_hook=self.object_hook)
        self.game.grid.create(*size, objects)
        self.opened_path = path
        self.text_field.text = get_name(path)
        self.game.astar_drawer.astar = None
        self.pop()

    def click_save(self):
        turtles = []
        obstacles = []
        apple = self.game.grid.apple.position
        for obj in self.game.grid:
            if isinstance(obj, Turtle):
                turtles.append(obj.position)
            if isinstance(obj, Obstacle):
                obstacles.append(obj.position)
        with open(self.opened_path, 'w') as file:
            json.dump({ 'turtles': turtles, 'obstacles': obstacles, 'apple': apple, 'size': self.game.grid.size }, file, sort_keys=True, indent=4)
        self.pop()

    def click_stop_all_ai(self):
        for turtle in self.game.grid.turtles:
            if turtle.ai: turtle.ai = False
    
    def object_hook(self, dct: dict):
        objects: list[GridObject] = []
        for pos in dct['turtles']:
            turtle = Turtle()
            turtle.position = Position(pos)
            objects.append(turtle)
        for pos in dct['obstacles']:
            ob = Obstacle()
            ob.position = Position(pos)
            objects.append(ob)
        apple = Apple()
        apple.position = Position(dct['apple'])
        objects.append(apple)
        return Size(*dct['size']), objects

class UITextField(gui.UIInputText):
    old = None

    def on_update(self, dt):
        if self.text != self.old:
            self.old = self.text
            self.text_changed(self.text)
        return super().on_update(dt)

    def text_changed(self, text: str): pass

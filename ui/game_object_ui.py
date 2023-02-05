import arcade.gui as gui
from game_objects.objects import *
from helpers import Position
from ui.manager import UIManagerRepresent, populate, v_stack

class ObstacleUI(UIManagerRepresent):
    def __init__(self, obj: Obstacle):
        super().__init__()
        self.obj = obj

    def setup_ui(self):
        box = populate(gui.UIBoxLayout(), self.list)
        yield gui.UIAnchorWidget(child=box, anchor_x='center', anchor_y='center')

    @property
    def list(self):
        yield self.create_label(f'{self.obj.__class__.__name__}')
        yield self.create_button('Remove', self.click_set_empty, key_press=self.keys.SPACE)

    def click_set_empty(self):
        self.game.grid.remove(self.obj)
        self.game.manager.pop()

class EmptySpaceUI(UIManagerRepresent):
    def __init__(self, mouse_position: Position):
        super().__init__()
        x, y = mouse_position / self.game.grid.node_px_size
        self.grid_position = Position(int(x), int(y))

    def setup_ui(self):
        box = populate(gui.UIBoxLayout(), self.list)
        yield gui.UIAnchorWidget(child=box, anchor_x='center', anchor_y='center')

    @property
    def list(self):
        yield self.create_label('Empty Space')
        yield self.create_button('Set Obstacle (Space)', self.click_set_obstacle, width=200, key_press=self.keys.SPACE)
        yield self.create_button('Set Apple (A)', self.click_set_apple, key_press=self.keys.A)
        yield self.create_button('Set Turtle (T)', self.click_set_turtle, key_press=self.keys.T)

    def click_set_obstacle(self):
        obj = Obstacle()
        obj.position = self.grid_position
        self.game.grid.append(obj)
        self.game.manager.pop()

    def click_set_apple(self):
        self.game.grid.apple.position = self.grid_position
        self.game.manager.pop()

    def click_set_turtle(self):
        turtle = Turtle()
        turtle.position = self.grid_position
        self.game.grid.append(turtle)
        self.game.manager.pop()


class TurtleUI(UIManagerRepresent):
    def __init__(self, turtle: Turtle):
        super().__init__()
        self.turtle = turtle
        self.grid = self.game.grid

    def setup_ui(self):
        yield gui.UIAnchorWidget(child=v_stack(self.list), anchor_x='center', anchor_y='center')
    
    @property
    def list(self):
        yield self.create_label(f'Turtle. Score: {self.turtle.score}')
        yield self.create_button('Calculate next step', self.click_calculate_next)
        yield self.create_button('Calculate all steps', self.click_calculate_all_steps)
        yield self.create_button('Reset A*', self.click_reset_astar)
        yield self.create_button('Automate', self.click_automate)
    
    def click_calculate_next(self):
        self.select_turtle()
        self.turtle.astar.next_step()
        self.update()
    
    def click_calculate_all_steps(self):
        self.turtle.create_astar()
        self.select_turtle()
        while not self.turtle.astar.is_done:
            self.turtle.astar.next_step()
        self.update()
    
    def click_reset_astar(self):
        self.game.astar_drawer.astar = None
        self.turtle.astar = None
        self.turtle.ai = False
        self.update()

    def update(self):
        self.game.astar_drawer.update_texts()
        self.game.grid.update(True)
        self.game.floor.update(True)
    
    def click_automate(self):
        self.turtle.ai = not self.turtle.ai
        if self.turtle.ai: self.turtle.create_astar()

    def select_turtle(self):
        if not self.turtle.astar: self.turtle.create_astar()
        self.game.astar_drawer.astar = self.turtle.astar
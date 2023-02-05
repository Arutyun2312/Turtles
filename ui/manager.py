from typing import Callable, Generator, Iterable
import arcade
import arcade.gui
import arcade.key as Keys
from itertools import chain

from helpers import game

class UIManagerRepresent: 
    def __init__(self): 
        self.game = game()
        self.dict = {}
        self.keys = Keys

    def setup_ui(self) -> Generator[arcade.gui.UIWidget, None, None]: yield
    
    def create_button(self, text: str, on_click: Callable[[], None], width=100, key_press=None):
        button = arcade.gui.UIFlatButton(text=text, width=width,)
        button.on_click = lambda _ : on_click()
        if key_press:
            self.dict[key_press] = on_click
        return button

    def create_label(self, text: str):
        return arcade.gui.UILabel(text=text, font_size=24)

    def pop(self): self.game.manager.pop()

    def refresh(self):
        ui = self.game.manager.current
        self.game.manager.pop()
        self.game.manager.push(ui)

    def on_key_press(self, symbol: int, modifiers: int): 
        if self.dict.get(symbol, None):
            self.dict[symbol]()

class UIManager:
    manager = None

    def __init__(self):
        self.presented: list[UIManagerRepresent] = []
        self.game = game()

    def push(self, value: UIManagerRepresent): 
        self.presented.append(value)
        self.rerender()
    
    def pop(self):
        if not len(self.presented): return
        self.presented.pop()
        self.rerender()
    
    def close(self):
        self.presented = []
        self.rerender()
    
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == Keys.LEFT and modifiers == Keys.MOD_COMMAND:
            self.pop()
            return
        if symbol == Keys.ESCAPE:
            if self.current:
                self.close()
            else:
                self.push(self.game.mainUI)
            return
        if self.current:
            self.current.on_key_press(symbol, modifiers)

    @property
    def current(self): return self.presented[-1] if len(self.presented) else None

    def rerender(self):
        if self.manager: self.manager.clear()
        if not self.current: return
        self.manager = arcade.gui.UIManager(auto_enable=True)
        for ui in self.current.setup_ui():
            self.manager.add(ui)    
    
    def draw(self):
        if not self.current: return
        self.manager.draw()

def populate(box: arcade.gui.UIBoxLayout | arcade.gui.UIManager, *iters: Iterable[Iterable[arcade.gui.UIWidget]]):
    for ui in chain(*iters): 
        box.add(ui)
    return box

def v_stack(*iters: Iterable[Iterable[arcade.gui.UIWidget]]):
    box = arcade.gui.UIBoxLayout()
    box._space_between = 10
    return populate(box, *iters)

def h_stack(*iters: Iterable[Iterable[arcade.gui.UIWidget]]):
    box = arcade.gui.UIBoxLayout()
    box._space_between = 10
    box.vertical = False
    return populate(box, *iters)

import arcade
import arcade.gui

class GridObject:
    def __init__(self, sprite: arcade.Sprite, need_ground=False, can_be_eaten=False, clickable=True, name=''):
        self.sprite = sprite
        self.need_ground = need_ground
        self.can_be_eaten = can_be_eaten
        self.last_position: tuple(int, int) | None = None
        self.clickable = clickable
        self.name = name

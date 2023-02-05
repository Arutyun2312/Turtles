import arcade
from game_objects.objects import *
from helpers import *

class Grid:
    def __init__(self):
        self.sprite_list = arcade.SpriteList(capacity=100)
        self.objects: list[GridObject] = []
        self.size = Size(0, 0)
        self.offset = Size(0, 0)
        self.semi_transparent: list[Position] = []

    def __getitem__(self, key: Position): return next((obj for obj in self.objects if obj.position == key), None)
    
    def create(self, width: int, height: int, objs: list[GridObject]):
        self.size = Size(width, height)
        self.sprite_list.clear()
        self.objects.clear()
        self.sprite_list.extend([obj.sprite for obj in objs])
        self.objects += objs
        self.update(True)

    def can_go(self, pos: Position):
        return is_valid_index(self.size, pos) and (not self[pos] or self[pos].can_be_eaten)

    def remove(self, obj: GridObject):
        self.objects.remove(obj)
        self.sprite_list.remove(obj.sprite)

    def append(self, obj: GridObject):
        self.objects.append(obj)
        self.sprite_list.append(obj.sprite)

    def __iter__(self): return iter(self.objects)

    @property
    def turtles(self):
        return (obj for obj in self if isinstance(obj, Turtle))

    @property
    def apple(self):
        return next(obj for obj in self.objects if isinstance(obj, Apple))
    
    def set_position(self, obj: GridObject, position: Position):
        obj.direction = position - obj.position
        if self.can_go(position):
            self.on_move(self[position], obj)
            obj.position = position
        else:
            self.on_hit()
    
    def calculate_price(self, position: Position): return 1 if isinstance(self[position], Obstacle) or not self.can_go(position) else 0

    def node_px_position(self, position: Position): return (position + 0.5) * self.node_px_size

    @property
    def node_px_size(self): return Size(*arcade.window_commands.get_window().size) / self.size

    def update(self, full_update=False):
        for node in self:
            node.sprite.width, node.sprite.height = self.node_px_size
            node.sprite.position = self.node_px_position(node.position)
            node.sprite.angle = angle(node.direction)
            if full_update or isinstance(node, Turtle) or len(self.semi_transparent) == 0:
                node.sprite.alpha = 255 / 2 if node.position in self.semi_transparent else 255

    def draw(self):
        self.update()
        self.sprite_list.draw()
    
    def on_move(self, old_obj: GridObject, new_obj: GridObject): pass
    def on_hit(self): pass

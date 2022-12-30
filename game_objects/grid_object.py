import arcade

class GridObject:
    def __init__(self, sprite: arcade.Sprite, need_ground=False, can_be_eaten=False, can_be_marked=True):
        self.sprite = sprite
        self.need_ground = need_ground
        self.can_be_eaten = can_be_eaten
        self.last_position: Optional[tuple(int, int)] = None
        self.can_be_marked = can_be_marked
        self.marked = False

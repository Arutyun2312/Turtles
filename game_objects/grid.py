import arcade
from game_objects.empty import EmptySpace
from game_objects.grid_object import GridObject
from game_objects.obstacle import Obstacle

def empty(n: int):
    return list(map(lambda _: EmptySpace(), range(n)))


class Grid:
    max_px_size = 50

    def __init__(self):
        self.width = 0
        self.height = 0
        self.grid: list[list[GridObject]] = []
        self.marked: list[tuple[int, int]] = []
        self.offset_x = self.offset_y = 0
        self.px_width = self.px_height = 50
    
    def create(self, width: int, height: int): 
        self.grid = list(map(lambda _: empty(width), empty(height)))
        self.width = width
        self.height = height
        ratio = 10 / width
        self.px_width = Grid.max_px_size * ratio
        self.px_height = Grid.max_px_size * ratio 

    def can_go(self, x: int, y: int):
        return 0 <= x and x < self.width and 0 <= y and y < self.height and self.grid[x][y].can_be_eaten
        
    def objects(self):
        for x, row in enumerate(self.grid):
            for y, node in enumerate(row):
                yield x, y, node
    
    def find_first(self, class_or_tuple):
        for _, _, obj in self.objects():
            if isinstance(obj, class_or_tuple):
                return obj
        return None

    def set_position(self, obj, x: int, y: int):
        if not self.can_go(x, y):
            return False
        self.__remove_from_grid(obj)
        self.grid[x][y] = obj
        return True

    def get_position(self, obj):
        for x, row in enumerate(self.grid):
            for y, node in enumerate(row):
                if node is obj:
                    return x, y
        raise Exception(f'{obj} is not in the grid')

    def __move(self, obj, dx: int, dy: int):
        x, y = self.get_position(obj)
        success = self.set_position(obj, x + dx, y + dy)
        obj.last_position = (dx, dy)
        return success

    def move_up(self, obj):
        return self.__move(obj, 0, 1)

    def move_down(self, obj):
        return self.__move(obj, 0, -1)

    def move_right(self, obj):
        return self.__move(obj, 1, 0)

    def move_left(self, obj):
        return self.__move(obj, -1, 0)

    def __remove_from_grid(self, obj):
        try:
            x, y = self.get_position(obj)
        except:
            return
        self.grid[x][y] = EmptySpace()

    def get_px_position(self, x: int, y: int):
        return self.px_width * x + self.px_width / 2 + self.offset_x, self.px_height * y + self.px_height / 2 + self.offset_y

    def draw(self):
        spriteList = arcade.SpriteList()
        for x, row in enumerate(self.grid):
            for y, node in enumerate(row):
                for node in [EmptySpace(clickable=False) if node.need_ground else None, node]:
                    if node is None:
                        continue
                    node.sprite.width = self.px_width
                    node.sprite.height = self.px_height
                    node.sprite.position = self.get_px_position(x, y)
                    
                    if not node.last_position or node.last_position == (0, 1):
                        node.sprite.angle = 0
                    elif node.last_position == (0, -1):
                        node.sprite.angle = 180
                    elif node.last_position == (1, 0):
                        node.sprite.angle = 270
                    elif node.last_position == (-1, 0):
                        node.sprite.angle = 90

                    if node.can_be_marked: # aka can be marked
                        node.marked = (x, y) in self.marked
                        node.sprite.color = (200, 200, 200) if node.marked else arcade.color.WHITE

                    spriteList.append(node.sprite)
        spriteList.draw()
    
    def create_astar_maze(self):
        return list(map(lambda row : list(map(lambda o : bool(isinstance(o, Obstacle)), row)), self.grid))

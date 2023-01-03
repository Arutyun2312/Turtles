import arcade
from game_objects.apple import Apple
from game_objects.empty import EmptySpace
from game_objects.grid_object import GridObject
from game_objects.obstacle import Obstacle
from astar import AStar
from game_objects.turtle import Turtle

def empty(n: int):
    return list(map(lambda _: EmptySpace(), range(n)))


class Grid:
    px_size = 500

    def __init__(self):
        self.width = 0
        self.height = 0
        self.grid: list[list[GridObject]] = []
        self.marked: list[tuple[int, int]] = []
        self.offset_x = self.offset_y = 0
        self.px_width = self.px_height = 50
        self.astars: dict[int, list[AStar]] = {}
        self.target_astar: AStar | None = None
        self.spriteList: arcade.SpriteList = None
    
    def create(self, width: int, height: int): 
        self.grid = list(map(lambda _: empty(width), empty(height)))
        self.width = width
        self.height = height
        self.px_width = Grid.px_size / width
        self.px_height = Grid.px_size / height
        self.spriteList = arcade.SpriteList(capacity=width * height)

    def can_go(self, x: int, y: int):
        return 0 <= x and x < self.width and 0 <= y and y < self.height and self.grid[x][y].can_be_eaten
        
    def objects(self):
        for x, row in enumerate(self.grid):
            for y, node in enumerate(row):
                yield x, y, node

    @property
    def turtles(self):
        for x, y, obj in self.objects():
            if isinstance(obj, Turtle):
                yield x, y, obj

    @property
    def apple(self):
        for x, y, obj in self.objects():
            if isinstance(obj, Apple):
                return obj
    
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
        return self.px_width * (x + 0.5) + self.offset_x, self.px_height * (y + 0.5) + self.offset_y

    def draw(self):
        spriteList = self.spriteList
        spriteList.clear()
        for x, row in enumerate(self.grid):
            for y, node in enumerate(row):
                nodes: list[GridObject | None] = [
                    # EmptySpace(clickable=False) if node.need_ground else None,
                    node
                ]
                for node in nodes:
                    if node is None: continue
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

                    node.sprite.color = arcade.color.WHITE
                    if self.target_astar: # aka can be marked
                        possible = (x, y) in self.target_astar.possibles
                        path = (x, y) in self.target_astar.path
                        node.sprite.color = arcade.color.RED if path else (200, 200, 200) if possible else arcade.color.WHITE

                    spriteList.append(node.sprite)
        spriteList.draw()
    
    def create_astar_maze(self):
        return list(map(lambda row : list(map(lambda o : bool(isinstance(o, Obstacle)), row)), self.grid))

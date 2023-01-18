# https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2

from __future__ import annotations

from utils import is_valid_index


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent: Node | None, position: tuple[int, int], g=0):
        self.parent = parent
        self.position = position

        self.g = g
        self.h = 0

    @property
    def f(self):
        return self.g + self.h

    def moved(self, dx: int, dy: int):
        return Node(self, (self.position[0] + dx, self.position[1] + dy), self.g + 1)

    def possibles(self, calculate_price):
        moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for dx, dy in moves:
            x, y = self.position[0] + dx, self.position[1] + dy
            if calculate_price(x, y) == 0:
                yield self.moved(dx, dy)

    def to_list(current):
        lst: list[tuple[int, int]] = []
        while current:
            lst.append(current.position)
            current = current.parent
        return lst[::-1]  # Return reversed

    def __eq__(self, other: Node | tuple[int, int]):
        return self.position == (other.position if isinstance(other, Node) else other)

    def __hash__(self):
        return hash(self.position)

class AStar:
    def __init__(self, start: tuple[int, int], end: tuple[int, int], maze: list[list[int]]):
        self.start = start
        self.end = end
        self.maze = maze
        self.possibles: set[Node] = set()
        self.closed_list: set[Node] = {}
        self.current_node: Node | None = None
    
    def reset(self):
        self.possibles = {Node(None, self.start)}
        self.closed_list = set()

    @property 
    def is_done(self):
        return self.current_node != None and (self.current_node.position == self.end or len(self.possibles) == 0)

    @property
    def path(self):
        return self.current_node.to_list() if self.current_node else []

    def new_possibles(self):
        def calculate_price(x: int, y: int):
            if not is_valid_index(self.maze, x, y): return 1000
            if (x, y) in self.closed_list: return 1000
            return self.maze[x][y]
        return self.current_node.possibles(calculate_price)

    def add_possible(self, node: Node):
        # Create the h value
        node.h = ((node.position[0] - self.end[0]) ** 2 + (node.position[1] - self.end[1]) ** 2) ** 0.5

        # Add the child to the open list
        self.possibles.add(node)
    
    def move_to(self, node: Node):
        self.current_node = node
        self.possibles.discard(node)
        self.closed_list.add(node)
    
    def next_step(self):
        if self.current_node is None: self.reset()

        # Found the goal
        if self.is_done: return
        
        # Get node with lowest cost
        node = min(self.possibles, key=lambda n : n.f, default=self.current_node)

        # move to it
        self.move_to(node)

        # generate new possibles
        for possible in self.new_possibles():
            self.add_possible(possible)

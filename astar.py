# https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2

from __future__ import annotations
from helpers import Position, game

def grid(): return game().grid

class Node(Position):
    """A node class for A* Pathfinding"""
    g = 0
    parent: Node | None = None

    @property
    def f(self): return self.g + self.distance_to(grid().apple.position)

    def possibles(self):
        moves: list[Position] = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for move in moves:
            new_node = self + move
            if grid().calculate_price(new_node) == 0:
                new_node.parent = self
                new_node.g = self.g + 1
                yield new_node

    def to_list(current):
        lst: list[Node] = []
        while current:
            lst.append((current))
            current = current.parent
        return lst[::-1]  # Return reversed

class AStar:
    def __init__(self, start: Position):
        self.start = start
        self.possibles = {Node(self.start)}
        self.closed_list = set()
        self.current_node: Node | None = None

    @property
    def end(self): return grid().apple.position

    @property 
    def is_done(self):
        return self.current_node and (self.current_node == self.end or len(self.possibles) == 0)

    @property
    def path(self):
        return self.current_node.to_list() if self.current_node else []
    
    def move_to(self, node: Node):
        self.current_node = node
        self.possibles.discard(node)
        self.closed_list.add(node)
    
    def next_step(self):
        # Found the goal
        if self.is_done: return
        
        # Get node with lowest cost
        node = min(self.possibles, key=lambda n : n.f, default=self.current_node)

        # move to it
        self.move_to(node)

        # generate new possibles
        for possible in self.current_node.possibles():
            if possible in self.closed_list: continue
            self.possibles.add(possible)

    def all_steps(self, start: Position):
        if self.start != start:
            path = self.path
            if start in self.path: # if start in path, then cut path. No need to recalculate
                node = next(node for node in path if node == start)
                node.parent = None
                self.current_node = path[-1]
            else: # otherwise recalculate
                self.current_node = None
                self.possibles.add(Node(start))
        while not self.is_done:
            self.next_step()

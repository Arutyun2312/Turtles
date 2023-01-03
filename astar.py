# https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2

from __future__ import annotations


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent: Node | None, position: tuple[int, int]):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0

    @property
    def f(self):
        return self.g + self.h

    def moved(self, dx: int, dy: int):
        return Node(self, (self.position[0] + dx, self.position[1] + dy))

    def possibles(self, maze: list[list] | None = None):
        moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for dx, dy in moves:
            x, y = self.position[0] + dx, self.position[1] + dy
            if 0 <= x and x < len(maze) and 0 <= y and y < len(maze[x]):
                yield self.moved(dx, dy)

    def __eq__(self, other: Node):
        return self.position == other.position
    
    def __add__(self, other: Node):
        return (self.position[0] - other.position[0]) ** 2 + (self.position[1] - other.position[1]) ** 2


def astar(maze: list[list[int]], start: tuple[int, int], end: tuple[int, int]):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    max_path_length = len(maze) * len(maze[0])

    # Initialize both open and closed list
    open_list: list[Node] = []
    closed_list: list[Node] = []

    # Add the start node
    open_list.append(Node(None, start))

    # Loop until you find the end
    while 0 < len(open_list) and len(open_list) < max_path_length:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for i, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = i

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node.position == end:
            path = []
            current = current_node
            while current:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate children
        children: list[Node] = []
        for new_node in current_node.possibles(maze):  # Create new nodes

            # Get node position
            x, y = new_node.position

            # Make sure walkable terrain
            if maze[x][y]: continue

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end[0]) ** 2) + ((child.position[1] - end[1]) ** 2)

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)
    return []

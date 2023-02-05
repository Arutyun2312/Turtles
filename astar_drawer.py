import arcade
from arcade import Text
from astar import AStar
from game_objects.grid import Grid
from helpers import *

class AStarDrawer:
    def __init__(self, grids: list[Grid]):
        self.grids = grids
        self.astar: AStar = None
        self.texts: list[Text] = []

    def update_texts(self):
        self.texts = []
        semi_transparent = [node for node in self.astar.path + list(self.astar.possibles) if node.f] if self.astar else []
        for grid in self.grids: 
            grid.semi_transparent = semi_transparent
        if not self.astar: return

        grid = self.grids[0]
        for astar_node, from_path in *((node, True) for node in self.astar.path), *((node, False) for node in self.astar.possibles.difference(self.astar.path)):
            if astar_node.f == 0: continue
            color = arcade.color.GREEN if from_path else (200, 200, 200)
            font_size = grid.node_px_size.height / 3
            position = grid.node_px_position(astar_node) - Size(font_size, font_size) / 2
            text = str(round(astar_node.f))
            self.texts.append(Text(text, *position, font_size=font_size, color=color))

    def update_positions(self):
        if not self.astar: return
        grid = self.grids[0]
        for i, astar_node in enumerate(node for node in self.astar.path + list(self.astar.possibles.difference(self.astar.path)) if node.f):
            font_size = grid.node_px_size.height / 3
            position = grid.node_px_position(astar_node) - Size(font_size, font_size) / 2
            self.texts[i].position = position

    def draw(self):
        if not self.astar: self.update_texts()
        for text in self.texts:
            text.draw()

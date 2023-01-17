from game_objects.turtle import Turtle
from game_objects.apple import Apple
from game_objects.obstacle import Obstacle
from ui.maze_preset_object import Preset, PresetItem
import arcade

presets = [
     Preset(
        'Easy', 
        PresetItem(Apple(), (2, 4)),
        PresetItem(Turtle('Turtle 1'), (2, 2)),
        *PresetItem.multiply(lambda: Obstacle(),
        ),
        size=(5, 5)
    ),
     Preset(
        'Easy', 
        PresetItem(Apple(), (10,9)),
        PresetItem(Turtle('Turtle 1'), (0, 0)),
        PresetItem(Turtle('Turtle 2', arcade.color.RED), (19, 19)),
        *PresetItem.multiply(lambda: Obstacle(), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7), (1,8), (1,9), (1,10), 
        (1,11), (1,12), (1,13), (1,14), (1,15), (1,16), (1,17), (1,18), (3,1), (4,1), (5,1), (6,1), (7,1), (8,1),
        (9,1), (10,1), (11,1), (12,1), (13,1), (14,1), (15,1), (16,1), (17,1), (18,1), (18,2), (18,3), (18,4), (18,5),
        (18,6), (18,7), (18,8), (18,9), (18,10), (18,11), (18,12), (18,13), (18,14), (18,15), (18,16), (18,17), (18,18), 
        (16,18), (15,18), (14,18), (13,18), (12,18), (11,18), (10,18), (9,18), (8,18), (7,18), (6,18), (5,18),
        (4,18), (3,18), (2,18), (1,18), (16,16), (16,15), (16,14), (16,13), (16,12), (16,11), (16,10), (16,9), (16,8), (16,7),
        (16,6), (16,5), (16,4), (16,3), (15,3), (14,3), (13,3), (12,3), (11,3), (10,3), (9,3), (8,3), (7,3), (6,3), (5,3),
        (3,3), (3,4), (3,5), (3,6), (3,7), (3,8), (3,9), (3,10), (3,11), (3,12), (3,13), (3,14), (3,15), (3,16),
        (4,16), (5,16), (6,16), (7,16), (8,16), (9,16), (10,16), (11,16), (12,16), (13,16), (14,16), 
        (14,14), (14,13), (14,12), (14,11), (14,10), (14,9), (14,8), (14,7), (14,6), (14,5), 
        (5,14), (5,12), (5,11), (5,10), (5,9), (5,8), (5,7), (5,6), (5,5), 
        (14,5), (13,5), (12,5), (11,5), (10,5), (9,5), (8,5), (7,5), 
        (12,14), (11,14), (10,14), (9,14), (8,14), (7,14), (6,14), 
        (7,7), (12,12), (10,10), (9,9), (9,10), (1,0), (18,19), (12,13), 
        (7,9), (7,10), (7,11), (7,12), (3,2), (16,17), (5,4), 
        (8,7), (9,7), (10,7), (11,7), (12,7),
        (12,8), (12, 9), (12,10), (12,11),
        (8,12), (9,12), (10,12),),
        size=(20, 20)
    ),
     Preset(
        'Medium', 
        PresetItem(Apple(), (11,11)),
        PresetItem(Turtle('Turtle 1'), (7, 19)),
        PresetItem(Turtle('Turtle 2'), (12, 0)),
        *PresetItem.multiply(lambda: Obstacle(), (19,8), (18,8), (17,8), (15,8), (15,9), (16,8), (14,9), (13,9), 
        (11,9), (6,9), (5,9), (4,9), (4,10), (11,1), (11,2),
        (18,1), (18,2), (17,1), (19,4), (18,4), (17,4), (16,1), (15,1), (14,1), (13,1), (16,4), (16,3), (15,3), 
        (13,1), (13,2), (13,3), (13,4), (13,5), (13,6), (13,7), (14,6), (15,6), (16,6), (17,6), (18,6),
        (11,4), (13,4),  (11,4), (10,4), (9,4), (9,3), (9,2), (7,1), (11,8), (11,7), (11,6),
        (7,3), (6,3), (5,3), (5,2), (5,1), (4,1), (3,1), (2,1), (0,0), (0,1), (0,2), (0,3), (1,3), (2,3), (3,3), (6,4), (6,6),
        (6,7),(8,6), (8,7), (8,8), (9,6), (2,7), (3,7), (4,7), (5,7), (2,8), (2,9), (3,5), (3,4), (3,3), (2,5), (1,5), (0,7),
        (0,8), (0,9), (6,5), (4,5), (7,7), (9,1), (8,1), 
          
        (1,18), (1,18), (2,18), (3,18), (4,18), (5,18), (6,18), (0,15), (1,15), (2,15), (3,15), (3,16), (4,16), 
        (6,17), (6,16), (6,15), (6,14), (6,13), (6,12), (1,13), (2,13), (3,13), (4,13), (5,13), (0,11), (1,11), (2,11), (3,11),
        (4,11), (6,10), (7,10), (8,10), (8,12), (8,13), (8,19), (8,18), (8,17), (10,19), (11,19), (12,19),
        (19,19), (19,18), (19,17), (19,16), (16,16), (17,16), (18,16), (16,15), (16,14), (15,14), (17,14), (18,14), 
        (19,12), (19,11), (19,10), (19, 9), (14,18), (15,18), (16,18), (17,18), (14,16), (14,17), (12,18), (12,16), (13,16),
        (13,12), (13,13), (13,14), (13,15), (14,12), (15,12), (16,12), (17,12), (17, 10), (17,8), (17,11), 
        (9,10), (11,10), (13,10), (7,14), (8,14), (9,14), (10,14), (10,15), (10,16), (10,17),
        (8,16), (11,12), (10,12), (12,14), (10,8), (9,8), (9,12), (12,12), (12,6),),
        size=(20, 20)
    ),
    Preset(
        'Hard', 
        PresetItem(Apple(), (12,10)),
        PresetItem(Turtle('Turtle 1'), (0, 19)),
        PresetItem(Turtle('Turtle 2'), (19, 0)),
        *PresetItem.multiply(lambda: Obstacle(), (19,8), (18,8), (17,8), (15,8), (15,9), (16,8), (14,9), (13,9), (12,9), 
        (11,9), (6,9), (5,9), (4,9), (4,10), (11,0), (11,1), (11,2),
        (18,1), (18,2), (17,1), (19,4), (18,4), (17,4), (16,1), (15,1), (14,1), (13,1), (16,4), (16,3), (15,3), 
        (13,1), (13,2), (13,3), (13,4), (12,4), (13,5), (13,6), (13,7), (14,6), (15,6), (16,6), (17,6), (18,6),
        (11,4), (13,4), (12,4), (11,4), (10,4), (9,4), (9,3), (9,2), (7,0), (7,1), (11,8), (11,7), (11,6),
        (7,3), (6,3), (5,3), (5,2), (5,1), (4,1), (3,1), (2,1), (0,0), (0,1), (0,2), (0,3), (1,3), (2,3), (3,3), (6,4), (6,6),
        (6,7),(8,6), (8,7), (8,8), (9,6), (2,7), (3,7), (4,7), (5,7), (2,8), (2,9), (3,5), (3,4), (3,3), (2,5), (1,5), (0,7),
        (0,8), (0,9), (6,5), (4,5), (7,7), (9,1), (8,1), 
        
        (1,18), (1,17), (1,18), (2,18), (3,18), (4,18), (5,18), (6,18), (0,15), (1,15), (2,15), (3,15), (3,16), (4,16), 
        (6,17), (6,16), (6,15), (6,14), (6,13), (6,12), (1,13), (2,13), (3,13), (4,13), (5,13), (0,11), (1,11), (2,11), (3,11),
        (4,11), (6,10), (7,10), (8,10), (8,11), (8,12), (8,13), (8,19), (8,18), (8,17), (10,19), (11,19), (12,19),
        (19,19), (19,18), (19,17), (19,16), (16,16), (17,16), (18,16), (16,15), (16,14), (15,14), (17,14), (18,14), 
        (19,12), (19,11), (19,10), (19, 9), (14,18), (15,18), (16,18), (17,18), (14,16), (14,17), (12,18), (12,16), (13,16),
        (13,12), (13,13), (13,14), (13,15), (14,12), (15,12), (16,12), (17,12), (17, 10), (17,8), (17,11), 
        (9,10), (11,10), (13,10), (7,14), (8,14), (9,14), (10,14), (10,15), (10,16), (10,17),
        (8,16), (11,12), (10,12), (12,14), (10,8), (9,8), (9,12), (12,12),),
        size=(20, 20), 
     ),
    Preset(
        'No Solution', 
        PresetItem(Apple(), (12,10)),
        PresetItem(Turtle('Turtle 1'), (0, 9)),
        PresetItem(Turtle('Turtle 2'), (9, 0)),
        *PresetItem.multiply(lambda: Obstacle(), (19,8), (17,8), (15,8), (15,9), (16,8), (14,9), (13,9), (12,9), 
        (11,9), (6,9), (5,9), (4,9), (4,10), (11,0), (11,1), (11,2),
        (18,1), (18,2), (17,1), (19,4), (18,4), (17,4), (16,1), (15,1), (14,1), (13,1), (16,4), (16,3), (15,3), 
        (13,1), (13,2), (13,3), (13,4), (12,4), (13,5), (13,6), (13,7), (14,6), (15,6), (16,6), (17,6), (18,6),
        (11,4), (13,4), (12,4), (11,4), (10,4), (9,4), (9,3), (9,2), (7,0), (7,1), (11,8), (11,7), (11,6),
        (7,3), (6,3), (5,3), (5,2), (5,1), (4,1), (3,1), (2,1), (0,0), (0,1), (0,2), (0,3), (1,3), (2,3), (3,3), (6,4), (6,6),
        (6,7),(8,6), (8,7), (8,8), (9,6), (2,7), (3,7), (4,7), (5,7), (2,8), (2,9), (3,5), (3,4), (3,3), (2,5), (1,5), (0,7),
        (0,8), (0,9), (6,5), (4,5), (7,7), (9,1), (8,1), 
          
        (1,18), (1,17), (1,18), (2,18), (3,18), (4,18), (5,18), (6,18), (0,15), (1,15), (2,15), (3,15), (3,16), (4,16), 
        (6,17), (6,16), (6,15), (6,14), (6,13), (6,12), (1,13), (2,13), (3,13), (4,13), (5,13), (0,11), (1,11), (2,11), (3,11),
        (4,11), (6,10), (7,10), (8,10), (8,11), (8,12), (8,13), (8,19), (8,18), (8,17), (10,19), (11,19), (12,19),
        (19,19), (19,18), (19,17), (19,16), (16,16), (17,16), (18,16), (16,15), (16,14), (15,14), (17,14), (18,14), 
        (19,12), (19,11), (19,10), (19, 9), (14,18), (15,18), (16,18), (17,18), (14,16), (14,17), (12,18), (12,16), (13,16),
        (13,12), (13,13), (13,14), (13,15), (14,12), (15,12), (16,12), (17,12), (17, 10), (17,8), (17,11), 
        (9,10), (11,10), (13,10), (7,14), (8,14), (9,14), (10,14), (10,15), (10,16), (10,17),
        (8,16), (12,14), (10,8), (9,8), (13,11), (10,10), (11,14), (9,12), (10,12), (11,12),),
        size=(20, 20)
    ),
    Preset(
        'AI', 
        PresetItem(Apple(), (15,19)),
        PresetItem(Turtle('Turtle 1'), (2, 9)),
        PresetItem(Turtle('Turtle 2'), (10, 9)),
        *PresetItem.multiply(lambda: Obstacle(), (2,2), (10,2), (6,17), (2,3), (2,4), (2,5), (2,6), (2,7), (2,8), (3,8),
        (10,3), (10,4), (10,5), (10,6), (10,7), (10,8), (9,8), (3,9), (3,10), (3,11), (3,12), (9,9), (9,10), (9,11), (9,12), (4,12),
        (4,13), (4,14), (4,15), (5,15), (8,12), (8,13), (8,14), (8,15), (7,15), (7,16), (5,16), (4,9), (5,9), (6,9), (7,9), (8,9),
        (15,2), (15,3), (15,4), (15,5), (15,6), (15,7), (15,8), (15,9), (15,10), (15,11), (15,12), (15,13), (15,14), (5,17), (7,17), 
        (15,15), (15,16), (15,17), (6,18), (15,18),),
        size=(20, 20)
    ),
]

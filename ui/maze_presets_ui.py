from typing import Callable
import arcade.gui
from ui.maze_preset_object import Preset
from ui.maze_presets import presets
from game_objects.grid import Grid

def create_maze_presets_ui(grid: Grid, on_selected: Callable[[], None], score: dict[str, int]):
    v_box = arcade.gui.UIBoxLayout(vertical=True)

    score_text = '; '.join(list(map(lambda name: f'{name} - {score[name]}', score)))
    v_box.add(arcade.gui.UILabel(text=score_text, font_size=16, bold=True, height=50))

    h_box = arcade.gui.UIBoxLayout(vertical=False)

    h_box.add(arcade.gui.UILabel(text='Mazes: ', font_size=16))

    def create_on_click(preset: Preset): 
        def on_click(_):
            preset.setup_grid(grid)
            on_selected()
        return on_click
    for preset in presets:
        button = arcade.gui.UIFlatButton(text=preset.name, width=100)
        button.on_click = create_on_click(preset)
        h_box.add(button)

    v_box.add(h_box)
        
    return v_box
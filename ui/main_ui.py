import arcade 
import arcade.gui
import pyperclip

def create_main_ui():
    v_box = arcade.gui.UIBoxLayout()

    quit_button = arcade.gui.UIFlatButton(text="Quit", width=100)
    quit_button.on_click = lambda _ : arcade.exit()
    v_box.add(quit_button)

    copy_button = arcade.gui.UIFlatButton(text='Copy to clipboard', width=100)
    copy_button.on_click = lambda _ : pyperclip.copy('The text to be copied to the clipboard.')
    v_box.add(copy_button)

    return v_box
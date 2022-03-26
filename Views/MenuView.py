import arcade
from Views import GameView
import arcade.gui

class MenuView(arcade.View):

    def __init__(self):
        super().__init__()
        self.manager = None
        self.v_box = None

    def on_show(self):
        """Called when switching to this view."""
        arcade.set_background_color(arcade.color.WHITE)
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UIBoxLayout()

        # Start Game Button
        start_button = arcade.gui.UIFlatButton(text="Start Game", width=200)
        self.v_box.add(start_button.with_space_around(bottom=20))
        start_button.on_click = self.on_click_start

        # Quit Button
        quit_button = arcade.gui.UIFlatButton(text="Quit Game", width=200)
        self.v_box.add(quit_button.with_space_around(bottom=20))
        quit_button.on_click = self.on_click_quit

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_draw(self):
        """Draw the menu"""
        self.clear()
        self.manager.draw()

    def on_click_start(self, event):
        game_view = GameView.GameView()
        self.window.show_view(game_view)

    def on_click_quit(self, event):
        arcade.close_window()
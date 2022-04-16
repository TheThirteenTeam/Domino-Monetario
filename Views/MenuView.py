import arcade
from Views import DifficultView
import arcade.gui
import gameConstants as gConst

class MenuView(arcade.View):

    def __init__(self):
        super().__init__()
        self.manager = None
        self.v_box = None
        self.background = arcade.load_texture("images/backgroundTest.png")
        self.logo = arcade.load_texture("images/domino_monetario_logo.png")
        self.dominozin = arcade.load_texture("images/dominozin.png")

    def on_show(self):
        """Called when switching to this view."""
        arcade.set_background_color(arcade.color.WHITE)
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UIBoxLayout()

        button_style = {"bg_color":(35, 161, 75), "font_size": 20, "font_name":"Kenney Pixel Square", "border_width": 2, "border_color":(21, 97, 45)}

        start_button = arcade.gui.UIFlatButton(text="Iniciar Jogo", height=75, width=300, style=button_style)
        start_button.on_click = self.start_game_click
        quit_button = arcade.gui.UIFlatButton(text="Sair do Jogo", height=75, width=275, style=button_style)
        quit_button.on_click = self.quit_game_click

        self.v_box.add(start_button.with_space_around(bottom=20))
        self.v_box.add(quit_button.with_space_around(bottom=50))

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
        arcade.draw_lrwh_rectangle_textured(0, 0, gConst.SCREEN_WIDTH, gConst.SCREEN_HEIGHT, self.background)
        arcade.draw_scaled_texture_rectangle(gConst.SCREEN_WIDTH / 2, gConst.SCREEN_HEIGHT * 0.77, texture=self.logo, scale=0.3)
        arcade.draw_scaled_texture_rectangle(gConst.SCREEN_WIDTH * 0.95, gConst.SCREEN_HEIGHT * 0.1, texture=self.dominozin, scale=0.2)
        self.manager.draw()

    def start_game_click(self, event):
        self.manager.disable()
        difficulty_view = DifficultView.DifficultView()
        self.window.show_view(difficulty_view)

    def quit_game_click(self, event):
        return self.window.close()


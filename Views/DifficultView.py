import arcade
from Views import GameView
from Views import MenuView
import arcade.gui
import gameConstants as gConst

class DifficultView(arcade.View):

    def __init__(self):
        super().__init__()
        self.clicked = False
        self.counter = 0
        self.manager = None
        self.game_view = None
        self.v_box = None
        self.background = arcade.load_texture("images/backgroundTest.png")

    def on_show(self):
        """Called when switching to this view."""
        arcade.set_background_color(arcade.color.WHITE)
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UIBoxLayout()

        button_style = {"bg_color": (35, 161, 75), "font_size": 20, "border_width": 2, "border_color": (21, 97, 45)}

        difficulty_label = arcade.gui.UILabel(text="Selecionar Dificuldade", font_size=48, bold=True, text_color=[255, 255, 255], align="center")
        easy_button = arcade.gui.UIFlatButton(text="Facil", height=75, width=250, style=button_style)
        easy_button.on_click = self.easy_game_click
        hard_button = arcade.gui.UIFlatButton(text="Dificil", height=75, width=250, style=button_style)
        hard_button.on_click = self.hard_game_click
        return_button = arcade.gui.UIFlatButton(text="Voltar", height=75, width=225, style=button_style)
        return_button.on_click = self.return_button_click

        self.v_box.add(difficulty_label.with_space_around(bottom=50))
        self.v_box.add(easy_button.with_space_around(bottom=20))
        self.v_box.add(hard_button.with_space_around(bottom=20))
        self.v_box.add(return_button.with_space_around(bottom=50))

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
        if not self.clicked:
            self.manager.draw()
        else:
            arcade.draw_text("Carregando... ({}%)".format(self.counter), 0, gConst.SCREEN_HEIGHT / 2, arcade.color.WHITE, font_size=48, width=gConst.SCREEN_WIDTH, align="center")
            self.counter += 2

        if self.counter == 100 and self.clicked == "Easy":
            self.manager.disable()
            self.game_view = GameView.GameView(opponentAlgorithm="GreedySearch")
            self.window.show_view(self.game_view)
        if self.counter == 100 and self.clicked == "Hard":
            self.manager.disable()
            self.game_view = GameView.GameView(opponentAlgorithm="AStar")
            self.window.show_view(self.game_view)

    def easy_game_click(self, event):
        self.clicked = "Easy"

    def hard_game_click(self, event):
        self.clicked = "Hard"

    def return_button_click(self, event):
        self.manager.disable()
        menu_view = MenuView.MenuView()
        self.window.show_view(menu_view)
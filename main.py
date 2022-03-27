""" Dominó Monetario """

# Packages Imports
from typing import Optional
import arcade

# Game Imports
import gameConstants as gConst
from Views import MenuView

def main():
    # Create Window
    window = arcade.Window(gConst.SCREEN_WIDTH, gConst.SCREEN_HEIGHT, gConst.SCREEN_TITLE, fullscreen=True)
    window.set_viewport(0, gConst.SCREEN_WIDTH, 0, gConst.SCREEN_HEIGHT)
    # Starts Menu View
    window.show_view(MenuView.MenuView())
    arcade.run()

if __name__ == "__main__":
    main()
import arcade
import random
from Objects import Bank
from Objects import Player
from Objects import Domino
from Objects import Placeholder
import gameConstants as gConst

class GameView(arcade.View):

    def __init__(self):
        super().__init__()

        # Background image will be stored in this variable
        self.background = None

        # Game Objects
        self.Bank = None
        self.Player1 = None
        self.Player2 = None
        self.CurDomino = None

        # Player Mouse Actions
        self.held_domino = None
        self.held_domino_original_position = None

    def setup(self):

        self.background = arcade.load_texture("images/backgroundTest.png")

        # Player Mouse Actions
        self.held_domino = []
        self.held_domino_original_position = []

        # Create Game Objects
        self.Bank = Bank.Bank()
        self.Player1 = Player.Player()
        self.Player2 = Player.Player()

        # Adiciona todos os dominos possíveis no banco
        for i, left_domino_value in enumerate(gConst.DOMINOS_VALUES):
            for j, right_domino_value in enumerate(gConst.DOMINOS_VALUES):
                print(left_domino_value, "_", right_domino_value)
                if i >= j:
                    domino = Domino.Domino(left_domino_value, right_domino_value, gConst.DOMINO_SCALE)
                    self.Bank.add_domino(domino) # Adiciona o domino ao banco
        self.Bank.shuffle() # Embaralha o banco

        # Sorteia a mão inicial do jogador 1
        for dom in range(0, gConst.PLAYER_START_HAND):
            sort = random.randrange(0, len(self.Bank.bankList))
            self.Player1.add_domino(self.Bank.bankList[sort])  # adiciona domino na mão do player 1
            self.Bank.remove_domino(self.Bank.bankList[sort]) # remove o domino do banco

        # Sorteia a mão inicial do jogador 2
        for dom in range(0, gConst.PLAYER_START_HAND):
            sort = random.randrange(0, len(self.Bank.bankList))
            self.Player2.add_domino(self.Bank.bankList[sort]) # adiciona domino na mão do player 2
            self.Bank.remove_domino(self.Bank.bankList[sort]) # remove o domino do banco

        # Escolhe o primeiro jogador
        higher_domino1, higher_domino2 = 0, 0
        for dom in self.Player1.playerHand:
            if dom.leftFace == dom.rightFace and int(dom.leftFace) > int(higher_domino1):
                higher_domino1 = int(dom.leftFace)
        for dom in self.Player2.playerHand:
            if dom.leftFace == dom.rightFace and int(dom.leftFace) > int(higher_domino2):
                higher_domino2 = int(dom.leftFace)
        if higher_domino1 >= higher_domino2:
            self.Player1.playTime = True
        else:
            self.Player2.playTime = True

        # Configurações iniciais dos objetos
        self.Bank.set_position(gConst.BANK_X, gConst.BANK_Y)
        self.Player1.set_position(0, gConst.SCREEN_HEIGHT / 8)
        self.Player2.set_position(0, gConst.SCREEN_HEIGHT)
        self.Bank.set_angle(0)
        self.Player1.set_angle(80)
        self.Player2.set_angle(80)
        self.Player2.turn_dominos("Down")
        self.Bank.turn_dominos("Down")

    def on_show(self):
        self.setup()

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()
        arcade.start_render()
        # Draw the objects in the screen
        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            gConst.SCREEN_WIDTH, gConst.SCREEN_HEIGHT,
                                            self.background)
        self.Bank.bankList.draw()
        self.Player1.playerHand.draw()
        self.Player2.playerHand.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        #if self.Player1.playTime:
            # Get list of cards we've clicked on
            domino = arcade.get_sprites_at_point((x, y), self.Player1.playerHand)
            print(domino)
            if domino in self.Player1.playerHand:
                self.Player1.remove_domino(domino)
            # Have we clicked on a card?
            if len(domino) > 0:
                # Might be a stack of cards, get the top one
                primary_domino = domino[-1]
                # All other cases, grab the face-up card we are clicking on
                self.held_domino = [primary_domino]
                # Save the position
                self.held_domino_original_position = [self.held_domino[0].position]
                # Put on top in drawing order
                #self.Bank.pull_to_top(self.held_domino[0])

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        """ Called when the user presses a mouse button. """
        # If we don't have any cards, who cares
        if len(self.held_domino) == 0:
            return

        self.Player1.readjustment_hand_position()
        # We are no longer holding cards
        self.held_domino = []

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """
        domino = arcade.get_sprites_at_point((x, y), self.Player1.playerHand)
        # If we are holding cards, move them with the mouse
        for domino in self.held_domino:
            domino.center_x += dx
            domino.center_y += dy
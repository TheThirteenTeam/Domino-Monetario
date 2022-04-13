import arcade
import random
from Objects import Bank
from Objects import Player
from Objects import Domino
from Objects import Placeholder
from Objects import GameTable
import gameConstants as gConst

def chooseFirstPlayer(player1, player2):
    higher_pair1, higher_sum1 = 0, 0
    higher_pair2, higher_sum2 = 0, 0
    for dom in player1.playerHand:
        if dom.leftFaceNum + dom.rightFaceNum > higher_sum1:
            higher_sum1 = dom.leftFaceNum + dom.rightFaceNum
        if dom.leftFaceNum == dom.rightFaceNum and dom.leftFaceNum > higher_pair1:
            higher_pair1 = dom.leftFaceNum
    for dom in player2.playerHand:
        if dom.leftFaceNum + dom.rightFaceNum > higher_sum2:
            higher_sum2 = dom.leftFaceNum + dom.rightFaceNum
        if dom.leftFaceNum == dom.rightFaceNum and dom.leftFaceNum > higher_pair2:
            higher_pair2 = dom.leftFaceNum
    if higher_pair1 != higher_pair2:
        if higher_pair1 > higher_pair2: return player1
        else: return player2
    else:
        if higher_sum1 > higher_sum2: return player1
        else: return player2

class GameView(arcade.View):

    def __init__(self, opponentAlgorithm):
        super().__init__()
        self.opponentAlgorithm = opponentAlgorithm

        # Background image will be stored in this variable
        self.background = None

        # Game Objects
        self.Bank = None
        self.Player1 = None
        self.Player2 = None
        self.GameTable = None

        # Player Mouse Actions
        self.held_domino = None
        self.held_screen = False
        self.last_domino_scale = None

        # Camera
        self.camera_sprites = arcade.Camera(gConst.SCREEN_WIDTH, gConst.SCREEN_HEIGHT)
        self.camera_gui = arcade.Camera(gConst.SCREEN_WIDTH, gConst.SCREEN_HEIGHT)

        self.setup()

    def setup(self):

        # Background texture
        self.background = arcade.load_texture("images/backgroundTest.png")

        # Player Mouse Actions
        self.held_domino = []

        # Create Game Objects
        self.Bank = Bank.Bank()
        self.Player1 = Player.Player()
        self.Player2 = Player.Player(self.opponentAlgorithm)

        # Adiciona todos os dominos possíveis no banco
        for i, left_domino_value in enumerate(zip(gConst.DOMINOS_VALUES, gConst.DOMINOS_VALUES_FLOAT)):
            for j, right_domino_value in enumerate(zip(gConst.DOMINOS_VALUES, gConst.DOMINOS_VALUES_FLOAT)):
                if i >= j:
                    domino = Domino.Domino(left_domino_value[0], left_domino_value[1], right_domino_value[0], right_domino_value[1], gConst.DOMINO_SCALE)
                    self.Bank.add_domino(domino) # Adiciona o domino ao banco
        self.Bank.shuffle() # Embaralha o banco
        self.last_domino_scale = self.Bank.bankList[0]

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

        self.camera_sprites.move_to([0, 0])

        # Cria objeto do game
        Dplaceholder1 = Domino.Domino("pholder", 0, "pholder", 0, gConst.DOMINO_SCALE)
        Dplaceholder2 = Domino.Domino("pholder", 0, "pholder", 0, gConst.DOMINO_SCALE)
        Dplaceholder3 = Domino.Domino("pholder", 0, "pholder", 0, gConst.DOMINO_SCALE)
        self.GameTable = GameTable.GameTable(gConst.DOMINO_MAX_HALF, chooseFirstPlayer(self.Player1, self.Player2), gConst.SCREEN_WIDTH / 2, gConst.SCREEN_HEIGHT / 2)
        self.GameTable.add_domino(Dplaceholder1)
        self.GameTable.add_domino(Dplaceholder2)
        self.GameTable.add_domino(Dplaceholder3)
        self.GameTable.currentPlayer = self.Player1

        # Configurações iniciais dos objetos
        self.Bank.set_position(gConst.BANK_X, gConst.BANK_Y)
        self.Player1.set_position(0, gConst.SCREEN_HEIGHT / 8)
        self.Player2.set_position(0, gConst.SCREEN_HEIGHT)
        self.Player1.set_angle(60)
        self.Player2.set_angle(60)
        self.Bank.set_angle(90)
        self.Player2.turn_dominos("Down")
        self.Bank.turn_dominos("Down")

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()
        arcade.start_render()
        # Draw the objects in the screen
        self.camera_sprites.use()
        arcade.draw_lrwh_rectangle_textured(0 - gConst.SCREEN_WIDTH / 2, 0 - gConst.SCREEN_HEIGHT / 2, gConst.SCREEN_WIDTH * 2, gConst.SCREEN_HEIGHT * 2, self.background)
        self.GameTable.tableList.draw()

        self.camera_gui.use()
        self.Bank.bankList.draw()
        arcade.draw_text("Banco", gConst.BANK_X - gConst.DOMINO_HEIGHT / 2 - 15, gConst.BANK_Y + gConst.DOMINO_WIDTH / 2 + 35, font_size=26)
        self.Player2.playerHand.draw()
        self.Player1.playerHand.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        if self.GameTable.currentPlayer == self.Player1:
            domino = arcade.get_sprites_at_point((x, y), self.Player1.playerHand)
            if len(domino) > 0:
                self.held_domino = [domino[-1]]
        if len(self.held_domino) == 0:
            self.held_screen = True

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        # If we don't have any dominos, who cares
        self.held_screen = False
        if len(self.held_domino) == 0:
            return
        # If we find a placeholder
        # Find the closest pile, in case we are in contact with more than one
        dom = arcade.get_sprites_at_point((x, y), self.GameTable.tableList)
        print(dom)
        if arcade.check_for_collision_with_list(self.held_domino[0], self.GameTable.tableList):
            print("Jogado")
            self.Player1.remove_domino(self.held_domino[0])
        else:
            print("Erro")
        self.Player1.desEmphasize()
        self.Player1.readjustment_hand_position()
        self.held_domino = []

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        if self.held_screen:
            newXPos = self.camera_sprites.position[0] - dx * gConst.SCREEN_MULTIPLIER
            newYPos = self.camera_sprites.position[1] - dy * gConst.SCREEN_MULTIPLIER
            if (0 < newXPos < 0) and (0 < newXPos < 0):
                self.camera_sprites.move_to((newXPos, newYPos), gConst.CAMERA_SPEED)
        else:
            # Player 1 - play time
            if self.GameTable.currentPlayer == self.Player1:
                domino = arcade.get_sprites_at_point((x, y), self.Player1.playerHand)
                if len(domino) > 0:
                    self.Player1.desEmphasize()
                    self.Player1.emphasize(domino[-1])
                else:
                    self.Player1.desEmphasize()
                for domino in self.held_domino:
                    domino.center_x += dx
                    domino.center_y += dy
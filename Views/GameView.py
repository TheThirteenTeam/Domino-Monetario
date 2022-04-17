import arcade
import random
from Views import MenuView
from Objects import Bank
from Objects import Player
from Objects import Domino
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
        self.Player1 = Player.Player("Player 1")
        self.Player2 = Player.Player("Player 2", self.opponentAlgorithm)
        self.GameTable = GameTable.GameTable(gConst.DOMINO_MAX_HALF, chooseFirstPlayer(self.Player1, self.Player2), gConst.SCREEN_WIDTH / 2, gConst.SCREEN_HEIGHT / 2)
        self.Vencedor = None

        # Player Mouse Actions
        self.held_domino = None
        self.last_domino_scale = None

        # Camera
        self.camera_sprites = arcade.Camera(gConst.SCREEN_WIDTH, gConst.SCREEN_HEIGHT)
        self.camera_gui = arcade.Camera(gConst.SCREEN_WIDTH, gConst.SCREEN_HEIGHT)

        self.logo = arcade.load_texture("images/domino_monetario_logo.png")
        self.setup()

    def setup(self):

        # Background texture
        self.background = arcade.load_texture("images/backgroundTest.png")

        print(self.GameTable.currentPlayer.name, "começa o jogo.")

        # Player Mouse Actions
        self.held_domino = []

        # Create Game Objects
        self.Bank = Bank.Bank()

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

        # Cria objeto do game
        Dplaceholder = Domino.Domino("pholder", 0, "pholder", 0, gConst.DOMINO_SCALE)
        self.GameTable.add_dom_to_end(Dplaceholder)

        # Configurações iniciais dos objetos
        self.Bank.set_position(gConst.BANK_X, gConst.BANK_Y)
        self.Player1.set_position(0, gConst.SCREEN_HEIGHT / 12)
        self.Player2.set_position(0, gConst.SCREEN_HEIGHT + 50)
        self.Player1.set_angle(60)
        self.Player2.set_angle(60)
        self.Bank.set_angle(90)
        self.Player2.turn_dominos("Down")
        self.Bank.turn_dominos("Down")
        self.GameTable.currentPlayer = chooseFirstPlayer(self.Player1, self.Player2)

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()
        arcade.start_render()
        # Draw the objects in the screen
        self.camera_sprites.use()
        arcade.draw_lrwh_rectangle_textured(0 - gConst.SCREEN_WIDTH * 6, 0, gConst.SCREEN_WIDTH * 13, gConst.SCREEN_HEIGHT, self.background)

        self.camera_gui.use()
        self.GameTable.tableList.draw()
        self.GameTable.tableList.draw_hit_boxes()
        arcade.draw_scaled_texture_rectangle(gConst.SCREEN_WIDTH * 0.92, gConst.SCREEN_HEIGHT * 0.1, texture=self.logo, scale=0.13)
        arcade.draw_text("Informações", gConst.SCREEN_WIDTH - 300, gConst.SCREEN_HEIGHT - 40, font_size=22, bold=True, font_name="Kenney Pixel Square")
        arcade.draw_text("Rodada: " + str(self.GameTable.gameRound) + " / Jogada: " + str(self.GameTable.gamePlay), gConst.SCREEN_WIDTH - 300, gConst.SCREEN_HEIGHT - 70, font_size=17)

        self.Bank.bankList.draw()
        self.Bank.bankList.draw_hit_boxes()
        arcade.draw_text("Banco", gConst.BANK_X - gConst.DOMINO_HEIGHT / 2 - 15, gConst.BANK_Y + gConst.DOMINO_WIDTH / 2 + 35, font_size=22, bold=True, font_name="Kenney Pixel Square")

        self.Player2.playerHand.draw()
        arcade.draw_text("Jogador 2", 20, gConst.SCREEN_HEIGHT - 40, font_size=22, bold=True, font_name="Kenney Pixel Square")
        arcade.draw_text("Poupança: " + str(self.Player2.savings), 20, gConst.SCREEN_HEIGHT - 70, font_size=17)
        arcade.draw_text("Dominos na mão: " + str(len(self.Player2.playerHand)), 20, gConst.SCREEN_HEIGHT - 100, font_size=17)

        self.Player1.playerHand.draw()
        arcade.draw_text("Jogador 1", 20, 90, font_size=22, bold=True, font_name="Kenney Pixel Square")
        arcade.draw_text("Poupança: " + str(self.Player1.savings), 20, 60, font_size=17)
        arcade.draw_text("Dominos na mão: " + str(len(self.Player1.playerHand)), 20, 30, font_size=17)

        if self.Vencedor is not None:
            arcade.draw_text("Pressione ESC para retornar ao menu.", gConst.SCREEN_WIDTH / 2, gConst.SCREEN_HEIGHT * 0.3, font_size=25, bold=True, font_name="Kenney Pixel Square")

        if self.Vencedor == self.Player1:
            arcade.draw_text("O vencedor foi o jogador 1 com R$ " + str(self.Player1.savings) + ".", gConst.SCREEN_WIDTH / 2, gConst.SCREEN_HEIGHT / 2, font_size=32, bold=True,
                             font_name="Kenney Pixel Square")
        if self.Vencedor == self.Player2:
            arcade.draw_text("O vencedor foi o jogador 2 com R$ " + str(self.Player2.savings) + ".", gConst.SCREEN_WIDTH / 2, gConst.SCREEN_HEIGHT / 2, font_size=32, bold=True,
                             font_name="Kenney Pixel Square")

    def on_update(self, deltatime):
        def computarJogada(domUsado):
            self.Player2.remove_domino(domUsado)
            self.GameTable.gamePlay += 1
            self.GameTable.currentPlayer = self.Player1
            self.GameTable.print_list()

        if len(self.Bank.bankList) == 0:
            numDominosPossiveis = 0
            if self.GameTable.currentPlayer == self.Player1:
                for dom in self.Player1.playerHand:
                    if dom.rightFaceNum == gamelist[1].leftFaceNum or dom.leftFaceNum == gamelist[len(gamelist) - 2].rightFaceNum:
                        numDominosPossiveis += 1
                if numDominosPossiveis == 0:
                    print("Jogador 1 perde")
            if self.GameTable.currentPlayer == self.Player2:
                for dom in self.Player2.playerHand:
                    if dom.rightFaceNum == gamelist[1].leftFaceNum or dom.leftFaceNum == gamelist[len(gamelist) - 2].rightFaceNum:
                        numDominosPossiveis += 1
                if numDominosPossiveis == 0:
                    print("Jogador 2 perde")

        if self.GameTable.gameRound > 3:
            print("Fim de jogo")
            self.GameTable.currentPlayer = None
            if self.Player1.savings > self.Player2.savings: self.Vencedor = self.Player1
            else: self.Vencedor = self.Player2
            return

        if len(self.Player1.playerHand) == 0: # Verifica se o player 1 venceu a partida
            print("Jogador 1 ganhou a rodada.")
            self.GameTable.tableList.clear()
            self.GameTable.gameRound += 1
            self.GameTable.gamePlay = 0
            for dom in self.Player2.playerHand:
                self.Player1.savings += dom.leftFaceNum + dom.rightFaceNum
            self.Player2.playerHand.clear()
            self.setup()

        if self.GameTable.currentPlayer == self.Player2: # Jogador 2 faz a jogada
            print("Jogador 2 faz a jogada")
            domUsado, placeholder = None, None
            if self.Player2.algorithm == "GreedySearch": domUsado, placeholder = self.Player2.greedySearchHeuristic(self.GameTable.tableList, self.Bank)
            elif self.Player2.algorithm == "AStar": domUsado, placeholder = self.Player2.aStarHeuristic(self.GameTable.tableList, self.Bank)
            if domUsado is None and placeholder is None:
                self.GameTable.currentPlayer = self.Player1
                return
            if len(self.GameTable.tableList) == 1:
                self.GameTable.add_dom_to_start(Domino.Domino("pholder", -2, "pholder", -2, gConst.DOMINO_SCALE))
                self.GameTable.add_dom_to_end(Domino.Domino("pholder", -1, "pholder", -1, gConst.DOMINO_SCALE))
                placeholder.update_domino(domUsado)
                computarJogada(domUsado)
            else:
                if placeholder.leftFaceNum == -2: # Jogando no começo
                    placeholder.update_domino(domUsado)
                    if self.GameTable.tableList[1].leftFaceNum == domUsado.leftFaceNum:
                        print("Turn right")
                        placeholder.reverse_domino()
                    computarJogada(domUsado)
                    self.GameTable.add_dom_to_start(Domino.Domino("pholder", -2, "pholder", -2, gConst.DOMINO_SCALE))
                if placeholder.leftFaceNum == -1:  # Jogando no fim
                    placeholder.update_domino(domUsado)
                    if self.GameTable.tableList[len(self.GameTable.tableList) - 2].rightFaceNum == domUsado.rightFaceNum:
                        print("Turn left")
                        placeholder.reverse_domino()
                    computarJogada(domUsado)
                    self.GameTable.add_dom_to_end(Domino.Domino("pholder", -1, "pholder", -1, gConst.DOMINO_SCALE))
            self.GameTable.currentPlayer = self.Player1

        if len(self.Player2.playerHand) == 0: # Verifica se o player 2 venceu a partida depois da jogada
            print("Jogador 2 ganhou a rodada.")
            self.GameTable.tableList.clear()
            self.GameTable.gameRound += 1
            self.GameTable.gamePlay = 0
            for dom in self.Player1.playerHand:
                self.Player2.savings += dom.leftFaceNum + dom.rightFaceNum
            self.Player1.playerHand.clear()
            self.setup()

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        if 0 - gConst.SCREEN_WIDTH * 6 < self.camera_sprites.position[0] + (scroll_y * gConst.SCROLL_SPEED) < gConst.SCREEN_WIDTH * 6:
            self.camera_sprites.move_to((self.camera_sprites.position[0] + (scroll_y * gConst.SCROLL_SPEED), self.camera_sprites.position[1]), 1)
            newPos = self.GameTable.cX - (scroll_y * gConst.SCROLL_SPEED)
            for dom in self.GameTable.tableList:
                dom.center_x = newPos - (self.camera_sprites.position[0] + (scroll_y * gConst.SCROLL_SPEED))
            self.GameTable.cX_flutuante = self.GameTable.tableList[0].center_x
            print(self.camera_sprites.position[0] + (scroll_y * gConst.SCROLL_SPEED))
            self.GameTable.tableList.update()
            self.GameTable.readjustment_table_position()

    def on_mouse_press(self, x, y, button, key_modifiers):
        if self.GameTable.currentPlayer == self.Player1:
            domino = arcade.get_sprites_at_point((x, y), self.Player1.playerHand)
            if len(domino) > 0:
                self.held_domino = [domino[-1]]
            compraDom = arcade.get_sprites_at_point((x, y), self.Bank.bankList)
            if compraDom: self.Bank.buy_domino(self.Player1)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        def computarJogada():
            self.Player1.remove_domino(self.held_domino[0])
            self.GameTable.gamePlay += 1
            self.GameTable.currentPlayer = self.Player2
            self.GameTable.print_list()

        # If we don't have any dominos, who cares
        if len(self.held_domino) == 0:
            return

        dom, distance = arcade.get_closest_sprite(self.held_domino[0], self.GameTable.tableList)
        if arcade.check_for_collision(self.held_domino[0], dom):
            if dom.leftFace == "pholder":
                if len(self.GameTable.tableList) == 1: # Primeira Jogada
                    self.GameTable.add_dom_to_start(Domino.Domino("pholder", -2, "pholder", -2, gConst.DOMINO_SCALE))
                    self.GameTable.add_dom_to_end(Domino.Domino("pholder", -1, "pholder", -1, gConst.DOMINO_SCALE))
                    dom.update_domino(self.held_domino[0])
                    computarJogada()
                else:
                    if dom.leftFaceNum == -2: # Placeholder do começo
                        posDomValue = self.GameTable.tableList[1].leftFaceNum
                        if posDomValue == self.held_domino[0].leftFaceNum or posDomValue == self.held_domino[0].rightFaceNum:
                            self.GameTable.add_dom_to_start(Domino.Domino("pholder", -2, "pholder", -2, gConst.DOMINO_SCALE))
                            dom.update_domino(self.held_domino[0])
                            if posDomValue == self.held_domino[0].leftFaceNum:
                                print("Turn right")
                                dom.reverse_domino()
                            computarJogada()
                    if dom.leftFaceNum == -1: # Placeholder do fim
                        posDomValue = self.GameTable.tableList[len(self.GameTable.tableList) - 2].rightFaceNum
                        if posDomValue == self.held_domino[0].leftFaceNum or posDomValue == self.held_domino[0].rightFaceNum:
                            self.GameTable.add_dom_to_end(Domino.Domino("pholder", -1, "pholder", -1, gConst.DOMINO_SCALE))
                            dom.update_domino(self.held_domino[0])
                            if posDomValue == self.held_domino[0].rightFaceNum:
                                print("Turn left")
                                dom.reverse_domino()
                            computarJogada()

        self.Player1.desEmphasize()
        self.Player1.readjustment_hand_position()
        self.held_domino = []

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
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

    def on_key_press(self, symbol, modifier):
        #if symbol == arcade.key.LEFT:

        #if symbol == arcade.KEY.RIGHT:

        if symbol == arcade.key.ESCAPE and self.Vencedor is not None:
            menu_view = MenuView.MenuView()
            self.window.show_view(menu_view)
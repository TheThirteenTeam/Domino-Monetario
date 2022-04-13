import arcade
import gameConstants as gConst

class Player: # Objeto Player (Lista de objetos dominos)

    def __init__(self, *args):
        self.savings = 0
        self.playerHandX = 0
        self.playerHandY = 0
        if len(args) == 1: self.algorithm = args[0]
        self.playerHand = arcade.SpriteList()

    def add_domino(self, domino):
        self.playerHand.append(domino)
        self.readjustment_hand_position()

    def remove_domino(self, domino: arcade.Sprite):
        self.playerHand.remove(domino)
        self.readjustment_hand_position()

    def turn_dominos(self, side):
        for dom in self.playerHand:
            if side == "Up":
                dom.texture = arcade.load_texture(f"images/domino{dom.leftFace}_{dom.rightFace}.png")
                dom.update()
            elif side == "Down":
                dom.texture = arcade.load_texture(f"images/dominoBack.png")
                dom.update()

    def set_position(self, x, y):
        self.playerHandX = x
        self.playerHandY = y
        self.readjustment_hand_position()

    def set_angle(self, value):
        for dom in self.playerHand:
            dom.angle = value

    def readjustment_hand_position(self):
        for i, domX in enumerate(self.playerHand):
            domX.position = ((gConst.SCREEN_WIDTH / (len(self.playerHand) + 6)) * (i + 3)) + self.playerHandX, self.playerHandY

    def emphasize(self, domino: arcade.Sprite):
        for dom in self.playerHand:
            if dom != domino: dom.alpha = 80

    def desEmphasize(self):
        for dom in self.playerHand:
            dom.alpha = 255

    ''' GreedySearch
        1 - Jogar as duplas primeiro.
        2 - Jogar a peça de valor mais alto. (É bom pro inimigo que tenha peças altas na minha mão por causa da poupança)
        3 - Jogar peças com valores dupliacados.
    '''
    def greedySearchHeuristic(self, gameList):
        for dom in self.playerHand:
            return

    ''' AStar
        1 - Jogar as duplas primeiro.
        2 - Jogar a peça de valor mais alto. (É bom pro inimigo que tenha peças altas na minha mão por causa da poupança)
        3 - Jogar peças com valores dupliacados.
    '''
    def aStarHeuristic(self, gameList):
        for dom in self.playerHand:
            return

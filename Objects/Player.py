import arcade
import gameConstants as gConst

class Player: # Objeto Player (Lista de objetos dominos)

    def __init__(self, name, *args):
        self.name = name
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
    '''
    def greedySearchHeuristic(self, gamelist, bankObj):
        def greaterDomino(listaPercorre):
            higher_pair = listaPercorre[0]
            contDuplas = 0
            higher_tile = listaPercorre[0]
            for dom in listaPercorre:
                if higher_tile.leftFaceNum + higher_tile.rightFaceNum < dom.leftFaceNum + dom.rightFaceNum:
                    higher_tile = dom
                if higher_pair.leftFaceNum == higher_pair.rightFaceNum:
                    contDuplas += 1
                else:
                    higher_pair = dom
                if dom.leftFaceNum == dom.rightFaceNum and dom.leftFaceNum > higher_pair.leftFaceNum:
                    higher_pair = dom
            if contDuplas == 0:
                return higher_tile
            else:
                return higher_pair
        # Jogador 2 é o primeiro a jogar
        if len(gamelist) == 1:
            return greaterDomino(self.playerHand), gamelist[0]
        # Outras jogadas do jogador 2
        domJogado = None
        while domJogado is None:
            listaDominosPossiveis = []
            for dom in self.playerHand:
                if dom.rightFaceNum == gamelist[1].leftFaceNum or dom.rightFaceNum == gamelist[len(gamelist) - 2].rightFaceNum or \
                    dom.leftFaceNum == gamelist[1].leftFaceNum or dom.leftFaceNum == gamelist[len(gamelist) - 2].rightFaceNum:
                    listaDominosPossiveis += [dom]
            if len(listaDominosPossiveis) == 0:
                if len(bankObj.bankList) == 0:
                    return None, None
                bankObj.buy_domino(self)
                self.playerHand[len(self.playerHand) - 1].turn_domino("Down")
                pass
            else:
                melhorDomino = greaterDomino(listaDominosPossiveis)
                if melhorDomino.leftFaceNum == gamelist[1].leftFaceNum or melhorDomino.rightFaceNum == gamelist[1].leftFaceNum:
                    return melhorDomino, gamelist[0]
                if melhorDomino.leftFaceNum == gamelist[len(gamelist) - 2].rightFaceNum or melhorDomino.rightFaceNum == gamelist[len(gamelist) - 2].rightFaceNum:
                    return melhorDomino, gamelist[len(gamelist) - 1]

    ''' AStar
        1 - Jogar as duplas primeiro.
        2 - Jogar peças que já estiverem em quantidade na mesa.
        3 - Jogar a peça de valor mais alto. (É bom pro inimigo que tenha peças altas na minha mão por causa da poupança)
    '''
    def aStarHeuristic(self, gameList, bankObj):
        for dom in self.playerHand:
            return

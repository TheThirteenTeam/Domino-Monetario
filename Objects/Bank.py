import arcade

class Bank: # Objeto Banco (Lista de objetos dominos)

    def __init__(self):
        self.bankList = arcade.SpriteList()

    def set_position(self, x, y):
        for dom in self.bankList:
            dom.position = x, y

    def shuffle(self):
        self.bankList.shuffle()

    def add_domino(self, domino):
        self.bankList.append(domino)

    def remove_domino(self, domino):
        self.bankList.remove(domino)

    def buy_domino(self, player):
        player.playerHand += self.bankList.pop()

    def set_angle(self, value):
        for dom in self.bankList:
            dom.angle = value

    def pull_to_top(self, domino: arcade.Sprite):
        """ Pull card to top of rendering order (last to render, looks on-top) """
        # Remove, and append to the end
        self.bankList.remove(domino)
        self.bankList.append(domino)

    def turn_dominos(self, side):
        for dom in self.bankList:
            if side == "Up":
                dom.texture = arcade.load_texture(f"images/domino{dom.leftFace}_{dom.rightFace}.png")
                dom.update()
            elif side == "Down":
                dom.texture = arcade.load_texture(f"images/dominoBack.png")
                dom.update()
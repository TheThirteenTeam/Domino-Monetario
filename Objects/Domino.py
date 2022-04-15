import arcade

class Domino(arcade.Sprite): # Sprite/Objeto domino

    def __init__(self, leftFace, leftFaceNum, rightFace, rightFaceNum, scale=1):
        self.img_source = f"images/domino{leftFace}_{rightFace}.png"
        super().__init__(self.img_source, scale, hit_box_algorithm="None")
        self.leftFace = leftFace
        self.leftFaceNum = leftFaceNum
        self.rightFace = rightFace
        self.rightFaceNum = rightFaceNum
        self.isUpSide = True
        self.angle = 0
        self.visible = True

    def update_domino(self, domino):
        self.leftFace = domino.leftFace
        self.leftFaceNum = domino.leftFaceNum
        self.rightFace = domino.rightFace
        self.rightFaceNum = domino.rightFaceNum
        self.texture = arcade.load_texture(f"images/domino{domino.leftFace}_{domino.rightFace}.png")

    def set_position(self, x, y):
        self.position = x, y

    def set_angle(self, value):
        self.angle = value

    def set_scale(self, value):
        self.scale = value

    def turn_domino(self, side):
        if side == "Up":
            self.texture = arcade.load_texture(f"images/domino{self.leftFace}_{self.rightFace}.png")
            self.update()
        elif side == "Down":
            self.texture = arcade.load_texture(f"images/dominoBack.png")
            self.update()

    def reverse_domino(self):
        aux = self.leftFaceNum
        self.leftFaceNum = self.rightFaceNum
        self.rightFaceNum = aux
        self.set_angle(180)

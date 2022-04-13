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

    def set_sprite(self, leftFace, rightFace):
        self.texture = arcade.load_texture(f"images/domino{leftFace}_{rightFace}.png")

    def set_position(self, x, y):
        self.position = x, y

    def set_angle(self, value):
        self.angle = value
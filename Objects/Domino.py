import arcade

class Domino(arcade.Sprite): # Sprite/Objeto domino

    def __init__(self, leftFace, rightFace, scale=1):
        self.img_source = f"images/domino{leftFace}_{rightFace}.png"
        super().__init__(self.img_source, scale, hit_box_algorithm="None")
        self.leftFace = leftFace
        self.rightFace = rightFace
        self.isUpSide = True
        self.angle = 90

    def set_sprite(self, leftFace, rightFace):
        self.texture = arcade.load_texture(f"images/domino{leftFace}_{rightFace}.png")
import arcade

class Placeholder(arcade.Sprite):

    def __init__(self, scale=1):
        self.img_source = f"images/placeholder.png"
        super().__init__(self.img_source, scale, hit_box_algorithm="None")
        self.angle = 90
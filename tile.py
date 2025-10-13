from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty

from spriteSheet import SpriteSheet

class Tile(Widget):
    texture = ObjectProperty(None)  # holds a Texture
    tileType = NumericProperty(0)

    def __init__(self, tileType, **kwargs):
        super().__init__(**kwargs)
        self.tileType = tileType
        self.sheet = SpriteSheet("images/shopsprite.png", (46, 46))
        self.texture = self.sheet.getImage(self.tileType)
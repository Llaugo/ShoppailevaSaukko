from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty

from spriteSheet import SpriteSheet
import item
import const
import random

class Tile(Widget):
    texture = ObjectProperty(None)  # holds a Texture
    tileType = NumericProperty(0)

    def __init__(self, tileType, roomDistance=0, **kwargs):
        super().__init__(**kwargs)
        self.tileType = tileType
        self.roomDistance = roomDistance
        self.sheet = SpriteSheet("images/shopsprite.png", (46, 46))
        self.texture = self.sheet.getImage(self.tileType)
        if self.isShelf() and const.itemProbability > random.random(): # Randomize if a shelf tile has an item or not
            self.addItem(self.roomDistance)

    # Adds an item to this tile if it is a shelf and the item isn't set already
    def addItem(self, roomDistance):
        if self.isShelf() and not self.item:
            self.item = item.Item(roomDistance)

    # Returns True if this tile is a shelf tile and False otherwise
    def isShelf(self):
        if self.tileType >= 10 and self.tileType <= 18:
            return True
        else:
            return False
        
    def isWater(self):
        if self.tileType == 20:
            return True
        else:
            return False
        
    def isWall(self):
        if self.tileType == 9:
            return True
        else:
            return False
        
    def isAdvert(self):
        if self.tileType == 7:
            return True
        else:
            return False
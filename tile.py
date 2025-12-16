from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty

from spriteSheet import SpriteSheet
import item
import const
import random

class Tile(Widget):
    texture = ObjectProperty(None)  # holds a Texture
    tileType = NumericProperty(0)
    item = ObjectProperty(allownone=True, rebind=True)

    def __init__(self, tileType, roomDistance=0, **kwargs):
        super().__init__(**kwargs)
        self.tileType = tileType
        self.roomDistance = roomDistance
        self.sheet = SpriteSheet("images/shopsprite.png", (46, 46))
        self.texture = self.sheet.getImage(self.tileType)
        if self.isShelf() and const.itemProbability > random.random(): # Randomize if a shelf tile has an item or not
            self.addItem(self.roomDistance)

    def on_kv_post(self, _):
        #self.item = self.ids.item
        pass

    def update(self, dt):
        if self.item:
            self.item.update(dt)

    # Adds an item to this tile if it is a shelf and the item isn't set already
    def addItem(self, roomDistance):
        if self.isShelf() and not self.item:
            newItem = item.Item(roomDistance)
            self.bind(size=lambda *_: setattr(newItem, "size", self.size))
            self.bind(pos=lambda *_: setattr(newItem, "pos", (self.pos[0] + 20*newItem.corner[0], self.pos[1] + 20*newItem.corner[1])))
            self.add_widget(newItem)
            self.item = newItem

    def removeItem(self):
        if self.item:
            self.remove_widget(self.item)
            self.item = None

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
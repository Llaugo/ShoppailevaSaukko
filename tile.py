from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty
from kivy.metrics import dp

from spriteSheet import SpriteSheet
from item import Item
import const
import random

# Tile class hold info on each individual tile on the game board
class Tile(Widget):
    texture = ObjectProperty(None)  # holds a Texture
    tileType = NumericProperty(0)
    item = ObjectProperty(allownone=True, rebind=True)
    crate = ObjectProperty(allownone=True, rebind=True)

    def __init__(self, tileType, roomDistance=0, **kwargs):
        super().__init__(**kwargs)
        self.tileType = tileType
        self.roomDistance = roomDistance
        self.solid = True  # Is the tile solid (player collides)
        if tileType < 9: self.solid = False # The first eight tile types are not solid and can be walked on
        self.sheet = SpriteSheet("images/shopsprite.png", (46, 46))
        self.texture = self.sheet.getImage(self.tileType)
        self.bind(size=self._syncItemGeometry, pos=self._syncItemGeometry)
        if self.isShelf() and const.itemProbability > random.random(): # Randomize if a shelf tile has an item or not
            self.addItem(self.roomDistance)
        # Adding crates
        if self.tileType == 5:
            crate = Crate() # Generate new item
            # Bind crate size and pos to tile size and pos to change reflexively with tile
            self.bind(size=lambda *_: setattr(crate, "size", (self.size[0]*0.5, self.size[1]*0.5)))
            self.bind(pos=lambda *_: setattr(crate, "pos", (self.pos[0] + 51, self.pos[1] + 18)))
            self.add_widget(crate) # Add item image on top of tile
            self.crate = crate

    def on_kv_post(self, _):
        #self.item = self.ids.item
        pass

    # Update tile and its item
    def update(self, dt):
        if self.item:
            self.item.update(dt)

    def updateImage(self):
        self.texture = self.sheet.getImage(self.tileType)

    def _syncItemGeometry(self, *_):
        if self.item is None:
            return
        self.item.size = (self.size[0]*0.76, self.size[1]*0.76)
        self.item.pos = (
            self.pos[0] + dp(8) + 10*dp(self.item.corner[0]),
            self.pos[1] + dp(8) + 10*dp(self.item.corner[1]),
        )

    # Adds an item to tile
    def addItem(self, roomDistance):
        if self.isShelf() and not self.item: # If it's a shelf and the item isn't set already
            newItem = Item(roomDistance) # Generate new item
            self.add_widget(newItem) # Add item image on top of tile
            self.item = newItem
            self._syncItemGeometry()
            return newItem
        return None

    # Delete any item on tile
    def removeItem(self):
        if self.item:
            self.remove_widget(self.item)
            self.item = None

    # Delete any crate on tile
    def removeCrate(self):
        if self.crate:
            self.remove_widget(self.crate)
            self.crate = None
            self.tileType = 6
            self.updateImage()
            return True
        return False

    # Make this tile a wall
    def makeWall(self):
        self.tileType = 9
        self.solid = True
        self.updateImage()

    # Returns True if this tile is a shelf tile and False otherwise
    def isShelf(self):
        if self.tileType >= 10 and self.tileType <= 18:
            return True
        else:
            return False
        
    # Returns True if this tile is a water tile and False otherwise
    def isWater(self):
        if self.tileType == 20:
            return True
        else:
            return False
        
    # Returns True if this tile is a wall tile and False otherwise
    def isWall(self):
        if self.tileType == 9:
            return True
        else:
            return False
        
    # Returns True if this tile is an advert tile and False otherwise
    def isAdvert(self):
        if self.tileType == 7:
            return True
        else:
            return False
        
    def hasCrate(self):
        if self.crate is not None:
            return True
        else:
            return False
        
    """
    def isDoor(self):
        if self.tileType == 21:
            return True
        else:
            return False
    """

class Crate(Widget):
    pass

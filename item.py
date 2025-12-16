from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty


import const
from spriteSheet import SpriteSheet
import random

class Item(Widget):
    texture = ObjectProperty(None)

    # roomDistance: How far away the room/item is from the middle. Far away rooms produce more rarer items.
    def __init__(self, roomDistance=0, **kwargs):
        super().__init__(**kwargs)
        self.picType = random.randint(0,3)*4 # Randomize item image
        self.shinePhase = 0 # Goes from 0 to 4 (Animation helper)
        self.sheet = SpriteSheet('images/item_sheet.png', (35,35))
        self.texture = self.sheet.getImage(self.picType)
        self.corner = (random.choice([-1,1]), random.choice([-1,1]))
        self.rarityLevel = -1
        self.name = "DefaultName"
        self.randomizeItem(roomDistance) # Determine item name/type

    def setName(self, newName, newRarity):
        self.name = newName
        self.rarityLevel = newRarity

    # update item animated shine effect
    def update(self, dt):
        oldShine = round(self.shinePhase)
        self.shinePhase += 0.05
        if oldShine != round(self.shinePhase):
            self.texture = self.sheet.getImage(self.picType + (round(self.shinePhase) % 4))

    # Set the name/type of the item randomly
    def randomizeItem(self, roomDistance):
        randomFloat = random.random()
        for i in range(len(const.itemRarity[roomDistance])): # Get item rarities according to the room distance
            if randomFloat <= const.itemRarity[roomDistance][i]: # Compare rarity list to the random float
                self.rarityLevel = i
                self.name = const.shop()[i][random.randint(0,4)]
                return
        raise ValueError('Could not determine item based on rarity level.')
        


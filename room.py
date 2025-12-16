from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty

import random
from tile import Tile
import const

class Room(FloatLayout):
    tileSize = NumericProperty(const.tileSize)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = None # Each tile in a grid
        self.exit = None
        self.items = []                         # items in the room
        self.carts = []                         # carts in the room
        self.npcs = []                          # npcs in the room
        self.npcCartPairs = []                  # pairs of npcs and carts
        self.pushableCarts = []                 # carts that can be pushed
        self.walls = []                         # walls and solid objects of the room
        self.shelves = []                       # outside walls of the room
        self.waters = []                        # watertiles in the room
        self.adverts = []                       # adverts in the room

    #def on_kv_post(self, _):
    #    pass

    def update(self, dt, player):
        for row in self.layout:
            for tile in row:
                tile.update(dt)

    def removeItem(self, item):
        for row in self.layout:
            for tile in row:
                if tile.item == item:
                    tile.removeItem()
                    break
        self.items.remove(item)

    def setRoom(self, layout):
        org_layout = layout
        g = self.ids.grid
        g.clear_widgets()
        self.layout = [[None]*len(org_layout[0]) for _ in range(len(org_layout))]
        g.cols = len(org_layout[0])
        lift = len(org_layout) <= 5
        for i, row in enumerate(org_layout):
            for j, c in enumerate(row):
                if c == 0: # Wall
                    if lift: # Lift has special walls
                        tile = Tile(19)
                    else:
                        tile = Tile(9)
                    self.walls.append(tile)
                elif c == 1: # Floor
                    if lift: # Lift has special floor
                        tile = Tile(4)
                    else:
                        if i == 0 or j == 0 or i == len(layout)-1 or j == len(layout)-1:
                            tile = Tile(8)
                        else:
                            tile = Tile(random.randint(1,3))
                elif c == 2: # Shelf
                    tile = Tile(random.randint(10,18)) # + self.roomDistance
                    if tile.item:
                        self.items.append(tile.item)
                    self.shelves.append(tile)
                elif c == 3: # Exit
                    tile = Tile(0)
                    self.exit = tile
                elif c == 4 or c == 40: # Crate
                    if c == 40 and random.random() > const.crateProbability:
                        tile = Tile(random.randint(1,3)) # Floor
                    else:
                        tile = Tile(5) # Crate
                elif 50 <= c <= 53: # Cart
                    tile = Tile(random.randint(1,3))
                    #self.carts.append(cart.Cart(cartPos, randDir(c-50), self.lang, self.roomDistance))
                elif 60 <= c <= 63: # NPC
                    tile = Tile(random.randint(1,3))
                    #self.npcs.append(npc.Npc(npcPos,randDir(c-60)))
                elif c == 7: # Water
                    tile = Tile(20)
                    self.waters.append(tile)
                elif 80 <= c <= 83: # Advert
                    tile = Tile(7)
                    #newTile.setAdvert(randDir(c-80))
                elif c > 0:
                    tile = Tile(4)
                else:
                    raise ValueError(f'The room layout contains unknown value: {c}')
                g.add_widget(tile)
                self.layout[i][j] = tile
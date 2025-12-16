from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty
from kivy.clock import Clock
from kivy.core.window import Window

import const
import room

# Class for the game (floors)
class ShopperGame(Widget):
    design_w = NumericProperty(const.worldWidth)
    design_h = NumericProperty(const.worldHeigth)
    player = ObjectProperty(None)
    currentRoom = ObjectProperty(None)
    timer = NumericProperty(const.floorTime)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pressed = set()
        Window.bind(on_key_down=self.on_key_down, on_key_up=self.on_key_up)

    def on_kv_post(self, _):
        self.currentRoom = self.ids.room
        layout = const.testRoom
        self.currentRoom.setRoom(layout[0])
        bg = self.ids.bg
        def rescale(*_):
            if not bg.texture:
                return
            drawn_w, drawn_h = bg.norm_image_size # actual rendered size
            scale = min(drawn_w/self.design_w, drawn_h/self.design_h) # uniform scale to fit
            self.ids.world.scale = scale
        self.size = Window.size
        self.bind(size=rescale)

        grid = self.currentRoom.ids.grid
        grid.col_default_width = const.worldHeigth/(const.floorSize*1.7)
        grid.row_default_height = const.worldHeigth/(const.floorSize*1.7)
        player = self.ids.player
        player.size = (player.width*0.8, player.height*0.8)

    def on_key_down(self, _win, key, _sc, _cp, _mods):
        self.pressed.add(key); return True
    def on_key_up(self, _win, key, *_):
        self.pressed.discard(key); return True
    
    def update(self, dt):
        player = self.ids.player
        if dt < 0.3: # Player can phase through walls if there's a spike in dt
            player.update(dt, self)
            self.currentRoom.update(dt, player)
            onItem = 0
            for i, item in enumerate(self.currentRoom.items):
                if player.collide_widget(item):
                    onItem = 1
                    break
            self.ids.itemButton.opacity = onItem
        self.timer = max(self.timer - dt, 0)

    def pickUpItem(self):
        for item in self.currentRoom.items:
            if self.ids.player.collide_widget(item):
                self.currentRoom.removeItem(item)
                break


        
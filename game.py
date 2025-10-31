from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.core.window import Window

import const
import room

# Class for the game (floors)
class ShopperGame(Widget):
    player = ObjectProperty(None)
    currentRoom = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pressed = set()
        Window.bind(on_key_down=self.on_key_down, on_key_up=self.on_key_up)
        Clock.schedule_interval(self.update, 1/60)

    def on_kv_post(self, _):
        self.currentRoom = self.ids.room
        layout = const.testRoom
        self.currentRoom.setRoom(layout[0])

    def on_key_down(self, _win, key, _sc, _cp, _mods):
        self.pressed.add(key); return True
    def on_key_up(self, _win, key, *_):
        self.pressed.discard(key); return True
    
    def update(self, dt):
        player = self.ids.player
        player.update(dt, self)
        
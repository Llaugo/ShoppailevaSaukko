from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from playerClass import Player

class ShopperGame(Widget):
    player = ObjectProperty(None)
    def update(self, dt):
        pass

class ShopperGame(Widget):
    def update(self, dt):
        pass  # game loop

class MenuScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class ShopperApp(App):

    def build(self):
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))

        return sm

if __name__ == '__main__':
    ShopperApp().run()

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
from playerClass import Player
import const

class ShopperGame(Widget):
    player = ObjectProperty(None)
    def update(self, dt):
        pass

class MenuScreen(Screen):
    pass

class StrengthScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class QuestionScreen(Screen):
    pass

class ShopperApp(App):

    def build(self):
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(StrengthScreen(name='strengths'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(QuestionScreen(name='?'))

        return sm

if __name__ == '__main__':
    Window.size = (1000, 600)
    ShopperApp().run()

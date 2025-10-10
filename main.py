from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty, DictProperty, StringProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.core.text import LabelBase
from playerClass import Player
import json, os
import strengthMenu
import const

# Default font Courier-Prime
LabelBase.register(
    name="Roboto",  # override Kivy's default family
    fn_regular="fonts/Courier_Prime/CourierPrime-Regular.ttf",
    fn_bold="fonts/Courier_Prime/CourierPrime-Bold.ttf",
    fn_italic="fonts/Courier_Prime/CourierPrime-Italic.ttf",
    fn_bolditalic="fonts/Courier_Prime/CourierPrime-Bolditalic.ttf",
)

class ShopperGame(Widget):
    player = ObjectProperty(None)
    def update(self, dt):
        pass

class MenuScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class QuestionScreen(Screen):
    pass

class ShopperApp(App):
    lang = StringProperty("fi") # Current language
    i18n = DictProperty({}) # Current language file

    def build(self):
        self.setLanguage(self.lang)
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(strengthMenu.StrengthMenu(name='strengths'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(QuestionScreen(name='?'))
        return sm
    
    def setLanguage(self, newLang):
        path = os.path.join("i18n", f"{newLang}.json")
        with open(path, "r", encoding="utf-8") as file:
            self.i18n = json.load(file)
        self.lang = newLang

    # get any text and print key if not set
    def tr(self, key):
        return self.i18n.get(key, key)

if __name__ == '__main__':
    Window.size = (1000, 600)
    ShopperApp().run()

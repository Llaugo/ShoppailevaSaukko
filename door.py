from kivy.uix.widget import Widget
from kivy.properties import StringProperty

class Door(Widget):
    direction = StringProperty("")  # "north", "south", "east", "west"
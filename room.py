from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ListProperty


from tile import Tile

class Room(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = None

    def setRoom(self, layout):
        org_layout = layout[0]
        g = self.ids.grid
        g.clear_widgets()
        self.layout = [[None]*len(org_layout[0]) for _ in range(len(org_layout))]
        g.cols = len(org_layout[0])
        for r, row in enumerate(org_layout):
            for c, n in enumerate(row):
                tile = Tile(n)
                g.add_widget(tile)
                self.layout[r][c] = tile
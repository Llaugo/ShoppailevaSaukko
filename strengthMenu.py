from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import NumericProperty, ListProperty, BooleanProperty, StringProperty
from kivy.animation import Animation
from kivy.app import App
import strengthCard
from spriteSheet import SpriteSheet
import random

class DeckButton(ButtonBehavior, Image):
    index = NumericProperty(0)

class CardButton(ButtonBehavior, Image):
    index = NumericProperty(0)
    selected = BooleanProperty(False)
    arrow_src = StringProperty("images/otter_1.png")

class StrengthMenu(Screen):
    inspectPile = NumericProperty(-1)
    decks = ListProperty()
    favorites = ListProperty([0, 0, 0, 0, 0, 0])

    @property
    def tr(self):
        return App.get_running_app().tr
    
    def on_kv_post(self, _):
        self.decks: list[list[int]] = []
        self.cardSprite = SpriteSheet('images/strength_sheet.png', (246, 386))
        for i in range(26):
            if i in (0, 5, 10, 14, 17, 21):
                self.decks.append([])
            self.decks[-1].append(i)
        self.favorites: list[int] = [0, 0, 0, 0, 0, 0]
            
    # Open selected deck's cards on the screen
    def selectDeck(self, i):
        if self.inspectPile != -1:
            self.restoreDeck(self.inspectPile)
            self.clearCards()
        if self.inspectPile == i:
            self.inspectPile = -1
            self.ids.selecttitle.text = ""
            self.ids.selectcategory.text = self.tr("strengths.pickpile")
            return
        self.inspectPile = i
        fav = self.favorites[i]
        cards = self.decks[i]
        self.ids.cards_rv.data = [{"source": f"images/cards/card{c}.png", "index": j, "selected": (j == fav)} for j, c in enumerate(cards)]
        self.openDeck(i)

    def deckAt(self,i):
        return self.ids.get(f"deck{i}")
    
    def labelAt(self,i):
        return self.ids.get(f"label{i}")
    
    def coverAt(self,i):
        return self.ids.get(f"cover{i}")
    
    def restoreDeck(self, i):
        b = self.deckAt(i)
        if b:
            b.opacity = 1
            self.coverAt(i).opacity = 1

    def clearCards(self):
        self.ids.cards_rv.data = []

    def openDeck(self, i):
        d = self.deckAt(i)
        if not d:
            return
        self.ids.selecttitle.text = self.labelAt(i).text
        self.ids.selectcategory.text = self.tr("strengths.pickcard")
        d.opacity = 0
        self.coverAt(i).opacity = 0
        rv = self.ids.cards_rv
        layout = rv.children[0]
        orig_spc = layout.spacing
        layout.spacing = -6*layout.spacing
        Animation(spacing=orig_spc, duration=0.3, t='out_cubic').start(layout)

    def on_card_tap(self, i):
        if self.inspectPile == -1: return
        self.favorites[self.inspectPile] = i
        self.coverAt(self.inspectPile).source = f"images/cards/card{self.decks[self.inspectPile][i]}.png"
        rv = self.ids.cards_rv
        for k in range(len(rv.data)):
            rv.data[k]["selected"] = (k == i)
        rv.refresh_from_data()

    def randomizeFavo(self):
        self.favorites = []
        for i in range(len(self.decks)):
            pickedCard = random.randint(0, len(self.decks[i])-1)
            self.favorites.append(pickedCard)
            self.coverAt(i).source = f"images/cards/card{self.decks[i][pickedCard]}.png"
        if self.inspectPile != -1:
            fav = self.favorites[self.inspectPile]
            cards = self.decks[self.inspectPile]
            self.ids.cards_rv.data = [{"source": f"images/cards/card{c}.png", "index": j, "selected": (j == fav)} for j, c in enumerate(cards)]
            


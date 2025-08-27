from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import NumericProperty, ListProperty
import strengthCard
from spriteSheet import SpriteSheet

class DeckButton(ButtonBehavior, Image):
    index = NumericProperty(0)

class StrengthMenu(Screen):
    decks = ListProperty()
    inspectPile = NumericProperty(-1)
    
    def on_kv_post(self, _):
        self.decks = []
        self.cardSprite = SpriteSheet('images/strength_sheet.png', (246, 386))
        for i in range(26):
            if i == 0 or i == 5 or i == 10 or i == 14 or i == 17 or i == 21:
                self.decks.append([])
            self.decks[-1].append(f"images/cards/card{i}.png")
        for i in range(6):
            deck = self.ids.get(f"deck{i}")
            if deck:
                deck.index = i
                deck.source = f"images/card_pile.png"

    def selectDeck(self, i):
        print("selected: " + str(i))
        if self.inspectPile == i:
            self.inspectPile = -1
            self.ids.cards_rv.data = []
            return
        self.inspectPile = i
        self.ids.cards_rv.data = [{"source": c} for c in self.decks[i]]


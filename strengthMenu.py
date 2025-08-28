from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import NumericProperty, ListProperty
from kivy.animation import Animation
import strengthCard
from spriteSheet import SpriteSheet

class DeckButton(ButtonBehavior, Image):
    index = NumericProperty(0)

class StrengthMenu(Screen):
    inspectPile = NumericProperty(-1)
    decks = ListProperty()
    
    def on_kv_post(self, _):
        self.decks = []
        self.cardSprite = SpriteSheet('images/strength_sheet.png', (246, 386))
        for i in range(26):
            if i == 0 or i == 5 or i == 10 or i == 14 or i == 17 or i == 21:
                self.decks.append([])
            self.decks[-1].append(i)
            #self.decks[-1].append(f"images/cards/card{i}.png")
            
    def selectDeck(self, i):
        if self.inspectPile != -1:
            self.restoreDeck(self.inspectPile)
            self.clearCards()
        if self.inspectPile == i:
            self.inspectPile = -1
            self.ids.cards_rv.data = []
            return
        self.inspectPile = i
        self.ids.cards_rv.data = [{"source": f"images/cards/card{c}.png"} for c in self.decks[i]]
        self.openDeck(i)

    def deckAt(self,i):
        return self.ids.get(f"deck{i}")
    
    def restoreDeck(self, i):
        b = self.deckAt(i)
        if b:
            b.opacity = 1

    def clearCards(self):
        view = self.ids.cards_rv
        cards = self.decks[self.inspectPile]
        for c in cards:
            view.remove_widget(c)

    def openDeck(self, i):
        d = self.deckAt(i)
        if not d:
            return
        d.opacity = 0
        rv = self.ids.cards_rv
        layout = rv.children[0]
        items = layout.children
        #for w in items:
            #orig_size = w.size
            #w.size = (w.size[0]*0.2,w.size[1]*0.2)
            #Animation(size=orig_size, duration=2, t='out_cubic').start(w)
        orig_spc = layout.spacing
        layout.spacing = -6*layout.spacing
        spcAnim = Animation(spacing=orig_spc, duration=0.3, t='out_cubic').start(layout)
            


from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import NumericProperty, ListProperty, BooleanProperty, StringProperty
from kivy.animation import Animation
from kivy.app import App
import strengthCard
from spriteSheet import SpriteSheet
import random

# Interactable deck image
class DeckButton(ButtonBehavior, Image):
    index = NumericProperty(0)

# Interactable card image
class CardButton(ButtonBehavior, Image):
    index = NumericProperty(0)
    selected = BooleanProperty(False)
    arrow_src = StringProperty("images/otter_1.png")

# Object that holds all the strength menu components
class StrengthMenu(Screen):
    inspectPile = NumericProperty(-1) # Which deck is selected for wiewing
    decks = ListProperty() # List of all decks
    favorites = ListProperty([0, 0, 0, 0, 0, 0]) # List of the favourite card from each deck

    # Get any text
    @property
    def tr(self):
        return App.get_running_app().tr
    
    def on_kv_post(self, _):
        self.decks: list[list[int]] = []
        self.cardSprite = SpriteSheet('images/strength_sheet.png', (246, 386))
        # Init decks
        for i in range(26):
            if i in (0, 5, 10, 14, 17, 21):
                self.decks.append([])
            self.decks[-1].append(i)
        self.favorites: list[int] = [0, 0, 0, 0, 0, 0]
            
    # Open selected deck's cards on the screen
    def selectDeck(self, i):
        if self.inspectPile != -1: # If any deck is already open
            self.restoreDeck(self.inspectPile) # Show deck image
            self.clearCards() # clear table
        if self.inspectPile == i: # If selected deck was already open
            # Show nothing on the table
            self.inspectPile = -1
            self.ids.selecttitle.text = ""
            self.ids.selectcategory.text = self.tr("strengths.pickpile")
            self.changeInfo(self.inspectPile)
            return
        self.inspectPile = i # Selected deck
        fav = self.favorites[i] # Selected deck's favorite card
        cards = self.decks[i] # Selected deck's all cards
        self.ids.cards_rv.data = [{"source": f"images/cards/card{c}.png", "index": j, "selected": (j == fav)} for j, c in enumerate(cards)] # Update table cards data
        self.openDeck(i)

    # get deck id
    def deckAt(self,i):
        return self.ids.get(f"deck{i}")
    
    # get label id
    def labelAt(self,i):
        return self.ids.get(f"label{i}")
    
    # get cover id
    def coverAt(self,i):
        return self.ids.get(f"cover{i}")
    
    # Show deck and the covering card image
    def restoreDeck(self, i):
        b = self.deckAt(i)
        if b:
            b.opacity = 1
            self.coverAt(i).opacity = 1

    # clear table
    def clearCards(self):
        self.ids.cards_rv.data = []

    # Change the info text
    # i: index of the text wanted. -1 for default
    def changeInfo(self, i):
        if i == -1:
            self.ids.infotext.text = self.tr("strengths.info")
        else:
            self.ids.infotext.text = self.tr(f"strengths.card{i}_info")

    # Open selected deck to table
    def openDeck(self, i):
        d = self.deckAt(i)
        if not d:
            return
        self.ids.selecttitle.text = self.labelAt(i).text
        self.ids.selectcategory.text = self.tr("strengths.pickcard")
        d.opacity = 0 # Make deck image vanish
        self.coverAt(i).opacity = 0 # Make deck cover vanish
        rv = self.ids.cards_rv
        layout = rv.children[0]
        orig_spc = layout.spacing
        layout.spacing = -6*layout.spacing
        Animation(spacing=orig_spc, duration=0.3, t='out_cubic').start(layout) # Roll cards onto table

    # Clicking a card sets it to favourite and shows its info text
    def on_card_tap(self, i):
        if self.inspectPile == -1: # If no deck is open, return
            return
        self.favorites[self.inspectPile] = i # Set favourite of the pile
        self.coverAt(self.inspectPile).source = f"images/cards/card{self.decks[self.inspectPile][i]}.png" # Change the pile cover
        self.changeInfo(self.decks[self.inspectPile][i]) # Change info text
        rv = self.ids.cards_rv
        for k in range(len(rv.data)):
            rv.data[k]["selected"] = (k == i)
        rv.refresh_from_data()

    # Randomize all favourite cards
    def randomizeFavo(self):
        self.favorites = []
        for i in range(len(self.decks)):
            pickedCard = random.randint(0, len(self.decks[i])-1) # Choose random card
            self.favorites.append(pickedCard) # Make favourite
            self.coverAt(i).source = f"images/cards/card{self.decks[i][pickedCard]}.png" # Make cover image
        if self.inspectPile != -1: # If a deck is open, update the open cards accordingly
            fav = self.favorites[self.inspectPile]
            cards = self.decks[self.inspectPile]
            self.ids.cards_rv.data = [{"source": f"images/cards/card{c}.png", "index": j, "selected": (j == fav)} for j, c in enumerate(cards)]
            


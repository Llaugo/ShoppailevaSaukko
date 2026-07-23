from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty

import math
import const
from spriteSheet import SpriteSheet
import strengthCard

class StrengthDeck(Widget):
    hasReadyCard = BooleanProperty(False)

    # cards: list of strength cards
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.shinePhase = 0
        self.overlaySheet = SpriteSheet('images/card_overlay.png', (250,350))
        self.cards = []
        self.activate = False # Activate current card

    def setCards(self, cardIDs):
        self.cards.clear()
        for i in cardIDs:
            self.cards.append(strengthCard.createStrengthCard(i)) # Create cards based on ids
        grid = self.ids.cards
        grid.clear_widgets() # Clear old widgets
        for card in self.cards: # Add cards to GUI
            grid.add_widget(card)

    # Override default method
    def on_touch_down(self, touch):
        # Only track touches inside the deck
        if self.collide_point(*touch.pos):
            # Check cards
            for card in self.cards:
                if card.collide_point(*touch.pos):
                    self.selectCard(card)
                    return True
        if not self.ids.activateButton.collide_point(*touch.pos):
            self.selectCard()
        return super().on_touch_down(touch)

    def selectCard(self, selectedCard=None):
        for card in self.cards:
            card.unpress()
        if selectedCard != None:
            selectedCard.press()
        self.updateReadyStatus()

    def update(self, dt, game):
        card4 = self.cards[4]
        cardReady = False
        for i, card in enumerate(self.cards):
            if card.ready:
                if self.activate:
                    card.tryActivate(game)
                    self.activate = False
                    self.updateReadyStatus()
                elif card.range:
                    game.player.updateRange(card.range)
                    cardReady = True
            if card4.imageNum == 19 and card4.timer and i != 4: # If prudence is on, update only cooldown timers
                if not card.timer:
                    card.updateCooldown(dt)
                    if card4.level == 3 and card4.timer % 2: # If prudence is on level 3, every other tick doubles the cooldown reduce
                        card.updateCooldown(dt)
                card.updateOverlay()
            else:
                card.update(dt, game)
        if not cardReady:
            game.player.updateRange(0)
    
    def updateReadyStatus(self):
        self.hasReadyCard = any(card.ready for card in self.cards)

    def activateCard(self):
        self.activate = True

    def reset(self, game):
        for card in self.cards:
            card.reset(game)
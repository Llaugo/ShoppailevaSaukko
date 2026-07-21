from kivy.uix.widget import Widget

import math
import const
from spriteSheet import SpriteSheet
import strengthCard

class StrengthDeck(Widget):
    # cards: list of strength cards
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.shinePhase = 0
        self.overlaySheet = SpriteSheet('images/card_overlay.png', (250,350))
        self.cards = []

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
        self.selectCard()
        return super().on_touch_down(touch)

    def selectCard(self, selectedCard=None):
        for card in self.cards:
            card.unpress()
        if selectedCard != None:
            selectedCard.press()

    def update(self, dt, game):
        cardReady = False
        card4 = self.cards[4]
        for i, card in enumerate(self.cards):
            if card.ready:
                pass
                # TODO
                """
                if self.activateButton.pressComplete:
                    if not card.tryActivate(game):
                        card.setOverlay(0)
                    cardReady = False
                elif card.auraDist:
                    game.player.changeAura(card.auraDist)
                    cardReady = True
                """
            if card4.imageNum == 19 and card4.timer and i != 4: # If prudence is on, update only cooldown timers
                if not card.timer:
                    card.updateCooldown()
                    if card4.level == 3 and card4.timer % 2: # If prudence is on level 3, every other tick doubles the cooldown reduce
                        card.updateCooldown()

                card.updateOverlay()
            else:
                card.update(game)
        if not cardReady:
            pass
            #game.player.changeAura(0)

        
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
        for i in cardIDs:
            self.cards.append(strengthCard.createStrengthCard(i)) # Create cards based on ids
        grid = self.ids.cards
        grid.clear_widgets() # Clear old widgets
        for card in self.cards: # Add cards to GUI
            grid.add_widget(card)

    def update(self, floor):
        cardReady = False
        card4 = self.cards[4]
        for i, card in enumerate(self.cards): 
            if card.ready:
                if self.activateButton.pressComplete:
                    if not card.tryActivate(floor):
                        self.overlays[i] = (self.overlaySprite.getImage(0,250,350,const.scale/2), self.overlays[i][1])
                    self.updateImages(self.pos)
                elif card.auraDist:
                    floor.player.changeAura(card.auraDist)
                    cardReady = True
            oldCooldownN = math.floor((card.cooldownMax - card.cooldown)/card.cooldownMax*16) + 9
            oldTimerN = math.floor(card.timer/10) % 4 + 5
            if card4.imageNum == 19 and card4.timer and i != 4: # If prudence is on, update only cooldown timers
                if not card.timer:
                    card.updateCooldown()
                    if card4.level == 3 and card4.timer%2: # If prudence is on level 3, every other tick doubles the cooldown reduce
                        card.updateCooldown()
            else:
                card.update(floor) # Update cards
            cooldownN = cooldownN = math.floor((card.cooldownMax - card.cooldown)/card.cooldownMax*16) + 9
            timerN = math.floor(card.timer/10) % 4 + 5
            if cooldownN != oldCooldownN:
                newImg = self.overlaySprite.getImage(cooldownN)
                self.overlays[i] = (newImg, self.overlays[i][1])
            elif timerN != oldTimerN and card.imageNum != 22:
                newImg = self.overlaySprite.getImage(timerN)
                self.overlays[i] = (newImg, self.overlays[i][1])
            elif not card.timer and card.cooldown == card.cooldownMax:
                self.overlays[i] = (self.overlaySprite.getImage(9), self.overlays[i][1])
        if not cardReady:
            floor.player.changeAura(0)
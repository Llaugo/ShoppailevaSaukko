from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.image import Image
from kivy.properties import NumericProperty, ObjectProperty, BooleanProperty

import const
from spriteSheet import SpriteSheet
import playerClass
from cardProgression import advanceCardLevel
import math

# Class for strength cards. There is a parent class and 26 child classes, one each strength.
# Each card gives the player some ability or boost, which has a timer during which the strength is active.
# After the ability ends, there is a cooldown for using the ability.
class StrengthCard(Widget):
    imageNum = NumericProperty(0)
    ready = BooleanProperty(False) # Is the card selected/pressed
    timer = NumericProperty(0)
    cooldown = NumericProperty(0)
    overlayTexture = ObjectProperty(None, allownone=True)
    
    # imageNum: the index of the card image
    def __init__(self, imageNum=0, **kwargs):
        kwargs["imageNum"] = imageNum
        super().__init__(**kwargs)

        self.imageNum = imageNum
        self.range = 0
        self.timerMax = 8       # timer duration in seconds
        self.cooldownMax = 30   # cooldown duration in seconds
        self.level = 1          # Level of the card
        self.shinePhase = 0
        self.overlaySheet = SpriteSheet("images/card_overlay.png", (250, 350))
        self.setOverlay(0)
        self.xpSprite = SpriteSheet('images/xp_sheet.png', (178, 18))
        self.xpImage = self.xpSprite.getImage(round((self.level*10)%10))

    def setOverlay(self, frameIndex):
        self.overlayTexture = self.overlaySheet.getImage(frameIndex)

    #def clearOverlay(self):
    #    self.overlayTexture = None

    def updateOverlay(self):
        frame = 0
        if self.timer > 0:
            # Active/running animation: frames 5–8
            progress = (self.timerMax - self.timer)/self.timerMax
            frame = math.floor(progress*64 % 4) + 5
        elif self.cooldown > 0:
            # Cooldown animation: frames 9–24
            progress = (self.cooldownMax - self.cooldown)/self.cooldownMax
            frame = math.floor(progress*16) + 9
            frame = min(frame, 24)
        elif self.ready:
            self.shinePhase += 1
            # Selected/glowing animation: frames 1–4
            frame = math.floor(self.shinePhase/15) % 4 + 1
        self.setOverlay(frame)


    # Activates the card and starts the active timer if the card is not on cooldown
    # Returns True if activation was successful, False otherwise
    def tryActivate(self, game):
        if not self.cooldown:
            self.timer = self.timerMax
            self.cooldown = self.cooldownMax
            self.unpress()
            return True
        return False
    
    def upgradeCard(self, timr=0, cool=0, range=0):
        self.timerMax += timr
        self.cooldownMax += cool
        self.range += range

    # Do card action if card is active
    def update(self, dt, game):
        self.updateOverlay()
        self.updateTimers(dt)

    # update the timers of the card
    def updateTimers(self, dt):
        if self.timer > 0:          # Update timer if timer is active
            self.timer = max(self.timer - dt, 0)
        elif self.cooldown > 0:     # Update cooldown timer if cooldown is active
            self.cooldown = max(self.cooldown - dt, 0)

    def updateCooldown(self, dt):
        if self.cooldown > 0:
            self.cooldown = max(self.cooldown - dt, 0)

    def levelup(self, amount=const.cardExp):
        self.level, leveledUp = advanceCardLevel(
            self.level,
            amount,
            const.maxCardLevel,
        )
        return leveledUp

    # Reset the card timers to the base state
    def reset(self, game):
        self.timer = 0
        self.cooldown = 0
        self.setOverlay(0)
        self.unpress()

    # Returns True if timer is on, False if not
    def isActive(self):
        if self.timer:
            return True
        return False
    
    # Choose the card if not running or on cooldown
    def press(self):
        if self.cooldown <= 0 and self.timer <= 0:
            self.ready = True
            self.shinePhase = 0

    def unpress(self):
        self.ready = False

# Creativity card jumps the player over a tile in a semirandom direction
class CreativityCard(StrengthCard):
    def __init__(self):
        super().__init__(0)
        self.timerMax = 1
        self.cooldownMax = 60*60
        self.range = 184

    def tryActivate(self, game):
        if super().tryActivate(game):
            game.jumpGap(math.floor(self.level))
            self.levelup()
            return True
        return False

# Curiosity card breaks open boxes that are in the way
class CuriosityCard(StrengthCard):
    def __init__(self):
        super().__init__(1)
        self.timerMax = 0
        self.range = 120

    def tryActivate(self, game):
        if super().tryActivate(game):
            if not game.removeCrate():
                self.reset(game)
            else:
                if self.levelup():
                    self.upgradeCard(0,0,25)
                return True
        return False

# Judgement cards shows what items there are in the room
class JudgementCard(StrengthCard):
    def __init__(self):
        super().__init__(2)

    # Show the item names in the room if not on cooldown
    def tryActivate(self, game):
        if super().tryActivate(game):
            self.timer = self.timerMax
            game.showItemNames(math.floor(self.level))
            self.levelup()
            return True
        return False

    # Hide item names, if timer ends
    def update(self, dt, game):
        if self.timer == 1:
            game.showItemNames(0)
        super().update(dt, game)

    # Reset timers and hide item names
    def reset(self, game):
        super().reset(game)
        game.showItemNames(0)

# Learning card gets rid of darkness in the dark rooms
class LearningCard(StrengthCard):
    def __init__(self):
        super().__init__(3)
        self.timerMax = 1
        self.cooldownMax = 120*60

    # Makes the visible area around the player wider if in a dark room
    def tryActivate(self, game):
        if super().tryActivate(game):
            if not game.changeDarkness(0, 0, True):
                self.reset(game)
            else:
                if self.levelup():
                    self.upgradeCard(0,-30*60)
                return True
        return False

# Perspective card shows the rooms around the current room
class PerspectiveCard(StrengthCard):
    def __init__(self):
        super().__init__(4)

    # Show rooms around the current room if not on cooldown
    def tryActivate(self, game):
        if super().tryActivate(game):
            game.setBirdsEye(math.floor(self.level)+2)
            if self.levelup():
                self.upgradeCard(120)
            return True
        return False

    # Set view to normal when the timer ends
    def update(self, dt, game):
        if self.timer == 1:
            game.setBirdsEye(0)
        super().update(dt, game)

    # Reset view to normal
    def reset(self, game):
        super().reset(game)
        game.setBirdsEye(0)

# Bravery card makes the player able to push heavier carts
class BraveryCard(StrengthCard):
    def __init__(self):
        super().__init__(5)

    def tryActivate(self, game):
        if super().tryActivate(game):
            game.player.changeStrength(8)
            if self.levelup():
                self.upgradeCard(3*60, -5*60)
            return True
        return False

    def update(self, dt, game):
        if self.timer == 1:
            game.player.changeStrength(const.basePlayerStrength)
        super().update(dt, game)

    def reset(self, game):
        super().reset(game)
        #game.player.changeStrength(const.basePlayerStrength)

# Perseverance card makes player to be able to walk through water
class PerseveranceCard(StrengthCard):
    def __init__(self):
        super().__init__(6)
        self.swimSpeed = const.basePlayerSpeed*0.25

    # Change player swimming speed if not on cooldown
    def tryActivate(self, game):
        if super().tryActivate(game):
            game.player.swim(self.swimSpeed, self.timerMax)
            if self.levelup():
                self.upgradeCard(5*60)
                self.swimSpeed += const.basePlayerSpeed*0.1
            return True
        return False

    # Reset player swimming speed to normal (off)
    def reset(self, game):
        super().reset(game)
        #game.player.resetSwim()

# Honesty card rotates the adverts
class HonestyCard(StrengthCard):
    def __init__(self):
        super().__init__(7)
        self.timerMax = 1
        self.range = const.tileSize*2

    def tryActivate(self, game):
        if super().tryActivate(game):
            if not game.rotateAdverts(self.range):
                self.reset(game)
            else:
                if self.levelup():
                    self.upgradeCard(0,-5*60,const.tileSize*1.5)
                return True
        return False
    
# Zest card gives the player a speed boost
class ZestCard(StrengthCard):
    def __init__(self):
        super().__init__(8)

    # Change players speed if not on cooldown
    def tryActivate(self, game):
        if super().tryActivate(game):
            game.player.changeSpeed(
                const.basePlayerSpeed*1.5,
                self.timerMax,
                source="zest",
            )
            if self.levelup():
                self.upgradeCard(5)
            return True
        return False

    # Reset player speed to normal
    def reset(self, game):
        super().reset(game)
        game.player.resetSpeed("zest")

# Grit card destroys advert in front of the player
class GritCard(StrengthCard):
    def __init__(self):
        super().__init__(9)
        self.timerMax = 1
        self.range = const.tileSize

    def tryActivate(self, game):
        if super().tryActivate(game):
            if not game.destroyAdvert(self.range):
                self.reset(game)
            else:
                if self.levelup():
                    self.upgradeCard(0,0,const.tileSize*1.2)
                return True
        return False

# Kindness card makes it possible to move through/past npcs
class KindnessCard(StrengthCard):
    def __init__(self):
        super().__init__(10)
        self.timerMax = 5*60

    def tryActivate(self, game):
        if super().tryActivate(game):
            game.player.setNpcCollitionTimer(self.timerMax)
            if self.levelup():
                self.upgradeCard(3*60)
            return True
        return False

    def update(self, dt, game):
        if self.level == 3 and self.timer and game.player.isOnNpc(game.currentRoom):
            game.player.changeSpeed(const.basePlayerSpeed*1.3, 30) # change speed upon collision
        super().update(dt, game)

    def reset(self, game):
        #game.player.setNpcCollitionTimer(0)
        super().reset(game)

# Love card loads the card five times with speaking to npcs and then is used to fly over obstacles
class LoveCard(StrengthCard):
    def __init__(self):
        super().__init__(11)
        self.cardSprite = SpriteSheet('images/love_jetpack.png', (250,350))
        self.image = self.cardSprite.getImage(0)
        self.batteryReset = 1
        self.battery = self.batteryReset
        self.timerMax = 1*60

    def tryActivate(self, game):
        leveledUp = False
        if super().tryActivate(game):
            if self.battery < 6:
                if game.findLove():
                    self.battery += 1
                    leveledUp = True
                else:
                    self.reset(game)
            elif self.battery >= 6:
                game.player.fly(self.timerMax)
                self.battery = self.batteryReset
                leveledUp = True
            if leveledUp:
                if self.levelup(const.cardExp/2):
                    self.upgradeCard(2*60)
                    self.batteryReset += 1
                return True
        return False

# Social card Shows the cart-npc pairs
class SocialCard(StrengthCard):
    def __init__(self):
        super().__init__(12)
        self.timerMax = 4*60
        self.cooldownMax = 40*60

    def tryActivate(self, game):
        if super().tryActivate(game):
            if not game.showCartOwners(self.timerMax):
                super().reset(game)
            else:
                if self.levelup():
                    self.upgradeCard(4*60,-5*60)
                return True
        return False

    def reset(self, game):
        #game.resetCartOwnerView()
        super().reset(game)

# Compassion card swaps the player with an npc
class CompassionCard(StrengthCard):
    def __init__(self):
        super().__init__(13)
        self.timerMax = 1
        self.cooldownMax = 16*60

    def tryActivate(self, game):
        if super().tryActivate(game):
            if not game.swapPlayer():
                self.reset(game)
            else:
                if self.levelup():
                    self.upgradeCard(0,-7*60)
                return True
        return False

# Fairness card gives the player the ability to push certain npc's cart
class FairnessCard(StrengthCard):
    def __init__(self):
        super().__init__(14)
        self.timerMax = 3*60 # Here timer counts how long the accessed cart is higlighted
        self.cooldownMax = 25*60

    def tryActivate(self, game):
        if super().tryActivate(game):
            if not game.askCartPushing(self.timerMax):
                super().reset(game)
            else:
                if self.levelup():
                    self.upgradeCard(0,-8*60)
                return True
        return False

    def reset(self, game):
        #game.resetCartOwnerView()
        super().reset(game)

# Leadership card makes an npc push their own cart
class LeadershipCard(StrengthCard):
    def __init__(self):
        super().__init__(15)
        self.timerMax = 1
        self.cooldownMax = 40*60

    def  tryActivate(self, game):
        if super().tryActivate(game):
            if not game.leadCartPushing():
                self.reset(game)
            else:
                if self.levelup():
                    self.upgradeCard(0,-5*60)
                return True
        return False

# Teamwork card makes it possible to trade items with npcs
class TeamworkCard(StrengthCard):
    def __init__(self):
        super().__init__(16)
        self.timerMax = 1

    def tryActivate(self, game):
        if super().tryActivate(game):
            if not game.tradeWithNpc(math.floor(self.level)):
                self.reset(game)
            else:
                if self.levelup():
                    self.upgradeCard(0,-3*60)
                return True
        return False

# Forgiveness card cleans nearby waters
class ForgivenessCard(StrengthCard):
    def __init__(self):
        super().__init__(17)
        self.timerMax = 1
        self.range = const.tileSize

    # Clean nearby water from the room if not on cooldown
    def tryActivate(self, game):
        if super().tryActivate(game):
            if not game.cleanWater(self.range):
                self.reset(game)
            else:
                if self.levelup():
                    self.upgradeCard(0,-5*60,const.tileSize)
                return True
        return False

# Humility card makes the player smaller to fit through small spaces
class HumilityCard(StrengthCard):
    def __init__(self):
        super().__init__(18)

    # Make player smaller if cooldown is not on
    def tryActivate(self, game):
        if super().tryActivate(game):
            game.player.setSize(game.currentRoom, 0.5)
            if self.levelup():
                self.upgradeCard(4,-4)
            return True
        return False

    # Turn player size back to normal if timer is out
    def update(self, dt, game):
        oldTimer = self.timer
        super().update(dt, game)
        if oldTimer > 0 and self.timer <= 0: # Timer just ended
            game.player.setSize(game.currentRoom)

    # Reset size to normal
    def reset(self, game):
        super().reset(game)
        game.player.setSize(game.currentRoom)

# Prudence card stops the time
class PrudenceCard(StrengthCard):
    def __init__(self):
        super().__init__(19)
        self.timerMax = 5*60

    def tryActivate(self, game):
        if super().tryActivate(game):
            game.stopTime()
            if self.levelup():
                self.upgradeCard(4*60,-4*60)
            return True
        return False

    def update(self, dt, game):
        if self.timer == 1:
            game.stopTime()
        super().update(dt, game)
    
    def reset(self, game):
        super().reset(game)
        #game.stopTime()

# Regulation card stop the pushing of the advert screens
class RegulationCard(StrengthCard):
    def __init__(self):
        super().__init__(20)

    def tryActivate(self, game):
        if super().tryActivate(game):
            game.advertBlockStart()
            if self.levelup():
                self.upgradeCard(5*60)
            return True
        return False

    def update(self, dt, game):
        if self.timer == 1:
            game.advertBlockEnd()
        super().update(dt, game)

    def reset(self,game):
        super().reset(game)
        #game.advertBlockEnd()

# Appreciation card makes a new item appear somewhere in the room
class AppreciationCard(StrengthCard):
    def __init__(self):
        super().__init__(21)
        self.timerMax = 1

    # Adds an item to room if not on cooldown
    def tryActivate(self, game):
        if super().tryActivate(game):
            if not game.addItem(math.floor(self.level)):
                self.reset(game)
            else:
                if self.levelup():
                    self.upgradeCard(0,-3*60)
                return True
        return False

# Gratitude card can drop stones on the ground to keep track of steps and gives a speed boost when walking over the stones
class GratitudeCard(StrengthCard):
    def __init__(self):
        super().__init__(22)
        self.timerMax = 1 # This card's timer means how long the speed boost lasts

    # Adds a stone to the ground if not on cooldown
    def tryActivate(self, game):
        if self.cooldown or not game.addStone():
            return False
        if self.levelup():
            self.upgradeCard(0.5, -5)
        self.cooldown = self.cooldownMax
        self.unpress()
        return True

    # Fill boost timer if player is standing on a stone
    def update(self, dt, game):
        if self.timer > 0:
            self.timer = max(self.timer - dt, 0)
        if self.cooldown > 0:
            self.cooldown = max(self.cooldown - dt, 0)
        if game.playerIsOnStone():
            self.timer = self.timerMax
            game.player.changeSpeed(
                const.basePlayerSpeed*1.3,
                self.timerMax,
                source="gratitude",
            )
        self.updateOverlay()
    
    # Reset player speed to normal
    def reset(self, game):
        super().reset(game)
        game.player.resetSpeed("gratitude")

# Hope card makes a long visible area in front of the player in the dark rooms
class HopeCard(StrengthCard):
    def __init__(self):
        super().__init__(23)
        self.timerMax = 20*60
        self.litWidth = -80

    # Makes the visible beam in front of the player if in a dark room
    def tryActivate(self, game):
        if super().tryActivate(game):
            if not game.changeDarkness(self.litWidth, self.timerMax):
                super().reset(game)
            else:
                if self.levelup():
                    self.upgradeCard(10*60)
                    self.litWidth -= 30
                return True
        return False

    # Reset visible area and timers
    def reset(self, game):
        super().reset(game)
        #game.currentRoom.resetLights()

# Humor card makes player to be able to swim through water
class HumorCard(StrengthCard):
    def __init__(self):
        super().__init__(24)
        self.timerMax = 5*60

    # Change player swimming speed if not on cooldown
    def tryActivate(self, game):
        if super().tryActivate(game):
            game.player.swim(const.basePlayerSpeed*0.5, self.timerMax)
            if self.levelup():
                self.upgradeCard(3*60,-5*60)
            return True
        return False

    # Reset player swimming speed to normal (off)
    def reset(self, game):
        super().reset(game)
        #game.player.resetSwim()

# Spirituality card makes the visible area around the player wider in the dark rooms
class SpiritualityCard(StrengthCard):
    def __init__(self):
        super().__init__(25)
        self.timerMax = 20*60
        self.litWidth = 70

    # Makes the visible area around the player wider if in a dark room
    def tryActivate(self, game):
        if super().tryActivate(game):
            if not game.changeDarkness(self.litWidth, self.timerMax):
                super().reset(game)
            else:
                if self.levelup():
                    self.upgradeCard(10*60)
                    self.litWidth += 30
                return True
        return False

    # Reset visible area and timers
    def reset(self, game):
        super().reset(game)
        #game.currentRoom.resetLights()
    

# Return a strength card respective to the given integer.
def createStrengthCard(n):
    if n == 0:
        return CreativityCard()
    elif n == 1:
        return CuriosityCard()
    elif n == 2:
        return JudgementCard()
    elif n == 3:
        return LearningCard()
    elif n == 4:
        return PerspectiveCard()
    elif n == 5:
        return BraveryCard()
    elif n == 6:
        return PerseveranceCard()
    elif n == 7:
        return HonestyCard()
    elif n == 8:
        return ZestCard()
    elif n == 9:
        return GritCard()
    elif n == 10:
        return KindnessCard()
    elif n == 11:
        return LoveCard()
    elif n == 12:
        return SocialCard()
    elif n == 13:
        return CompassionCard()
    elif n == 14:
        return FairnessCard()
    elif n == 15:
        return LeadershipCard()
    elif n == 16:
        return TeamworkCard()
    elif n == 17:
        return ForgivenessCard()
    elif n == 18:
        return HumilityCard()
    elif n == 19:
        return PrudenceCard()
    elif n == 20:
        return RegulationCard()
    elif n == 21:
        return AppreciationCard()
    elif n == 22:
        return GratitudeCard()
    elif n == 23:
        return HopeCard()
    elif n == 24:
        return HumorCard()
    elif n == 25:
        return SpiritualityCard()
    else:
        return StrengthCard(n)

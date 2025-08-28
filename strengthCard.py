from kivy.uix.widget import Widget
from kivy.core.image import Image
import const
from spriteSheet import SpriteSheet
import playerClass
import math

# Class for strength cards. There is a parent class and 26 child classes, one each strength.
# Each card gives the player some ability or boost, which has a timer during which the strength is active.
# After the ability ends, there is a cooldown for using the ability.
class StrengthCard(Widget):
    # imageNum: the index of the card image
    def __init__(self, imageNum):
        self.imageNum = imageNum
        self.auraDist = 0
        self.timer = 0          # timer for the ability
        self.cooldown = 0       # timer for the cooldown
        self.timerMax = 8*60     # timer duration
        self.cooldownMax = 30*60  # cooldown duration
        self.level = 1          # Level of the card
        self.image = Image(f"images/cards/card{self.imageNum}").texture
        self.xpSprite = SpriteSheet('images/xp_sheet.png', (178, 18))
        self.xpImage = self.xpSprite.getImage(round((self.level*10)%10))
        self.ready = False

    # Activates the card and starts the active timer if the card is not on cooldown
    # Returns True if activation was successful, False otherwise
    def tryActivate(self, floor):
        if not self.cooldown:
            self.timer = self.timerMax
            self.cooldown = self.cooldownMax
            self.unpress()
            return True
        return False
    
    def upgradeCard(self, timr=0, cool=0, aura=0):
        self.timer += timr
        self.cooldown += cool
        self.auraDist += aura

    # Do card action if card is active
    def update(self, floor):
        self.updateTimers()

    # update the timers of the card
    def updateTimers(self):
        if self.timer:          # Update timer if timer is active
            self.timer -= 1
        elif self.cooldown:     # Update cooldown timer if cooldown is active
            self.cooldown -= 1

    def updateCooldown(self):
        if self.cooldown:
            self.cooldown -= 1

    def levelup(self, amount=const.cardExp):
        self.level = min(self.level+amount, const.maxCardLevel)
        if self.level == 2 or self.level == 3:
            return True
        return False

    # Reset the card timers to the base state
    def reset(self, floor):
        self.timer = 0
        self.cooldown = 0
        self.unpress()

    # Returns True if timer is on, False if not
    def isActive(self):
        if self.timer:
            return True
        return False
    
    def press(self):
        self.ready = True

    def unpress(self):
        self.ready = False

# Creativity card jumps the player over a tile in a semirandom direction
class CreativityCard(StrengthCard):
    def __init__(self):
        super().__init__(0)
        self.timerMax = 1
        self.cooldownMax = 60*60
        self.auraDist = 184

    def tryActivate(self, floor):
        if super().tryActivate(floor):
            floor.jumpGap(math.floor(self.level))
            self.levelup()
            return True
        return False

# Curiosity card breaks open boxes that are in the way
class CuriosityCard(StrengthCard):
    def __init__(self):
        super().__init__(1)
        self.timerMax = 1
        self.auraDist = 80

    def tryActivate(self, floor):
        if super().tryActivate(floor):
            if not floor.breakBox(self.auraDist):
                self.reset(floor)
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
    def tryActivate(self, floor):
        if super().tryActivate(floor):
            self.timer = self.timerMax
            floor.showItemNames(math.floor(self.level))
            self.levelup()
            return True
        return False

    # Hide item names, if timer ends
    def update(self, floor):
        if self.timer == 1:
            floor.showItemNames(0)
        self.updateTimers()

    # Reset timers and hide item names
    def reset(self, floor):
        super().reset(floor)
        floor.showItemNames(0)

# Learning card gets rid of darkness in the dark rooms
class LearningCard(StrengthCard):
    def __init__(self):
        super().__init__(3)
        self.timerMax = 1
        self.cooldownMax = 120*60

    # Makes the visible area around the player wider if in a dark room
    def tryActivate(self, floor):
        if super().tryActivate(floor):
            if not floor.changeDarkness(0, 0, True):
                self.reset(floor)
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
    def tryActivate(self, floor):
        if super().tryActivate(floor):
            floor.setBirdsEye(math.floor(self.level)+2)
            if self.levelup():
                self.upgradeCard(120)
            return True
        return False

    # Set view to normal when the timer ends
    def update(self, floor):
        if self.timer == 1:
            floor.setBirdsEye(0)
        self.updateTimers()

    # Reset view to normal
    def reset(self, floor):
        super().reset(floor)
        floor.setBirdsEye(0)

# Bravery card makes the player able to push heavier carts
class BraveryCard(StrengthCard):
    def __init__(self):
        super().__init__(5)

    def tryActivate(self, floor):
        if super().tryActivate(floor):
            floor.player.changeStrength(8)
            if self.levelup():
                self.upgradeCard(3*60, -5*60)
            return True
        return False

    def update(self, floor):
        if self.timer == 1:
            floor.player.changeStrength(const.basePlayerStrength)
        self.updateTimers()

    def reset(self, floor):
        super().reset(floor)
        floor.player.changeStrength(const.basePlayerStrength)

# Perseverance card makes player to be able to walk through water
class PerseveranceCard(StrengthCard):
    def __init__(self):
        super().__init__(6)
        self.swimSpeed = const.basePlayerSpeed*0.25

    # Change player swimming speed if not on cooldown
    def tryActivate(self, floor):
        if super().tryActivate(floor):
            floor.player.swim(self.swimSpeed, self.timerMax)
            if self.levelup():
                self.upgradeCard(5*60)
                self.swimSpeed += const.basePlayerSpeed*0.1
            return True
        return False

    # Reset player swimming speed to normal (off)
    def reset(self, floor):
        super().reset(floor)
        floor.player.resetSwim()

# Honesty card rotates the adverts
class HonestyCard(StrengthCard):
    def __init__(self):
        super().__init__(7)
        self.timerMax = 1
        self.auraDist = const.tileSize*2

    def tryActivate(self, floor):
        if super().tryActivate(floor):
            if not floor.rotateAdverts(self.auraDist):
                self.reset(floor)
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
    def tryActivate(self, floor):
        if super().tryActivate(floor):
            floor.player.changeSpeed(const.basePlayerSpeed*1.5, self.timerMax)
            if self.levelup():
                self.upgradeCard(5*60)
            return True
        return False

    # Reset player speed to normal
    def reset(self, floor):
        super().reset(floor)
        floor.player.resetSpeed()

# Grit card destroys advert in front of the player
class GritCard(StrengthCard):
    def __init__(self):
        super().__init__(9)
        self.timerMax = 1
        self.auraDist = const.tileSize

    def tryActivate(self, floor):
        if super().tryActivate(floor):
            if not floor.destroyAdvert(self.auraDist):
                self.reset(floor)
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

    def tryActivate(self, floor):
        if super().tryActivate(floor):
            floor.player.setNpcCollitionTimer(self.timerMax)
            if self.levelup():
                self.upgradeCard(3*60)
            return True
        return False

    def update(self, floor):
        if self.level == 3 and self.timer and floor.player.isOnNpc(floor.currentRoom):
            floor.player.changeSpeed(const.basePlayerSpeed*1.3, 30) # change speed upon collision
        self.updateTimers()

    def reset(self, floor):
        floor.player.setNpcCollitionTimer(0)
        super().reset(floor)

# Love card loads the card five times with speaking to npcs and then is used to fly over obstacles
class LoveCard(StrengthCard):
    def __init__(self):
        super().__init__(11)
        self.cardSprite = SpriteSheet('images/love_jetpack.png', (250,350))
        self.image = self.cardSprite.getImage(0)
        self.batteryReset = 1
        self.battery = self.batteryReset
        self.timerMax = 1*60

    def tryActivate(self, floor):
        leveledUp = False
        if super().tryActivate(floor):
            if self.battery < 6:
                if floor.findLove():
                    self.battery += 1
                    leveledUp = True
                else:
                    self.reset(floor)
            elif self.battery >= 6:
                floor.player.fly(self.timerMax)
                self.battery = self.batteryReset
                leveledUp = True
            if leveledUp:
                if self.levelup(const.cardExp/2):
                    self.upgradeCard(2*60)
                    self.batteryReset += 1
                return True
        return False
                

    def reset(self, floor):
        super().reset(floor)
        self.blitXP()

    def press(self):
        self.ready = True
        self.blitXP(self.battery)

    def unpress(self):
        self.ready = False
        self.blitXP()

# Social card Shows the cart-npc pairs
class SocialCard(StrengthCard):
    def __init__(self):
        super().__init__(12)
        self.timerMax = 4*60
        self.cooldownMax = 40*60

    def tryActivate(self, floor):
        if super().tryActivate(floor):
            if not floor.showCartOwners(self.timerMax):
                super().reset(floor)
            else:
                if self.levelup():
                    self.upgradeCard(4*60,-5*60)
                return True
        return False

    def reset(self, floor):
        floor.resetCartOwnerView()
        super().reset(floor)

# Compassion card swaps the player with an npc
class CompassionCard(StrengthCard):
    def __init__(self):
        super().__init__(13)
        self.timerMax = 1
        self.cooldownMax = 16*60

    def tryActivate(self, floor):
        if super().tryActivate(floor):
            if not floor.swapPlayer():
                self.reset(floor)
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

    def tryActivate(self, floor):
        if super().tryActivate(floor):
            if not floor.askCartPushing(self.timerMax):
                super().reset(floor)
            else:
                if self.levelup():
                    self.upgradeCard(0,-8*60)
                return True
        return False

    def reset(self, floor):
        floor.resetCartOwnerView()
        super().reset(floor)

# Leadership card makes an npc push their own cart
class LeadershipCard(StrengthCard):
    def __init__(self):
        super().__init__(15)
        self.timerMax = 1
        self.cooldownMax = 40*60

    def  tryActivate(self, floor):
        if super().tryActivate(floor):
            if not floor.leadCartPushing():
                self.reset(floor)
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

    def tryActivate(self, floor):
        if super().tryActivate(floor):
            if not floor.tradeWithNpc(math.floor(self.level)):
                self.reset(floor)
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
        self.auraDist = const.tileSize

    # Clean nearby water from the room if not on cooldown
    def tryActivate(self, floor):
        if super().tryActivate(floor):
            if not floor.cleanWater(self.auraDist):
                self.reset(floor)
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
    def tryActivate(self, floor):
        if super().tryActivate(floor):
            floor.player.toggleSize(floor.currentRoom, 0.5)
            if self.levelup():
                self.upgradeCard(4*60,-4*60)
            return True
        return False

    # Turn player size back to normal if timer is out
    def update(self, floor):
        if self.timer == 1:
            floor.player.toggleSize(floor.currentRoom)
        self.updateTimers()

    # Reset size to normal
    def reset(self, floor):
        super().reset(floor)
        floor.player.toggleSize(floor.currentRoom)

# Prudence card stops the time
class PrudenceCard(StrengthCard):
    def __init__(self):
        super().__init__(19)
        self.timerMax = 5*60

    def tryActivate(self, floor):
        if super().tryActivate(floor):
            floor.stopTime()
            if self.levelup():
                self.upgradeCard(4*60,-4*60)
            return True
        return False

    def update(self, floor):
        if self.timer == 1:
            floor.stopTime()
        self.updateTimers()
    
    def reset(self, floor):
        super().reset(floor)
        floor.stopTime()

# Regulation card stop the pushing of the advert screens
class RegulationCard(StrengthCard):
    def __init__(self):
        super().__init__(20)

    def tryActivate(self, floor):
        if super().tryActivate(floor):
            floor.advertBlockStart()
            if self.levelup():
                self.upgradeCard(5*60)
            return True
        return False

    def update(self, floor):
        if self.timer == 1:
            floor.advertBlockEnd()
        self.updateTimers()

    def reset(self,floor):
        super().reset(floor)
        floor.advertBlockEnd()

# Appreciation card makes a new item appear somewhere in the room
class AppreciationCard(StrengthCard):
    def __init__(self):
        super().__init__(21)
        self.timerMax = 1

    # Adds an item to room if not on cooldown
    def tryActivate(self, floor):
        if super().tryActivate(floor):
            if not floor.addItem(math.floor(self.level)):
                self.reset(floor)
            else:
                if self.levelup():
                    self.upgradeCard(0,-3*60)
                return True
        return False

# Gratitude card can drop stones on the ground to keep track of steps and gives a speed boost when walking over the stones
class GratitudeCard(StrengthCard):
    def __init__(self):
        super().__init__(22)
        self.timerMax = 60 # This card's timer means how long the speedboost lasts

    # Adds a stone to the ground if not on cooldown
    def tryActivate(self, floor):
        if not self.cooldown:
            floor.addStone()
            self.cooldown = self.cooldownMax
            self.unpress()
            if self.levelup():
                self.upgradeCard(30,-5*60)
            return True
        return False

    # Fill boost timer if player is standing on a stone
    def update(self, floor):
        for stn in floor.currentRoom.stones:
            if floor.player.rect.colliderect(stn[1]): # Check collision with all the stones
                self.timer = self.timerMax
                floor.player.changeSpeed(const.basePlayerSpeed*1.3, self.timerMax) # change speed upon collision
                break
        # Update both timers
        if self.timer:
            self.timer -= 1
        if self.cooldown:
            self.cooldown -= 1
    
    # Reset player speed to normal
    def reset(self, floor):
        super().reset(floor)
        floor.player.resetSpeed()

# Hope card makes a long visible area in front of the player in the dark rooms
class HopeCard(StrengthCard):
    def __init__(self):
        super().__init__(23)
        self.timerMax = 20*60
        self.litWidth = -80

    # Makes the visible beam in front of the player if in a dark room
    def tryActivate(self, floor):
        if super().tryActivate(floor):
            if not floor.changeDarkness(self.litWidth, self.timerMax):
                super().reset(floor)
            else:
                if self.levelup():
                    self.upgradeCard(10*60)
                    self.litWidth -= 30
                return True
        return False


    # Reset visible area and timers
    def reset(self, floor):
        super().reset(floor)
        floor.currentRoom.resetLights()

# Humor card makes player to be able to swim through water
class HumorCard(StrengthCard):
    def __init__(self):
        super().__init__(24)
        self.timerMax = 5*60

    # Change player swimming speed if not on cooldown
    def tryActivate(self, floor):
        if super().tryActivate(floor):
            floor.player.swim(const.basePlayerSpeed*0.5, self.timerMax)
            if self.levelup():
                self.upgradeCard(3*60,-5*60)
            return True
        return False

    # Reset player swimming speed to normal (off)
    def reset(self, floor):
        super().reset(floor)
        floor.player.resetSwim()

# Spirituality card makes the visible area around the player wider in the dark rooms
class SpiritualityCard(StrengthCard):
    def __init__(self):
        super().__init__(25)
        self.timerMax = 20*60
        self.litWidth = 70

    # Makes the visible area around the player wider if in a dark room
    def tryActivate(self, floor):
        if super().tryActivate(floor):
            if not floor.changeDarkness(self.litWidth, self.timerMax):
                super().reset(floor)
            else:
                if self.levelup():
                    self.upgradeCard(10*60)
                    self.litWidth += 30
                return True
        return False

    # Reset visible area and timers
    def reset(self, floor):
        super().reset(floor)
        floor.currentRoom.resetLights()
    

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

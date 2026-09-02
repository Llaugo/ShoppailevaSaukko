from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock


import const
import localization
from spriteSheet import SpriteSheet
from random import randint

# Class for the listing the wanted items. Has also the accompanied images and texts.
class ShoppingList(Widget):
    texture = ObjectProperty(None)  # holds a Texture
    showImgTimer = NumericProperty(0) # Seconds left showing the received item

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.contents has 5 lists of type [item name, items posessed, items needed] for each item rarity level
        self.contents = []
        self.contents.append([const.shop()[4][randint(0,4)],0,1]) # Item from each rarity level is picked at random
        self.contents.append([const.shop()[3][randint(0,4)],0,2])
        self.contents.append([const.shop()[2][randint(0,4)],0,4])
        self.contents.append([const.shop()[1][randint(0,4)],0,6])
        self.contents.append([const.shop()[0][randint(0,4)],0,10])
        self.sheet = SpriteSheet('images/items.png',(46,46))
        self.texture = self.sheet.getImage(0)
        self.filled = False # True if the list is completed
        Clock.schedule_once(lambda dt: self.refreshContents(), 0)

    def refreshContents(self):
        box = self.ids.contentsBox
        box.clear_widgets() # Clear old widgets

        for name, possessed, needed in self.contents:
            row = BoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=62,
                spacing=5,
            )
            nameLabel = Label(
                text=name,
                size_hint_x=None,
                width=565,
                halign="left",
                valign="middle",
                font_size=40,
                color=(0, 0, 0, 1),
            )
            nameLabel.bind(size=lambda widget, _: setattr(widget, "text_size", widget.size))
            countLabel = Label(
                text=f"{possessed}/{needed}",
                size_hint_x=None,
                width=140,
                font_size=46,
                color=(0, 0, 0, 1),
                halign="center",
                valign="middle",
            )
            countLabel.bind(size=lambda widget, _: setattr(widget, "text_size", widget.size))
            row.add_widget(nameLabel)
            row.add_widget(countLabel)
            box.add_widget(row)


    def checkFillStatus(self):
        for con in self.contents:
            if con[1] != con[2]:
                return False
        self.filled = True
        return True

    # Add an item to collection if it is in the list
    # Returns True if item is needed and False if not
    # itemName: name of the received item
    def receiveItem(self, itemName):
        received = False
        for i in range(len(self.contents)):
            if self.contents[i][0] == itemName: # Check if item is in the list
                self.contents[i][1] = min(self.contents[i][1] + 1, self.contents[i][2]) # Increase item count
                imgNum = 0
                for j,name in enumerate([x for xs in const.shop() for x in xs]): # Find item name in flattened list of all items
                    if name == itemName:
                        imgNum = j
                self.texture = self.sheet.getImage(imgNum) # show item image
                self.checkFillStatus()
                received = True
                break
        if received: # Refresh if item added
            self.refreshContents()
            self.ids.itemText.text = localization.tr("game.found_item") + "\n[b]" + itemName + "[/b]\n" + localization.tr("game.correct_item_text")
        else:
            self.ids.itemText.text = localization.tr("game.found_item") + "\n[b]" + itemName + "[/b]\n" + localization.tr("game.incorrect_item_text")
        self.showImgTimer = 5
        return received
    
    def loseItem(self, itemI):
        self.contents[itemI] = [self.contents[itemI][0], self.contents[itemI][1]-1, self.contents[itemI][2]]
        self.refreshContents()

    def update(self, dt):
        self.showImgTimer = max(0, self.showImgTimer-dt)
            

"""
    def saveList(self):
        return self.contents

# listArr: [5x names, 5x quantities]
def listLoader(listArr, lang):
    list = ShoppingList((0,0), lang)
    list.contents = listArr
    return list
"""

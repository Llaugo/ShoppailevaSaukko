from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty
from kivy.clock import Clock
from kivy.core.window import Window

import const
from room import Room
from door import Door
import random

# Class for the game (floors)
class ShopperGame(Widget):
    design_w = NumericProperty(const.worldWidth)
    design_h = NumericProperty(const.worldHeigth)
    player = ObjectProperty(None)
    currentRoom = ObjectProperty(None)
    timer = NumericProperty(const.floorTime)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pressed = set() # All pressed buttons show up in here
        Window.bind(on_key_down=self.on_key_down, on_key_up=self.on_key_up)
        # Initialize floor room list
        self.rooms: list[list[Room]] = [[None]*const.floorSize for _ in range(const.floorSize)]
        self.half = const.floorSize // 2
        self.currentLocation = (self.half,self.half) # Player's current room coords (start from the middle)
        self.doors = [None, None, None, None] # door widgets, s,e,n,w

    def on_kv_post(self, _):
        self.currentRoom = self.ids.room # Set currentRoom parameter
        layout = const.testRoom
        self.currentRoom.tileSize = const.worldHeigth/const.roomSize*0.98
        self.currentRoom.setRoom(layout[0])
        self.centerRoom(self.currentRoom)
        self.rooms[self.half][self.half] = self.currentRoom

        bg = self.ids.bg # Background element
        def rescale(*_):
            if not bg.texture:
                return
            drawn_w, drawn_h = bg.norm_image_size # actual rendered size
            scale = min(drawn_w/self.design_w, drawn_h/self.design_h) # uniform scale to fit
            self.ids.world.scale = scale
            self.ids.world.center = bg.center
        self.bind(size=rescale) # Resize/rescale everything reflexively
        Clock.schedule_once(rescale, 0)

        grid = self.currentRoom.ids.grid # Grid of tiles
        grid.col_default_width = const.worldHeigth/const.roomSize*0.98
        grid.row_default_height = const.worldHeigth/const.roomSize*0.98
        player = self.ids.player
        player.size = (player.width*0.8, player.height*0.8) # Set player size
        # Set doors
        Clock.schedule_once(lambda dt: self.resetDoors(), 0)

    # Reset doors
    def resetDoors(self):
        for d in self.doors:
            if d and d.parent:
                d.parent.remove_widget(d)
        self.doors = [None, None, None, None]
        grid = self.currentRoom.ids.grid # Grid of tiles
        gx, gy = grid.pos
        gw, gh = grid.size
        door_size = gh/const.roomSize
        north = Door(direction="north", size=(door_size, door_size), pos=(gx + gw/2 - door_size/2, gy + gh - 10))
        south = Door(direction="south", size=(door_size, door_size), pos=(gx + gw/2 - door_size/2, gy - door_size - 10))
        east = Door(direction="east", size=(door_size, door_size), pos=(gx + gw, gy + gh/2 - door_size/2))
        west = Door(direction="west", size=(door_size, door_size), pos=(gx - door_size, gy + gh/2 - door_size/2))
        for i, d in enumerate((south, east, north, west)):
            self.ids.world.add_widget(d)
            self.doors[i] = d

    # Detect pressed and unpressed keys
    def on_key_down(self, _win, key, _sc, _cp, _mods):
        self.pressed.add(key); return True
    def on_key_up(self, _win, key, *_):
        self.pressed.discard(key); return True
    
    # Update everything
    def update(self, dt):
        player = self.ids.player
        if dt < 0.3: # Player can phase through walls if there's a spike in dt
            player.update(dt, self) # update player
            self.currentRoom.update(dt, player) # update room
            # Show itemButton if player collides with an item
            onItem = 0
            for i, item in enumerate(self.currentRoom.items):
                if player.collide_widget(item):
                    onItem = 1
                    break
            self.ids.itemButton.opacity = onItem
            # Check room exiting
            self.checkRoomExit()
        self.timer = max(self.timer - dt, 0) # update timer

    # Check player collision with all the four doors
    def checkRoomExit(self):
        for door in self.doors:
            if self.ids.player.collide_widget(door):
                self.nextRoom(door.direction)
                return True
        return False

    # Pick up the first detected item colliding with the player.
    def pickUpItem(self):
        for item in self.currentRoom.items:
            if self.ids.player.collide_widget(item):
                self.currentRoom.removeItem(item)
                break

    # Go to next room in the given direction
    # dir: direction of the next room (0=d,1=r,2=u,3=l)
    def nextRoom(self, dir):
        player = self.ids.player
        oldRoom = self.currentRoom
        grid = oldRoom.ids.grid
        if dir == "south":
            self.currentLocation = (self.currentLocation[0], self.currentLocation[1] + 1)
            player.center = (player.center[0], player.center[1] + grid.height - player.height)
        elif dir == "east":
            self.currentLocation = (self.currentLocation[0] + 1, self.currentLocation[1])
            player.center = (player.center[0] - grid.width + player.width, player.center[1])
        elif dir == "north":
            self.currentLocation = (self.currentLocation[0], self.currentLocation[1] - 1)
            player.center = (player.center[0], player.center[1] - grid.height + player.height)
        elif dir == "west":
            self.currentLocation = (self.currentLocation[0] - 1, self.currentLocation[1])
            player.center = (player.center[0] + grid.width - player.width, player.center[1])
        else:
            raise ValueError(f'Cannot go to the next room in direction: {dir}')
        # Open new room view
        newRoom = self.getRoom(self.currentLocation)

        world = self.ids.world
        if oldRoom.parent:
            old_index = oldRoom.parent.children.index(oldRoom)
            oldRoom.parent.remove_widget(oldRoom)
            world.add_widget(newRoom, index=old_index)
        else:
            world.add_widget(newRoom)
        self.currentRoom = newRoom
        Clock.schedule_once(lambda dt: self.centerRoom(self.currentRoom), 0)
        Clock.schedule_once(lambda dt: self.resetDoors(), 0)

    def getRoom(self, pos):
        x,y = pos
        # Out of bounds
        if len(self.rooms) <= x or len(self.rooms[0]) <= y or x < 0 or y < 0:
            return None
        # Select existing room
        if self.rooms[x][y]:
            return self.rooms[x][y]
        # Create a new one
        distFromMiddle = abs(x - self.half) + abs(y - self.half)
        newRoom = Room()
        newRoom.tileSize = const.worldHeigth/const.roomSize*0.98
        newRoom.setRoom(random.choice(const.roomLayouts), distFromMiddle)
        self.centerRoom(newRoom)
        # Delete doors leading outside the floor limits
        if x == 0:
            newRoom.removeDoor(0)
        elif x == len(self.rooms)-1:
            newRoom.removeDoor(2)
        if y == 0:
            newRoom.removeDoor(1)
        elif y == len(self.rooms)-1:
            newRoom.removeDoor(3)
        self.rooms[x][y] = newRoom
        return newRoom

    def centerRoom(self, room):
        room.size_hint = (None, None)
        room.center = (
            self.ids.world.width/2,
            self.ids.world.height/2,
        )
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty
from spriteSheet import SpriteSheet

class Player(Widget):
    texture = ObjectProperty(None)  # holds a Texture
    speed  = NumericProperty(100)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sheet = SpriteSheet("images/player_sheet.png", (36, 41))
        self.texture = self.sheet.getImage(0)
        self.facing = 0 # 0,1,2,3 = down,right,up,left
        self.walking = 0 # When rounded 0 = standing, 1,2,3 = walking (Animation helper)

    def update(self, dt, game):
        keys = game.pressed
        dx = 0
        dy = 0
        if ord('s') in keys: # Down key or button
            self.facing = 0
            dy -= 1
        elif ord('d') in keys: # Right key or button
            self.facing = 1
            dx += 1
        elif ord('w') in keys: # Up key or button
            self.facing = 2
            dy += 1
        elif ord('a') in keys: # Left key or button
            self.facing = 3
            dx -= 1
        if not dx and not dy: # If there's no movement, we want the first picture of the animation (standing)
            self.walking = 0
        else:
            s = self.speed*dt
            if dy: 
                self.y += dy * s # Prefer vertical movement
            elif dx: 
                self.x += dx * s # Move horizontally
            self.walking = (self.walking + s/40.0) % 4
            animationFrame = self.facing*4 + round(self.walking) % 4 # Get the correct image (frame of the animation)
            self.texture = self.sheet.getImage(animationFrame)
            
    

    '''
    # controls: Consists of four control buttons (d,r,u,l) of the Button class
    # pos: player location on the screen
    def __init__(self, pos):
        super().__init__()
        self.scale = const.scale # Scale of the player image
        self.playerSpeed = const.basePlayerSpeed
        self.speedDuration = 0 # Duration of a possible speed boost
        self.swimSpeed = 0     # Player's speed on water
        self.swimDuration = 0  # Duration of the swim speed
        self.npcCollDuration = 0 # Does the player collide with npc's
        self.flyDuration = 0    # Duration of being able to fly
        self.playerSprite = spriteSheet.SpriteSheet('images/player_sheet.png')
        self.image = self.playerSprite.getImage(0,36,41,self.scale)
        self.facing = 0 # 0,1,2,3 = down,right,up,left
        self.walking = 0 # When rounded 0 = standing, 1,2,3 = walking (Animation helper)
        self.strength = const.basePlayerStrength
        self.aura = 0 # an area highlighted around the player to show distance of actions
        self.speechText = text.Text(const.gameFont(14),"Init player text",pos,(50,50,50),center=True)
        self.speechDuration = 0
        self.resetRect(pos) # Set player pos
        self.pos: Vector2 = Vector2(self.rect.center)
        self.controls = controls

        
    # Tracks for each movement key/button if they are pressed and updates the direction the
    # player is facing and moves the walking animation value up.
    # room: The room the player is in
    def playerInput(self, room: room.Room):
        keys = pygame.key.get_pressed()
        velocity = Vector2()
        speed = self.playerSpeed*self.swimSpeed if self.isInWater(room) and not self.flyDuration else self.playerSpeed
        if keys[pygame.K_s] or self.controls[0].activeFinger: # Down key or button
            self.facing = 0
            velocity += Vector2(0,1)
        elif keys[pygame.K_d] or self.controls[1].activeFinger: # Right key or button
            self.facing = 1
            velocity += Vector2(1,0)
        elif keys[pygame.K_w] or self.controls[2].activeFinger: # Up key or button
            self.facing = 2
            velocity += Vector2(0,-1)
        elif keys[pygame.K_a] or self.controls[3].activeFinger: # Left key or button
            self.facing = 3
            velocity += Vector2(-1,0)
        #if velocity.y:
        #    velocity.x = 0
        # self.facing = 1 - velocity.y ? 2 - velocity.x
        if not velocity: # If no buttons are pressed, we want the first picture of the animation (standing)
            self.walking = 0
        else:
            self.pos += (velocity*speed)
            self.rect.center = (self.pos.x, self.pos.y)
            room.collideCarts(self, self.facing, (velocity*speed), self)
            self.rect.center = (self.pos.x, self.pos.y)
            self.walking = (self.walking + speed/20.0) % 4
        animationFrame = self.facing*4 + round(self.walking) % 4 # Get the correct image (frame of the animation)
        self.image = self.playerSprite.getImage(animationFrame,36,41,self.scale)
        
    # Handle player collision with a wall in a room
    # Returns True if a collition happened
    def resolveCollision(self, room: room.Room, preferDir=None):
        self.rect.center = (self.pos.x, self.pos.y)
        if self.flyDuration > 1:
            solids = room.wallRects.copy()
        else:
            solids = room.solidRects.copy()
            if not self.swimDuration:
                solids += room.waterRects
            if not self.npcCollDuration:
                for npc in room.npcs:
                    solids.append(npc.rect)
        collided = False
        for solid in solids:                                # Check all the solid rects in the room
            if self.rect.colliderect(solid):
                overlap = self.rect.clip(solid)             # Compute overlap rectangle
                if preferDir == "x" or (overlap.width < overlap.height and preferDir != "y"): # Choose the smaller overlap dimension if there is no preferation
                    if self.rect.centerx > solid.centerx:   # Player is on right side of tile -> push right
                        #self.pos.x = (solid.right+self.pos.x + math.ceil(self.rect.width/2))/2
                        self.pos.x = min(self.pos.x + 5, solid.right + math.ceil(self.rect.width/2))
                    else:
                        #self.pos.x = (solid.left+self.pos.x - math.ceil(self.rect.width/2))/2
                        self.pos.x = max(self.pos.x - 5, solid.left - math.ceil(self.rect.width/2))
                else:
                    if self.rect.centery > solid.centery:   # Player is below tile -> push down
                        #self.pos.y = (solid.bottom+self.pos.y + math.ceil(self.rect.height/2))/2
                        self.pos.y = min(self.pos.y + 5, solid.bottom + math.ceil(self.rect.height/2))
                    else:
                        #self.pos.y = (solid.top+self.pos.y - math.ceil(self.rect.height/2))/2
                        self.pos.y = max(self.pos.y - 5, solid.top - math.ceil(self.rect.height/2))
                self.rect.center = (self.pos.x, self.pos.y)
                collided = True
        return collided
                
    # Update player's state in the room
    def update(self, room):
        self.playerInput(room) # Take input
        self.speedDuration = max(self.speedDuration-1, 0) # update speedboost timer
        if not self.speedDuration: # Reset speed when timer runs out
            self.resetSpeed()
        if self.swimDuration == 1 and self.isInWater(room): # Keep timer at 1, if player is still in the water
            self.swimSpeed = const.basePlayerSpeed*0.1
        else:
            self.swimDuration = max(self.swimDuration-1, 0) # update swimming timer
        if not self.swimDuration:
            self.resetSwim()
        if self.npcCollDuration != 1 or not self.isOnNpc(room):
            self.npcCollDuration = max(self.npcCollDuration-1, 0) # update npc passthrough timer
        if self.speechDuration:
            self.speechDuration = max(self.speechDuration-1, 0)
        
        if self.flyDuration == 1:
            if self.resolveCollision(room,'x') or self.resolveCollision(room,'y'):
                self.flyDuration -= 1
                self.swimDuration = 1
        else:
            self.resolveCollision(room)
            self.flyDuration = max(self.flyDuration-1,0)
        self.updateSpeech()

    # Update the pos of the player
    # screenMove: how much the screen size (x,y) has been changed
    def updatePos(self, screenMove):
        self.resetRect((self.pos.x + screenMove[0]/2, self.pos.y + screenMove[1]/2))

    # Reset player to the center of the screen
    # screenSize: dimensions of the window
    def resetPos(self, screenSize):
        self.resetRect((screenSize[0]/2, screenSize[1]/2))
        self.facing = 0

    # Set a new position for the rect and make it smaller than the image
    def resetRect(self, pos):
        self.pos = Vector2(pos)
        self.image = self.playerSprite.getImage(self.facing*4,36,41,self.scale)
        self.rect = self.image.get_rect()
        self.rect.height = 21*self.scale
        self.rect.width = 26*self.scale
        self.rect.center = self.pos

    
    def updateSpeech(self):
        self.speechText.updatePos(self.pos + (0,-36*self.scale))

    # Toggle the player size
    # room: room the player is in
    # newScale: the scale with respect to the original player size
    def toggleSize(self, room, newScale=1):
        if self.scale == const.scale:           # If the scale is normal
            self.scale = const.scale*newScale   # Change scale to new scale
        else:
            self.scale = const.scale            # Set scale back to normal
        self.resetRect(self.pos)
        self.resolveCollision(room)             # Resolve any collitions from changing the size

    # Change player speed
    def changeSpeed(self, speed, duration):
        if duration > self.speedDuration: # If new speed duration is longer than current, change speed
            self.playerSpeed = speed
            self.speedDuration = duration

    # Reset player speed to normal
    def resetSpeed(self):
        self.playerSpeed = const.basePlayerSpeed
        self.speedDuration = 0

    # Change players swimming speed
    def swim(self, speed, duration):
        if duration > self.swimDuration:
            self.swimSpeed = speed
            self.swimDuration = duration

    # Reset player swimming speed
    def resetSwim(self):
        self.swimSpeed = 0
        self.swimDuration = 0
    
    # Returns true if player is colliding with water tiles in the given room
    def isInWater(self,room):
        for water in room.waterRects:
            if self.rect.colliderect(water):
                return True
        return False
    
    def changeStrength(self, newStr):
        self.strength = newStr

    def isOnNpc(self, room):
        for npc in room.npcs:
            if self.rect.colliderect(npc.rect):
                return True
        return False

    def setNpcCollitionTimer(self, time):
        self.npcCollDuration = time

    def fly(self, time):
        self.flyDuration = time

    # Return True if teleport was successful, False if collision happened
    def teleport(self, newPos, room):
        oldPos = self.pos
        self.resetRect(newPos)
        solids = room.solidRects.copy()
        solids += room.waterRects
        for npc in room.npcs:
            solids.append(npc.rect)
        for cart in room.carts:
            solids.append(cart.rect)
        collided = False
        for solid in solids:
            if self.rect.colliderect(solid):
                collided = True
                break
        if not self.rect.colliderect(room.rect): # Player tried to teleport outside the map
            collided = True
        if collided:
            self.resetRect(oldPos)
        return not collided

    # Push player to a direction
    def push(self, pushSpeed, dir, velocity, room):
        speed = pushSpeed*self.swimSpeed if self.isInWater(room) else pushSpeed
        self.pos += (velocity*speed)
        self.rect.center = (self.pos.x, self.pos.y)
        room.collideCarts(self, dir, (velocity*speed), self)
        if not self.flyDuration:
            if velocity.x:
                self.resolveCollision(room, "x") # Resolve collisions with walls etc.
            else:
                self.resolveCollision(room, "y")
        self.rect.center = (self.pos.x, self.pos.y)

    # Returns the npc standing in front of the player, or None if there is no npc
    def npcInFront(self, room):
        if self.facing == 0:
            playerFront = self.pos + (0,23)
        elif self.facing == 1:
            playerFront = self.pos + (23,0)
        elif self.facing == 2:
            playerFront = self.pos + (0,-23)
        elif self.facing == 3:
            playerFront = self.pos + (-23,0)
        frontRect = pygame.Rect(0, 0, 10, 10)
        frontRect.center = playerFront
        for c in room.npcs:
            if c.rect.colliderect(frontRect):
                return c
        return None
    
    def changeAura(self, dist):
        self.aura = dist

    def speak(self, text, duration=const.basePlayerSpeechDuration):
        self.speechDuration = duration
        self.speechText.setText(text)

    # Draw the player
    def draw(self, screen):
        if self.aura:
            pygame.draw.rect(screen, "black", [self.rect.centerx-self.aura/2, self.rect.centery-self.aura/2, self.aura, self.aura], 2)
        drawRect = self.rect.copy()
        drawRect.y -= 20*self.scale # Adjust hitbox position to center on the image
        drawRect.x -= 5*self.scale
        screen.blit(self.image, drawRect)
        if self.speechDuration:
            self.speechText.draw(screen)

    '''
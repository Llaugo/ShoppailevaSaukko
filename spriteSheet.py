from kivy.core.image import Image

class SpriteSheet:
    def __init__(self, sheetPath, dim):
        self.image = Image(sheetPath).texture
        self.dim = dim

    def getImage(self, frame):
        return self.image.get_region(frame*self.dim[0], 0, self.dim[0], self.dim[1])

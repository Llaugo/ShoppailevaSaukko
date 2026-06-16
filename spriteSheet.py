from kivy.core.image import Image

# Class handles imagesheets
class SpriteSheet:
    def __init__(self, sheetPath, dim):
        self.image = Image(sheetPath).texture # Image sheet
        self.dim = dim # Dimensions of one image

    # Get a spesific frame/part of the sheet.
    def getImage(self, frame):
        return self.image.get_region(frame*self.dim[0], 0, self.dim[0], self.dim[1])

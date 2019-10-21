import pygame as pg

# for first creating the copies of maps (so that they can be edited)
class CopyMap:
    def __init__(self, copy, settings, endNum, flowNum, bgColor):
            self.data = []
            self.mapName = copy
            self.endNum = endNum
            self.flowNum = flowNum
            self.bgColor = bgColor
            with open(self.mapName, 'rt') as x:
                for line in x:
                    self.data.append(line.strip())

            self.settings = settings
            self.tileWidth = len(self.data[0])
            self.tileHeight = len(self.data)
            self.width = self.tileWidth * self.settings.tileSize
            self.height = self.tileHeight * self.settings.tileSize

class Camera:
    def __init__(self, width, height, settings):
        self.settings = settings
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, player):
        return player.rect.move(self.camera.topleft)

    def update(self, player):
        x = -player.rect.x + int(self.settings.w / 2)
        y = -player.rect.y + int(self.settings.h / 2)

        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - self.settings.w), x) # right
        y = max(-(self.height - self.settings.h), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)
        

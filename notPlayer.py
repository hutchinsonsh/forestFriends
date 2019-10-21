import pygame
import random
from pygame.sprite import Sprite


class flower(Sprite):
    def __init__(self, game, x, y, settings, type):
        super(flower, self).__init__()
        self.game = game
        self.settings = settings
        self.type = type

        self.image = pygame.Surface((settings.tileSize, settings.tileSize))
        self.rect = self.image.get_rect()
        self.x = x * settings.tileSize
        self.y = y * settings.tileSize
        self.rect.x = self.x
        self.rect.y = self.y

        self.visible = True

        if self.type == 'deadFlower':
            self.image = pygame.image.load('images/beeDeadFlower.png')
            self.image = pygame.transform.scale(self.image, (self.settings.tileSize * 2, self.settings.tileSize * 2))
        elif self.type == 'movingFlower':
            self.visible = False
            self.image = pygame.image.load('images/forwardFlower/movingFlower1.png')
            self.image = pygame.transform.scale(self.image, (self.settings.tileSize * 2, self.settings.tileSize * 2))

        self.leftEdge = self.rect.x + 10
        self.rightEdge = self.rect.x + (self.settings.tileSize * 2) - 15
        self.topEdge = self.rect.y + 15
        self.bottomEdge = self.rect.y + (self.settings.tileSize * 2) - 25

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def updateFlower(self):
        if self.type == 'deadFlower':
            self.image = pygame.image.load('images/beeFlower.png')
            self.image = pygame.transform.scale(self.image, (self.settings.tileSize * 2, self.settings.tileSize * 2))
        elif self.type == 'movingFlower':
            if self.settings.slowImage2 % 5 == 0:
                self.image = pygame.image.load(self.settings.movingFlower[self.settings.imageCount2])
                if self.settings.imageCount2 >= 6:
                    self.settings.imageCount2 = 0
                else:
                    self.settings.imageCount2 += 1
            self.settings.slowImage2 += .5

    def update(self, camera):
        self.x *= camera.width
        self.y *= camera.height


class notFlower(Sprite):
    def __init__(self, game, x, y, settings, type):
        super(notFlower, self).__init__()

        self.settings = settings
        self.game = game
        self.type = type

        self.image = pygame.Surface((settings.tileSize, settings.tileSize))
        self.rect = self.image.get_rect()

        if self.type == 'stem':
            self.x = (x + 1) * settings.tileSize
            self.y = y * settings.tileSize
            self.rect.x = self.x
            self.rect.y = self.y

            self.leftEdge = self.rect.x
            self.rightEdge = self.rect.x + self.settings.tileSize
            self.topEdge = self.rect.y
            self.bottomEdge = self.rect.y + self.settings.tileSize
        else:
            self.x = x * settings.tileSize
            self.y = y * settings.tileSize
            self.rect.x = self.x
            self.rect.y = self.y

            self.leftEdge = self.rect.x
            self.rightEdge = self.rect.x + self.settings.tileSize
            self.topEdge = self.rect.y
            self.bottomEdge = self.rect.y + self.settings.tileSize

        self.determineType()

    def determineType(self):
        if self.game.currentMap != self.game.endScreen and self.game.currentMap != self.game.gameOver:
            if self.type == 'border':
                if self.game.currentMap.bgColor == 'blue':
                    self.image.fill(self.settings.blue)
                elif self.game.currentMap.bgColor == 'grey':
                    self.image.fill(self.settings.grey)
            elif self.type == 'ground':
                self.image = pygame.image.load('images/dirt.png')
                self.image = pygame.transform.scale(self.image, (32, 32))
            elif self.type == 'rain':
                self.image = pygame.image.load('images/raindrop.png')
                self.image = pygame.transform.scale(self.image, (32, 32))
            elif self.type == 'stem':
                self.image = pygame.image.load('images/stem.png')
                self.image = pygame.transform.scale(self.image, (16, 32))
            elif self.type == 'tree':
                self.image = pygame.image.load('images/tree.png')
                self.image = pygame.transform.scale(self.image, (192, 256))
            elif self.type == 'hive':
                self.image = pygame.image.load('images/honeyHive.png')
                self.image = pygame.transform.scale(self.image, (64, 64))
            elif self.type == 'honey':
                self.image = pygame.image.load('images/honey.png')
                self.image = pygame.transform.scale(self.image, (32, 32))
                self.rect.y = self.y - (self.settings.tileSize * (self.game.sb.honeyCount - 1))
                self.topEdge = self.rect.y
                self.bottomEdge = self.rect.y + self.settings.tileSize
            elif self.type == 'load':
                self.image = pygame.image.load('images/loadingBar/loadOne.png')
                self.image = pygame.transform.scale(self.image, (32, 32))
        else:
            if self.type == 'border':
                self.image.fill(self.settings.grey)
            elif self.type == 'ground':
                self.image = pygame.image.load('images/dirt.png')
                self.image = pygame.transform.scale(self.image, (32, 32))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        if self.type == 'load':
            if self.settings.slowImage % 5 == 0:
                self.image = pygame.image.load(self.settings.load[self.settings.imageCount])
                if self.settings.imageCount > 2:
                    self.settings.imageCount = 0
                else:
                    self.settings.imageCount +=1
            self.settings.slowImage += .5
            if self.settings.slowImage == 75:
                self.settings.honeyDone = True
        if self.type == 'rain':
            self.rect.y += self.settings.rainSpeed
            self.topEdge += self.settings.rainSpeed
            self.bottomEdge += self.settings.rainSpeed


class wormStuff(Sprite):
    def __init__(self, game, x, y, settings, type):
        super(wormStuff, self).__init__()

        self.settings = settings
        self.game = game
        self.type = type

        self.image = pygame.Surface((settings.tileSize, settings.tileSize))
        self.rect = self.image.get_rect()

        self.x = x * settings.tileSize
        self.y = y * settings.tileSize
        self.rect.x = self.x
        self.rect.y = self.y

        self.leftEdge = self.rect.x
        self.rightEdge = self.rect.x + self.settings.tileSize
        self.topEdge = self.rect.y
        self.bottomEdge = self.rect.y + self.settings.tileSize

        self.determineType()

    def determineType(self):
        if self.game.currentMap != self.game.endScreen and self.game.currentMap != self.game.gameOver:
            if self.type == 'dirt':
                self.image = pygame.image.load('images/dirt.png')
                self.image = pygame.transform.scale(self.image, (32, 32))
            elif self.type == 'rock':
                self.image = pygame.image.load('images/bedrock.png')
                self.image = pygame.transform.scale(self.image, (32, 32))
            elif self.type == 'leaf':
                self.image = pygame.image.load('images/leaf.png')
                self.image = pygame.transform.scale(self.image, (32, 32))
        else:
            if self.type == 'border':
                self.image.fill(self.settings.grey)
            elif self.type == 'ground':
                self.image = pygame.image.load('images/dirt.png')
                self.image = pygame.transform.scale(self.image, (32, 32))
            elif self.type == 'endLeaf':
                self.image = pygame.image.load('images/leaf.png')
                self.image = pygame.transform.scale(self.image, (64, 64))
                self.bottomEdge += self.settings.tileSize
                self.rightEdge += self.settings.tileSize

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class homeStuff(Sprite):
    def __init__(self, game, x, y, settings, type):
        super(homeStuff, self).__init__()

        self.settings = settings
        self.game = game
        self.type = type

        self.image = pygame.Surface((settings.tileSize, settings.tileSize))
        self.rect = self.image.get_rect()

        self.x = x * settings.tileSize
        self.y = y * settings.tileSize
        self.rect.x = self.x
        self.rect.y = self.y

        self.leftEdge = self.rect.x
        self.rightEdge = self.rect.x + (self.settings.tileSize * 2)
        self.topEdge = self.rect.y
        self.bottomEdge = self.rect.y +  (self.settings.tileSize * 2)

        self.determineType()

        self.birdArray = ['images/bird/birdOne.png', 'images/bird/birdUp.png', 'images/bird/birdOne.png',
                          'images/bird/birdDown.png']
        self.count = 0
        self.whichBird = 0

    def determineType(self):
        if self.type == 'bird':
            self.image = pygame.image.load('images/bird/birdOne.png')
            self.image = pygame.transform.scale(self.image, (64, 64))
        elif self.type == 'bee':
            self.image = pygame.image.load('images/bee.png')
            self.image = pygame.transform.scale(self.image, (64, 64))
        elif self.type == 'worm':
            self.image = pygame.image.load('images/worm/wormOne.png')
            self.image = pygame.transform.scale(self.image, (64, 64))


    def draw(self, screen):
        screen.blit(self.image, self.rect)


    def update(self):
        # for flapping wings
        if self.count % 10 == 0:
            self.image = pygame.image.load(self.birdArray[self.whichBird])
            self.image = pygame.transform.scale(self.image, (64, 64))
            self.whichBird += 1
            if self.whichBird > 3:
                self.whichBird = 0
        self.count += 1

        # for moving forward
        self.rect.x += self.settings.birdSpeed
        self.leftEdge += self.settings.birdSpeed
        self.rightEdge += self.settings.birdSpeed
        

import pygame
from pygame.sprite import Sprite


class beePlayer(Sprite):
    def __init__(self, game, x, y, settings, screen):
        super(beePlayer, self).__init__()
        self.screen = screen
        self.settings = settings
        self.game = game

        self.image = pygame.Surface((settings.tileSize, settings.tileSize))
        self.rect = self.image.get_rect()

        self.image = pygame.image.load('images/bee.png')
        self.image = pygame.transform.scale(self.image, (32, 32))

        self.imageType = 'right'

        self.x = x * settings.tileSize
        self.y = y * settings.tileSize
        self.rect.x = self.x
        self.rect.y = self.y

        self.leftEdge = self.rect.x
        self.rightEdge = self.rect.x + self.settings.tileSize
        self.topEdge = self.rect.y
        self.bottomEdge = self.rect.y + self.settings.tileSize

        # for moving right/if user is pressing on a key
        self.movingRight = False
        self.movingLeft = False
        self.movingUp = False
        self.falling = False

        # this makes sense to have in my head
        self.canMoveRight = True
        self.canMoveLeft = True
        self.canMoveUp = True
        self.canMoveDown = True

        # if collision, by how much can user move
        self.rightV = self.settings.beeSpeed
        self.leftV = self.settings.beeSpeed
        self.upV = self.settings.upBeeSpeed
        self.downV = self.settings.upBeeSpeed

        self.onFlower = False

        self.fallCount = 0

    def update(self, honey):
        # updates left/right movement
        if self.movingRight and self.canMoveRight:
            if self.imageType == 'left':
                self.image = pygame.image.load('images/bee.png')
                self.image = pygame.transform.scale(self.image, (32, 32))
                self.imageType = 'right'
            for x in honey:
                x.rect.x += self.rightV
                x.leftEdge = self.rect.x
                x.rightEdge = self.rect.x + self.settings.tileSize
            self.rect.x += self.rightV
            self.leftEdge = self.rect.x
            self.rightEdge = self.rect.x + self.settings.tileSize
        if self.movingLeft and self.canMoveLeft:
            if self.imageType == 'right':
                self.image = pygame.image.load('images/beeLeft.png')
                self.image = pygame.transform.scale(self.image, (32, 32))
                self.imageType = 'left'
            for x in honey:
                x.rect.x -= self.leftV
                x.leftEdge = self.rect.x
                x.rightEdge = self.rect.x + self.settings.tileSize
            self.rect.x -= self.leftV
            self.leftEdge = self.rect.x
            self.rightEdge = self.rect.x + self.settings.tileSize
        if self.movingUp and self.canMoveUp:
            for x in honey:
                x.rect.y -= self.upV
                x.topEdge = self.rect.y
                x.bottomEdge = self.rect.y + self.settings.tileSize
            self.rect.y -= self.upV
            self.topEdge = self.rect.y
            self.bottomEdge = self.rect.y + self.settings.tileSize
        if self.falling and self.canMoveDown:
            for x in honey:
                x.rect.y += self.downV
                x.topEdge = self.rect.y
                x.bottomEdge = self.rect.y + self.settings.tileSize
            self.rect.y += self.downV
            self.topEdge = self.rect.y
            self.bottomEdge = self.rect.y + self.settings.tileSize
            self.fallCount += 1
        if not self.canMoveDown or not self.falling:
            self.fallCount = 0

    def draw(self):
        self.screen.blit(self.image, self.rect)


class wormPlayer(Sprite):
    def __init__(self, game, x, y, settings, screen, num):
        super(wormPlayer, self).__init__()
        self.screen = screen
        self.settings = settings
        self.game = game

        self.image = pygame.Surface((settings.tileSize, settings.tileSize))
        self.rect = self.image.get_rect()

        self.tempX = 0
        self.tempY = 0

        if num == 0:
            self.name = 'wormOne.png'
            self.image = pygame.image.load('images/worm/wormOne.png')
            self.x = x * settings.tileSize
            self.y = y * settings.tileSize
            self.rect.x = self.x
            self.rect.y = self.y
            self.leftEdge = self.rect.x
            self.rightEdge = self.rect.x + self.settings.tileSize
            self.topEdge = self.rect.y
            self.bottomEdge = self.rect.y + self.settings.tileSize
        elif num == 1:
            self.name = 'wormTwo.png'
            self.image = pygame.image.load('images/worm/wormTwo.png')
            self.x = (x-num) * settings.tileSize
            self.y = y * settings.tileSize
            self.rect.x = self.x
            self.rect.y = self.y
            self.leftEdge = self.rect.x
            self.rightEdge = self.rect.x + self.settings.tileSize
            self.topEdge = self.rect.y
            self.bottomEdge = self.rect.y + self.settings.tileSize
        elif num == 2:
            self.name = 'wormThree.png'
            self.image = pygame.image.load('images/worm/wormThree.png')
            self.x = (x-num) * settings.tileSize
            self.y = y * settings.tileSize
            self.rect.x = self.x
            self.rect.y = self.y
            self.leftEdge = self.rect.x
            self.rightEdge = self.rect.x + self.settings.tileSize
            self.topEdge = self.rect.y
            self.bottomEdge = self.rect.y + self.settings.tileSize

        self.imageType = 'right'
        self.imageType2 = 'down'

        # for moving right/if user is pressing on a key
        self.movingRight = False
        self.movingLeft = False
        self.movingUp = False
        self.movingDown = False

        # this makes sense to have in my head
        self.canMoveRight = True
        self.canMoveLeft = True
        self.canMoveUp = True
        self.canMoveDown = True

        # if collision, by how much can user move
        self.rightV = self.settings.wormSpeed
        self.leftV = self.settings.wormSpeed
        self.upV = self.settings.wormSpeed
        self.downV = self.settings.wormSpeed

        self.changed = 0

    def update(self, worm):
       pass

    def draw(self):
        self.screen.blit(self.image, self.rect)


class noPlayer(Sprite):
    def __init__(self, game, x, y, settings, screen):
        super(noPlayer, self).__init__()
        self.screen = screen
        self.settings = settings
        self.game = game

        self.image = pygame.Surface((settings.tileSize, settings.tileSize))
        self.rect = self.image.get_rect()

        self.image.fill(self.settings.blue)

    def update(self, worm):
       pass

    def draw(self):
        self.screen.blit(self.image, self.rect)
        

import sys
import pygame
import pygame.font
from pygame.locals import *
from pygame.sprite import Group
import gameFunction as gf
from settings import Settings
from tileMap import *
from notPlayer import *
from player import *
from scoreboard import ScoreBoard


class MainGame:
    def __init__(self):
        # initializes game
        pygame.init()
        self.screen = pygame.display.set_mode((settings.w, settings.h))
        pygame.display.set_caption(settings.title)
        pygame.key.set_repeat(300, 100)

        pygame.time.set_timer(USEREVENT + 1, random.randrange(3000, 5000))

        self.home = CopyMap("maps/home.txt", settings, 0, 0, 'blue')
        self.new1()

        self.type = 'home'

        self.image = pygame.image.load('images/grassBackground.png')
        self.image = pygame.transform.scale(self.image, (settings.w, settings.h))

    def new1(self):
        self.walls = Group()
        for row, tiles in enumerate(self.home.data):
                for col, tile in enumerate(tiles):
                    gf.checkNormalType(self, tile, col, row, settings)
        self.camera = Camera(self.home.width, self.home.height, settings)

    def new(self):
        self.camera = Camera(self.home.width, self.home.height, settings)

    def draw(self):
        self.screen.blit(self.image, (0, 0) )
        for x in self.walls:
            self.screen.blit(x.image, self.camera.apply(x))

        self.font = pygame.font.SysFont(None, 100)
        self.text = self.font.render('FOREST FRIENDS', 2, (70, 120, 158))
        self.screen.blit(self.text, (215, 225))

        pygame.display.flip()

    def run(self, settings):
        self.notChosen = True
        while self.notChosen:
            self.new()
            gf.checkMovement(self, settings, self.walls, USEREVENT)
            self.draw()
        self.notChosen = True


class Game:
    def __init__(self, type):
        # initializes game
        pygame.init()
        self.screen = pygame.display.set_mode((settings.w, settings.h))
        self.sb = ScoreBoard(self, settings, self.screen)
        pygame.display.set_caption(settings.title)
        pygame.key.set_repeat(300, 100)

        self.seconds = 59
        self.minutes = 3
        pygame.time.set_timer(USEREVENT + 1, 1000)  # 1 second is 1000 milliseconds
        pygame.time.set_timer(USEREVENT + 2, 75)
        self.clock = pygame.time.Clock()

        self.gameOver = CopyMap("maps/endScreen.txt", settings, 0, 0, 'blue')
        self.endScreen = CopyMap("maps/gameOver.txt", settings, 0, 0, 'blue')

        self.lengthOfLevel = 0

        self.movingForward = False
        self.movingBack = False
        self.newLevel = True
        self.levelType = type

        self.loadMaps()

        self.stillPlaying = True
        self.pause = False

        self.showGameOver = False
        self.showEndScreen = False

    def loadMaps(self):
        if self.levelType == 'bee':
            self.map1 = CopyMap("maps/flowerField", settings, 1, 11, 'blue')
            self.map2 = CopyMap("maps/flowerField2.txt", settings, 2, 14, 'grey')
            self.currentMap = self.map1
            self.new1()
        elif self.levelType == 'worm':
            self.map1 = CopyMap("maps/dirt.txt", settings, 1, 1, 'dirt')
            self.currentMap = self.map1
            self.new1()

    def findNewMap(self):
        if self.currentMap == self.endScreen or self.currentMap == self.gameOver:
            self.stillPlaying = False
        elif self.movingForward:
            if self.showGameOver:
                self.showGameOver = False
                self.currentMap = self.gameOver
            elif self.showEndScreen:
                self.showEndScreen = False
                self.currentMap = self.endScreen
            if self.levelType == 'bee' and self.currentMap == self.map1:
                self.currentMap = self.map2
            self.movingForward = False
            self.new1()

    # creates the tileMap/player locations/sets up camera
    def new1(self):
        self.walls = Group()
        self.collection = Group()
        if self.levelType == 'worm':
            self.wormParts = []
        for row, tiles in enumerate(self.currentMap.data):
            for col, tile in enumerate(tiles):
                self.lengthOfLevel = col
                if self.levelType == 'bee':
                    gf.checkBeeType(self, tile, col, row, settings)
                elif self.levelType == 'worm':
                    gf.checkWormType(self, tile, col, row, settings, self.sb)
        self.camera = Camera(self.currentMap.width, self.currentMap.height, settings)
        if self.levelType == 'worm':
            self.player = self.wormParts[0]

    def new(self):
        self.camera = Camera(self.currentMap.width, self.currentMap.height, settings)

    # draws the walls, characters, and player
    def draw(self):
        if self.levelType == 'bee':
            if self.currentMap.bgColor == 'blue':
                self.screen.fill(settings.blue)
            else:
                self.screen.fill(settings.grey)
            for x in self.walls:
                if x.type == 'movingFlower':
                    if x.visible:
                        self.screen.blit(x.image, self.camera.apply(x))
                else:
                    self.screen.blit(x.image, self.camera.apply(x))
            for x in self.collection:
                self.screen.blit(x.image, self.camera.apply(x))
            self.screen.blit(self.player.image, self.camera.apply(self.player))
            self.sb.showScore(self)

        elif self.levelType == 'worm':
            self.screen.fill(settings.brown)
            for x in self.walls:
                self.screen.blit(x.image, self.camera.apply(x))
            for x in self.wormParts:
                self.screen.blit(x.image, self.camera.apply(x))
            self.screen.blit(self.player.image, self.camera.apply(self.player))
            self.sb.showScore(self)

        pygame.display.flip()

    # checks events, updates any changes, draws events/changes
    # where the main game is ran- only stops if player finishes or loses
    def run(self, settings):
        while self.stillPlaying:
            if not self.pause:
                self.new()
                if self.levelType == 'bee':
                    gf.checkBeeEvents(self, self.sb, settings, self.walls, self.collection, self.player, USEREVENT)
                    if self.movingForward:
                        self.sb.levelHoney = 0
                        self.findNewMap()
                    self.update()
                if self.levelType == 'worm':
                    gf.checkWormEvents(self, self.sb, settings, self.walls, self.player, self.wormParts, USEREVENT)
                    if self.movingForward:
                        self.findNewMap()
                    self.update()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            self.pause = False
            self.draw()


    # updates players movement; camera; and enemy movement
    def update(self):
        if self.levelType == 'bee':
            self.player.update(self.collection)
        elif self.levelType == 'worm':
            self.player.update(self.wormParts)
        self.camera.update(self.player)


settings = Settings()
game = MainGame()
running = True
# main loop
while running:
    game.run(settings)
    g = Game(game.type)
    g.run(settings)
pygame.quit()
sys.exit()

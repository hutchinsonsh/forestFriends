import pygame.font
import os
from pygame.sprite import Group

class ScoreBoard():
    def __init__(self, g, settings, screen):
        self.g = g
        self.settings = settings
        self.screen = screen

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        self.livesLeft = 3

        self.honeyCount = 0
        self.totalHoney = 0
        self.levelHoney = 0
        self.score = 0

        self.skip = False

        self.image1 = pygame.image.load(os.path.join('images', 'honey.png'))
        self.image1 = pygame.transform.scale(self.image1, (32, 32))
        self.image2 = pygame.image.load(os.path.join('images', 'bee.png'))
        self.image2 = pygame.transform.scale(self.image2, (32, 32))

        self.leavesCollected = 0
        self.leavesTotal = 0

        self.image3 = pygame.image.load('images/leaf.png')
        self.image3 = pygame.transform.scale(self.image3, (32, 32))
        self.image4 = pygame.image.load('images/worm/wormOne.png')
        self.image4 = pygame.transform.scale(self.image4, (32, 32))



    # takes off a life/removes coins
    def lostALife(self):
        self.livesLeft -= 1
        self.totalHoney = 0
        self.levelHoney = 0
        self.leavesCollected = 0

    # for when player collects 100 coins- adds a life
    def gainALife(self):
        self.livesLeft += 1

    # adds a certain amount of coins to total collection
    def collectHoney(self):
        self.totalHoney += 1
        self.levelHoney += 1

    # displays livesLeft, coinsCollected, and total score
    def showScore(self, g):
        if g.currentMap != g.endScreen and g.currentMap != g.gameOver:
            if g.pause:
                self.textPause = self.font.render('PAUSE', 1, (0, 0, 0))
            self.text3 = self.font.render(str(g.minutes) + " : " + str(g.seconds), 1, (0, 0, 0))

            if g.levelType == 'bee':
                self.text = self.font.render(str(self.totalHoney), 1, (0, 0, 0))
                self.text2 = self.font.render(str(self.livesLeft), 1, (0, 0, 0))

                self.screen.blit(self.text, (925, 25))
                self.screen.blit(self.image1, (890, 25))
                self.screen.blit(self.text2, (925, 65))
                self.screen.blit(self.image2, (890, 65))
                self.screen.blit(self.text3, (50, 25))
            else:
                self.text = self.font.render((str(self.leavesCollected) + "/" + str(self.leavesTotal)), 1, (0, 0, 0))
                self.text2 = self.font.render(str(self.livesLeft), 1, (0, 0, 0))

                self.screen.blit(self.text, (925, 25))
                self.screen.blit(self.image3, (890, 25))
                self.screen.blit(self.text2, (925, 65))
                self.screen.blit(self.image4, (890, 65))
                self.screen.blit(self.text3, (50, 25))

            if g.pause:
                self.screen.blit(self.textPause, (512, 352))
                

import sys
import pygame
from notPlayer import *
from player import *


""" for bee level ___________________________________________________________________________________________________"""
def checkBeeEvents(g, sb, settings, walls, honey, bee, USEREVENT):
    checkBeeCollision(g, sb, settings, walls, honey, bee)
    checkFlower(g, sb, settings, bee)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            keyDownBee(g, event, bee)
        elif event.type == pygame.KEYUP:
            keyUpBee(event, bee)
        if event.type == USEREVENT + 1 and g.currentMap != g.endScreen and g.currentMap != g.gameOver:
            if g.seconds > 0:
                g.seconds -= 1
            else:
                if g.minutes == 0:
                    takeOffBeeLife(g, sb)
                g.minutes -= 1
                g.seconds = 60
        if event.type == USEREVENT + 2 and g.currentMap == g.map2:
            makeItRain(g, settings, walls)
    if g.currentMap == g.map2:
        updateRain(g, sb, settings, walls, bee)


def checkBeeCollision(g, sb, settings, walls, honey, bee):
    leftNum = 30
    rightNum = 30
    upNum = 30
    downNum = 30

    for x in walls:
        if x.type != 'tree' and x.type != 'load' and x.type != 'stem':
            if x.type == 'movingFlower' and not x.visible:
                pass
            else:
                # check left
                if (x.type != 'flower' and x.type != 'deadFlower'):
                    if x.rightEdge <= bee.leftEdge and abs(bee.leftEdge - x.rightEdge) <= settings.beeSpeed:
                        if (x.topEdge < bee.bottomEdge < x.bottomEdge) or (x.topEdge < bee.topEdge < x.bottomEdge) or \
                                (x.topEdge == bee.topEdge and bee.bottomEdge == x.bottomEdge):
                            if x.type != 'hive':
                                if x.type == 'rain':
                                    takeOffBeeLife(g, sb)
                                leftNum = bee.leftEdge - x.rightEdge
                                bee.leftV = leftNum
                                if leftNum != 0:
                                    bee.update(g.collection)
                                    bee.leftV = 0
                                bee.canMoveLeft = False
                            else:
                                num = abs(settings.timePassed - g.seconds)
                                if num > 1 and sb.honeyCount > 0:
                                    sb.collectHoney()
                                    settings.timePassed = g.seconds
                                    tempHoneyCount = sb.honeyCount - 1
                                    sb.honeyCount = 0
                                    honey.empty()
                                    for y in range(tempHoneyCount):
                                        sb.honeyCount += 1
                                        wall = notFlower(g, bee.leftEdge / 32, bee.topEdge / 32, settings, 'honey')
                                        g.collection.add(wall)


                # checks right
                if x.type != 'flower' and x.type != 'deadFlower':
                    if x.leftEdge >= bee.rightEdge and abs(x.leftEdge - bee.rightEdge) <= settings.beeSpeed:
                        if (x.topEdge < bee.bottomEdge < x.bottomEdge) or (x.topEdge < bee.topEdge < x.bottomEdge) or \
                                (x.topEdge == bee.topEdge and bee.bottomEdge == x.bottomEdge):
                            if x.type != 'hive':
                                if x.type == 'rain':
                                    takeOffBeeLife(g, sb)
                                rightNum = x.leftEdge - bee.rightEdge
                                bee.rightV = rightNum
                                if rightNum != 0:
                                    bee.update(g.collection)
                                    bee.rightV = 0
                                bee.canMoveRight = False
                            else:
                                num = abs(settings.timePassed - g.seconds)
                                if num > 1 and sb.honeyCount > 0:
                                    sb.collectHoney()
                                    settings.timePassed = g.seconds
                                    tempHoneyCount = sb.honeyCount - 1
                                    sb.honeyCount = 0
                                    honey.empty()
                                    for y in range(tempHoneyCount):
                                        sb.honeyCount += 1
                                        wall = notFlower(g, bee.leftEdge / 32, bee.topEdge / 32, settings, 'honey')
                                        g.collection.add(wall)
                # checks up
                if x.type != 'flower' and x.type != 'deadFlower':
                    num = settings.upBeeSpeed
                    if x.type == 'rain':
                        num += settings.rainSpeed
                    if x.bottomEdge <= bee.topEdge and abs(bee.topEdge - x.bottomEdge) <= num:
                        if (x.leftEdge < bee.leftEdge < x.rightEdge) or (x.leftEdge < bee.rightEdge < x.rightEdge) or \
                                (x.leftEdge == bee.leftEdge and x.rightEdge == bee.rightEdge):
                            if x.type != 'hive':
                                if x.type == 'rain':
                                    takeOffBeeLife(g, sb)
                                upNum = bee.topEdge - x.bottomEdge
                                bee.upV = upNum
                                if upNum != 0:
                                    bee.update(g.collection)
                                    bee.upV = 0
                                bee.canMoveUp = False
                                bee.movingUp = False
                                bee.falling = True
                            else:
                                num = abs(settings.timePassed - g.seconds)
                                if num > 1 and sb.honeyCount > 0:
                                    sb.collectHoney()
                                    settings.timePassed = g.seconds
                                    tempHoneyCount = sb.honeyCount - 1
                                    sb.honeyCount = 0
                                    honey.empty()
                                    for y in range(tempHoneyCount):
                                        sb.honeyCount += 1
                                        wall = notFlower(g, bee.leftEdge / 32, bee.topEdge / 32, settings, 'honey')
                                        g.collection.add(wall)
                # checks down
                if x.topEdge >= bee.bottomEdge and abs(x.topEdge - bee.bottomEdge) <= settings.beeFalling[bee.fallCount]:
                    if (x.leftEdge < bee.leftEdge < x.rightEdge) or (x.leftEdge < bee.rightEdge < x.rightEdge) or \
                            (x.leftEdge == bee.leftEdge and x.rightEdge == bee.rightEdge):
                        if x.type != 'hive':
                            if x.type == 'movingFlower' and x.visible:
                                if g.currentMap == g.gameOver or g.currentMap == g.endScreen:
                                    g.stillPlaying = False
                                if g.currentMap == g.map2:
                                    g.showEndScreen = True
                                g.movingForward = True
                            if x.type == 'rain':
                                takeOffBeeLife(g, sb)
                            downNum = x.topEdge - bee.bottomEdge
                            bee.downV = downNum
                            if downNum != 0:
                                bee.update(g.collection)
                                bee.downV = 0
                            if x.type == 'deadFlower':
                                if not bee.onFlower:
                                    wall = notFlower(g, x.leftEdge / 32, x.topEdge / 32 - 1, settings, 'load')
                                    g.walls.add(wall)
                                bee.onFlower = True
                            bee.canMoveDown = False
                            bee.falling = False
                            bee.fallCount = 0
                        else:
                            num = abs(settings.timePassed - g.seconds)
                            if num > 1 and sb.honeyCount > 0:
                                sb.collectHoney()
                                settings.timePassed = g.seconds
                                tempHoneyCount = sb.honeyCount - 1
                                sb.honeyCount = 0
                                honey.empty()
                                for y in range(tempHoneyCount):
                                    sb.honeyCount += 1
                                    wall = notFlower(g, bee.leftEdge / 32, bee.topEdge / 32, settings, 'honey')
                                    g.collection.add(wall)


    if leftNum == 30:
        bee.canMoveLeft = True
        bee.leftV = settings.beeSpeed
    if rightNum == 30:
        bee.canMoveRight = True
        bee.rightV = settings.beeSpeed
    if upNum == 30:
        bee.canMoveUp = True
        bee.upV = settings.upBeeSpeed
        if bee.movingUp:
            bee.falling = False
    if downNum == 30:
        bee.onFlower = False
        bee.downV = settings.beeFalling[bee.fallCount]
        bee.canMoveDown = True
        if not bee.movingUp:
            bee.falling = True


def checkFlower(g, sb, settings, bee):
    if not settings.honeyDone:
        if bee.onFlower:
            for x in g.walls:
                if x.type == 'load':
                    x.update()

    if not bee.onFlower or settings.honeyDone:
            if settings.honeyDone:
                addHoney(g, sb, settings, bee)
            for x in g.walls:
                if x.type == 'load':
                    g.walls.remove(x)
            settings.slowImage = 0
            settings.imageCount = 0
            settings.honeyDone = False
    if sb.levelHoney == g.currentMap.flowNum and sb.honeyCount == 0:
        for x in g.walls:
            if x.type == 'movingFlower':
                x.visible = True
                x.updateFlower()
    if g.currentMap == g.gameOver or g.currentMap == g.endScreen:
        for x in g.walls:
            if x.type == 'movingFlower':
                x.visible = True
                x.updateFlower()


def takeOffBeeLife(g, sb):
    if sb.livesLeft >= 0 and not sb.skip:
        g.new1()
        sb.lostALife()
        sb.skip = True
        g.seconds = 60
        g.minutes = 3
    elif sb.livesLeft >= 0 and sb.skip:
        sb.skip = False
    if sb.livesLeft < 0:
        g.movingForward = True
        g.showGameOver = True


def makeItRain(g, settings, walls):
    num = random.randint(0, (g.lengthOfLevel))
    rain = notFlower(g, num, 0, settings, 'rain')
    g.walls.add(rain)


def updateRain(g, sb, settings, walls, bee):
    for x in walls:
        if x.type == 'rain':
            x.update()
            if x.bottomEdge >= (settings.h):
                walls.remove(x)


def addHoney(g, sb, settings, bee):
    sb.honeyCount += 1
    col = bee.leftEdge / 32
    row = (bee.topEdge % 32 + bee.topEdge) / 32
    wall = notFlower(g, col, row, settings, 'honey')
    g.collection.add(wall)
    for x in g.walls:
        if x.type == 'deadFlower' and x.topEdge == bee.bottomEdge:
            if (x.leftEdge < bee.leftEdge < x.rightEdge) or (x.leftEdge < bee.rightEdge < x.rightEdge) or \
                    (x.leftEdge == bee.leftEdge and x.rightEdge == bee.rightEdge):
                x.updateFlower()
                x.type = 'flower'


def checkBeeType(g, tile, col, row, settings):
    if tile == '.':
        pass
    else:
        if tile == '1':
            wall = notFlower(g, col, row, settings, 'border')
            g.walls.add(wall)
        elif tile == '2':
            wall = notFlower(g, col, row, settings, 'ground')
            g.walls.add(wall)
        elif tile == 'f':
            wall = flower(g, col, row, settings, 'deadFlower')
            g.walls.add(wall)
            for x in range((settings.h / 32) - row - 2):
                stem = notFlower(g, col, (row + x + 2), settings, 'stem')
                g.walls.add(stem)
        elif tile == 'F':
            wall = flower(g, col, row, settings, 'movingFlower')
            g.walls.add(wall)
        elif tile == 't':
            wall = notFlower(g, col, row, settings, 'tree')
            g.walls.add(wall)
        elif tile == 'h':
            wall = notFlower(g, col, row, settings, 'hive')
            g.walls.add(wall)
        elif tile == 'P':
            g.player = beePlayer(g, col, row, settings, g.screen)


def keyDownBee(g, event, bee):
    if event.key == pygame.K_RIGHT:
        bee.movingRight = True
    if event.key == pygame.K_LEFT:
        bee.movingLeft = True
    if event.key == pygame.K_SPACE:
        bee.movingUp = True
        bee.falling = False
    if event.key == pygame.K_p:
        g.pause = True
        bee.movingLeft = False
        bee.movingRight = False
        bee.movingUp = False
        bee.falling = False

    if event.key == pygame.K_ESCAPE:
        sys.exit()


def keyUpBee(event, bee):
    if event.key == pygame.K_RIGHT:
        bee.movingRight = False
    if event.key == pygame.K_LEFT:
        bee.movingLeft = False
    if event.key == pygame.K_SPACE:
        bee.movingUp = False
        bee.falling = True


""" for worm level __________________________________________________________________________________________________"""
def checkWormEvents(g, sb, settings, walls, worm, worms, USEREVENT):
    checkWormCollision(g, sb, settings, walls, worms)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            keyDownWorm(g, event, worms)
        elif event.type == pygame.KEYUP:
            keyUpWorm(event, worms)
        if event.type == USEREVENT + 1 and g.currentMap != g.endScreen and g.currentMap != g.gameOver:
            if g.seconds > 0:
                g.seconds -= 1
            else:
                if g.minutes == 0:
                    takeOffBeeLife(g, sb)
                g.minutes -= 1
                g.seconds = 60
    updateDirt(g, sb, settings, walls, worms)
    updateWormMovement(g, sb, settings, worms)
    if sb.leavesCollected == sb.leavesTotal and g.currentMap == g.map1:
        g.movingForward = True
        g.showEndScreen = True


def checkWormCollision(g, sb, settings, walls, worm):
    leftNum = 30
    rightNum = 30
    upNum = 30
    downNum = 30

    for x in walls:
        if x.type == 'rock':
            # for checking if can move left
            if x.rightEdge == worm[0].leftEdge and x.topEdge == worm[0].topEdge and x.bottomEdge == worm[0].bottomEdge:
                    leftNum = 0
            # for checking if can move right
            if x.leftEdge == worm[0].rightEdge and x.topEdge == worm[0].topEdge and x.bottomEdge == worm[0].bottomEdge:
                    rightNum = 0
            # for checking if can move down
            if x.topEdge == worm[0].bottomEdge and x.rightEdge == worm[0].rightEdge and x.leftEdge == worm[0].leftEdge:
                    downNum = 0
            # for checking if can move up
            if x.bottomEdge == worm[0].topEdge and x.rightEdge == worm[0].rightEdge and x.leftEdge == worm[0].leftEdge:
                    upNum = 0
        if x.type == 'endLeaf':
            # for movingLeft
            if x.rightEdge == worm[0].leftEdge and (x.topEdge == worm[0].topEdge or x.bottomEdge == worm[0].bottomEdge):
                leftNum = 0
                g.stillPlaying = False
            # for movingRight
            if x.leftEdge == worm[0].rightEdge and (x.topEdge == worm[0].topEdge or x.bottomEdge == worm[0].bottomEdge):
                rightNum = 0
                g.stillPlaying = False
            # for movingDown
            if x.topEdge == worm[0].bottomEdge and (x.rightEdge == worm[0].rightEdge or x.leftEdge == worm[0].leftEdge):
                downNum = 0
                g.stillPlaying = False
            # for movingDown
            if x.bottomEdge == worm[0].topEdge and (x.rightEdge == worm[0].rightEdge or x.leftEdge == worm[0].leftEdge):
                upNum = 0
                g.stillPlaying = False

    if leftNum == 30:
        for x in worm:
            x.canMoveLeft = True
    else:
        for x in worm:
            x.canMoveLeft = False
    if rightNum == 30:
        for x in worm:
            x.canMoveRight = True
    else:
        for x in worm:
            x.canMoveRight = False
    if downNum == 30:
        for x in worm:
            x.canMoveDown = True
    else:
        for x in worm:
            x.canMoveDown = False
    if upNum == 30:
        for x in worm:
            x.canMoveUp = True
    else:
        for x in worm:
            x.canMoveUp = False


def updateDirt(g, sb, settings, walls, worm):
    for x in walls:
        if x.type == 'dirt' or x.type == 'leaf':
            if worm[0].canMoveLeft and worm[0].movingLeft:
                if x.rightEdge == worm[0].leftEdge and x.topEdge == worm[0].topEdge and x.bottomEdge == worm[0].bottomEdge:
                    if x.type == 'leaf':
                        sb.leavesCollected += 1
                    walls.remove(x)
            if worm[0].canMoveRight and worm[0].movingRight:
                if worm[0].rightEdge == x.leftEdge and x.topEdge == worm[0].topEdge and x.bottomEdge == worm[0].bottomEdge:
                    if x.type == 'leaf':
                        sb.leavesCollected += 1
                    walls.remove(x)
            if worm[0].canMoveUp and worm[0].movingUp:
                if worm[0].topEdge == x.bottomEdge and x.rightEdge == worm[0].rightEdge and x.leftEdge == worm[0].leftEdge:
                    if x.type == 'leaf':
                        sb.leavesCollected += 1
                    walls.remove(x)
            if worm[0].canMoveDown and worm[0].movingDown:
                if worm[0].bottomEdge == x.topEdge and x.rightEdge == worm[0].rightEdge and x.leftEdge == worm[0].leftEdge:
                    if x.type == 'leaf':
                        sb.leavesCollected += 1
                    walls.remove(x)


# for checking buttons (up/down/left/right)/pause button
def keyDownWorm(g, event, worm):
    if event.key == pygame.K_RIGHT:
        for x in worm:
            x.movingRight = True
    if event.key == pygame.K_LEFT:
        for x in worm:
            x.movingLeft = True
    if event.key == pygame.K_UP:
        for x in worm:
            x.movingUp = True
    if event.key == pygame.K_DOWN:
        for x in worm:
            x.movingDown = True
    if event.key == pygame.K_p:
        g.pause = True
        for x in worm:
            x.movingLeft = False
            x.movingRight = False
            x.movingUp = False
            x.falling = False

    if event.key == pygame.K_ESCAPE:
        sys.exit()


def keyUpWorm(event, worm):
    if event.key == pygame.K_RIGHT:
        for x in worm:
            x.movingRight = False
    if event.key == pygame.K_LEFT:
        for x in worm:
            x.movingLeft = False
    if event.key == pygame.K_UP:
        for x in worm:
            x.movingUp = False
    if event.key == pygame.K_DOWN:
        for x in worm:
            x.movingDown = False


# for making the tile-map
def checkWormType(g, tile, col, row, settings, sb):
    if tile == '.':
        pass
    else:
        if tile == '1':
            wall = wormStuff(g, col, row, settings, 'dirt')
            g.walls.add(wall)
        elif tile == '2':
            wall = wormStuff(g, col, row, settings, 'rock')
            g.walls.add(wall)
        elif tile == '3':
            wall = wormStuff(g, col, row, settings, 'leaf')
            g.walls.add(wall)
            sb.leavesTotal += 1
        elif tile == 'F':
            wall = wormStuff(g, col, row, settings, 'endLeaf')
            g.walls.add(wall)
        elif tile == 'P':
            for x in range(0, 3):
                worm = wormPlayer(g, col, row, settings, g.screen, x)
                g.wormParts.append(worm)


# updates the list of worm parts
def updateWormMovement(g, sb, settings, worm):
    checkLeftRightWorm(g, settings, worm)
    checkUpDownWorm(g, settings, worm)


# checks left/right movement
def checkLeftRightWorm(g, settings, worm):
    # for moving right
    if worm[0].movingRight and worm[0].canMoveRight and (worm[0].rightEdge <= (g.lengthOfLevel * 32)):
        switch = True
        for x in range(0, 2):
            if worm[x].topEdge != worm[x + 1].topEdge:
                switch = False
        if worm[0].rightEdge < worm[2].rightEdge and switch:
            switchItUp(g, worm)
        for y in range(0, 3):
            if worm[y].topEdge == worm[0].topEdge and worm[y].rightEdge == worm[0].rightEdge:
                worm[0].tempX = worm[y].rect.x
                worm[0].tempY = worm[y].rect.y
                worm[y].rect.x += worm[0].rightV
                worm[y].leftEdge = worm[y].rect.x
                worm[y].rightEdge = worm[y].rect.x + settings.tileSize
            else:
                followSuit(settings, worm, y)
        updatePics(worm)
        for x in worm:
            x.movingRight = False

    # for moving left
    if worm[0].movingLeft and worm[0].canMoveLeft and worm[0].leftEdge > 0:
        switch = True
        for x in range(0, 2):
            if worm[x].topEdge != worm[x + 1].topEdge:
                switch = False
        if worm[0].rightEdge > worm[2].rightEdge and switch:
            switchItUp(g, worm)
        for y in range(0, 3):
            if worm[y].topEdge == worm[0].topEdge and worm[y].rightEdge == worm[0].rightEdge:
                worm[0].tempX = worm[y].rect.x
                worm[0].tempY = worm[y].rect.y
                worm[y].rect.x -= worm[0].leftV
                worm[y].leftEdge = worm[y].rect.x
                worm[y].rightEdge = worm[y].rect.x + settings.tileSize
            else:
                followSuit(settings, worm, y)
        updatePics(worm)
        for x in worm:
            x.movingLeft = False


# checks up/down movement
def checkUpDownWorm(g, settings, worm):
    # for moving down
    if worm[0].movingDown and worm[0].canMoveDown and worm[0].bottomEdge < (36 * 32):
        switch = True
        for x in range(0, 2):
            if worm[x].rightEdge != worm[x + 1].rightEdge:
                switch = False
        if worm[0].topEdge < worm[2].topEdge and switch:
            switchItUp(g, worm)
        for y in range(0, 3):
            if worm[y].topEdge == worm[0].topEdge and worm[y].rightEdge == worm[0].rightEdge:
                worm[0].tempX = worm[y].rect.x
                worm[0].tempY = worm[y].rect.y
                worm[y].rect.y += worm[0].downV
                worm[y].topEdge = worm[y].rect.y
                worm[y].bottomEdge = worm[y].rect.y + settings.tileSize
            else:
                followSuit(settings, worm, y)
        updatePics(worm)
        for x in worm:
            x.movingDown = False

    # for moving up
    if worm[0].movingUp and worm[0].canMoveUp and worm[0].topEdge > 0:
        switch = True
        for x in range(0, 2):
            if worm[x].rightEdge != worm[x + 1].rightEdge:
                switch = False
        if worm[0].topEdge > worm[2].topEdge and switch:
            switchItUp(g, worm)
        for y in range(0, 3):
            if worm[y].topEdge == worm[0].topEdge and worm[y].rightEdge == worm[0].rightEdge:
                worm[0].tempX = worm[y].rect.x
                worm[0].tempY = worm[y].rect.y
                worm[y].rect.y -= worm[0].upV
                worm[y].topEdge = worm[y].rect.y
                worm[y].bottomEdge = worm[y].rect.y + settings.tileSize
            else:
                followSuit(settings, worm, y)
        updatePics(worm)
        for x in worm:
            x.movingUp = False


# for if changing from left to right
def switchItUp(g, worm):
    temp1 = worm[0]
    worm[0] = worm[2]
    worm[2] = temp1


# for having the other parts follow the main one
def followSuit(settings, worm, y):
    num1 = worm[y].rect.x
    num2 = worm[y].rect.y
    worm[y].rect.y = worm[0].tempY
    worm[y].rect.x = worm[0].tempX
    worm[y].topEdge = worm[y].rect.y
    worm[y].bottomEdge = worm[y].rect.y + settings.tileSize
    worm[y].leftEdge = worm[y].rect.x
    worm[y].rightEdge = worm[y].rect.x + settings.tileSize
    worm[0].tempX = num1
    worm[0].tempY = num2


# for updating pics                                                 THERE IS PROBABLY AN EASIER WAY TO DO THIS
def updatePics(worm):
    for x in range (0, 3):
        if x == 0:
            if worm[x].movingRight:
                worm[x].image = pygame.image.load('images/worm/wormOne.png')
            elif worm[x].movingLeft:
                worm[x].image = pygame.image.load('images/worm/wormOneLeft.png')
            elif worm[x].movingDown:
                worm[x].image = pygame.image.load('images/worm/wormOneDown.png')
            elif worm[x].movingUp:
                worm[x].image = pygame.image.load('images/worm/wormOneUp.png')
        if x == 1:
            if worm[x].movingRight or worm[x].movingLeft:
                worm[x].image = pygame.image.load('images/worm/wormTwo.png')
            elif worm[x].movingDown or worm[x].movingUp:
                worm[x].image = pygame.image.load('images/worm/wormTwoDown.png')
        if x == 2:
            if worm[x].movingRight:
                worm[x].image = pygame.image.load('images/worm/wormThree.png')
            elif worm[x].movingLeft:
                worm[x].image = pygame.image.load('images/worm/wormThreeLeft.png')
            elif worm[x].movingDown and worm[x].rightEdge == worm[0].rightEdge:
                worm[x].image = pygame.image.load('images/worm/wormThreeDown.png')
            elif worm[x].movingUp and worm[x].rightEdge == worm[0].rightEdge:
                worm[x].image = pygame.image.load('images/worm/wormThreeUp.png')


""" for home level __________________________________________________________________________________________________"""
def checkNormalType(g, tile, col, row, settings):
    if tile == '.':
        pass
    else:
        if tile == '1' or tile == '2':
            pass
        elif tile == 'b':
            wall = homeStuff(g, col, row, settings, 'bee')
            g.walls.add(wall)
        elif tile == 'w':
            wall = homeStuff(g, col, row, settings, 'worm')
            g.walls.add(wall)
        elif tile == 'P':
            player = noPlayer(g, col, row, settings, g.screen)
            g.player = player


def checkMovement(g, settings, walls, USEREVENT):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            keyDownHome(g, event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            xClick, yClick = pygame.mouse.get_pos()
            checkMoveForward(g, xClick, yClick, walls)
        if event.type == USEREVENT+1:
            num = random.randint(0, 7)
            bird = homeStuff(g, -10, num, settings, 'bird')
            g.walls.add(bird)

    for x in walls:
        if x.type == 'bird':
            x.update()


def keyDownHome(g, event):
    if event.key == pygame.K_ESCAPE:
        sys.exit()


def checkMoveForward(g, xClick, yClick, walls):
    for x in walls:
        if x.type == 'bee':
            if x.leftEdge <= xClick and x.rightEdge >= xClick and x.topEdge <= yClick and x.bottomEdge >= yClick:
                g.notChosen = False
                g.type = 'bee'
        elif x.type == 'worm':
            if x.leftEdge <= xClick and x.rightEdge >= xClick and x.topEdge <= yClick and x.bottomEdge >= yClick:
                g.notChosen = False
                g.type = 'worm'
                

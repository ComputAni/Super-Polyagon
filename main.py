# Term Project
# Anirudh Ramakrishnan
# Some ideas were made possible thanks to Yousof Soliman and Yeongwoo Hwang
###############################################

from __future__ import with_statement # for Python 2.5 and 2.6
from Tkinter import *
from eventBasedAnimationClass import EventBasedAnimationClass
from InvinciblePieceClass import InvinciblePiece
from PauseScreenClass import PauseScreen
from SplashScreenClass import SplashScreen
from BackgroundClass import Background
from GameOverClass import GameOver
from ObstacleClass import Obstacles
from BasePolygonClass import BasePolygon
import random,copy,time
import contextlib # for urllib.urlopen()
import urllib
import os
import math

class SuperHex(EventBasedAnimationClass):
    def __init(self):
        super(SuperHex,self).__init(width =1000, height = 1000)

    def onKeyPressed(self,event):
        if event.keysym == "r":
            self.initAnimation()
            self.isSplashScreen = False
            self.isRunning = True
        elif event.keysym == "Left":
            #changes angle
            self.moveLeft()
        elif event.keysym == "Right":
            self.moveRight()
        elif event.keysym == "n" and self.isGameOver:
            self.isGameOver = False
            self.initAnimation()
            self.isSplashScreen = False
            self.isRunning = True
        elif event.keysym == "p" and not self.isSplashScreen:
            #pausing feature
            self.isPaused = not self.isPaused
        self.onOtherKeyPressed(event)

    def onOtherKeyPressed(self,event):
        if event.keysym == "b":
                self.splashScreen.controls = False
                self.splashScreen.options = False
                self.splashScreen.credits = False
                self.splashScreen.highScore = False
        elif event.keysym == "m" and self.isGameOver:
            self.initAnimation()
        elif event.keysym == "h" and self.isGameOver:
            self.initAnimation()
            self.splashScreen.highScore = True
        elif event.keysym == "q" and self.isRunning:
            self.initAnimation()
        elif event.keysym == "a":
            self.isInvinciblePiece = True

    ###############obstacle creation methods##############
    def createObstacle(self):
        if self.customMode:
            self.createCustomObstacles()
        else:
            self.obstacleCount += 1
            (minObstacles,skipObstacle) = (5,6)
            #the whirlpool obstacle is a subset of a hexagon obstacle
            if self.basePolygon.baseType == "Hexagon":
                if self.obstacleCount % 5 == 0 and self.obstacleCount < 7:
                    self.hardObstacleCount +=1
                    obsNum = random.choice([0,1,2])
                    if obsNum == 1: self.createWhirlpoolObstacle()
                    elif obsNum == 0: self.createStairObstacle()
                    elif obsNum == 2: self.createMultiCObstacle()
                elif self.checkHardObsPresent(): self.createHexObstacle()
            elif self.basePolygon.baseType == "Pentagon":
                self.createPentObstacle()
            elif self.basePolygon.baseType == "Square":
                self.createSquareObstacle()

    def createCustomObstacles(self):
            print self.obstacleCount
            #the whirlpool obstacle is a subset of a hexagon obstacle
            if self.basePolygon.baseType == "Hexagon":          
                if (self.hardObstacleCount < self.customObstacles) and self.obstacleCount % 3 == 1:
                    self.hardObstacleCount +=1
                    self.obstacleCount += 1      
                    print "hard obs has been created"
                    obsNum = random.choice([0,1,2])
                    if obsNum == 0: self.createWhirlpoolObstacle()
                    elif obsNum == 1: self.createStairObstacle()
                    elif obsNum == 2: self.createMultiCObstacle()
                elif self.checkHardObsPresent(): 
                    self.obstacleCount += 1      
                    self.createHexObstacle()
            elif self.basePolygon.baseType == "Pentagon":
                self.createPentObstacle()
                self.obstacleCount += 1      
            elif self.basePolygon.baseType == "Square":
                self.obstacleCount += 1      
                self.createSquareObstacle()

    def createMultiCObstacle(self):
        numOfSides = 5
        sideList = [1,2,3,4,5]
        obstacleType = "MultiC"
        #it is a 6 hexagon pattern
        nHexagons = 4
        radius = 500
        angle = math.pi/2
        for i in xrange(nHexagons):
            newObstacle = Obstacles(self.width,self.height,numOfSides,sideList,
                                self.backColor,self.currentRotDir,obstacleType,
                                angle,radius)
            self.obstacles.append(newObstacle)
            radius += 250
            angle += math.pi/3

    def createStairObstacle(self):
        numOfSides = 4
        sideList = [0,2,3,5]
        obstacleType = "Stairs"
        #pattern of 2 adjacent sides
        sSides = 3
        radius = 500
        angle = math.pi/2
        for i in xrange(sSides):
            newObstacle = Obstacles(self.width,self.height,numOfSides,sideList,
                                        self.backColor,self.currentRotDir,
                                        obstacleType,angle,radius)
            self.obstacles.append(newObstacle)
            radius += 250
            angle += math.pi/3

    def createWhirlpoolObstacle(self):
        numOfSides = 1
        sideList = [0]
        obstacleType = "Whirlpool"
        wSides = 10
        radius = 500
        angle = math.pi/2
        for i in xrange(wSides):
            newObstacle = Obstacles(self.width,self.height,numOfSides,sideList,
                        self.backColor,self.currentRotDir,obstacleType,angle,radius)
            self.obstacles.append(newObstacle)
            radius += 60
            angle += math.pi/3

    def createPentWhirlpoolObstacle(self):
        numOfSides = 1
        sideList = [0]
        obstacleType = "Pent Whirlpool"
        wSides = 10
        radius = 500
        angle = math.pi/2
        for i in xrange(wSides):
            newObstacle = Obstacles(self.width,self.height,numOfSides,sideList,
                        self.backColor,self.currentRotDir,obstacleType,angle,radius)
            self.obstacles.append(newObstacle)
            radius += 100
            angle += 2*math.pi/5

    def createSquareZigObstacle(self):
        numOfSides = 1
        sideList = [0]
        obstacleType = "Square Zig"
        wSides = 10
        radius = 500
        angle = math.pi/2
        for i in xrange(wSides):
            newObstacle = Obstacles(self.width,self.height,numOfSides,sideList,
                        self.backColor,self.currentRotDir,obstacleType,angle,radius)
            self.obstacles.append(newObstacle)
            radius += 100
            angle += math.pi/2

    def createPentObstacle(self):
        if self.obstacleCount % 5 == 0 and self.obstacleCount < 7:
            self.hardObstacleCount +=1
            self.createPentWhirlpoolObstacle()
        elif self.checkHardObsPresent():
            numOfSides = 4
            sideList = Obstacles.choosePentSides(numOfSides)
            obstacleType = "Pentagon"
            angle = self.randomAngle()
            newObstacle = Obstacles(self.width,self.height,numOfSides,sideList,
                self.backColor,self.currentRotDir,obstacleType,angle)
            self.obstacles.append(newObstacle)

    def createHexObstacle(self):
        numOfSides = random.choice([2,3,4,5])
        sideList = Obstacles.chooseHexSides(numOfSides)
        obstacleType = "Hexagon"
        angle = self.randomAngle()
        newObstacle = Obstacles(self.width,self.height,numOfSides,sideList,
                                    self.backColor,self.currentRotDir,
                                    obstacleType,angle)
        self.obstacles.append(newObstacle)

    def createSquareObstacle(self):
        if self.obstacleCount % 5 == 0 and self.obstacleCount < 7:
            self.hardObstacleCount +=1
            self.createSquareZigObstacle()
        elif self.checkHardObsPresent():
            numOfSides = 3
            sideList = Obstacles.chooseSquareSides(numOfSides)
            obstacleType = "Square"
            angle = self.randomAngle()
            newObstacle = Obstacles(self.width,self.height,numOfSides,sideList,
                self.backColor,self.currentRotDir, obstacleType,angle)
            self.obstacles.append(newObstacle)
    ##########end obstacle creation methods#################

    #character movement
    def moveLeft(self):
        angleShift = 6
        self.newCharacter.charAngle += math.pi/angleShift

    def moveRight(self):
        angleShift = 6
        self.newCharacter.charAngle -= math.pi/angleShift
    #end character movement

    #######MOUSE CLICK EVENTS##############
    def onMousePressed(self,event):
        (x,y) = (event.x,event.y)
        #if user presses start, change self.isSplashScreen to false, and isRunning to true
        if self.isSplashScreen:
            if SplashScreen.startClicked(x,y) and not self.splashScreen.options:
                self.isSplashScreen = False
                self.isRunning = True
            elif SplashScreen.controlsClicked(x,y):
                self.splashScreen.controls = True
            elif ((SplashScreen.optionsClicked(x,y)) and 
                                            (not self.splashScreen.options)):
                self.splashScreen.options = True
            elif SplashScreen.creditsClicked(x,y):
                self.splashScreen.credits = True
            elif SplashScreen.highScoreClicked(x,y):
                self.splashScreen.highScore = True
        self.checkBackButton(x,y)
        self.checkSplashScreenOptions(x,y)

    #checks to see if back is pressed in menus
    def checkBackButton(self,x,y):
        if self.isSplashScreen:
            if self.splashScreen.controls and SplashScreen.backButtonClicked(x,y):
                self.splashScreen.controls = False
            elif self.splashScreen.options and SplashScreen.backButtonClicked(x,y):
                self.splashScreen.options = False
            if self.splashScreen.credits and SplashScreen.backButtonClicked(x,y):
                self.splashScreen.credits = False
            if self.splashScreen.highScore and SplashScreen.backButtonClicked(x,y):
                self.splashScreen.highScore = False

    def checkSplashScreenOptions(self,x,y):
        if self.splashScreen.options:
            if SplashScreen.easyDiffClicked(x,y) or SplashScreen.easySpeedClicked(x,y):
                self.splashScreen.currentDifficulty = 0
                self.currentDifficulty = 0
                self.creationTimer = 18
            elif SplashScreen.medDiffClicked(x,y) or SplashScreen.medSpeedClicked(x,y):
                self.splashScreen.currentDifficulty = 1
                self.currentDifficulty = 1
                self.creationTimer = 14
            elif SplashScreen.hardDiffClicked(x,y) or SplashScreen.hardSpeedClicked(x,y):
                self.splashScreen.currentDifficulty = 2
                self.currentDifficulty = 2
                self.creationTimer = 12     
            else: self.checkCustomOptions(x,y)
        self.checkGameOverOptions(x,y)

    def checkCustomOptions(self,x,y):
            if SplashScreen.twoObsClicked(x,y) and self.customMode:
                self.customObstacles = 2
                self.splashScreen.customObs = 2
            elif SplashScreen.fourObsClicked(x,y) and self.customMode:
                self.customObstacles = 4
                self.splashScreen.customObs = 4
            elif SplashScreen.sixObsClicked(x,y) and self.customMode:
                self.customObstacles = 10
                self.splashScreen.customObs = 10
            elif SplashScreen.twentyTimeClicked(x,y) and self.customMode:
                self.customTime,self.maxScore = 20,20
                self.splashScreen.customTime = 20
            elif SplashScreen.thirtyTimeClicked(x,y) and self.customMode:
                self.customTime,self.maxScore = 30,30
                self.splashScreen.customTime = 30
            elif SplashScreen.minuteTimeClicked(x,y) and self.customMode:
                self.customTime,self.maxScore = 60,60
                self.splashScreen.customTime = 60
            elif SplashScreen.customModeClicked(x,y):
                self.customMode = not self.customMode
                self.splashScreen.customMode = not self.splashScreen.customMode
                self.gameOverScreen.customMode = not self.gameOverScreen.customMode

    def checkGameOverOptions(self,x,y):
        if self.isGameOver:
            if SplashScreen.startClicked(x,y):
                self.initAnimation()
                self.isSplashScreen = False
                self.isRunning = True
            #options menu
            elif SplashScreen.controlsClicked(x,y):
                self.initAnimation()
                self.isSplashScreen = True
            elif SplashScreen.highScoreClicked(x,y):
                self.initAnimation()
                self.isSplashScreen = True
                self.splashScreen.highScore = True
            elif SplashScreen.creditsClicked(x,y):
                self.initAnimation()
                self.isSplashScreen,self.splashScreen.credits = True,True
            elif SplashScreen.optionsClicked(x,y):
                self.initAnimation()
                self.isSplashScreen,self.splashScreen.options = True,True
    #####END MOUSE CLICK OPTIONS###############
    

    #returns False if the character angle is within any of the obstacle angles
    def isLegal(self,angleInterval,charAngle):
        for intervals in angleInterval:
            #checks to see if char angle is greater than min, or less than max
            if charAngle > intervals[0] and charAngle < intervals[1]:
                return False
        return True
    
    #basic collision detection between character and obstacles
    def checkCollision(self,obstacle):
        #obstacle method, gets the min and max angle for collision testing
        angleInterval = \
            obstacle.getAngleInt(obstacle.initialAngle,obstacle.sideList)
        #Character method, gets the angle of the character
        currCharacterAngle = \
        self.newCharacter.getCharAngle(self.newCharacter.charAngle)
        #if the angle is within the angle interval, and less than radius 100
        #then it must be a collision
        if (not self.isLegal(angleInterval,currCharacterAngle) and  
                                        (obstacle.initialRadius <= 100)):
            self.isRunning = False
            self.isGameOver = True
            self.finalScore=self.gameTimerAndScore if not self.customMode else 0
            gameWon = self.customGameWon if self.customMode else self.gameWon
            self.splashScreen.updateScore(self.finalScore,self.customMode,gameWon)

    #helper function, decrements angle
    def decrementObstacle(self,obstacle,minRadius,decrement,hexDecrement,\
                                                pentDecrement,squareDecrement):
        if obstacle.initialRadius > minRadius: 
                    obstacle.initialRadius -= decrement
        if obstacle.obsRotDir:
            if ((obstacle.obstacleType == "Hexagon") or 
                (obstacle.obstacleType in self.hardObstacles)):
                obstacle.initialAngle += hexDecrement
            elif ((obstacle.obstacleType == "Pentagon") or 
                (obstacle.obstacleType in self.hardPentObstacles)):
                obstacle.initialAngle += pentDecrement
            elif ((obstacle.obstacleType == "Square") or 
                (obstacle.obstacleType in self.hardSquareObstacles)):
                obstacle.initialAngle += squareDecrement
        else:
            if ((obstacle.obstacleType == "Hexagon") or 
                (obstacle.obstacleType in self.hardObstacles)):
                obstacle.initialAngle -= hexDecrement
            elif ((obstacle.obstacleType == "Pentagon") or 
                (obstacle.obstacleType in self.hardPentObstacles)):
                obstacle.initialAngle -= pentDecrement
            elif ((obstacle.obstacleType == "Square") or 
                (obstacle.obstacleType in self.hardSquareObstacles)):
                obstacle.initialAngle -= squareDecrement

    #hard obstacles are multi piece obstacles
    def checkHardObsPresent(self):
        for obstacle in self.obstacles:
            if ((obstacle.obstacleType in self.hardObstacles) or 
                (obstacle.obstacleType in self.hardPentObstacles) or
                (obstacle.obstacleType  in self.hardSquareObstacles)):
                return False
        return True

    #decrements the object radius and rotates the angle of the object
    def shrinkObstacles(self):
        (minRadius,decrement,sSides,pSides,hSides) = (80,20,4,5,6)
        (hexDecrement,pentDecrement,squareDecrement) = \
                    (1/(hSides*math.pi),1/(pSides*math.pi),1/(sSides*math.pi))
        for obstacle in self.obstacles:
            self.decrementObstacle(obstacle,minRadius,decrement,hexDecrement,
                                        pentDecrement,squareDecrement)
            if not self.invincibilityMode: self.checkCollision(obstacle)
            if obstacle.initialRadius <= minRadius:
                #only creates new obstacles when the hard obstacle is gone
                if self.checkHardObsPresent(): self.hardObsPresent = False
                self.obstacles.remove(obstacle)

    #obstacle rotation direction
    def changeRotationDir(self):
        updateTime = 100
        if self.timeElapsed % updateTime == 0 and self.checkHardObsPresent():
            self.currentRotDir = not self.currentRotDir
            for obstacle in self.obstacles:
                obstacle.obsRotDir = not self.currentRotDir

    #background and center polygon rotation
    def rotate(self):
        if self.timeElapsed % 1 == 0:
            if self.currentRotDir:
                    self.basePolygon.shift += math.pi/17
                    self.background.shift += math.pi/17
            else:
                    self.basePolygon.shift -= math.pi/17
                    self.background.shift -= math.pi/17

    #changes the base based on timing
    def changeBase(self):
        #every 5 seconds, change base
        if self.obstacleTimer == (self.obstacleTimerReset - 20):
            previousBase = self.basePolygon.baseType
            if previousBase == "Hexagon":
                newBase = "Pentagon"
            elif previousBase == "Pentagon":
                newBase = random.choice(["Square","Hexagon"])
            elif previousBase == "Square":
                newBase = "Pentagon"
            (self.obstacles,self.obstacleCount) = ([],0)
            self.basePolygon.baseType = newBase
            self.changeRotationDir()
            #self.changeBackColor()

    #timer that updates the score, every 1 second.
    #score is based on how long you last
    def updateScore(self):
        if self.timeElapsed % 20 == 0:
            self.gameTimerAndScore += 1

    def updateCustomScore(self):
        if self.timeElapsed % 20 == 0:
            self.maxScore -= 1
        self.gameTimerAndScore = self.maxScore
    
    #every 10 seconds, changes the color of everything
    def changeBackColor(self):
        while True:
            newColor = random.choice(["navy","mint cream","dark orchid",
                        "MediumPurple4","firebrick","gold4","black","black"])
            if newColor != self.backColor:
                break
        self.backColor = newColor
        (self.background.pulseColor,self.background.pentagonColor) =  \
                                Background.choosePulseColor(self.background)
        self.newCharacter.color = \
                                Character.chooseCharColor(self.newCharacter)
        self.basePolygon.baseColor = \
                            BasePolygon.choosePulseColor(self.basePolygon)
        for obstacle in self.obstacles:
            obstacle.color = Obstacles.chooseObstacleColor(obstacle)

    #every 15 secs, make obstacles come faster
    def changeCreationTimer(self):
        if self.timeElapsed % 300 == 0 and self.timeElapsed > 2:
            if self.creationTimer > 6:
                self.creationTimer -=1
        #self.initializeTimers()

    #resets timer every cycle (basically when change of base)
    def resetObstacleTimer(self):
        #after every cycle, it resets the obstacle timer
        if self.obstacleTimer == self.obstacleTimerReset:
            self.obstacleTimer = 0

    #detects collision between character and token, initates inv mode if true
    def checkInvPieceCollision(self):
        currCharacterAngle = \
        self.newCharacter.getCharAngle(self.newCharacter.charAngle)
        pieceAngle = self.invinciblePiece.pieceAngle
        pieceAngleRange = [pieceAngle - .4, pieceAngle +.4]
        if ((currCharacterAngle > pieceAngleRange[0]) and 
            (currCharacterAngle < pieceAngleRange[1])):
            self.invincibilityMode = True
            self.isInvinciblePiece = False

    #checks to see if invinc timer is up, resets if so
    def checkInvPieceTimer(self):
        if self.invinciblePiece.pieceTimer == 0:
            self.isInvinciblePiece = False
            self.invinciblePiece.pieceTimer = 40

    #after 3 seconds of invincibility mode, disables
    def removeInvincibility(self):
        if self.invinciblePiece.invincibilityTimer == 0:
            self.invincibilityMode = False
            self.isInvinciblePiece = False
            self.invinciblePiece.invincibilityTimer = 40

    def checkEnd(self):
        #if the user lasts a full 3 minutes, they they win
        if self.timeElapsed == 500:
            self.gameWon = True
            self.isRunning = False
            self.isGameOver = True
            self.finalScore = self.gameTimerAndScore
            self.splashScreen.updateScore(self.finalScore,self.customMode,
                                                                self.gameWon)

    def checkCustomEnd(self):
        if self.gameTimerAndScore == 0:
            self.gameWon = True
            self.isRunning = False
            self.isGameOver = True
            self.finalScore= 0
            self.splashScreen.updateScore(self.finalScore,self.customMode,
                                                self.gameWon)

    #handles the bulk of obstacle timings
    def doMainTimerEvents(self):
        self.checkInvPieceTimer()
        self.removeInvincibility()
        if not self.customMode: 
            self.updateScore()
            self.checkEnd()
        elif self.customMode: 
            self.updateCustomScore()
            self.checkCustomEnd()
        self.changeBase()
        self.rotate()
        self.shrinkObstacles()
        self.changeCreationTimer()
        self.resetObstacleTimer()

    #handles timers pertaining to invincibility tokens
    def doInvincibilityTimings(self):
        if self.isInvinciblePiece:
            if self.invinciblePiece.pieceTimer > 0:
                self.invinciblePiece.pieceTimer -=1
            self.checkInvPieceCollision()
        if (self.invincibilityMode):
            self.invinciblePiece.invincibilityTimer -=1
        #every 10 seconds, creates a token for invincibility
        #the user must collide to get it
        if self.obstacleTimer % 150 == 0 and self.timeElapsed > 5:
            self.isInvinciblePiece = True

    #main timer function
    def onTimerFired(self):
        if self.isRunning and not self.isPaused:
            self.timeElapsed +=1
            self.obstacleTimer += 1
            self.doInvincibilityTimings()
            #every x seconds, create new obstacle, depends on difficulty
            if self.obstacleTimer % self.creationTimer == 0:
                self.createObstacle()
            self.doMainTimerEvents()
        elif self.isSplashScreen and not self.isPaused:
            self.splashTime +=1
            self.splashScreen.rotateSplashBackground(self.splashTime)
        elif self.isGameOver and not self.isPaused:
            self.gameOverTime +=1
            self.splashScreen.rotateSplashBackground(self.gameOverTime)

    @staticmethod
    def randomAngle():
        pi = math.pi
        return random.choice([pi/6,pi/2,5*pi/6,7*pi/6,3*pi/2,11*pi/6])
    
    def initAnimation(self):
        self.timerDelay = 50
        (self.timeElapsed,self.splashTime,self.gameOverTime) = (0,0,0)
        self.backColor = random.choice(["navy","mint cream","dark orchid",
                        "MediumPurple4","firebrick","gold4","black","black"])
        #True is clockwise, False is counterclockwise
        self.obstacles = []
        self.obstacleCount,self.currentDifficulty,self.obstacleTimer = 0,0,0
        self.currentRotDir,self.invincibilityMode = True,False
        self.isRunning,self.gameWon,self.customGameWon = False,False,False
        self.isSplashScreen,self.isInvinciblePiece = True,False
        self.isGameOver,self.isPaused = False, False
        self.gameTimerAndScore,self.finalScore = 0,0
        self.splashScreen = SplashScreen(self.width,self.height)
        self.gameOverScreen = GameOver(self.width,self.height)
        self.pauseScreen = PauseScreen(self.width,self.height)
        self.background = Background(self.width,self.height,self.backColor)
        self.newCharacter = Character(self.width,self.height,self.backColor)
        self.basePolygon = BasePolygon(self.backColor)
        self.invinciblePiece = InvinciblePiece(self.width,self.height)
        self.hardObstacles = ["MultiC","Stairs", "Whirlpool"]
        self.hardPentObstacles = ["Pent Whirlpool"]
        self.hardSquareObstacles = ["Square Zig"]
        self.shift = 5
        self.hardObstacleCount,self.maxScore = 0,20
        self.customObstacles,self.customTime,self.customMode = (None,None,False)

    ################################
    #########  Drawing #############
    ################################
    def drawCharacter(self):
        canvas = self.canvas
        Character.drawCharacter(self.newCharacter,canvas)

    def drawCenterPolygon(self):
        canvas = self.canvas
        self.basePolygon.drawBasePolygon(canvas,self.width/2,self.height/2)

    def drawObstacles(self):
        pi = math.pi
        canvas = self.canvas
        for obstacle in self.obstacles:
            Obstacles.draw(obstacle,canvas,self.basePolygon.baseType,
                                            obstacle.obstacleType)

    def drawBackground(self):
        canvas = self.canvas
        canvas.create_rectangle(0,0,self.width,self.height,fill=self.backColor)
        self.background.drawPulseBackground(canvas,self.width,self.height,
                                self.basePolygon.baseType)

    #the score is based off of how long you last
    def drawScore(self):
        canvas = self.canvas
        margin = 30
        canvas.create_text(self.width - margin, margin, 
            text = str(self.gameTimerAndScore), font = "Aerial 25 bold", 
                    fill = "white")

    def drawSplashScreen(self):
        canvas = self.canvas
        canvas.create_rectangle(0,0,self.width,self.height,fill = "SteelBlue3")
        self.splashScreen.draw(canvas)

    def drawGameOverScreen(self):
        canvas = self.canvas
        canvas.create_rectangle(0,0,self.width,self.height,fill = "coral1")
        self.gameOverScreen.draw(self.splashScreen,canvas,self.finalScore,
                                        self.splashScreen.currentDifficulty)

    def drawInvinciblePiece(self):
        canvas = self.canvas
        self.invinciblePiece.draw(canvas)

    def drawPauseScreen(self):
        canvas = self.canvas
        #canvas.create_rectangle(200,200,800,800,fill = "coral1")
        self.pauseScreen.draw(self.splashScreen,canvas,self.gameTimerAndScore)

    def initializeTimers(self):
        if not self.customMode:
            self.obsTimer = 2*self.currentDifficulty
            self.creationTimer = 14 - self.obsTimer
            self.obstacleTimerReset = (self.creationTimer * 10) + 40

    def redrawAll(self):
        self.canvas.delete(ALL)
        if self.isRunning:
            print self.creationTimer
            self.drawBackground()
            self.newCharacter.updateCharCoords()
            self.drawCenterPolygon()
            self.drawCharacter()
            self.drawObstacles()
            self.drawScore()
            if self.isInvinciblePiece:
                self.drawInvinciblePiece()
            if self.isPaused:
                self.drawPauseScreen()
        elif self.isSplashScreen and not self.isPaused:
            self.drawSplashScreen()
            self.initializeTimers()
        elif self.isGameOver and not self.isPaused:
            self.drawGameOverScreen()





SuperHex().run()

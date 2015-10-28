# Term Project
# Anirudh Ramakrishnan
# Some ideas were made possible thanks to Yousof Soliman and Yeongwoo Hwang
###############################################

from __future__ import with_statement # for Python 2.5 and 2.6
from Tkinter import *
from eventBasedAnimationClass import EventBasedAnimationClass
from InvinciblePieceClass import InvinciblePiece
from PauseScreenClass import PauseScreen
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

#Game over screen
class GameOver(object):
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.writeScore = True
        self.customMode = False

    #taken from ntoes
    @staticmethod
    def readFile(filename, mode="rt"):
        # rt = "read text"
        with open(filename, mode) as fin:
            return fin.read()

    def checkIfHighScore(self,score):
        newList = []
        path = "tempDir" + os.sep + "SuperPolyagon.txt"
        contents = SplashScreen.readFile(path)
        tempList = contents.split()
        for element in tempList:
            newList.append(int(element))
        if score >= max(newList):
            return True
        return False
    
    def draw(self,splashInst,canvas,score,difficulty):
            SplashScreen.drawCenterHexagon(splashInst,canvas,True)
            SplashScreen.drawTitle(splashInst,canvas)
            text = dict()
            text["textOptions"] = ("Menu","Options","High Scores","Credits")
            (r,yShift) = (170,100)
            (scoreText,font) = ("Current run: "+ str(score) + " second(s)!", "Aerial 18")
            highScoreText = "NEW HIGH SCORE: " + str(score) + " second(s)!"
            #dictionary for coordinates
            (textD,cx,cy) = (dict(),self.width/2,self.height/2)
            textD["gameOver"] = [(cx,150),(cx-190,110,cx+190,190)]
            textD["score"] = [(cx,250),(cx-270,200,cx+270,300)]
            textD["square"] = (cx-100,cy,cx, cy - 150,cx+100,cy,cx,cy + 150)
            textD["newGame"] = (cx,cy-170)
            textD["menu"] = (cx+105,cy)
            textD["highScores"] = (cx-105,cy)
            textD["difficulty"] = (cx,cy+170)
            textD["highScore"] = (cx, 250)
            textD["winGame"] = (cx + 350, 150)
            SplashScreen.drawMenu(splashInst,canvas,text,r,yShift)
            self.drawOptions(canvas,scoreText,textD,highScoreText,font,
                difficulty,score,splashInst)

    def getDifficulty(self,difficulty):
        if difficulty == 0: 
            diffText = "     Easy"
        elif difficulty == 1: 
            diffText = "  Medium"
        elif difficulty == 2:
            diffText = "     Hard"
        elif difficulty == 3: 
            diffText = "  Custom"
        return diffText
    
    def drawOptions(self,canvas,text,textD,HSText,font,difficulty,score,splashInst):
        diffText = self.getDifficulty(difficulty)
        if splashInst.gameWon:
            canvas.create_text(textD["winGame"], text = "You win!!!!", 
                                                font = "Aerial 30 bold")
        canvas.create_oval(textD["gameOver"][1], fill = "misty rose")
        canvas.create_text(textD["gameOver"][0], text = "Game Over!", 
                                font = "Aerial 30 bold")
        canvas.create_oval(textD["score"][1], fill = "SeaGreen1")
        (d,r,yShift) = (dict(), 210,100)
        d["textOptions"] = ("New Game: \n   Press n.","  Menu:\n   Press m",
                "  High Scores: \n    Press h"," Current level: \n  " + diffText)        
        if not self.customMode:
            if not self.checkIfHighScore(score):
                canvas.create_text(textD["score"][0], text = text, 
                                                        font = "Aeiral 25 bold")
            if self.checkIfHighScore(score): canvas.create_text(textD["highScore"],
                                        text = HSText, font = "Aerial 20 bold")
        elif self.customMode:
            canvas.create_text(textD["score"][0], text = "No score: Custom Mode!",
                                                        font = "Aeiral 25 bold")

#splash Screen object (Menu, etc..)
class SplashScreen(object):
    def __init__(self,width,height):
        self.width = width
        self.height = height
        #self.colorList = ["turquoise", "SteelBlue1", "SteelBlue3","tan1", "salmon3"]
        self.innerRadius = 200 
        self.outerRadius = 450
        self.shift= 0 
        (self.options,self.controls,self.highScore,self.credits) = \
                                                    (False,False,False,False)
        self.splashScreen = True
        self.radiusShift = 0
        #Easy,medium, Hard, custom
        self.currentDifficulty = 0
        self.difficultyColor = "orange"
        self.titlFont = "fixedsys 50 bold"
        self.customMode = False
        self.customObs = 2
        self.customTime = 20
        (self.gameWon,self.customGameWon) = (False,False)

    #taken from ntoes
    @staticmethod
    def readFile(filename, mode="rt"):
        # rt = "read text"
        with open(filename, mode) as fin:
            return fin.read()

    #taken from notes
    @staticmethod
    def writeFile(filename, contents, mode="wt"):
        # wt = "write text"
        with open(filename, mode) as fout:
            fout.write(contents)

    #if the game is over, attempts to update the high score
    def updateScore(self,score,mode,gameWon):
        if gameWon:
            self.gameWon = self.customGameWon = True
        path = "tempDir" + os.sep + "SuperPolyagon.txt"
        s = SplashScreen.readFile(path)
        finalScore = str(score)
        contents = s + " " + finalScore
        SplashScreen.writeFile(path,contents)

    def rotateSplashBackground(self,time):
        if time % 1 == 0:
            self.shift += math.pi/50

    def draw(self,canvas):
        centerHex = False
        if self.options:
            self.drawCenterHexagon(canvas,centerHex)
            self.drawOptionsMenu(canvas)
        elif self.controls:
            self.drawCenterHexagon(canvas,centerHex)
            self.drawControlsMenu(canvas)
        elif self.highScore:
            self.drawCenterHexagon(canvas,centerHex)
            self.drawHighScoreMenu(canvas)
        elif self.credits:
            self.drawCenterHexagon(canvas,centerHex)
            color = "SlateBlue2"
            self.drawMainHexagon(canvas,color)
            self.drawCreditsMenu(canvas)
        else: self.splashScreenDraw(canvas)

    def splashScreenDraw(self,canvas):
        if self.splashScreen:
            centerHex = True
            self.drawCenterHexagon(canvas,centerHex)
            self.drawTitle(canvas)
            text = dict()
            text["textOptions"] = ("Controls","Options","High Scores","Credits")
            (r,yShift) = (170,100)
            self.drawMenu(canvas,text,r,yShift)

    def drawMainHexagon(self,canvas,color):
        d = dict()
        (shift,left,right,x,y,r) = (0,4,5,self.width/2,self.height/2,330)
        d["polygon"] = (x + r*math.cos(2*math.pi/3 + shift),
                        (y- r*math.sin(2*math.pi/3 + shift)),
                        (x + r*math.cos(math.pi/3 + shift)),
                        (y- r*math.sin(math.pi/3 + shift)),
                        (x + r*math.cos(shift)),
                        (y - r*math.sin(shift)),
                        (x + r*math.cos(right*math.pi/3 + shift)),
                        (y- r*math.sin(right*math.pi/3 + shift)),
                        (x + r*math.cos(left*math.pi/3 + shift)),
                        (y- r*math.sin(left*math.pi/3 + shift)),
                        (x + r*math.cos(math.pi + shift)),
                        (y- r*math.sin(math.pi + shift)))
        canvas.create_polygon(d["polygon"],fill = color, width = 3, 
                                    outline = "black")

    def drawControlsMenu(self,canvas):
        d = dict()
        d["title"] = (self.width/2,55)
        d["text"] = [(500,285),(500,380),(500,455),(500,515),(500,595),
                                                (500,665),(500,725)]
        self.controlDrawer(canvas,d)

    def controlDrawer(self,canvas,d):
        canvas.create_text(d["title"], text = "Super Polya-gon", 
                                        font = "fixedsys 50 bold")
        color = "hotpink1"
        self.drawMainHexagon(canvas,color)
        self.drawNextControls(canvas,d)

    def drawNextControls(self,canvas,d):
        canvas.create_text(d["text"][0],text = "Game directions", 
                                            font = "Aerial 30 bold underline")
        canvas.create_text(d["text"][1],text ="Try and dodge the obstacles\n" + 
                                "for as long as you can",font = "Aerial 20")
        canvas.create_text(d["text"][2],text="Use left/right arrow keys to move"
                                            ,font = "Aerial 20")
        canvas.create_text(d["text"][3], text = "Press P to pause game", 
                                             font = "Aerial 20")
        canvas.create_text(d["text"][4], text = "The circular power-ups grant\n invincibility for 3 seconds", 
                                             font = "Aerial 20")
        canvas.create_text(d["text"][5], text = "Press Q to quit in-game",
                                            font = "Aerial 20")
        canvas.create_text(d["text"][6], text = "Press R to restart in-game",
                                            font = "Aerial 20")
        self.backToMenu(canvas)

    def getHighScoreText(self):
        newList = []
        path = "tempDir" + os.sep + "SuperPolyagon.txt"
        contents = SplashScreen.readFile(path)
        #sorting in terms of highest scores        
        tempList = contents.split()
        for element in tempList:
            newList.append(int(element))
        sortList = sorted(newList)
        #reverses
        reversedList = sortList[::-1]
        return reversedList[:10]

    def drawHighScoreMenu(self,canvas):
        (r,shift,x,y) = (250,0,self.width/2,self.height/2-150)
        d = dict()
        d["title"] = (self.width/2, 55)
        color,color1 =  "pink1", "white"
        d["polyCoords"] = (x-120,y-150,x+120,y-150,x+200,y-50,x+100,y+75,x-120,
                                                            y+75,x-200,y-50)
        d["text"] = (x,(y-75))
        d["bottom"] = (x-200,y-50,x-120,y+75,x-120,y+475,x-200,y+400)
        d["left"] = (x-120,y+75,x+100,y+475)
        d["right"] = (x+100,y+75,x+200,y-50,x+200,y +350,x+100,y+475)
        self.drawNextHSMenu(canvas,d,color,color1)
    
    def drawNextHSMenu(self,canvas,d,color,color1):
        canvas.create_text(d["title"],text ="Super Polya-gon",font=self.titlFont)
        canvas.create_polygon(d["polyCoords"],fill = color, width = 3,
                                                        outline = color1)
        canvas.create_text(d["text"], text = "High Scores", 
                                            font = "Aerial 30 bold underline")
        canvas.create_polygon(d["bottom"], fill = color, outline = color1)
        canvas.create_rectangle(d["left"], fill = color, outline = color1)
        canvas.create_polygon(d["right"],fill = color,outline = color1)
        highScoreText = self.getHighScoreText()
        self.drawHighScores(canvas,highScoreText)
        self.backToMenu(canvas)

    def drawHighScores(self,canvas,highScoreText):
        height = 450
        for i in xrange(len(highScoreText)):
            scoreText = str(highScoreText[i])
            canvas.create_text(self.width/2,height, text = scoreText, font = "Aeiral 20 bold")
            height += 40
        height = 450
        for i in xrange(len(highScoreText)):
            scoreText = str((i+1)) + ". "
            canvas.create_text(self.width/2-40,height,text = scoreText, font = "Aerial 20 bold")
            height +=40

    def getCurrDiff(self):
        if self.currentDifficulty == 0:
            currDiff = "Easy"
        elif self.currentDifficulty == 1:
            currDiff = "Kinda not easy"
        elif self.currentDifficulty == 2:
            currDiff = "Definitely not easy"
        return currDiff

    def getCurrTime(self):
        if self.customTime == 20:
            currTime = 20
        elif self.customTime == 30:
            currTime = 30
        elif self.customTime == 60:
            currTime = 60
        return currTime

    def getCurrObs(self):
        if self.customObs == 2:
            currObs = 2
        elif self.customObs == 4:
            currObs = 4
        elif self.customObs == 10:
            currObs = 10
        return currObs

    def drawOptionsMenu(self,canvas):
        (d,font,currDiff) = (dict(), "Aerial 13 bold", self.getCurrDiff())
        (d["title"], d["eCoordinates"])=((500,55),[(300,175,500,250),(400,213)])
        d["textDiff"],d["mCoordinates"]= (150,200),[(300,275,500,350),(400,313)]
        d["hCoordinates"] = [(300,375,500,450),(400,413)]
        d["currDifCord"] =[(50,250,250,350),(150,300)]
        canvas.create_text(d["title"],text="Super Polya-gon",font=self.titlFont)
        canvas.create_text(d["textDiff"],text = "Difficulty: ", 
                                                    font = "Aerial 20 bold")
        canvas.create_rectangle(d["eCoordinates"][0], fill = "VioletRed1")
        canvas.create_text(d["eCoordinates"][1],text = "Easy", font = font)
        canvas.create_rectangle(d["mCoordinates"][0], fill = "IndianRed1")
        canvas.create_text(d["mCoordinates"][1], text = "Kinda not easy",
                                                                font = font)
        canvas.create_rectangle(d["hCoordinates"][0], fill = "SlateBlue1")
        canvas.create_text(d["hCoordinates"][1], text = "Definitely not easy", 
                                                    font = font)
        canvas.create_rectangle(d["currDifCord"][0], fill = "wheat1")
        canvas.create_text(d["currDifCord"][1], text = currDiff, font = font)
        self.backToMenu(canvas)
        self.drawLevelGenMenu(canvas)

    def drawLevelGenMenu(self,canvas):
        d = dict()
        d["levTitle"] = (170,500)
        d["createLevCoord"] = (100,550,225,850)
        d["options"] = [(162,600),(170,700),(162,800)]
        d["timeTextCord"] = [(300,600),(450,600),(600,600)]
        d["timeRect"] = [(250,575,350,625),(400,575,500,625),(550,575,650,625)]
        d["timeText"] = ["20 seconds","30 seconds","1 minute"]
        d["obsRect"] = [(250,675,350,725),(400,675,500,725),(550,675,650,725)]
        d["obsTextCoord"] = [(300,700),(450,700),(600,700)]
        d["obsText"] = ["2 obstacles","4 obstacles","10 obstacles"]
        d["speedRect"] = [(250,775,350,825),(400,775,500,825),(550,775,650,825)]
        d["speedTextCoord"] = [(300,800),(450,800),(600,800)]
        d["speedText"] = ["Easy","Medium","Hard"]
        d["customRect"] = (350,475,600,565)
        d["customText"] = (475,520)
        self.drawLevelGenMain(canvas,d)
        self.drawTimeOptions(d,canvas)

    def drawLevelGenMain(self,canvas,d):
        (currDiff,currTime) = (self.getCurrDiff(),self.getCurrTime()) 
        currObs = self.getCurrObs()
        modeText = "On" if self.customMode else "Off"
        canvas.create_rectangle(d["customRect"], fill = "")
        canvas.create_text(d["customText"], 
            text = "Click for custom\nCustom Mode: " + modeText,
                                                        font = "Aerial 15")
        canvas.create_text(d["levTitle"],text = "Create your own level:",
                                        font = "Aerial 16 bold")
        canvas.create_rectangle(d["createLevCoord"],fill = "white")
        canvas.create_text(d["options"][0],text = "Amount of\n    time: ", 
                                                    font = "Aerial 12 bold")
        canvas.create_text(d["options"][1],
            text = "Number of \nhard \nobstacles: ", font = "Aerial 12 bold")
        canvas.create_text(d["options"][2],text = "Speed of\n obstacles: ", 
                                                    font = "Aerial 12 bold")
        canvas.create_text((162,830), text = currDiff, font = "Aerial 10", 
                                                            fill = "red")
        canvas.create_text((162,650), text = currTime, font = "Aerial 10", 
                                                            fill = "red")
        canvas.create_text((162,750), text = currObs, font = "Aerial 10", 
                                                            fill = "red")
    
    def drawTimeOptions(self,d,canvas):
        #20 seconds button
        #30 seconds button
        #1 minute button
        for i in xrange(3):
            canvas.create_rectangle(d["timeRect"][i], fill = "white")            
            canvas.create_text(d["timeTextCord"][i],text = d["timeText"][i], 
                                                    font = "Aeiral 11")
        #obstacle buttons
        for j in xrange(3):
            canvas.create_rectangle(d["obsRect"][j], fill = "white")            
            canvas.create_text(d["obsTextCoord"][j],text = d["obsText"][j],
                                                        font = "Aeiral 11")
        #speed buttons
        for k in xrange(3):
            canvas.create_rectangle(d["speedRect"][k], fill = "white")            
            canvas.create_text(d["speedTextCoord"][k],text = d["speedText"][k],
                                                            font = "Aeiral 11")

    def drawCreditsMenu(self,canvas):
        canvas.create_text(self.width/2, 55, text = "Super Polyagon", 
                    font = "fixedsys 50 bold")
        canvas.create_text(500,250,text = "Credits", 
                                            font = "Aerial 30 bold underline")
        canvas.create_text(500,340, text = "Developed by: \n\tAni Ramakrishnan",
                                                font = "Aerial 20")
        canvas.create_text(380, 500, text = "Inspired by: \n", font = "Aerial 20")
        canvas.create_text(550,540,text = "Terry Cavanagh's Super Hexagon",
                                    font = "Aerial 20")         
        canvas.create_text(600,700, text = "Free version", font = "Aerial 12")
        self.backToMenu(canvas)

    def backToMenu(self,canvas):
        d = dict()
        d["backCoords"] = ((700,700,900,800),(800,750))
        canvas.create_oval(d["backCoords"][0], fill = "turquoise")
        canvas.create_text(d["backCoords"][1], text = "Back to menu", 
                            font = "Aerial 15 bold")

    def drawMenu(self,canvas,text,r,yShift):
        #controls rectangular button
        shift= self.radiusShift
        (cx,cy) = self.width/2,self.height/2
        (left,right) = (7,11)
        (x2,y2) = (cx + r*math.cos(5*math.pi/6 + shift),
                    (cy- r*math.sin(5*math.pi/6 + shift)))
        (x1,y1) = (x2 - r, y2 - yShift)
        canvas.create_oval(x1,y1,x2,y2, fill = "violet")
        canvas.create_text((x1+x2)/2,(y1+y2)/2, text = text["textOptions"][0], 
                                                    font = "Aerial 17 bold")
        #options button
        (x1,y1) = ((cx + r*math.cos(math.pi/6 + shift)),
                    (cy- r*math.sin(math.pi/6 + shift))-yShift)
        (x2,y2) = (x1+r,y1 + yShift)
        canvas.create_oval(x1,y1,x2,y2,fill = "tan1")
        canvas.create_text((x1+x2)/2,(y1+y2)/2, text = text["textOptions"][1], 
                                                        font = "Aerial 17 bold")
        self.drawNextMenu(canvas,shift,cx,cy,r,left,right,yShift,text)

    def drawNextMenu(self,canvas,shift,cx,cy,r,left,right,yShift,text):
        (scaleX,scaleY) = (110,75)
        #highscore  button
        (x2,y2) = (cx + r*math.cos(left*math.pi/6 + shift),
                    (cy- r*math.sin(left*math.pi/6 + shift)) +yShift)
        (x1,y1) = (x2 - r, y2 - yShift)
        canvas.create_oval(x1,y1,x2,y2,fill = "salmon3")
        canvas.create_text((x1+x2)/2,(y1+y2)/2, text = text["textOptions"][2], 
                                                    font = "Aerial 17 bold")
        # credits button
        (x1,y1) = (cx + r*math.cos(right*math.pi/6 + shift),
                    (cy- r*math.sin(right*math.pi/6 + shift)))
        (x2,y2) = (x1 + r, y1 + yShift)
        canvas.create_oval(x1,y1,x2,y2,fill = "turquoise")
        canvas.create_text((x1+x2)/2,(y1+y2)/2, text = text["textOptions"][3], 
                                                    font = "Aerial 17 bold")
        canvas.create_text(cx,cy,text = "Start", font = "Aerial 50 bold")

    def drawCenterHexagon(self,canvas,centerHex):
        (r,shift,x,y) = (self.innerRadius,self.shift,self.width/2,self.height/2)
        (left,right,hexNum,rDec) = (4,5,6,50)
        for i in xrange(hexNum):
            if i == 0 and centerHex: (shift,color) = (0,"light goldenrod")
            else: (shift,color) = (self.shift,"")
            (x1,y1) = (x + r*math.cos(2*math.pi/3 + shift),
                        (y- r*math.sin(2*math.pi/3 + shift)))
            (x2,y2) = (x + r*math.cos(math.pi/3 + shift),
                        (y- r*math.sin(math.pi/3 + shift)))
            (x3,y3) = (x + r*math.cos(shift),y - r*math.sin(shift))
            (x4,y4) = (x + r*math.cos(right*math.pi/3 + shift),
                        (y- r*math.sin(right*math.pi/3 + shift)))
            (x5,y5) = (x + r*math.cos(left*math.pi/3 + shift),
                        (y- r*math.sin(left*math.pi/3 + shift)))
            (x6,y6) = (x + r*math.cos(math.pi + shift),
                        (y- r*math.sin(math.pi + shift)))
            canvas.create_polygon(x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6, 
                                    fill = color, width = 3, outline = "black")
            r += rDec

    def drawTitle(self,canvas):
        canvas.create_text(self.width/2, 70, text = "Super Polya-gon", 
                    font = self.titlFont)
    
    #These methods check if the user clicks on a menu option
    #Takes in x and y coordinates, returns T/F depending on location of click

    @staticmethod
    def easyDiffClicked(x,y):
        d = dict()
        d["eCoordinates"] = [(300,175,500,250),(400,213)]
        if ((x > d["eCoordinates"][0][0]) and (x < d["eCoordinates"][0][2]) and
            (y > d["eCoordinates"][0][1]) and (y < d["eCoordinates"][0][3])):
            return True
        return False

    @staticmethod
    def medDiffClicked(x,y):
        d = dict()        
        d["mCoordinates"] = [(300,275,500,350),(400,313)]
        if ((x> d["mCoordinates"][0][0]) and (x < d["mCoordinates"][0][2]) and 
            (y > d["mCoordinates"][0][1]) and (y < d["mCoordinates"][0][3])):
            return True
        return False

    @staticmethod
    def hardDiffClicked(x,y):
        d = dict()
        d["hCoordinates"] = [(300,375,500,450),(400,413)]
        if ((x > d["hCoordinates"][0][0]) and (x < d["hCoordinates"][0][2]) and
            (y > d["hCoordinates"][0][1]) and (y < d["hCoordinates"][0][3])):
            return True
        return False

    @staticmethod
    def easySpeedClicked(x,y):
        d = dict()
        d["speedRect"] = (250,775,350,825)
        if ((x > d["speedRect"][0]) and (x < d["speedRect"][2]) and
            (y > d["speedRect"][1]) and (y < d["speedRect"][3])):
            return True
        return False   
    
    @staticmethod
    def medSpeedClicked(x,y):
        d = dict()
        d["speedRect"] = (400,775,500,825)
        if ((x > d["speedRect"][0]) and (x < d["speedRect"][2]) and
            (y > d["speedRect"][1]) and (y < d["speedRect"][3])):
            return True
        return False 

    @staticmethod
    def hardSpeedClicked(x,y):
        d = dict()
        d["speedRect"] = (550,775,650,825)
        if ((x > d["speedRect"][0]) and (x < d["speedRect"][2]) and
            (y > d["speedRect"][1]) and (y < d["speedRect"][3])):
            return True
        return False 
    
    @staticmethod
    def customModeClicked(x,y):
        d = dict()
        d["customRect"] = (350,475,600,565)
        if ((x > d["customRect"][0]) and (x < d["customRect"][2]) and
            (y > d["customRect"][1]) and (y < d["customRect"][3])):
            return True
        return False 

    @staticmethod 
    def twoObsClicked(x,y):
        d = dict()
        d["speedRect"] = (250,675,350,725)
        if ((x > d["speedRect"][0]) and (x < d["speedRect"][2]) and
            (y > d["speedRect"][1]) and (y < d["speedRect"][3])):
            return True
        return False 

    @staticmethod
    def fourObsClicked(x,y):
        d = dict()
        d["speedRect"] = (400,675,500,725)
        if ((x > d["speedRect"][0]) and (x < d["speedRect"][2]) and
            (y > d["speedRect"][1]) and (y < d["speedRect"][3])):
            return True
        return False 

    @staticmethod
    def sixObsClicked(x,y):
        d = dict()
        d["speedRect"] = (550,675,650,725)
        if ((x > d["speedRect"][0]) and (x < d["speedRect"][2]) and
            (y > d["speedRect"][1]) and (y < d["speedRect"][3])):
            return True
        return False

    @staticmethod
    def twentyTimeClicked(x,y):
        d = dict()
        d["speedRect"] = (250,575,350,625)
        if ((x > d["speedRect"][0]) and (x < d["speedRect"][2]) and
            (y > d["speedRect"][1]) and (y < d["speedRect"][3])):
            return True
        return False

    @staticmethod
    def thirtyTimeClicked(x,y):
        d = dict()
        d["speedRect"] = (400,575,500,625)
        if ((x > d["speedRect"][0]) and (x < d["speedRect"][2]) and
            (y > d["speedRect"][1]) and (y < d["speedRect"][3])):
            return True
        return False

    @staticmethod
    def minuteTimeClicked(x,y):
        d = dict()
        d["speedRect"] = (550,575,650,625)
        if ((x > d["speedRect"][0]) and (x < d["speedRect"][2]) and
            (y > d["speedRect"][1]) and (y < d["speedRect"][3])):
            return True
        return False

    @staticmethod
    def backButtonClicked(x,y):
        d = dict()
        d["backCoords"] = (700,700,900,800)
        if ((x > d["backCoords"][0]) and (x < d["backCoords"][2]) and
            (y > d["backCoords"][1]) and (y < d["backCoords"][3])):
            return True
        return False   
    
    @staticmethod
    def startClicked(x,y):
        d = dict()
        d["sCoordinates"] = (350,236,650,673)
        if ((x > d["sCoordinates"][0]) and (x < d["sCoordinates"][2]) and
            (y > d["sCoordinates"][1]) and (y < d["sCoordinates"][3])):
            return True
        return False        

    @staticmethod
    def optionsClicked(x,y):
        d = dict()
        d["dimensions"] = (638, 320, 798, 420)
        if ((x > d["dimensions"][0]) and (x < d["dimensions"][2]) and 
            (y > d["dimensions"][1]) and (y < d["dimensions"][3])):
            return True
        return False

    @staticmethod
    def highScoreClicked(x,y):
        d = dict()
        d["dimensions"] =  (201, 580, 361, 680)
        if ((x > d["dimensions"][0]) and (x < d["dimensions"][2]) and 
            (y > d["dimensions"][1]) and (y < d["dimensions"][3])):
            return True
        return False

    @staticmethod
    def creditsClicked(x,y):
        d = dict()
        d["dimensions"] = (638, 580, 798, 680)
        if ((x > d["dimensions"][0]) and (x < d["dimensions"][2]) and 
            (y > d["dimensions"][1]) and (y < d["dimensions"][3])):
            return True
        return False

    @staticmethod
    def controlsClicked(x,y):
        #the dimensions of the control box
        d = dict()
        d["dimensions"] = (201, 320, 361, 420)
        if ((x > d["dimensions"][0]) and (x < d["dimensions"][2]) and 
            (y > d["dimensions"][1]) and (y < d["dimensions"][3])):
            return True
        return False

#class for all the different background types
class Background(object):
    #pulse
    #Must be unique
    def choosePulseColor(self):
        backColors = (["navy","mint cream","dark orchid","MediumPurple4",
                                "firebrick","gold4","black","black"])
        pulseColorsList = (["DodgerBlue4","lavender","medium orchid",
                            "MediumPurple3","brown3","gold3","black","black"])
        colorComboIndex = backColors.index(self.backColor)
        pentagonList = (["DodgerBlue3","alice blue", "orchid", "MediumPurple2",
                         "brown2","gold2","black","black"])
        return (pulseColorsList[colorComboIndex], pentagonList[colorComboIndex])

    def __init__(self,width,height,backgroundColor):
        self.width = width
        self.height = height
        self.backColor = backgroundColor
        self.pulseBackground = True
        self.pulseColor,self.pentagonColor =  self.choosePulseColor()
        self.spinDirection = True
        self.shift = 0

    def drawPulseBackground(self,canvas,w,h,type):
        if type == "Hexagon":
            self.drawHexagonBackground(canvas,w,h)
        elif type == "Pentagon":
            self.drawPentagonBackground(canvas,w,h)
        elif type == "Square":
            self.drawSquareBackground(canvas,w,h)

    def drawHexagonBackground(self,canvas,w,h):
        (pi,r,cx,cy,angle) = (math.pi,800,w/2,h/2,3)
        drawPulse = self.pulseBackground
        spinDir = self.spinDirection
        shift = self.shift
        for i in xrange(angle):
            (lx,ly) = (cx + r*math.cos(2*i*pi/angle + shift), 
                        (cy - r*math.sin(2*i*pi/angle + shift)))
            (rx,ry) = (cx + r*math.cos((1+2*i)*pi/angle + shift),
                        (cy - r*math.sin((1+2*i)*pi/angle + shift)))
            canvas.create_polygon(lx,ly,rx,ry,cx,cy, fill = self.pulseColor)

    def drawPentagonBackground(self,canvas,w,h):
        (pi,r,cx,cy,angle) = (math.pi,800,w/2,h/2,3)
        (cos,sin) = (math.cos,math.sin)
        drawPulse = self.pulseBackground
        spinDir = self.spinDirection
        shift = self.shift
        (scale, mult) = (10,8)
        for i in xrange(3):
            (lx,ly) = (cx + r*cos(pi/2 - mult*i*pi/scale +shift), cy - r*sin(pi/2 - mult*i*pi/scale + shift))
            (rx,ry) = (cx + r*cos(pi/scale - mult*i*pi/scale + shift), cy-r*sin(pi/scale- mult*i*pi/scale + shift))
            color = self.pulseColor if i < 2 else self.pentagonColor
            canvas.create_polygon(lx,ly,rx,ry,cx,cy, fill = color)

    def drawSquareBackground(self,canvas,w,h):
        (r,cx,cy) = (800,w/2,h/2)
        (pi,sin,cos) = (math.pi,math.sin,math.cos)
        shift = self.shift
        for i in xrange(2):
            (lx,ly) = (cx + r*cos(pi/4 + i*pi + shift), cy - r*sin(pi/4 + i*pi+ shift))
            (rx,ry) = (cx + r*cos(-pi/4+ i*pi + shift), cy-r*sin(-pi/4 + i*pi +shift))
            canvas.create_polygon(lx,ly,rx,ry,cx,cy, fill = self.pulseColor)

#the center triangle that the user controls
class Character(object):

    def chooseCharColor(self):
        backColors = ["navy","mint cream","dark orchid","MediumPurple4","firebrick","gold4","black","black"]
        colorList = ["deep sky blue","magenta","deep pink","MediumPurple1","orange red","yellow2","hot pink","green"]
        colorComboIndex = backColors.index(self.backColor)
        return colorList[colorComboIndex]

    def __init__(self,width,height,backgroundColor):
        self.charAngle = math.pi/2
        self.radius = 75
        self.backColor = backgroundColor
        self.width = width
        self.height = height
        self.updateCharCoords()
        self.color = self.chooseCharColor()

    def getCharAngle(self,angle):
        sign = 0
        pi = math.pi
        #ensures the angle is positive
        if angle < 0:
            posAngle = 2.0*pi - abs(angle)
        else: posAngle = angle
        moddedAngle = posAngle % (2.0*pi)
        return moddedAngle

    def getCharHexagonCoords(self):
        (edgeLen, angleLen,hght) = (15,16,4)
        margin = self.radius / edgeLen
        edgeRadius = self.radius + margin
        charHeight = self.radius / hght
        cX,cY = self.width/2, self.height/2
        #gets coordinates of top vertex of triangle
        (tX,tY) = ((cX + (edgeRadius + charHeight)*math.cos(self.charAngle)), 
                    ((cY - (edgeRadius + charHeight)*math.sin(self.charAngle))))
        #gets coordinates of left vertex of triangle
        leftAngle = self.charAngle + math.pi/angleLen
        (lX,lY) = ((cX + edgeRadius*math.cos(leftAngle)), 
                    ((cY - edgeRadius*math.sin(leftAngle))))
        #right vertex
        rightAngle = self.charAngle - math.pi/angleLen
        (rX,rY) = ((cX + edgeRadius*math.cos(rightAngle)), 
                    ((cY - edgeRadius*math.sin(rightAngle))))
        return (tX,tY,rX,rY,lX,lY)

    def updateCharCoords(self):
        (self.tX,self.tY,self.rX,self.rY,self.lX,self.lY) = \
                                            (self.getCharHexagonCoords())
    def drawCharacter(self,canvas):
        canvas.create_polygon(self.tX,self.tY,self.lX,self.lY,self.rX,self.rY, fill = self.color)

#center polygon
class BasePolygon(object):

    #gets color of center hexagon with respect to background color
    def choosePulseColor(self):
        backColors = ["navy","mint cream","dark orchid","MediumPurple4","firebrick","gold4","black","black"]
        centBaseList = \
        ["deep sky blue","magenta","deep pink","MediumPurple1","orange red","yellow2","hot pink","green"]
        colorComboIndex = backColors.index(self.backgroundColor)
        return (centBaseList[colorComboIndex])

    def __init__(self,backgroundColor):
        self.backgroundColor = backgroundColor
        self.baseColor = self.choosePulseColor()
        self.baseTypeList = ["Hexagon","Pentagon","Square"] #"Pentagon",
        self.baseType = "Hexagon"
        self.pulseBase = True
        self.shift = 0
        self.radius = 75

    def drawBasePolygon(self,canvas,x,y):
        if self.baseType == "Pentagon":
            self.drawBasePentagon(canvas,x,y)
        elif self.baseType == "Hexagon":
            self.drawBaseHex(canvas,x,y)
        elif self.baseType == "Square":
            self.drawBaseSquare(canvas,x,y)

    def drawBaseHex(self,canvas,x,y):
        pulse = self.pulseBase
        shift = self.shift
        r = self.radius
        if pulse: 
            radiusInc = random.choice([2,4,6,8,10])
            r -= radiusInc
        else: r += radiusInc
        (left,right) = (4,5)
        (x1,y1) = (x + r*math.cos(2*math.pi/3 + shift),
                    (y- r*math.sin(2*math.pi/3 + shift)))
        (x2,y2) = (x + r*math.cos(math.pi/3 + shift),
                    (y- r*math.sin(math.pi/3 + shift)))
        (x3,y3) = (x + r*math.cos(shift),y - r*math.sin(shift))
        (x4,y4) = (x + r*math.cos(right*math.pi/3 + shift),
                    (y- r*math.sin(right*math.pi/3 + shift)))
        (x5,y5) = (x + r*math.cos(left*math.pi/3 + shift),
                    (y- r*math.sin(left*math.pi/3 + shift)))
        (x6,y6) = (x + r*math.cos(math.pi + shift),
                    (y- r*math.sin(math.pi + shift)))
        canvas.create_polygon(x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6, fill = "", 
                                    width = 3, outline = self.baseColor)
    
    def drawBasePentagon(self,canvas,x,y):
        pulse = self.pulseBase
        shift = self.shift
        r = self.radius
        (pi,cos,sin) = (math.pi,math.cos,math.sin)
        if pulse: 
            radiusInc = random.choice([2,4,6,8,10])
            r -= radiusInc
        else: r += radiusInc
        (scndPt,scale,thrdPt,fthPt) = (9,10,13,17)
        (x1,y1) = (x+r*cos(pi/2 + shift), y- r*sin(pi/2 + shift))
        (x2,y2) = (x+r*cos(pi/scale + shift), y- r*sin(pi/scale + shift))
        (x3,y3) = (x+r*cos(fthPt*pi/scale +shift), y- r*sin(fthPt*pi/scale + shift))
        (x4,y4) = (x+r*cos(thrdPt*pi/scale + shift), y- r*sin(thrdPt*pi/scale+ shift))
        (x5,y5) = (x+r*cos(scndPt*pi/scale + shift), y- r*sin(scndPt*pi/scale + shift))
        canvas.create_polygon(x1,y1,x2,y2,x3,y3,x4,y4,x5,y5, fill = "", width = 3, outline = self.baseColor)

    def drawBaseSquare(self,canvas,x,y):
        pulse = self.pulseBase
        shift = self.shift
        r = self.radius
        (pi,cos,sin) = (math.pi,math.cos,math.sin)
        if pulse: 
            radiusInc = random.choice([2,4,6,8,10])
            r -= radiusInc
        else: r += radiusInc
        (x1,y1) = (x + r*cos(3*pi/4 +shift), y- r*sin(3*pi/4 + shift))
        (x2,y2) = (x + r*cos(pi/4 +shift), y- r*sin(pi/4 + shift))
        (x3,y3) = (x + r*cos(7*pi/4 +shift), y- r*sin(7*pi/4 + shift))
        (x4,y4) = (x + r*cos(5*pi/4 +shift), y- r*sin(5*pi/4 + shift))
        canvas.create_polygon(x1,y1,x2,y2,x3,y3,x4,y4, fill = "", width = 3, outline = self.baseColor)

    def drawBaseSketchShape(self,canvas,x,y):
        pulse = self.pulseBase
        shift = self.shift
        r = self.radius
        (pi,cos,sin) = (math.pi,math.cos,math.sin)
        if pulse: 
            radiusInc = random.choice([2,4,6,8,10])
            r -= radiusInc
        else: r += radiusInc
        (x1,y1) = (x + r*cos(pi/4 +shift), y- r*sin(pi/4 + shift))
        (x2,y2) = (x + r*cos(7*pi/4 +shift), y- r*sin(7*pi/4 + shift))
        (x3,y3) = (x + r*cos(5*pi/4 +shift), y- r*sin(5*pi/4 + shift))
        (x4,y4) = (x + r*cos(3*pi/4 +shift), y- r*sin(3*pi/4 + shift))
        canvas.create_polygon(x1,y1,x2,y2,x3,x3,x4,x4, fill = "", width = 3, outline = self.baseColor)

#Class for different types of obstacles
class Obstacles(object):

    #chooses obstacle color according to the background color
    def chooseObstacleColor(self):
        backgroundList = ["navy","mint cream","dark orchid","MediumPurple4",
                                    "firebrick","gold4","black","black"]
        index = backgroundList.index(self.backColor)
        colorList = ["deep sky blue","magenta","deep pink","MediumPurple1",
                                "orange red","yellow2","hot pink","green"]
        return colorList[index]
    
    def __init__(self,x,y,numSides,sideType,backgroundColor,rotationDir,oType,angle,radius = 500):
        self.width = x
        self.height = y
        pi = math.pi
        #pentagon,hexagon,square,whirlpool,multiC,Square Zig,Pent Whirlpool,Stairs
        self.obstacleType = oType
        #number of sides
        self.numOfSides = numSides
        self.backColor = backgroundColor
        #the list of sides to draw
        self.sideList = sideType
        self.initialAngle = angle
        self.initialRadius = radius
        self.color = self.chooseObstacleColor()
        self.angleSides = []
        #True is counterclockwise, False clockwise
        self.obsRotDir = rotationDir

    @staticmethod
    def chooseSquareSides(numOfSides):
        sideList = []
        while len(sideList) < numOfSides:
            number = random.randint(0,3)
            if number not in sideList:
                sideList.append(number)
        return sideList

    @staticmethod
    #randomly selects sides and adds to list
    def chooseHexSides(numOfSides):
        sideList = []
        previousNumber = -5
        if numOfSides == 2:
            return random.choice([[0,3],[1,4],[2,5]])
        #loops through how many ever sides in the obstacle type
        while len(sideList) < numOfSides:
            number = random.randint(0,5)
            if ((number not in sideList and number > previousNumber +1) or 
                    (number < previousNumber -1)):
                sideList.append(number)
                previousNumber = number
        return sideList

    @staticmethod
    def choosePentSides(numOfSides):
        sideList = []
        while len(sideList) < numOfSides:
            number = random.randint(0,4)
            if number not in sideList:
                sideList.append(number)
        return sideList

    def draw(self,canvas,baseType,pieceType):
        (cx,cy) = (self.width/2, self.height/2)
        (pi,cos,sin) = (math.pi,math.cos,math.sin)
        (angle, r) = (self.initialAngle,self.initialRadius)
        if pieceType == "Whirlpool" and baseType == "Hexagon":
            sides = 6
            self.drawWhirpool(canvas,cx,cy,r,angle,sides)
        elif pieceType == "Stairs" and baseType == "Hexagon":
            sides = 6
            self.drawStairObstacle(canvas,cx,cy,r,angle,sides)
        elif pieceType == "MultiC" and baseType == "Hexagon":
            sides = 6
            self.drawMultiC(canvas,cx,cy,r,angle,sides)
        elif baseType == "Hexagon":
            sides = 6
            self.drawPiece(canvas,cx,cy,r,angle,sides)
        elif pieceType == "Pent Whirlpool" and baseType == "Pentagon":
            sides = 5
            self.drawPiece(canvas,cx,cy,r,angle,sides)
        elif baseType == "Pentagon":
            sides= 5
            self.drawPiece(canvas,cx,cy,r,angle,sides)
        elif pieceType == "Square Zig" and baseType == "Square":
            sides = 4
            self.drawPiece(canvas,cx,cy,r,angle,sides)
        elif baseType == "Square":
            sides = 4
            self.drawPiece(canvas,cx,cy,r,angle,sides)

    def drawMultiC(self,canvas,cx,cy,r,angle,sides):
        for i in xrange(sides):
            if i in self.sideList:
                self.drawSide(canvas,cx,cy,r,angle,i,sides)

    def drawStairObstacle(self,canvas,cx,cy,r,angle,sides):
        for i in xrange(sides):
            if i in self.sideList:
                self.drawSide(canvas,cx,cy,r,angle,i,sides)

    def drawPiece(self,canvas,cx,cy,r,angle,sides):
        for i in xrange(sides):
            if i in self.sideList:
                self.drawSide(canvas,cx,cy,r,angle,i,sides)

    def drawSide(self,canvas,cx,cy,r,angle,i,sides):
        (pi,sin,cos) = (math.pi,math.sin,math.cos)
        mag = .8
        topLeftX,topLeftY = ((cx + r*cos(angle + pi/sides + 2*i*pi/sides)),
                            (cy - r*sin(angle+pi/sides + 2*i*pi/sides)))
        topRightX,topRightY = ((cx + r*cos(angle - pi/sides + 2*i*pi/sides)), 
                                (cy - r*sin(angle - pi/sides+2*i*pi/sides)))
        #the bottom two points are at a shrunk radius
        botLeftX,botLeftY = ((cx + r*cos(angle + pi/sides + 2*i*pi/sides)*mag), 
                            (cy - r*sin(angle+  pi/sides + 2*i*pi/sides)*mag))
        botRightX,botRightY = ((cx + r*cos(angle - pi/sides + 2*i*pi/sides)*mag),
                                (cy-r*sin(angle-pi/sides+2*i*pi/sides)*mag))
        canvas.create_polygon(topLeftX,topLeftY,topRightX,topRightY,
                                        botRightX,botRightY,botLeftX,botLeftY,fill = self.color)

    def getAngleInt(self,angle,sideList):
        angleInterval = []
        if ((self.obstacleType == "Hexagon") or 
            (self.obstacleType == "Whirlpool") or(self.obstacleType == "Stairs")
             or (self.obstacleType == "MultiC")):
            sides = 6
        elif ((self.obstacleType == "Pentagon") or 
            (self.obstacleType == "Pent Whirlpool")):
            sides = 5
        elif self.obstacleType == "Square" or self.obstacleType == "Square Zig":
            sides = 4       
        for i in xrange(sides):
            minAngle = ((angle + (2*math.pi/sides *i) -math.pi/sides) % 
                                    (2.0*math.pi))
            maxAngle = ((angle + (2*math.pi/sides *i) + math.pi/sides) % 
                                                                (2.0*math.pi))
            if i in sideList:
                angleInterval += [(minAngle,maxAngle)]
        return angleInterval

    def drawWhirpool(self,canvas,cx,cy,r,angle,sides):
        i = 0
        self.drawSide(canvas,cx,cy,r,angle,i,sides)

SuperHex().run()

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

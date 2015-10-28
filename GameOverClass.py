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

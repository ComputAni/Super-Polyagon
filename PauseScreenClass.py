import math

#pause screen object
class PauseScreen(object):
    def __init__(self,width,height):
        self.width = width
        self.height = height

    def draw(self,splashInst,canvas,score):
        SplashScreen.drawMainHexagon(splashInst,canvas,"white")        
        canvas.create_text(self.width/2,self.height/2 - 250, 
                text = "Game paused", font = "Aeiral 30 bold underline")
        canvas.create_text(self.width/2,self.height/2 -175, 
            text = "Current Score: " + str(score), font = "Aerial 20 bold")
        canvas.create_text(self.width/2,self.height/2 -100, 
            text = "Press p to un-pause", font = "Aerial 20 bold")
        canvas.create_text(self.width/2,self.height/2 - 25, 
            text = "Press r to restart", font = "Aerial 20 bold")

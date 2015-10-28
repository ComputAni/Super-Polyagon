import math

#for the invincible token that occasionally appears
class InvinciblePiece(object):
    def __init__(self,width,height):
        self.pieceAngle = random.choice([math.pi/2,math.pi,3*math.pi/2,2*math.pi])
        self.width = width
        self.height = height
        self.radius = 80
        self.pieceTimer = 40
        self.invincibilityTimer = 40

    def draw(self,canvas):
        (cx,cy,r) = self.width/2,self.height/2,self.radius
        (cos,sin,angle,d) = (math.cos,math.sin,self.pieceAngle,dict())
        centerX,centerY = cx + r*cos(angle), cx - r*sin(angle)
        d["coordinates"] = (centerX - 15,centerY - 15,centerX + 15,centerY + 15)
        canvas.create_oval(d["coordinates"],fill = "red")

    def checkPieceCollision(self):
        pass

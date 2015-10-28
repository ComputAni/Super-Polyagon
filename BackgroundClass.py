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

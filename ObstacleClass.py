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

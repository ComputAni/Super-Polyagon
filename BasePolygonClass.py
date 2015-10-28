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

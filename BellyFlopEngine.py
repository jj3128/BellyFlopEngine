import time
import turtle
import math
import threading

monoInstances = []

TicksPerSecond = 4
SecondsPerTick = 1 / TicksPerSecond

class MonoBehaviour1:
    def __init__(self):
        self.lastTime = 0
        self.counter = 0
        self.deltaTime = 0
        for aClass in monoInstances:
            aClass.FixedUpdate()
        while True:
            try:
                for aClass in monoInstances:
                    aClass.EarlyUpdate()
            except Exception as e:
                print(e)
            try:
                for aClass in monoInstances:
                    aClass.Update()
            except Exception as e:
                print(e)
            self.currentTime = time.perf_counter()
            self.deltaTime = self.currentTime - self.lastTime
            try:
                for aClass in monoInstances:
                    aClass.deltaTime = self.deltaTime
            except Exception as e:
                print(e)
            self.lastTime = self.currentTime
            self.counter = self.counter + self.deltaTime
            if self.counter > SecondsPerTick:
                try:
                    for aClass in monoInstances:
                        aClass.FixedUpdate()
                except Exception as e:
                    print(e)
                self.counter = 0
            try:
                for aClass in monoInstances:
                    aClass.LateUpdate()
            except Exception as e:
                print(e)

_monoBehaviour = MonoBehaviour1

class MonoBehaviour:
    def __init__(self, *args):
        if type(self) is MonoBehaviour:
            raise Exception("Cannot create an instance of monobehaviour")
        monoInstances.append(self)
        self.deltaTime = 0
        try:
            self.Start(*args)
        except Exception as e:
            print(e)
    def SetTps(self, tps):
        global TicksPerSecond, SecondsPerTick
        TicksPerSecond = tps
        SecondsPerTick = 1 / TicksPerSecond

Screen = None

class Screen(MonoBehaviour):
    def Start(self, width, height, title, bgcolor, resizable):
        self.width = width
        self.height = height
        self.wn = turtle.Screen()
        self.wn.title(title)
        self.wn.bgcolor(bgcolor)
        self.wn.setup(width=width, height=height)
        self.wn.tracer(0,0)
        self.wn._root.resizable(resizable,resizable)
        global Screen
        Screen = self
    def EarlyUpdate(self):
        self.wn.update()
    def Update(self):
        pass
    def LateUpdate(self):
        pass
    def FixedUpdate(self):
        pass
    def mousePosX(self):
        screen_w, screen_h = self.wn._window_size()
        return (self.wn._root.winfo_pointerx() - screen_w // 2 - self.wn._root.winfo_x() - 8) * Cameras[0].sizecor() + Cameras[0].xcor()
    def mousePosY(self):
        screen_w, screen_h = self.wn._window_size()
        return (screen_h // 2 - self.wn._root.winfo_pointery() + self.wn._root.winfo_y() + 30) * Cameras[0].sizecor() + Cameras[0].ycor()
        


turtles = []

class Box:
    def __init__(self, _width, _height, _xPos, _yPos, _color, _cornerSmooth):
        self.width = _width
        self.height = _height
        self.xPos = _xPos
        self.yPos = _yPos
        self.color = _color
        self.tempBool = False #IDK
        self.cornerSmooth = _cornerSmooth
        self.turtle = turtle.Turtle()
        self.turtle.shape("square")
        self.turtle.color(self.color)
        self.turtle.turtlesize(self.height, self.width, self.cornerSmooth)
        self.turtle.penup()
        self.turtle.goto(self.xPos, self.yPos)
        turtles.append(self)
    def xcor(self):
        return self.xPos
    def ycor(self):
        return self.yPos
    def setx(self, x):
        self.xPos = x
    def sety(self, y):
        self.yPos = y
    def setpos(self, x, y):
        self.xPos = x
        self.yPos = y

class keyInput:
    def __init__(self, _key):
        self.key = _key
        self.keyDownBool = False
        self.keyPressedBool = False
        self.keyReleasedBool = False
    def keyPressed(self):
        if self.keyDownBool != True:
            self.keyDownBool = True
            self.keyPressedBool = True
    def keyReleased(self):
        self.keyDownBool = False
        self.keyReleasedBool = True
        
    def isKey(self):
        return self.keyDownBool
    def isKeyDown(self):
        value = self.keyPressedBool
        return value
    def isKeyReleased(self):
        value = self.keyReleasedBool
        return value

class mouseInput:
    def __init__(self, _key):
        self.key = _key
        self.keyDownBool = False
        self.keyPressedBool = False
        self.keyReleasedBool = False
    def keyPressed(self, temp):
        if self.keyDownBool != True:
            self.keyDownBool = True
            self.keyPressedBool = True
    def keyReleased(self, temp):
        self.keyDownBool = False
        self.keyReleasedBool = True
        
    def isKey(self):
        return self.keyDownBool
    def isKeyDown(self):
        value = self.keyPressedBool
        return value
    def isKeyReleased(self):
        value = self.keyReleasedBool
        return value

class Input(MonoBehaviour):
    def Start(self):
        self.keyInputs = {}
        self.mouseInputs = {}
    def EarlyUpdate(self):
        pass
    def Update(self):
        pass
    def FixedUpdate(self):
        pass
    def LateUpdate(self):
        for mouseInput in self.mouseInputs:
            self.mouseInputs[mouseInput].keyPressedBool = False
            self.mouseInputs[mouseInput].keyReleasedBool = False
        for keyInput in self.keyInputs:
            self.keyInputs[keyInput].keyPressedBool = False
            self.keyInputs[keyInput].keyReleasedBool = False
    def CheckIfKeyExists(self, key):
        if key not in self.keyInputs:
            self.keyInputs[key] = keyInput(key)
            Screen.wn.onkeypress(self.keyInputs[key].keyPressed, key)
            Screen.wn.onkeyrelease(self.keyInputs[key].keyReleased, key)
            Screen.wn.listen()
    def CheckIfMouseExists(self, mouseKey):
        if mouseKey not in self.mouseInputs:
            self.mouseInputs[mouseKey] = mouseInput(mouseKey)
            Screen.wn._root.bind("<Button-"+str(mouseKey)+">", self.mouseInputs[mouseKey].keyPressed)
            Screen.wn._root.bind("<ButtonRelease-"+str(mouseKey)+">", self.mouseInputs[mouseKey].keyReleased)
    def GetKey(self, key):   
        self.CheckIfKeyExists(key)
        return self.keyInputs[key].isKey()
    def GetKeyDown(self, key):
        self.CheckIfKeyExists(key)
        return self.keyInputs[key].isKeyDown()
    def GetKeyUp(self, key):
        self.CheckIfKeyExists(key)
        return self.keyInputs[key].isKeyReleased()
    def GetMouseButton(self, key):   
        self.CheckIfMouseExists(key)
        return self.mouseInputs[key].isKey()
    def GetMouseButtonDown(self, key):
        self.CheckIfMouseExists(key)
        return self.mouseInputs[key].isKeyDown()
    def GetMouseButtonUp(self, key):
        self.CheckIfMouseExists(key)
        return self.mouseInputs[key].isKeyReleased()
        

Input = Input()

class Physics:
    def __init__(self):
        pass
    def CheckCollision(self, a, b):
        if a.xcor() + a.width * 10 > b.xcor() - b.width * 10 and a.xcor() - a.width * 10 < b.xcor() + b.width * 10:
                if a.ycor() + a.height * 10 > b.ycor() - b.height * 10 and a.ycor() - a.height * 10 < b.ycor() + b.height * 10:
                    return True
        return False
    def Distance(self, a, b):
        return math.sqrt(pow(a.xcor() - b.xcor(), 2) + pow(a.ycor() - b.ycor(), 2))
    def DistanceSqrd(self, a, b):
        return (pow(a.xcor() - b.xcor(), 2) + pow(a.ycor() - b.ycor(), 2))

Physics = Physics()

Cameras = []

class Camera(MonoBehaviour):
    def Start(self, _posX, _posY, _size):
        self.xPos = _posX
        self.yPos = _posY
        self.size = _size
        Cameras.append(self)
    def setpos(self, x, y):
        self.xPos = x
        self.yPos = y
    def xcor(self):
        return self.xPos
    def ycor(self):
        return self.yPos
    def sizecor(self):
        return self.size
    def setsize(self, size):
        self.size = size
    def EarlyUpdate(self):
        pass
    def Update(self):
        for box in turtles:
            box.turtle.setx((box.xPos - self.xcor()) / self.size)
            box.turtle.sety((box.yPos - self.ycor()) / self.size)
            box.turtle.turtlesize(box.height / self.size, box.width / self.size, box.cornerSmooth)
    def LateUpdate(self):
        pass
    def FixedUpdate(self):
        pass


class UIButton(MonoBehaviour):
    def Start(self, x, y, width, height, text, color, textSize, onClick):
        self.visible = True
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.textSize = textSize
        self.onClick = onClick
        self.pen = turtle.Turtle()
        self.pen.speed(0)
        self.pen.shape("square")
        self.pen.color(color)
        self.pen.penup()
        self.pen.hideturtle()
        #self.box = Box(self.width, self.height, self.x, self.y, "#FFFFFF", 0.1)
    def EarlyUpdate(self):
        pass
    def Update(self):
        if Input.GetMouseButtonDown(1) and self.visible == True:
            if Screen.mousePosX() < self.x + self.width * 10 and Screen.mousePosX() > self.x - self.width * 10:
                if Screen.mousePosY() < self.y + self.height * 10 and Screen.mousePosY() > self.y - self.height * 10:
                    self.onClick()
    def LateUpdate(self):
        pass
    def FixedUpdate(self): #Note : The UIButton and UIText update their text in fixed update function so if you have a low tick per second then your text will appear laggy, you can move it to Update but it causes lag to the entire program
        self.pen.goto(self.x * 2, self.y * 2 - self.width * 10)
        self.pen.clear()
        if self.visible == True:
            self.pen.write(self.text, align="center", font=("Calibri", self.textSize, "bold"))


class UIText(MonoBehaviour):
    def Start(self, x, y, width, height, text, color, textSize):
        self.visible = True
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.textSize = textSize
        self.pen = turtle.Turtle()
        self.pen.speed(0)
        self.pen.shape("square")
        self.pen.color(color)
        self.pen.penup()
        self.pen.hideturtle()
        #self.box = Box(self.width, self.height, self.x, self.y, "#FFFFFF", 0.1)
    def EarlyUpdate(self):
        pass
    def Update(self):
        pass
    def LateUpdate(self):
        pass
    def FixedUpdate(self):
        self.pen.goto(self.x * 2, self.y * 2 - self.width * 10)
        self.pen.clear()
        if self.visible == True:
            self.pen.write(self.text, align="center", font=("Calibri", self.textSize, "bold"))


#This isn't used idk why i added it
class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def magnitude(self):
        return math.sqrt(self.x*self.x + self.y*self.y)
    def normalized(self):
        mag = self.magnitude()
        x = 0
        y = 0
        if mag != 0:
            x = self.x / mag
            y = self.y / mag
        return Vector2(x, y)
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector2(x, y)
    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Vector2(x, y)            

        
    

#demo
from BellyFlopEngine import *
import random
import os
import sys






#--------------------------




rgbMode = True




#--------------------------







boxSpeed = 300
lavaSpeed = 30

tps = .5

def random_color():
    x = random.randint(0, 255)
    y = random.randint(0, 255)
    z = random.randint(0, 255)
    return "#{:02x}{:02x}{:02x}".format(x,y,z)
    

class Main(MonoBehaviour):
    def Start(self):
        self.Screen = Screen(600, 600, "Avalanche Game", "black", True)
        self.Camera = Camera(0, 0, 0.5)
        self.Camera.size = 1.5

        self.SetTps(.25)        

        self.xVelocity = 0
        self.yVelocity = 0
        self.grounded = False
        self.gravity = -2000

        self.moveSpeed = 5600
        self.maxSpeed = 600
        self.friction = 3600

        self.onWall = False
        self.wallDir = 0
        self.wallJumpXStrength = 1500 #900
        self.wallJumpYStrength = 900

        self.jumpStrength = 950

        self.playerHighestY = 0

        self.playerXago = 0
        self.playerYago = 0

        self.groundCheck = Box(3.5 , 2.5, 0, 150, "black", 0)
        self.player = Box(2, 2, 0, 1, "#11c223", 0)
        self.playerInside = Box(1.5, 1.5, 0, 500, "black", 0)
        self.playerEyes1 = Box(.1, .05, 0, 500, "white", 0)
        self.playerEyes2 = Box(.1, .05, 0, 500, "white", 0)
        self.leftWall = Box(1, 1000, -300, 0, "white", 3)
        self.rightWall = Box(1, 1000, 300, 0, "white", 3)
        self.floor = Box(50, 4, 0, -300, "white", 3)
        self.vanityFloor = Box(50, 21, 0, -480, "black", 3)
        self.leftVanityWall = Box(10, 1000, -400, 0, "black", 3)
        self.rightVanityWall = Box(10, 1000, 400, 0, "black", 3)

        self.boxWall = None

        self.lava = Box(50, 1, 0, -750, "#850c12", 3)

        self.highScoreText = UIText(0, 125, 1, 1, "0", "white", 24)
        self.highScoreText.FixedUpdate()
               
        self.fallingBoxes = []
        if rgbMode:
            for i in range(50):
                self.fallingBoxes.append(FallingBox(random.randint(6, 8), False, self.fallingBoxes, self.floor, self.lava, random_color())) #default 6
                self.fallingBoxes[i].SetPos(0, -2500)
        else:
            for i in range(50):
                self.fallingBoxes.append(FallingBox(random.randint(6, 8), False, self.fallingBoxes, self.floor, self.lava, "white")) #default 6
                self.fallingBoxes[i].SetPos(0, -2500)

        self.lava = Box(500, 1, 0, -750, "#850c12", 3)
        self.vanityLava = Box(500, 50, 0, -750, "#610c10", 3)

        self.cameraFixed = False

        self.loading = Box(100, 100, 0, 0, "white", 0)
    def Distance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1)*(x2 - x1) + (y2-y1)*(y2-y1))
    def CollisionResolution(self, movingThing, staticThing):
        closestDistance = 10000000
        closestPoint = 0
        corner = 9.9
        distance = self.Distance(movingThing.xcor(), movingThing.ycor() - movingThing.height * 10, staticThing.xcor() - staticThing.width * corner, staticThing.ycor() + staticThing.height * 10)
        if distance < closestDistance:
            closestPoint = 1
            closestDistance = distance
        distance = self.Distance(movingThing.xcor(), movingThing.ycor() - movingThing.height * 10, staticThing.xcor() + staticThing.width * corner, staticThing.ycor() + staticThing.height * 10)
        if distance < closestDistance:
            closestPoint = 2
            closestDistance = distance

        distance = self.Distance(movingThing.xcor() - movingThing.width * 10, movingThing.ycor(), staticThing.xcor() + staticThing.width * 10, staticThing.ycor() + staticThing.height * corner)
        if distance < closestDistance:
            closestPoint = 3
            closestDistance = distance
        distance = self.Distance(movingThing.xcor() - movingThing.width * 10, movingThing.ycor(), staticThing.xcor() + staticThing.width * 10, staticThing.ycor() - staticThing.height * corner)
        if distance < closestDistance:
            closestPoint = 4
            closestDistance = distance
   
        distance = self.Distance(movingThing.xcor(), movingThing.ycor() + movingThing.height * 10, staticThing.xcor() + staticThing.width * corner, staticThing.ycor() - staticThing.height * 10)
        if distance < closestDistance:
            closestPoint = 5
            closestDistance = distance
        distance = self.Distance(movingThing.xcor(), movingThing.ycor() + movingThing.height * 10, staticThing.xcor() - staticThing.width * corner, staticThing.ycor() - staticThing.height * 10)
        if distance < closestDistance:
            closestPoint = 6
            closestDistance = distance
           
        distance = self.Distance(movingThing.xcor() + movingThing.width * 10, movingThing.ycor(), staticThing.xcor() - staticThing.width * 10, staticThing.ycor() - staticThing.height * corner)
        if distance < closestDistance:
            closestPoint = 7
            closestDistance = distance
        distance = self.Distance(movingThing.xcor() + movingThing.width * 10, movingThing.ycor(), staticThing.xcor() - staticThing.width * 10, staticThing.ycor() + staticThing.height * corner)
        if distance < closestDistance:
            closestPoint = 8
            closestDistance = distance
       
        if closestPoint == 1 or closestPoint == 2:
            movingThing.sety(staticThing.ycor() + staticThing.height * 10 + movingThing.height * 10)
            self.yVelocity = 0
            self.grounded = True
        if closestPoint == 3 or closestPoint == 4:
            self.onWall = True
            self.wallDir = -1
            movingThing.setx(staticThing.xcor() + staticThing.width * 10 + movingThing.width * 10)
            self.boxWall = staticThing
        if closestPoint == 5 or closestPoint == 6:
            movingThing.sety(staticThing.ycor() - staticThing.height * 10 - movingThing.height * 10)
            if self.yVelocity > 0:
                self.yVelocity = 0
        if closestPoint == 7 or closestPoint == 8:
            self.onWall = True
            self.wallDir = 1
            movingThing.setx(staticThing.xcor() - staticThing.width * 10 - movingThing.width * 10)
            self.boxWall = staticThing
    def EarlyUpdate(self):
        pass
    def RandomFunction(self, number):
        if number < -1:
            return -1
        if number > 1:
            return 1
        else:
            return number
    def Update(self):
        self.highScoreText.text = str(int(self.playerHighestY))
        global lavaSpeed, tps
        lavaSpeed += .12 * self.deltaTime
        tps += .0005 * self.deltaTime
        self.SetTps(tps)
        self.lava.sety(self.lava.ycor() + lavaSpeed * self.deltaTime)

        if Input.GetKey("a"):
            self.xVelocity -= self.moveSpeed * self.deltaTime
        elif Input.GetKey("d"):
            self.xVelocity += self.moveSpeed * self.deltaTime
        if self.xVelocity < -self.maxSpeed:
            self.xVelocity = -self.maxSpeed
        if self.xVelocity > self.maxSpeed:
            self.xVelocity = self.maxSpeed
        if self.xVelocity > 10 or self.xVelocity < -10:
            self.xVelocity += -self.RandomFunction(self.xVelocity) * self.friction * self.deltaTime
        else:
            self.xVelocity = 0


        if Input.GetKeyDown("space"):
            if self.grounded:
                self.player.sety(self.player.ycor() + 1)
                self.yVelocity = self.jumpStrength
                if self.onWall and (Input.GetKey("a") or Input.GetKey("d")):
                    self.xVelocity = -self.wallDir * self.wallJumpXStrength
                    
       
        self.yVelocity = self.yVelocity + self.gravity * self.deltaTime
         
        if self.onWall == True:
            if self.yVelocity < 0:
                if self.boxWall != None:
                    if self.boxWall.tempBool == False:
                        self.yVelocity = -100
                    else:
                        self.yVelocity = -200
                else:
                    self.yVelocity = self.yVelocity
        self.player.setx(self.player.xcor() + self.xVelocity * self.deltaTime)    
        self.player.sety(self.player.ycor() + self.yVelocity * self.deltaTime)

        self.groundCheck.setx(self.player.xcor())
        self.groundCheck.sety(self.player.ycor() - 15)

        self.playerEyes1.setx(((self.playerXago - self.player.xcor()) * -1.2 + self.player.xcor()) - 10)
        self.playerEyes1.sety(((self.playerYago - self.player.ycor()) * .5 + self.player.ycor()) + 5)
        self.playerEyes2.setx(((self.playerXago - self.player.xcor()) * -1.2 + self.player.xcor()) + 10)
        self.playerEyes2.sety(((self.playerYago - self.player.ycor()) * .5 + self.player.ycor()) + 5)

        self.playerInside.setx(self.player.xcor())
        self.playerInside.sety(self.player.ycor())

        self.vanityLava.sety(self.lava.ycor() - 510)

        self.grounded = False
        self.onWall = False
        self.boxWall = None
        for box1 in turtles:
            if box1 == self.player or box1 == self.leftWall or box1 == self.rightWall or box1 == self.groundCheck or box1 == self.leftVanityWall or box1 == self.rightVanityWall or box1 == self.playerInside or box1 == self.loading or box1 == self.lava or box1 == self.playerEyes2 or box1 == self.playerEyes1:
                continue
            if Physics.CheckCollision(self.player, box1):
                self.CollisionResolution(self.player, box1)
            if Physics.CheckCollision(self.groundCheck, box1):
                self.grounded = True
               
        if self.player.xcor() < self.leftWall.xcor():
            self.player.setx(self.rightWall.xcor() - 1)
        if self.player.xcor() > self.rightWall.xcor():
            self.player.setx(self.leftWall.xcor() + 1)

        if self.player.ycor() > self.playerHighestY:
            self.playerHighestY = self.player.ycor()

        if self.player.ycor() < self.lava.ycor() + 15:
            print("You Died!!! Restarting....")
            time.sleep(2)
            self.Screen.wn.bye()
            os.system('FullGameDemo.py')
            sys.exit()
       
        self.Camera.setpos(0, self.player.ycor())

        self.playerXago = self.player.xcor()
        self.playerYago = self.player.ycor()
    def FixedUpdate(self):
        if self.loading.xcor() != 8000:
            self.loading.setx(8000)
            self.player.sety(100)
        #print(tps, ",", lavaSpeed)
        BoxChoice = None
        for box in self.fallingBoxes:
            if box.box.ycor() < self.lava.ycor() - 200:
                BoxChoice = box
                break
       
        BoxChoice.SetPos(random.randint(-250, 250), self.lava.ycor() + 2000)
        BoxChoice.moving = True
        BoxChoice.box.tempBool = True
    def LateUpdate(self):
        pass

class FallingBox(MonoBehaviour):
    def Start(self, size, moving, otherBoxes, ground, lava, color):
        self.box = Box(size, size, 0, 0, color, 0)
        self.insideBox = Box(size - .75, size - .75, 0, 0, "black", 0)
        self.moving = moving
        self.otherBoxes = otherBoxes
        self.ground = ground
        self.lava = lava
    def EarlyUpdate(self):
        pass
    def Update(self):
        self.insideBox.setx(self.box.xcor())
        self.insideBox.sety(self.box.ycor())
        if self.moving:
            self.box.sety(self.box.ycor() - boxSpeed * self.deltaTime)
            for otherBox in self.otherBoxes:
                if otherBox.box != self.box:
                    if Physics.CheckCollision(self.box, otherBox.box):
                        self.moving = False
                        self.box.tempBool = False
            if Physics.CheckCollision(self.box, self.ground):
                self.moving = False
                self.box.tempBool = False
        if self.box.ycor() < self.lava.ycor() - 200:
            self.moving = False
            self.box.tempBool = False
            self.SetPos(0, -2500)
        if self.box.ycor() < -240:
            self.moving = False
            self.box.tempBool = False
            self.SetPos(0, -2500)
    def SetPos(self, x, y):
        self.box.setx(x)
        self.box.sety(y)
    def LateUpdate(self):
        pass
    def FixedUpdate(self):
        pass
       
   
main = Main()
_monoBehaviour = MonoBehaviour1() #Do this

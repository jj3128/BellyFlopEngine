from BellyFlopEngine import *

class Main(MonoBehaviour):
    def OnButtonClick(self):
        print("Button Clicked\n\n")
    def Start(self):
        self.Screen = Screen(600, 600, "Game Engine Test", "black", False)
        self.Camera = Camera(0, 0, 0.5)

        self.TutorialText = UIText(0, 125, 1, 1, "Controls : WASD, Space, Left Click", "white", 24)
        self.BasicButton = UIButton(50, 50, 1, 1, "Button", "white", 24, self.OnButtonClick)
    
        self.SetTps(1) #1 tick per second for fixed update calls

        self.box = Box(1, 1, 0, 0, "white", 3)
        self.test = Box(1, 1, 0, 0, "white", 3)
        self.cameraFixed = False
    def EarlyUpdate(self):
        pass
    def Update(self):
        if Input.GetKey("a"):
            self.box.setx(self.box.xcor() - 100 * self.deltaTime)
        if Input.GetKey("d"):
            self.box.setx(self.box.xcor() + 100 * self.deltaTime)
        if Input.GetKey("s"):
            self.box.sety(self.box.ycor() - 100 * self.deltaTime)
        if Input.GetKey("w"):
            self.box.sety(self.box.ycor() + 100 * self.deltaTime)

        if Input.GetKeyDown("space"):
            print("Space pressed!")
        if Input.GetKeyUp("space"):
            print("Space released")

        if Input.GetKeyDown("r"):
            self.cameraFixed = not self.cameraFixed
            if self.cameraFixed == False:
                self.Camera.setpos(0,0)

        if Input.GetMouseButtonDown(1):
            print("Left Mouse Clicked at", self.Screen.mousePosX(), self.Screen.mousePosY())
        if Input.GetMouseButtonUp(1):
            print("Left Mouse Un Clicked at", self.Screen.mousePosX(), self.Screen.mousePosY())
        if Input.GetMouseButton(1):
            #returns true every frame while the mouse is being held down
            pass
            
        if Physics.CheckCollision(self.box, self.test):
            #You need to impliment ur own collision resolution
            pass

        self.test.setpos(self.Screen.mousePosX(), self.Screen.mousePosY())  #Sets the cube to be at the cursors position

        if self.cameraFixed:
            self.Camera.setpos(self.box.xcor(), self.box.ycor()) #parents the camera to the player
    def FixedUpdate(self):
        pass
    def LateUpdate(self):
        pass
    
main = Main()
_monoBehaviour = MonoBehaviour1()

## BellyFlop Python-Turtle Game Engine

BellyFlopEngine is a Python Game Engine which does not require any external libraries in order to use. It uses the turtle library in order to render everything (which automatically comes with python).

It uses similar naming conventions to Unity in C# for certain things, I was unsure what to name them.


## Getting Started

Create a new python file in a folder and copy [BellyFlopEngine.py](BellyFlopEngine.py) into the same folder.

Add "from BellyFlopEngine import*" to the top of the python file and create a new class which inherits from MonoBehaviour. At the very bottom of the python file create an instance of that class.

Add the line of code "_monoBehaviour = MonoBehaviour1()" at the bottom of your file (this is important as it starts the while loop which runs the entire game)

Create 5 functions in the class, Start, EarlyUpdate, Update, LateUpdate, FixedUpdate each with the argument "self" in them. Add a "pass" in each of these functions for now.
Note : if you want to pass a variable into the class when creating it you can add extra arguments to the start class which basically acts like "def "__innit__"

Create a Screen, Camera and Box class in the start function, as seen in the demo file

If you want to actually make a game, try looking at some of the code in the [Demo File](Demo.py) and the [Game Example File](https://github.com/jj3128/BellyFlopEngine/tree/main/Game%20Example) to see what functions you can use.

## Info

<div align=";eft">
  <a href="https://github.com/jj3128/BellyFlopEngine">
    <img src="https://i.imgur.com/Y1QJrsK.png" width="300px" height="auto">
  </a>
</div>

Here is a screenshot of the [Game Example](https://github.com/jj3128/BellyFlopEngine/tree/main/Game%20Example). Its a small game where you climb cubes to avoid the lava, I made it to demonstrate the engine.

Note : Input is case sensitive so if its not working, check if you have caps lock on

If you have any issues or need help, Join the [Discord Server](https://discord.gg/ZwwQNQzwPQ)

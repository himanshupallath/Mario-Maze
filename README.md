# Mario-Maze
This is a game I developed written in Python. It utilizes pygame to create a graphical display  
I'll describe different aspects of this code  
  
### Maze Map
The map was created using an array. The letters in the array indicate different colors.  
There is a dictionary that contains different RGB color values.

### Character and Background Images
Images were selected and uploaded into the pygame window using pygame.image.load().convert_alpha()
Images used were:
- Mario background
- Mario character
- Finish checkered flag

### Keybinds
Pygame has built-in arrow key bind controls, which control how the Mario character travels.  
The character moves that way when K_UP, K_DOWN, K_LEFT, and K_RIGHT are pressed down and don't move when they are not pressed.  

### Camera Panning
This is a class control that displays movement when the character is moving.  
When the character moves, the camera shifts and updates the Pygame window. 

### Gravity and Wall Detection 
Within the class for the character, some functions deal with gravity and wall collision detection.  
The update function deals with the character moving with gravity logic included within it.
The collide function checks if the character runs into the wall. Once they do, they can't move in that same direction again. This is to prevent players from running through the wall.  

### Characters and Finish Line Sprites
The character and the two finish lines have their own classes. These classes describe the width, height, and the x and y velocity.  

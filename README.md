# CVTetris

A cooler version of the Tetris game which allows the user to control the falling tiles using hand motion. It retains the classical game entertainment but now encouraging users to be on the 'move' as they relish the game! Check out our video and submission (here)[https://devpost.com/software/cvtetris]

# Motivation:

Generations of us have enjoyed a good game of Tetris for long. But it is now getting mundane to control the falling blocks using the keyboard keys, and thus losing its excitement in the current generation. 
Hence, we came up with an idea of allowing the users to use their hand movements instead to control the falling blocks! This game establishes two main purposes:

1. Bringing back the lost glory and fun of the game of Tetris by allowing the players to play using their hand gestures.
2. Encouraging physcial movement and providing a more interactive and immersive user experience.

# Directions:

Most directions of the game are retained, differing in the fact how the moves are indicated:

1. Control the falling block using a green object.
2. Move the object left to translate the block to the left of the screen.
3. Move the object right to translate the block to the right of the screen.
4. Move the object up to rotate the block by 90 degrees.
5. Move the object down to speed up the fall.

# Tech Used:

1. OpenCV: lbrary used to implement real-time Computer Vision. Used to detect the green object and its motion by the user.
2. Imutils: used to make basic image processing operations in conjuction with OpenCV
3. PyGame: python module to design game including computer graphics and background music.
4. Python: the underlaying programming language in which the entire logic of the game was coded.

# How to Play:

```
pip install -r requirements.txt
python tetris.py
```
Tried and tested on mac





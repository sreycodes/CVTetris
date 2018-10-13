#! /usr/bin/env python
from helpers import load_image

class base_level:
    '''The base class for the game stage'''
    def getLayout(self):
        '''Get the layout of the stage
            Returns a [][] list'''
        pass

    def getImages(self):
        '''Get a list of all the images used by the stage
            Returns a lsit of all the images used. The indices
            in the layout refer to sprites in the list returned
            by the function'''
        pass

class level(base_level):
    '''The layout of the game'''
    def __init__(self):
        '''Initialize the layout, assigned values to different components
        These values of components will be used in the matrix as the start position of
        each components
        '''
        self.BRICK = 1
        self.CHARACTER = 2
        self.PELLET = 0
        self.MONSTER = 3
        self.MONSTER_WEAK = 4
        self.SUPER_PELLET = 5

    def getLayout(self):
        '''This is the Initialization format of the game. In the matrix below,
        9 = the dark area of the game.
        1 = The bricks
        2 = where the character starts
        3 = where the monsters at the begining of the game
        4 = There is no weak monster in the begining of the game, so we do not have 4 at the start
        5 = where the 'super pellet' is at
        '''
        return [[9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9 ,9, 9, 9, 9, 9, 9, 9, 9, 9, 9],\
                [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9 ,9, 9, 9, 9, 9, 9, 9, 9, 9, 9],\
                [9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ,1, 1, 1, 1, 1, 1, 1, 1, 1, 9],\
                [9, 1, 5, 0, 0, 0, 0, 0, 0, 5, 1 ,5, 0, 0, 0, 0, 0, 3, 5, 1, 9],\
                [9, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1 ,0, 1, 1, 1, 0, 1, 1, 0, 1, 9],\
                [9, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0, 0, 0, 0, 1, 9],\
                [9, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1 ,1, 1, 0, 1, 0, 1, 1, 0, 1, 9],\
                [9, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1 ,0, 0, 0, 1, 0, 0, 0, 0, 1, 9],\
                [9, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 9],\
                [9, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 9],\
                [9, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 9],\
                [9, 1, 0, 3, 0, 5, 0, 0, 1, 0, 0, 0, 1, 0, 0, 5, 0, 0, 0, 1, 9],\
                [9, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 9],\
                [9, 1, 1, 1, 1, 0, 1, 0, 0, 3, 0, 0, 3, 0, 1, 0, 1, 1, 1, 1, 9],\
                [9, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 9],\
                [9, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 3, 0, 0, 1, 9],\
                [9, 1, 5, 1, 1, 0, 1, 1, 1, 5, 1, 5, 1, 1, 1, 0, 1, 1, 5, 1, 9],\
                [9, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 9],\
                [9, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 9],\
                [9, 1, 5, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 5, 1, 9],\
                [9, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 9],\
                [9, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1, 9],\
                [9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9]]

    def getSprites(self):
        '''Load all the images needed in the game

        Parameters:
        self = the layout itself

        Return:
        A list of information of each components on the surface'''
        brick, rect = load_image('brick.png')
        pellet, rect = load_image('pellet.png', -1)
        character, rect = load_image('character.png', -1)
        monster,rect = load_image('ghost.png', -1)
        monster_weak,rect = load_image('ghost2.png',-1)
        super_pellet, rect = load_image('super_pellet.png',-1)
        return [pellet, brick, character,monster,monster_weak,super_pellet]

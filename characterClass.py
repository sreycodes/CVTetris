import basicSprite
import pygame
from pygame.locals import *
import random


SUPER_STATE_START = pygame.USEREVENT + 1
SUPER_STATE_OVER = SUPER_STATE_START + 1
SNAKE_EATEN = SUPER_STATE_OVER + 1

class Monster(basicSprite.Sprite):
    '''A class for Monsters.
    Loads the '''
    def __init__(self,centerPoint,image,weakMon_image = None):
        basicSprite.Sprite.__init__(self,centerPoint,image)
        # Store the original rect information
        self.normal_image = image
        self.original_rect = pygame.Rect(self.rect)
        if weakMon_image != None:
            self.weakMon_image = weakMon_image
        else:
            self.weakMon_image = image
        self.weak = False
        #When the variable movecount matches the random number self.moves,
        #the next direction will be randomly chosen
        #Here is the initialization of each variables
        self.direction = random.randint(1,4)
        self.dist = 1
        self.moves = random.randint(50,200)
        self.moveCount = 0;
    def update(self,brick_group):
        '''This function updates the movement of the Monster

        Parameters:
        self = class of monsters itself
        brick_group = a list that contains all the information of each brick'''
        x_move,y_move = 0,0
        if self.direction==1:
            #Move right
            x_move = self.dist
        elif self.direction==2:
            #Move left
            x_move = -self.dist
        elif self.direction==3:
            #Move up
            y_move = -self.dist
        elif self.direction==4:
            #Move down
            y_move = self.dist
        self.rect.move_ip(x_move,y_move)
        self.moveCount += 1

        if pygame.sprite.spritecollideany(self, brick_group):
            #in case the monster hits the brick, it should reverse the movement
            self.rect.move_ip(-x_move,-y_move)
            self.direction = random.randint(1,4)
        elif self.moves == self.moveCount:
            # at a certain time, the monster will change its direction
            self.direction = random.randint(1,4)
            self.moves = random.randint(100,200)
            self.moveCount = 0;
    def M_dead(self):
        '''When the monster is dead, they will be regenerated at their original position
        This function used the previouly stored rect information to regenerate the monster

        Parameter:
        self = Monster: a class itself
        '''
        self.weak = False
        self.rect = self.original_rect
        self.image = self.normal_image

    def weakMon(self,weak):

        '''This functino checked whether the monster should be in weak stage
        When the monster is in weak stage, change the image to weakMon_image.
        Else it is normal_image

        Parameters:
        self = Monster: a class itself
        weak = a bool stage: if weak is True it is in weak stage
                else it is not.

        '''
        if self.weak != weak:
            self.weak = weak
            if weak:
                self.image = self.weakMon_image
            else:
                self.image = self.normal_image




class Character(basicSprite.Sprite):
    def __init__(self, centerPoint, image):
        basicSprite.Sprite.__init__(self, centerPoint, image)
        #Initialize the number of pellets eaten
        self.pellets = 0
        # set the number of pixels to move each set_repeat
        self.dist=3
        # Initialize how much the character moves
        self.x_move = 0
        self.y_move = 0
        self.direction = 0
        self.nextdir = 0
        self.xdir = [0,-self.dist,self.dist,0,0]
        self.ydir=[0,0,0,-self.dist,self.dist]

    def MoveKeyDown(self, key):
        '''This function sets the x_move or y_move variables
        that will then move the snake when update() function
        is called. The x_move and y_move values will be returned
        to normal when this MoveKeyUp function is called'''

        self.direction=self.nextdir

        if (key == K_RIGHT):
            self.nextdir=2
        elif (key == K_LEFT):
            self.nextdir=1
        elif (key == K_UP):
            self.nextdir=3
        elif (key == K_DOWN):
            self.nextdir=4


    def update(self, brick_group,pellet_group,monster_group,big_pellet_group):
        '''called when the Character spirit should update itself

        Parameters:
        self = class of character itself
        brick_group = a list containing each bricks information
        pellet_group = a list containing each pellet information
        monster_group = a list containing each monster information
        big_pellet_group = a list containing each super pellet information'''
        self.xMove=self.xdir[self.nextdir]
        self.yMove=self.ydir[self.nextdir]

        self.rect.move_ip(self.xMove,self.yMove)

        """IF we hit a block, don't move - reverse the movement"""
        if pygame.sprite.spritecollide(self, brick_group, False):
            self.rect.move_ip(-self.xMove,-self.yMove)
            """IF we can't move in the new direction... continue in old direction"""
            self.xMove=self.xdir[self.direction]
            self.yMove=self.ydir[self.direction]
            self.rect.move_ip(self.xMove,self.yMove)
            if pygame.sprite.spritecollide(self, brick_group, False):
                self.rect.move_ip(-self.xMove,-self.yMove)
                self.yMove=0
                self.xMove=0
                self.direction=0
                self.nextdir=0
        else:
                self.direction=0




        lst_monsters = pygame.sprite.spritecollide(self,monster_group,False)
        # Monster, Character collision check
        if len(lst_monsters)>0:
            # Collide with a monster
            self.MonsterCollide(lst_monsters)
        else:
            # Character, Pellets collision check
            lst_pellet = pygame.sprite.spritecollide(self,pellet_group,True)
            if len(lst_pellet)>0:
                # Collide with normal pellets
                self.pellets += len(lst_pellet)
            elif len(pygame.sprite.spritecollide(self, big_pellet_group, True))>0:
                # Collide with super pellets
                self.superState = True
                pygame.event.post(pygame.event.Event(SUPER_STATE_START,{}))
                pygame.time.set_timer(SUPER_STATE_OVER,0)
                pygame.time.set_timer(SUPER_STATE_OVER,3000)

    def MonsterCollide(self,lst):
        '''This function is used when there is a collision between monster
        and character.

        Parameters
        self = Character class itself
        lst = list of monsters has been hit by the character'''
        if len(lst)<=0:
            #list is empty, did not hit anything
            return
        for monster in lst:
            if monster.weak:
                monster.M_dead()
            else:
                pygame.event.post(pygame.event.Event(SNAKE_EATEN,{}))

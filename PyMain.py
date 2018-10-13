import os
import sys
import pygame
from pygame.locals import *
from helpers import *
import game_level
from characterClass import*
import numpy as np
import cv2
import imutils
from collections import deque


if not pygame.font:
    print("Warning, fonts disabled")
if not pygame.mixer:
    print("Warning, sound disabled")

black = 0, 0, 0
white = 255, 255, 255
BLOCK_SIZE = 24
cap = cv2.VideoCapture(0)
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
pts = deque(maxlen=12)
direction_deque = deque(maxlen=10)


# main class that handles the higest level functionality


class PacmanMain:
    '''This is the main class of the whole game. This class combined all the sub-class made in
    other different files. This class recognizes the status of each sub-class and using the
    result of the recognization to perform different actions. This class will do all the
    main control and the drawing part of the game.
    '''
    def __init__(self, width=640, height=480):
        '''This function initialize the bacground and the windows of the game

        Parameters:
        self = the whole game itself
        width = the width of the game window
        height = the height of the game window
        '''
        pygame.init()
        # set window size
        self.width = width
        self.height = height
        # generate the screen
        self.screen = pygame.display.set_mode((self.width, self.height))

    def MainLoop(self):
        '''This is main loop of the game. This function recognize and update
        the status of the whole game. At the end of the function, the drawing
        part of the game was also applied

        Parameter:
        self = whole game itself.
        '''
        direction = "ND"
        frame_counter = 0
        self.LoadSprites()
        pygame.key.set_repeat(500, 30)
        # create the background
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(black)
        # draw the bricks onto the background, only once
        self.brick_sprites.draw(self.screen)
        self.brick_sprites.draw(self.background)
        pygame.display.flip()
        # grabs a frame from the video camera and processes it to make it run faster
        # reduces resolution and removes imperfections
        while True:
            grabbed, frame = cap.read()
            frame = imutils.resize(frame, width=600)
            frame = cv2.flip(frame, 1)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, greenLower, greenUpper)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)
            
            #finds any green object in the frame
            coords = cv2.findContours(
                mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            center = None
            
            #if there are more than one detected object pick the biggest
            if len(coords) > 0:
                circle_1 = max(coords, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(circle_1)
                M = cv2.moments(circle_1)
                center = (int(M["m10"] / M["m00"]),
                          int(M["m01"] / M["m00"]))

                if radius > 10:
                    cv2.circle(frame, (int(x), int(y)),
                               int(radius), (0, 255, 255), 2)
                    cv2.circle(frame, center, 5, (0, 0, 255), -1)
            #only add acceptable centres of objects to the deque
            if type(center) == tuple:
                pts.appendleft(center)

            # Redraw the background over the sprite.
            self.character_sprites.clear(self.screen, self.background)
            self.monster_sprites.clear(self.screen, self.background)

            # Check the event in queue, get the status of the game
            # Also check the status of the character
            for event in pygame.event.get():
                # When the state is quit, exist the game
                if event.type == pygame.QUIT:
                    sys.exit()
                # When character has been eaten
                elif event.type == SNAKE_EATEN:
                    print("Game Over")
                    print("Your Score is:", self.character.pellets)
                    sys.exit()
                # Contradicts to the SUPER_STATE_OVER. At this state, character
                # could eat the monster, and the monster state is weak
                elif event.type == SUPER_STATE_START:
                    for monster in self.monster_sprites.sprites():
                        monster.weakMon(True)
                # When the state is SUPER_STATE_OVER, set the character to
                # normal state, and let the character.superState be False
                # and set the monsters to be strong enough to eat the character
                elif event.type == SUPER_STATE_OVER:
                    self.character.superState = False
                    pygame.time.set_timer(SUPER_STATE_OVER, 0)
                    for monster in self.monster_sprites.sprites():
                        monster.weakMon(False)

            #if we have a full deque then determine a direction and add
            # to the direction deque
            if len(pts) == 12:
                temp_direction = translation(pts[0], pts[len(pts) - 1])
                print(temp_direction)
                if direction != temp_direction:
                    direction = temp_direction
                    direction_deque.appendleft(direction)


            # the direction deque and frame counters are attempts to smoothen the inputs
            # and eliminate unintentional movements from the player
            # only deliberate motions are accepted, the numbers have been chosen
            # from trial and error offering the best results
            if len(direction_deque) == 10 and all(x == direction_deque[0] for x in direction_deque) and frame_counter == 3:
                if (direction_deque[0] == "Up"):
                    self.character.MoveKeyDown(K_UP)
                elif direction_deque[0] == "Down":
                    self.character.MoveKeyDown(K_DOWN)
                elif direction_deque[0] == "Right":
                    self.character.MoveKeyDown(K_RIGHT)
                elif direction_deque[0] == "Left":
                    self.character.MoveKeyDown(K_LEFT)
            if frame_counter == 3:
                frame_counter = 0
            else:
                frame_counter += 1

            direction = "ND"
            # RenderUpdates sub-class that draws Sprites in order of addition
            self.character_sprites.update(
                self.brick_sprites, self.pellet_sprites, self.monster_sprites, self.big_pellet_sprites)
            self.monster_sprites.update(self.brick_sprites)
            
            # Drawing part
            self.screen.blit(self.background, (0, 0))
            if pygame.font:
                # this gives the front size of the text that showing the score
                font = pygame.font.Font(None, 50)
                # What is the containt of the text and what is the position of the front
                text = font.render("Pellets {}".format(
                    self.character.pellets), 1, (255, 0, 0))
                # position is in the mide area
                textpos = text.get_rect(centerx=(self.width / 2))
                self.screen.blit(text, textpos)
            
            # this time we only need to update the portion of the screen
            show_list = [textpos]
            show_list += self.pellet_sprites.draw(self.screen)
            show_list += self.big_pellet_sprites.draw(self.screen)
            show_list += self.character_sprites.draw(self.screen)
            show_list += self.monster_sprites.draw(self.screen)
            pygame.display.update(show_list)


    def LoadSprites(self):
        '''In this Function, all the sub-images should be loaded. Corresponding to the layout
        in game_level file, different sub-images should be loaded in different position at the initial
        condition. This function recognize which sub-images should be loaded where. This function also
        needs to create different groups for the different characters. These groups are needed in the
        main loop fucntion

        Parameter:
        self = the whole game it self.

        Create:
        different groups of characters: the name should follow the rules: self.'name'_sprites
        layout the game in initial condition'''
        # calculate the center point offset
        x_offset = (BLOCK_SIZE / 2)
        y_offset = (BLOCK_SIZE / 2)
        # load the level
        level1 = game_level.level()
        layout = level1.getLayout()
        image_list = level1.getSprites()

        # creating the pellet group
        self.pellet_sprites = pygame.sprite.RenderUpdates()
        self.big_pellet_sprites = pygame.sprite.RenderUpdates()
        # creating the brick Group
        self.brick_sprites = pygame.sprite.RenderUpdates()
        self.monster_sprites = pygame.sprite.RenderUpdates()
        # initializing all the pellets and add them to pellet Group

        for i in range(len(layout)):
            for j in range(len(layout[i])):
                # get the center point for the rects
                centerPoint = [(j * BLOCK_SIZE) + x_offset,
                               (i * BLOCK_SIZE + y_offset)]
                if layout[i][j] == level1.BRICK:
                    brick = basicSprite.Sprite(
                        centerPoint, image_list[level1.BRICK])
                    self.brick_sprites.add(brick)
                elif layout[i][j] == level1.CHARACTER:
                    self.character = Character(
                        centerPoint, image_list[level1.CHARACTER])
                    print(type(self.character))
                elif layout[i][j] == level1.PELLET:
                    pellet = basicSprite.Sprite(
                        centerPoint, image_list[level1.PELLET])
                    self.pellet_sprites.add(pellet)
                elif layout[i][j] == level1.MONSTER:
                    monster = Monster(centerPoint, image_list[
                                      level1.MONSTER], image_list[level1.MONSTER_WEAK])
                    self.monster_sprites.add(monster)
                    pellet = basicSprite.Sprite(
                        centerPoint, image_list[level1.PELLET])
                    self.pellet_sprites.add(pellet)
                elif layout[i][j] == level1.SUPER_PELLET:
                    big_pellet = basicSprite.Sprite(
                        centerPoint, image_list[level1.SUPER_PELLET])
                    self.big_pellet_sprites.add(big_pellet)
                # create the Character group
        self.character_sprites = pygame.sprite.RenderUpdates(self.character)
        # print(self.pellet)


class Pellet(pygame.sprite.Sprite):
    '''This is one of the sub-class. This class create the pellet. Since the pellets
    should not move the whole time, the class is comparativly easy. This sub-class
    load the images of the pellet and set the rect of the image.
    '''
    def __init__(self, rect=None):
        '''Initializing the information for the pellets.

        Parameters:
        self = pellet itself
        rect = the rect of the imag. Could let us put the pellet whereever we want
        '''
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('pellet.png', -1)
        #self.image = pygame.image.load('pellet.png')
        #self.rect = self.image.get_rect()
        if rect != None:
            self.rect = rect


def translation(first_coord, second_coord):
    '''Calculates the direction of motion. A deque is used for the coordinates
        so that the function only detects the general direction of movement
        and can interpret movements that are not completely verical or 
        horizontal

        Arguments: Two center variables used to determine direction of motion

        Returns: A string specifying the direction of motion'''
    # check if translation in x or y direction
    delta_y = int(second_coord[1] - first_coord[1])
    delta_x = int(second_coord[0] - first_coord[0])
    if delta_x != 0:
        axis = abs(delta_y) / abs(delta_x)
    else:
        axis = 0

    if axis > 1:
        if delta_y > 0:
            return "Up"
        elif delta_y < 0:
            return "Down"
    elif axis < 1:
        if delta_x > 0:
            return "Left"
        elif delta_x < 0:
            return "Right"
    else:
        return "ND"


if __name__ == "__main__":
    '''Main function of the game'''
    MainWindow = PacmanMain(500, 575)
    MainWindow.MainLoop()
    cap.release()

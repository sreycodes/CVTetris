# By Pramod Jacob

# CELL = square space on grid
# BLOCK = colored square
# PIECE = 4 colored squares that form a shape

## REQUIRED FIXES
## 1) if a piece is squeezed into a spot at the very last possible moment, it will move down 

import random, pygame, sys
from pygame.locals import *
import numpy as np
import cv2
import imutils
import time
from collections import deque
from datetime import datetime

from AppKit import NSScreen

cap = cv2.VideoCapture(0)
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
pts = deque(maxlen=12)
direction = "ND"
height = 320
width = 600
height = int(NSScreen.mainScreen().frame().size.height)
width = int(NSScreen.mainScreen().frame().size.width)


FPS = 25
WINDOWWIDTH_TOTAL = 480
#WINDOWWIDTH_TETRIS = 300
WINDOWWIDTH_TETRIS = 280
WINDOWWIDTH_SIDE = WINDOWWIDTH_TOTAL-WINDOWWIDTH_TETRIS
#WINDOWHEIGHT = 600
WINDOWHEIGHT = 520
CELLSIZE = 20
assert WINDOWWIDTH_TETRIS % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
assert WINDOWWIDTH_TOTAL > WINDOWWIDTH_TETRIS, "Tetris window is larger than total window."
CELLWIDTH_TOTAL = int(WINDOWWIDTH_TOTAL/CELLSIZE)
CELLWIDTH_TETRIS = int(WINDOWWIDTH_TETRIS/CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT/CELLSIZE)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY  = (40, 40, 40)

LITERED = (255, 0, 0)
DARKRED = (155, 0, 0)
LITEGREEN = (0, 255, 0)
DARKGREEN = (0, 180, 0)
LITEBLUE = (0, 0, 255)
DARKBLUE = (0, 0, 155)
LITEYELLOW = (255, 255, 0)
DARKYELLOW = (200, 200, 0)
LITEPURPLE = (255, 0, 255)
DARKPURPLE = (155, 0, 155)
LITEORANGE = (255, 128, 0)
DARKORANGE = (255, 75, 0)
LITETEAL = (0, 175, 175)
DARKTEAL = (0, 128, 128)

BGCOLOR = BLACK
TEXTCOLOR = WHITE
GRIDCOLOR = GRAY

ROTATE_CW = 'rotate right'
ROTATE_CCW = 'rotate left'

PIECE_T = 't-shaped piece'
PIECE_L = 'l-shaped piece 1'
PIECE_J = 'j-shaped piece 2'
PIECE_Z = 'z-shaped piece 1'
PIECE_S = 's-shaped piece 2'
PIECE_O = 'o-shaped piece' 
PIECE_I = 'i-shaped piece'

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

PIVOT = CURRENTPIECE = 0
NEXTPIECE = 1

CURRENTPIECE_STARTX = int(CELLWIDTH_TETRIS/2)
CURRENTPIECE_STARTY = 1
NEXTPIECE_STARTX = 19 ## requires tweaking if window dimensions are changed
NEXTPIECE_STARTY = 6 ## requires tweaking if window dimensions are changed

def find_move(coords):
    '''Calculates the direction of motion

        Arguments: Two center variables used to determine direction of motion

        Returns: A string specifying the direction of motion'''
    # check if translation in x or y direction
    # print(coords)
    if(len(coords) == 0):
        return "NONE"
    elif(coords[0] < width / 4):
        return "LEFT"
    elif(coords[0] > 3 * width / 4):
        return "RIGHT"
    elif(coords[1] > 3 * height / 4):
        return "DOWN"
    elif(coords[1] < height / 4):
        return "UP"
    else:
        return "NONE"

def main():

    # main function

    global FPSCLOCK, DISPLAYSURF, BASICFONT

    # print("Works 1")

    pygame.init()

    # print("Works 1")

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH_TOTAL, WINDOWHEIGHT))
    BASICFONT = pygame.font.SysFont('Courier New', 24)
    pygame.display.set_caption('Tetris')

    while True:
        pygame.mixer.music.load('tetrissong.mid')
        pygame.mixer.music.play(-1, 0.0)
        runGame()
        pygame.mixer.music.stop()
        showGameOver()

def runGame():

    # run the game

    # print("Works 5")

    pieces = [[],[]]

    currentPieceShape, currentPieceColors = generatePiece()
    nextPieceShape, nextPieceColors = generatePiece()
    pieces[CURRENTPIECE] = placePiece(currentPieceShape, currentPieceColors, CURRENTPIECE_STARTX, CURRENTPIECE_STARTY)
    pieces[NEXTPIECE] = placePiece(nextPieceShape, nextPieceColors, NEXTPIECE_STARTX, NEXTPIECE_STARTY)

    pile = []
    pieceMoveCounter = 0
    totalScore = 0

    movePieceLeft = False
    movePieceRight = False
    speedUp = False
    lastRotated = datetime.now()

    while True: 

        grabbed, frame = cap.read()
        frame = imutils.resize(frame, width=width, height=height)
        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, greenLower, greenUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        radius = -1
        x, y = width / 2, height / 2

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(2) & 0xFF

        # print("Works 1")

        coords = cv2.findContours(
            mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # print("Works 2")

        if len(coords) > 0:
            circle_1 = max(coords, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(circle_1)
            M = cv2.moments(circle_1)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # print("Works 3")

        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

        # print("Works 4")

        pieceMoveCounter += 1

        if pieceMoveCounter % 3 == 0 and (pieceHitBottom(pieces[CURRENTPIECE]) or pieceHitPileFromTop(pieces[CURRENTPIECE], pile)):
            addPieceToPile(pieces[CURRENTPIECE], pile)
            currentPieceShape, currentPieceColors = nextPieceShape, nextPieceColors
            pieces[CURRENTPIECE] = placePiece(currentPieceShape, currentPieceColors, CURRENTPIECE_STARTX, CURRENTPIECE_STARTY)
            nextPieceShape, nextPieceColors = generatePiece()
            pieces[NEXTPIECE] = placePiece(nextPieceShape, nextPieceColors, NEXTPIECE_STARTX, NEXTPIECE_STARTY)
            pieceMoveCounter = 0
        elif pieceMoveCounter % 4 == 0: 
            movePiece(pieces[CURRENTPIECE], DOWN) 
            pieceMoveCounter = 0

        if movePieceLeft and pieceHitSide(pieces[CURRENTPIECE]) != 'LEFT WALL' and not pieceHitPileFromRight(pieces[CURRENTPIECE], pile):
            movePiece(pieces[CURRENTPIECE], LEFT)

        if movePieceRight and pieceHitSide(pieces[CURRENTPIECE]) != 'RIGHT WALL' and not pieceHitPileFromLeft(pieces[CURRENTPIECE], pile):
            movePiece(pieces[CURRENTPIECE], RIGHT)

        if speedUp:
            speedFactor = 100
        else:
            speedFactor = 1
            # speedFactor = 3

        move = find_move([x, y])
        print(move)

        if move == "UP":
            speedUp = False
            print((datetime.now() - lastRotated).seconds)
            if((datetime.now() - lastRotated).seconds > 1):
                pieces[CURRENTPIECE] = rotatePiece(pieces[CURRENTPIECE], pile)
                lastRotated = datetime.now()
        elif move == "LEFT":
            movePieceLeft = True
            speedUp = False
        elif move == "RIGHT":
            movePieceRight = True
            speedUp = False
        elif move == "DOWN":
            speedUp = True
        else:
            movePieceLeft = False
            movePieceRight = False
            speedUp = False

        # for event in pygame.event.get(): 
        #     if event.type == QUIT:
        #         terminate()
        #     elif event.type == KEYDOWN:
        #         if event.key == K_ESCAPE:
        #             terminate()
        #         if event.key == K_SPACE:
        #             pieces[CURRENTPIECE] = rotatePiece(pieces[CURRENTPIECE], pile)
        #         if event.key == K_LEFT or event.key == K_a:
        #             movePieceLeft = True
        #         if event.key == K_RIGHT or event.key == K_d:
        #             movePieceRight = True
        #         if event.key == K_DOWN or event.key == K_s:
        #             speedUp = True
        #     elif event.type == KEYUP:
        #         if event.key == K_LEFT or event.key == K_a:
        #             movePieceLeft = False
        #         if event.key == K_RIGHT or event.key == K_d:
        #             movePieceRight = False
        #         if event.key == K_DOWN or event.key == K_s:
        #             speedUp = False

        fullRowYs = checkFullRow(pile)
        score = removeAndScoreRows(fullRowYs, pile)
        totalScore += score
        moveRows(fullRowYs, pile)
        
        if gameLose(pieces[CURRENTPIECE], pile):
            break

        DISPLAYSURF.fill(BGCOLOR)
        drawSideWindow()
        drawScore(totalScore)
        drawGrid(0, WINDOWWIDTH_TETRIS, 0, WINDOWHEIGHT)
        drawPieceOrPile(pieces[CURRENTPIECE])
        drawPieceOrPile(pieces[NEXTPIECE])
        drawPieceOrPile(pile)
        pygame.display.update()
        FPSCLOCK.tick(FPS*speedFactor)
        if(not speedUp):
            time.sleep(0.2)
        
        # if key == ord("E"):
        #     break

# cap.release()
# cv2.destroyAllWindows()

def generatePiece():

    # choose random piece

    pieceChoices = (PIECE_T, PIECE_L, PIECE_J, PIECE_Z, PIECE_S, PIECE_O, PIECE_I)
    pieceShape = random.choice(pieceChoices)
    
    if pieceShape == PIECE_T:
        pieceColors = {'lite': LITERED, 'dark': DARKRED}
    elif pieceShape == PIECE_L:
        pieceColors = {'lite': LITEBLUE, 'dark': DARKBLUE}
    elif pieceShape == PIECE_J:
        pieceColors = {'lite': LITEGREEN, 'dark': DARKGREEN}
    elif pieceShape == PIECE_Z:
        pieceColors = {'lite': LITEYELLOW, 'dark': DARKYELLOW}
    elif pieceShape == PIECE_S:
        pieceColors = {'lite': LITEPURPLE, 'dark': DARKPURPLE}
    elif pieceShape == PIECE_O:
        pieceColors = {'lite': LITEORANGE, 'dark': DARKORANGE}
    elif pieceShape == PIECE_I:
        pieceColors = {'lite': LITETEAL, 'dark': DARKTEAL}

    return pieceShape, pieceColors
    
def placePiece(pieceShape, pieceColors, startx, starty):

    # place piece at starting coordinates

    if pieceShape == PIECE_T:
        pieceColors = {'lite': LITERED, 'dark': DARKRED}
        piece = [{'x': startx     , 'y': starty     , 'block colors': pieceColors}, # pivot point
                 {'x': startx - 1 , 'y': starty     , 'block colors': pieceColors},
                 {'x': startx + 1 , 'y': starty     , 'block colors': pieceColors},
                 {'x': startx     , 'y': starty + 1 , 'block colors': pieceColors}]

    elif pieceShape == PIECE_L:
        pieceColors = {'lite': LITEBLUE, 'dark': DARKBLUE}
        piece = [{'x': startx     , 'y': starty     , 'block colors': pieceColors}, # pivot point
                 {'x': startx - 1 , 'y': starty     , 'block colors': pieceColors},
                 {'x': startx + 1 , 'y': starty     , 'block colors': pieceColors},
                 {'x': startx - 1 , 'y': starty + 1 , 'block colors': pieceColors}]

    elif pieceShape == PIECE_J:
        pieceColors = {'lite': LITEGREEN, 'dark': DARKGREEN}
        piece = [{'x': startx     , 'y': starty     , 'block colors': pieceColors}, # pivot point
                 {'x': startx - 1 , 'y': starty     , 'block colors': pieceColors},
                 {'x': startx + 1 , 'y': starty     , 'block colors': pieceColors},
                 {'x': startx + 1 , 'y': starty + 1 , 'block colors': pieceColors}]

    elif pieceShape == PIECE_Z:
        pieceColors = {'lite': LITEYELLOW, 'dark': DARKYELLOW}
        piece = [{'x': startx     , 'y': starty     , 'block colors': pieceColors}, # pivot point
                 {'x': startx - 1 , 'y': starty     , 'block colors': pieceColors},
                 {'x': startx     , 'y': starty + 1 , 'block colors': pieceColors},
                 {'x': startx + 1 , 'y': starty + 1 , 'block colors': pieceColors}]
                    
    elif pieceShape == PIECE_S:
        pieceColors = {'lite': LITEPURPLE, 'dark': DARKPURPLE}
        piece = [{'x': startx     , 'y': starty     , 'block colors': pieceColors}, # pivot point
                 {'x': startx + 1 , 'y': starty     , 'block colors': pieceColors},
                 {'x': startx     , 'y': starty + 1 , 'block colors': pieceColors},
                 {'x': startx - 1 , 'y': starty + 1 , 'block colors': pieceColors}]
                    
    elif pieceShape == PIECE_O:
        pieceColors = {'lite': LITEORANGE, 'dark': DARKORANGE}
        piece = [{'x': startx     , 'y': starty     , 'block colors': pieceColors}, # pivot point
                 {'x': startx + 1 , 'y': starty     , 'block colors': pieceColors},
                 {'x': startx     , 'y': starty + 1 , 'block colors': pieceColors},
                 {'x': startx + 1 , 'y': starty + 1 , 'block colors': pieceColors}]
        
    elif pieceShape == PIECE_I:
        pieceColors = {'lite': LITETEAL, 'dark': DARKTEAL}
        piece = [{'x': startx     , 'y': starty - 1 , 'block colors': pieceColors}, # pivot point
                 {'x': startx     , 'y': starty     , 'block colors': pieceColors},
                 {'x': startx     , 'y': starty + 1 , 'block colors': pieceColors},
                 {'x': startx     , 'y': starty + 2 , 'block colors': pieceColors}]
                    
    return piece

def movePiece(piece, direction):

    # move piece one cell in specified direction

    if direction == UP:
        for i in range(len(piece)):
            piece[i]['y'] -= 1
    if direction == DOWN:
        for i in range(len(piece)):
            piece[i]['y'] += 1
    if direction == LEFT:
        for i in range(len(piece)):
            piece[i]['x'] -= 1
    if direction == RIGHT:
        for i in range(len(piece)):
            piece[i]['x'] += 1

    return piece

def rotatePiece(piece, pile):

    # rotate piece 90 deg clockwise

    piv_x = piece[PIVOT]['x'] 
    piv_y = piece[PIVOT]['y']

    piece_copy = [{'x': piv_x, 'y': piv_y, 'block colors': piece[PIVOT]['block colors']}]

    for n in range(1, 4):
        
        up          =   {'x': piv_x    , 'y': piv_y - n, 'block colors': piece[PIVOT]['block colors']}
        down        =   {'x': piv_x    , 'y': piv_y + n, 'block colors': piece[PIVOT]['block colors']}
        left        =   {'x': piv_x - n, 'y': piv_y    , 'block colors': piece[PIVOT]['block colors']}
        right       =   {'x': piv_x + n, 'y': piv_y    , 'block colors': piece[PIVOT]['block colors']}
        left_up     =   {'x': piv_x - n, 'y': piv_y - n, 'block colors': piece[PIVOT]['block colors']} 
        right_up    =   {'x': piv_x + n, 'y': piv_y - n, 'block colors': piece[PIVOT]['block colors']}
        left_down   =   {'x': piv_x - n, 'y': piv_y + n, 'block colors': piece[PIVOT]['block colors']}
        right_down  =   {'x': piv_x + n, 'y': piv_y + n, 'block colors': piece[PIVOT]['block colors']}
        
        if up in piece:
            piece_copy.append(right)
        if down in piece:
            piece_copy.append(left)
        if left in piece:
            piece_copy.append(up)
        if right in piece:
            piece_copy.append(down)
        if left_up in piece:
            piece_copy.append(right_up)
        if right_up in piece:
            piece_copy.append(right_down)
        if right_down in piece:
            piece_copy.append(left_down)
        if left_down in piece:
            piece_copy.append(left_up)

    for pieceCopyBlock in piece_copy:
        if pieceCopyBlock['x'] > CELLWIDTH_TETRIS-1 or pieceCopyBlock['x'] < 0 or pieceCopyBlock['y'] > CELLHEIGHT-2: 
            return piece
        for pileBlock in pile:
            if pieceCopyBlock['x'] == pileBlock['x'] and pieceCopyBlock['y'] == pileBlock['y']:
                return piece
    
    return piece_copy

def pieceHitSide(piece):

    # check if piece has collided with side

    for block in piece:
        blockRect = pygame.Rect(block['x']*CELLSIZE, block['y']*CELLSIZE, CELLSIZE, CELLSIZE)
        if blockRect.left == 0:
            return 'LEFT WALL'
        if blockRect.right == WINDOWWIDTH_TETRIS:
            return 'RIGHT WALL'

    return None

def pieceHitBottom(piece):

    # check if piece has collided with wall

    for block in piece:
        blockRect = pygame.Rect(block['x']*CELLSIZE, block['y']*CELLSIZE, CELLSIZE, CELLSIZE)
        if blockRect.bottom == WINDOWHEIGHT:
            return True
        
    return False

def addPieceToPile(piece, pile):

    # add piece to pile

    for block in piece:
        pile.append(block)

def pieceHitPileFromTop(piece, pile):

    # check if piece has collided with pile from top

    for pieceBlock in piece:
        pieceBlockRect = pygame.Rect(pieceBlock['x']*CELLSIZE, pieceBlock['y']*CELLSIZE, CELLSIZE, CELLSIZE)
        for pileBlock in pile:
            pileBlockRect = pygame.Rect(pileBlock['x']*CELLSIZE, pileBlock['y']*CELLSIZE, CELLSIZE, CELLSIZE)
            if pieceBlockRect.right == pileBlockRect.right and pieceBlockRect.left == pileBlockRect.left and pieceBlockRect.bottom == pileBlockRect.top:
                return True

    return False

def pieceHitPileFromLeft(piece, pile):

    # check if piece has collided with pile from left

    for pieceBlock in piece:
        pieceBlockRect = pygame.Rect(pieceBlock['x']*CELLSIZE, pieceBlock['y']*CELLSIZE, CELLSIZE, CELLSIZE)
        for pileBlock in pile:
            pileBlockRect = pygame.Rect(pileBlock['x']*CELLSIZE, pileBlock['y']*CELLSIZE, CELLSIZE, CELLSIZE)
            if pieceBlockRect.bottom == pileBlockRect.bottom and pieceBlockRect.top == pileBlockRect.top and pieceBlockRect.right == pileBlockRect.left:
                return True

    return False

def pieceHitPileFromRight(piece, pile):

    # check if piece has collided with pile from right

    for pieceBlock in piece:
        pieceBlockRect = pygame.Rect(pieceBlock['x']*CELLSIZE, pieceBlock['y']*CELLSIZE, CELLSIZE, CELLSIZE)
        for pileBlock in pile:
            pileBlockRect = pygame.Rect(pileBlock['x']*CELLSIZE, pileBlock['y']*CELLSIZE, CELLSIZE, CELLSIZE)
            if pieceBlockRect.bottom == pileBlockRect.bottom and pieceBlockRect.top == pileBlockRect.top and pieceBlockRect.left == pileBlockRect.right:
                return True

    return False

def checkFullRow(pile):

    # checks if there is a full row in pile, returns row value (y coordinate) if full

    blockInCell = blankBoolDS(CELLWIDTH_TETRIS, CELLHEIGHT)
    fullRowYs = []

    for block in pile:
        blockInCell[block['y']][block['x']] = True

    for y in range(CELLHEIGHT):
        if False not in blockInCell[y][:]:
            fullRowYs.append(y)

    return fullRowYs

def removeAndScoreRows(fullRowYs, pile):

    # remove all dicts in pile with y in fullRowYs (list of full rows, y coordinates)
    # scoring -> 1 row = 100*1 points, 2 rows = 200*2 pnts, 3 rows = 300*3 points

    for block in pile[:]:
        if block['y'] in fullRowYs:
            pile.remove(block)

    if len(fullRowYs) > 0: 
        score = 100*len(fullRowYs)*len(fullRowYs)
    else:
        score = 0

    return score

def moveRows(fullRowYs, pile):

    # move blocks in pile based on which rows are empty (initially full but removeRows used)

    n = 0
    nList = []
    fullRowYs = sorted(fullRowYs)

    for row in range(CELLHEIGHT, -1, -1):
        if len(fullRowYs) > 0 and row < fullRowYs[-1]:
            n += 1
            fullRowYs.remove(fullRowYs[-1])
        nList.append(n)

    nList = list(reversed(nList))

    for block in pile:
        block['y'] += nList[block['y']]

def blankBoolDS(sizeX, sizeY):

    # creates "blank" boolean data structure (all False values)

    boolDS = []
    for y in range(sizeY):
        boolDS.append([False]*sizeX)

    return boolDS

def gameLose(piece, pile):

    # if pile overlaps piece, game over

    for pileBlock in pile:
        if pileBlock['y'] in range(0,2): 
            return True

    return False

def drawPieceOrPile(pieceOrPile):

    # draw piece onto board surface

    for block in pieceOrPile:
        x = block['x'] * CELLSIZE
        y = block['y'] * CELLSIZE
        pieceSegmentOuter = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pieceSegmentInner = pygame.Rect(x+4, y+4, CELLSIZE-8, CELLSIZE-8)
        pygame.draw.rect(DISPLAYSURF, block['block colors']['lite'], pieceSegmentOuter)
        pygame.draw.rect(DISPLAYSURF, block['block colors']['dark'], pieceSegmentInner)

def drawSideWindow():

    # draw side window, which displays next piece and score

    sideWindowRect = pygame.Rect(WINDOWWIDTH_TETRIS, 0, WINDOWWIDTH_SIDE, WINDOWHEIGHT)
    nextPieceRect = pygame.Rect(0, 0, CELLSIZE*5, CELLSIZE*6)
    nextPieceRect.centerx = WINDOWWIDTH_TETRIS+0.5*WINDOWWIDTH_SIDE
    nextPieceRect.centery = 140 ## number found after significant tweaking

    pygame.draw.rect(DISPLAYSURF, BGCOLOR, sideWindowRect)
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, nextPieceRect)

def drawScore(totalScore):

    # draw score onto side window
    
    scoreTitleSurf = BASICFONT.render('SCORE:', True, TEXTCOLOR)
    scoreTitleRect = scoreTitleSurf.get_rect()
    scoreTitleRect.centerx = WINDOWWIDTH_TETRIS+0.5*WINDOWWIDTH_SIDE
    scoreTitleRect.centery = 370
    DISPLAYSURF.blit(scoreTitleSurf, scoreTitleRect)
    
    scoreNumberSurf = BASICFONT.render('%s' %(totalScore), True, TEXTCOLOR)
    scoreNumberRect = scoreNumberSurf.get_rect()
    scoreNumberRect.centerx = WINDOWWIDTH_TETRIS+0.5*WINDOWWIDTH_SIDE
    scoreNumberRect.centery = scoreTitleRect.centery + 30
    DISPLAYSURF.blit(scoreNumberSurf, scoreNumberRect)
    
def drawGrid(start_x, end_x, start_y, end_y):

    # draw gridlines

    for x in range(start_x, end_x+CELLSIZE, CELLSIZE): ## +CELLSIZE added to add grid line between tetris window and side window
        pygame.draw.line(DISPLAYSURF, GRIDCOLOR, (x, start_y), (x, end_y))
    for y in range(start_y, end_y, CELLSIZE): 
        pygame.draw.line(DISPLAYSURF, GRIDCOLOR, (start_x, y), (end_x, y))

def showGameOver():

    # shows game over screen
    
    gameOverFont = pygame.font.SysFont('Courier New', 36)
    gameSurf = gameOverFont.render('GAME', True, TEXTCOLOR)
    overSurf = gameOverFont.render('OVER', True, TEXTCOLOR)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.centerx = WINDOWWIDTH_TETRIS+0.5*WINDOWWIDTH_SIDE
    gameRect.centery = 270
    overRect.centerx = WINDOWWIDTH_TETRIS+0.5*WINDOWWIDTH_SIDE
    overRect.centery = gameRect.centery + 30

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

def drawPressKeyMsg():

    # shows "press any key to continue)

    pressKeyFont = pygame.font.SysFont('Courier New', 16)

    pressKey1Surf = pressKeyFont.render('PRESS ANY KEY', True, TEXTCOLOR)
    pressKey1Rect = pressKey1Surf.get_rect()
    pressKey1Rect.centerx = WINDOWWIDTH_TETRIS+0.5*WINDOWWIDTH_SIDE
    pressKey1Rect.centery = 460
    DISPLAYSURF.blit(pressKey1Surf, pressKey1Rect)

    pressKey2Surf = pressKeyFont.render('TO PLAY AGAIN', True, TEXTCOLOR)
    pressKey2Rect = pressKey2Surf.get_rect()                    
    pressKey2Rect.centerx = WINDOWWIDTH_TETRIS+0.5*WINDOWWIDTH_SIDE
    pressKey2Rect.centery = pressKey1Rect.centery + 20
    DISPLAYSURF.blit(pressKey2Surf, pressKey2Rect)

def checkForKeyPress():

    # checks for key press and reacts accordingly
    
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

def terminate():

    # exit program 
        
    pygame.quit()
    sys.exit()
        
if __name__ == '__main__':
    main()

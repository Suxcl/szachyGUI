import pygame
from classes.constants import *
from classes.static_colors import *
# --- miscellaneous ---

def getColorOfSquare(x,y):
    return BLACK if (x + y) % 2 == 0 else WHITE

def getRectForCoordinates(x,y):
    return pygame.Rect(y * SQUARE_SIZE, x * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)

def getRectForSQ(sq):
    return pygame.Rect(sq[1] * SQUARE_SIZE, sq[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)

def getCircleForCoordinates(x,y, color):
    return pygame.circle(color, )

def checkIfSquareHasPiece(x,y, cb):
    if(cb[x][y]!=''): return True
    return False

def transformListOfTuplesIntoRect(l):
    return [getRectForCoordinates(a[0], a[1]) for a in l]

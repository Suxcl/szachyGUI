import pygame

# Constants
IMG_SIZE = 60
ROWS, COLS = 8, 8
SQUARE_SIZE = 60
WIDTH, HEIGHT = IMG_SIZE*ROWS*2, IMG_SIZE*COLS
CHESSBOARD_WIDTH = SQUARE_SIZE*ROWS
CHESSBOARD_HEIGHT = SQUARE_SIZE*COLS

CHESSBOARD_SQUARES_POS = [(a * SQUARE_SIZE, b * SQUARE_SIZE) for a in range(ROWS) for b in range(COLS)]

MAIN_MENU_BUTTON_HOR_POS = WIDTH-200
MAIN_MENU_BUT_WIDTH = 100
MAIN_MENU_BUT_HEIGHT = 50
MAIN_MENU_BUTTONS_POS = []
MAIN_MENU_BUTTONS_NAMES = ['start', 'continue', 'credits', 'quit']
how_many_buttons = 4
offset = 5*(10+MAIN_MENU_BUT_HEIGHT)+80
tmp = HEIGHT
for a in range(4):
    MAIN_MENU_BUTTONS_POS.append((MAIN_MENU_BUTTON_HOR_POS, HEIGHT-offset))
    offset = offset -(MAIN_MENU_BUT_HEIGHT+10)

# main manu

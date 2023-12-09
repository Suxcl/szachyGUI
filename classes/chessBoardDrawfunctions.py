import pygame
from classes.static_colors import *
from classes.constants import *
from classes.miscellaneous import *
from classes.pieces_path import *
# --- square drawings ---

# defining colors of the chessboard
def draw_chessboard(screen, chessboard):
    for row in range(ROWS):
        for col in range(COLS):
            color = getColorOfSquare(col,row)
            rect = getRectForCoordinates(row,col)
            pygame.draw.rect(screen, color, rect)
            piece = chessboard[row][col]
            if(piece != ''):
                img = pygame.image.load(pieces_paths[piece]).convert_alpha()
                screen.blit(img, rect)

# define buttons for clicking purposes
def draw_chessboard_buttons():
    buttons = []
    for row in range(ROWS):
        for col in range(COLS):                
            button_rect = getRectForCoordinates(row,col)
            buttons.append(button_rect)
    # print("Buttons", buttons)
    return buttons

def clearSquare(screen, square):
    x = square[0]
    y = square[1]
    color = getColorOfSquare(x,y)
    rect = getRectForCoordinates(x,y)
    pygame.draw.rect(screen, color, rect)
    return

def rednerPieceInSquare(screen, square, piece):
    x = square[0]
    y = square[1]
    color = getColorOfSquare(x,y)
    rect = getRectForCoordinates(x,y)
    pygame.draw.rect(screen, color, rect)
    img = pygame.image.load(pieces_paths[piece]).convert_alpha()
    screen.blit(img, rect)

def highlightSquareWithPiece(screen, square, piece):
    x = square[0]
    y = square[1]
    color = GREEN
    rect = getRectForCoordinates(x,y)
    pygame.draw.rect(screen, color, rect)
    img = pygame.image.load(pieces_paths[piece]).convert_alpha()
    screen.blit(img, rect)
    return rect

def highlightSquare(screen, square):
    x = square[0]
    y = square[1]
    color = GREEN
    rect = getRectForCoordinates(x,y)
    pygame.draw.rect(screen, color, rect)

# def unhighlightSquareWithPiece(screen, x,y,piece):
#     color = getColorOfSquare(x,y)
#     rect = getRectForCoordinates(x,y)
#     pygame.draw.rect(screen, color, rect)
#     img = pygame.image.load(pieces_paths[piece]).convert_alpha()
#     screen.blit(img, rect)

def unhighlightSquare(screen,square):
    x = square[0]
    y = square[1]
    color = getColorOfSquare(x,y)
    rect = getRectForCoordinates(x,y)
    pygame.draw.rect(screen, color, rect)

def highlightSquareAsMove(screen, square):
    x = square[0]
    y = square[1]
    color = GRAY
    pygame.draw.circle(screen, color, (y*SQUARE_SIZE+SQUARE_SIZE/2, x*SQUARE_SIZE+SQUARE_SIZE/2), SQUARE_SIZE/6) 

def highlightSquareAsAttack(screen, square):
    x = square[0]
    y = square[1]
    color = RED
    pygame.draw.circle(screen, color, (y*SQUARE_SIZE+SQUARE_SIZE/2, x*SQUARE_SIZE+SQUARE_SIZE/2), SQUARE_SIZE/6) 

def cancelSelectedSquareHighlight(screen, square, piece, moves, attacks, attack_pieces):
    rednerPieceInSquare(screen,square, piece)
    for a in moves:
        clearSquare(screen,a)
    for a in range(len(attacks)):
        rednerPieceInSquare(screen, (attacks[a][0], attacks[a][1]), attack_pieces[a])
    
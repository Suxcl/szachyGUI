import pygame
import sys

from classes.chessboard import chessboard
from classes.dicts import *
from classes.pieces_path import pieces_paths
from classes.constants import *
from classes.colors import *

import logging
logging.basicConfig(filename='example.log',format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', encoding='utf-8', level=logging.DEBUG)
logging.debug("Launching Main.py")


for a in CHESSBOARD_SQUARES_POS:
    print(a)





# c--- ustom cursor handling ---

def changeCursorToPiece(piece):
    piece_img_path = pieces_paths[piece]
    surf = pygame.image.load(piece_img_path).convert_alpha()
    cursor = pygame.cursors.Cursor((15,15), surf)
    pygame.mouse.set_cursor(cursor)

def changeCursorToHand():
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

# --- miscellaneous ---

def getColorOfSquare(x,y):
    return BLACK if (x + y) % 2 == 0 else WHITE

def getRectForCoordinates(x,y):
    return pygame.Rect(y * SQUARE_SIZE, x * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)

def getCircleForCoordinates(x,y, color):
    return pygame.circle(color, )

def checkIfSquareHasPiece(x,y, cb):
    if(cb[x][y]!=''): return True
    return False


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
    print("Buttons", buttons)
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

# def highlightSquare(screen, x,y):
#     color = GREEN
#     rect = getRectForCoordinates(x,y)
#     pygame.draw.rect(screen, color, rect)

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
    # cir = getCircleForCoordinates(x,y, color)
    rect = getRectForCoordinates(x,y)
    pygame.draw.circle(screen, color, (y*SQUARE_SIZE+SQUARE_SIZE/2, x*SQUARE_SIZE+SQUARE_SIZE/2), SQUARE_SIZE/6) 

def highlightSquareAsAttack(screen, square):
    x = square[0]
    y = square[1]
    color = RED
    cir = getCircleForCoordinates(x,y, color)
    pygame.draw.circle(screen, color, cir)

def cancelSelectedSquareHighlight(screen, square, piece, moves, attacks, attack_pieces):
    rednerPieceInSquare(screen,square, piece)
    for a in moves:
        clearSquare(screen,a)
    for a in range(len(attacks)):
        rednerPieceInSquare(screen, (attacks[a][0], attacks[a][1]), attack_pieces[a])
    

def joinSquaresToRefresh(selected, moves, attacks):
    tmp = []
    tmp.append(getRectForCoordinates(selected[0], selected[1]))
    tmp+=moves
    tmp+=attacks
    return tmp

def updateScreen(squares):
    pygame.display.update(squares)
# --- main ---

def main():

    cb = chessboard()
    cb.newBoard()
    res = cb.returnBoard()

    # for a in range(len(res)):
    #     for b in range(len(res[a])):
    #         print(res[a][b], a, b)

    # for a in res:
    #     print(a)


    pygame.init() # x
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # cheesBoard_surface = pygame.surface.
    pygame.display.set_caption("Chessboard with Buttons")
    clock = pygame.time.Clock()

    draw_chessboard(screen, res) 
    buttons = draw_chessboard_buttons()

    
    
    last_turn_choosen_field = None
    last_turn_des = None

    selected_square = []
    piece_in_square = None
    move_rect = []
    attacks_rect = []
    moves = []
    attacks = []


    

# wybranie pionka - podswietlenie pola z pionekime, pokazanie mozliwych ruchów, niezrobienie nieczego jesli pionek należy do przecinweo gracza
# ponownie kliknecie na wybranym polu zpowoduje odwybranie pionka
# przesuniecie/klikniecie go na pole z możliwym ruchem - podswietlenie skąd i dokąd pinek sie ruszył, usuniecie pokazanych ruchów na planszy
# ruch przeciwnika
# 
# w momencie kliknecia w pinek powinien on podac ruchy i powinny one zostal przedstawione na planszy
# 

    refereshed_once = False

    while True:
        
        squares_to_update = []

        def refreshScreen():
            pygame.display.update(squares_to_update)
            squares_to_update = []



        for event in pygame.event.get():
            # closing game on clicking the red X
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # catching mouse down event
            if event.type == pygame.MOUSEBUTTONDOWN:
            
                if event.button == 1:  # Left mouse button
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    x, y = event.pos
                    for i, button in enumerate(buttons):
                        if button.collidepoint(x, y):
                            x_row = y // SQUARE_SIZE
                            y_col = x // SQUARE_SIZE
                            
                            if(selected_square):
                                # clear selected square and its moves
                                cancelSelectedSquareHighlight(screen, selected_square, piece, moves, attacks, attacks_pieces)
                                squares_to_update = joinSquaresToRefresh(selected_square, move_rect, attacks_rect)
                                selected_square = []
                            

                            if(cb.checkIfFieldHasSameColorASCurrentPlayer(x_row, y_col)):

                                # if(checkIfSquareHasPiece(x_row, y_col, res)):
                                selected_square = (x_row, y_col)
                                piece = res[x_row][y_col]
                                piece_in_square = piece
                                moves, attacks = cb.GetPossibleMoves(x_row, y_col)
                                move_rect = []
                                attacks_rect = []
                                attacks_pieces = []
                                    # FUN SquareSeleected?
                                # chainging cursor to picked up piece
                                changeCursorToPiece(piece)
                                # changing color of selected swuare
                                highlightSquareWithPiece(screen, selected_square, piece)
                                # drawing possible moves 
                                
                                for c in moves:
                                    move_rect.append(getRectForCoordinates(c[0],c[1]))
                                    highlightSquareAsMove(screen, c)
                                # drawing possibles attacks
                                for c in attacks:
                                    attacks_rect.append(getRectForCoordinates(c[0],c[1]))
                                    attacks_pieces.append(res[a[0]][a[1]])
                                    highlightSquareAsAttack(screen, c)
                                

                                squares_to_update = joinSquaresToRefresh(selected_square, move_rect, attacks_rect)

                                

                            print(f"Button clicked: {i} ({i // COLS}, {i % COLS})")
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    changeCursorToHand()
                    # handling if cursor with piece is at move possible Square
                    x, y = event.pos
                    if(selected_square and selected_square == (x,y)):
                        rect = getRectForCoordinates(selected_square[0], selected_square[1])

                        if rect.collidepoint(x,y):
                            cancelSelectedSquareHighlight(screen, selected_square, piece, moves, attacks, attacks_pieces)
                            squares_to_update = joinSquaresToRefresh(selected_square, move_rect, attacks_rect)
                            selected_square = []

                    for pos in move_rect:
                        if pos.collidepoint(x, y):
                            x_row = y // SQUARE_SIZE
                            y_col = x // SQUARE_SIZE
                            print('clicked on posible move')
                    for pos in move_rect:
                        if pos.collidepoint(x, y):
                            x_row = y // SQUARE_SIZE
                            y_col = x // SQUARE_SIZE
                            print('clicked on posible move')
                    
                    
            if event.type in [pygame.WINDOWSHOWN, pygame.WINDOWENTER, pygame.WINDOWFOCUSGAINED, pygame.WINDOWRESTORED]:
                pygame.display.flip()
            
            # if pygame.mouse.get_pressed()[0]:
            #     try:
            #         print("is hold")
            #     except:
            #         print("is realsed")
        
        
        # print('to update',squares_to_update)
        # pygame.display.flip()
        # if False==refereshed_once:
        #    pygame.display.update()
        #    pygame.display.flip()
        #    refereshed_once = True
        if(squares_to_update):
            print(squares_to_update)
            pygame.display.update(squares_to_update)    
            squares_to_update = []
        clock.tick(30)

if __name__ == "__main__":
    main()

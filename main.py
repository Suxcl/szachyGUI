import pygame
import sys

import pygame_gui
# import pygame_gui



pygame.init() 
from classes.logic.chessboard import chessboard
from classes.logic.dicts import *
from classes.pieces_path import pieces_paths
from classes.constants import *
from classes.static_colors import *
from classes.miscellaneous import* 
from classes.chessBoardDrawfunctions import *
from classes.cursorHandling import *


import logging
logging.basicConfig(filename='example.log',format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', encoding='utf-8', level=logging.DEBUG)
logging.debug("Launching Main.py")

pygame.font.init()
FONT = pygame.font.Font(None, 24)

def draw_button(screen, x, y, width, height, text):
    print('drawing rect as button: ',screen, x, y, width, height, text)
    # Check for mouse hover
    mouse_x, mouse_y = pygame.mouse.get_pos()
    hover = x < mouse_x < x + width and y < mouse_y < y + height

    # Draw the button
    button_color = BUTTON_HOVER if hover else BUTTON_NORMAL
    pygame.draw.rect(screen, button_color, (x, y, width, height),0,5)

    # Draw the text
    button_text = FONT.render(text, True, TEXT_WHITE)
    text_rect = button_text.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(button_text, text_rect)


    menu_display = pygame.Rect(0,0,WIDTH*10, HEIGHT)
    # menu_display = pygame.Surface((WIDTH, HEIGHT), flags=0, depth=0)

    # menu_display.background(WHITE)
    screen.blit(screen, menu_display)


# --- main ---
def main():
    # creating chessboard class
    cb = chessboard()
    cb.newBoard()
    res = cb.returnBoard()
    for a in res:
        
        print("res", a)


    # pygame.init() 
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("pygame Chess - Sak Jakub")

    # menu = pygame.Surface((WIDTH, HEIGHT))
    

    # rect = pygame.Rect(0,0,WIDTH,HEIGHT)
    # pygame.draw.rect(menu, WHITE, rect)
    # pygame.display.flip()
    
    # values for gameplay
    buttons = draw_chessboard_buttons()
    selected_square = []        # selected square to move from
    piece_in_square = None      # piece value from sq
    moves = []                  # list of moves x,y coordinates
    attacks = []                # list of attacks x,y coordinates
    attacks_pieces = []             # list of pieces in attack positions
    last_turn_choosen_field = None  # last turn data for clearing purposes
    last_turn_des = None            # --||--    
    last_turn_piece = None          # --||--


    is_running = True
    

    refreshOnce = True
    squares_to_update = []
    draw_chessboard(screen, res)
    for row in range(ROWS):
        for col in range(COLS):
            squares_to_update.append(getRectForSQ((row,col)))
    print(squares_to_update)
            

    # game display
    while is_running:
        time_delta = clock.tick(60)/1000.0
        squares_to_update = []

        for event in pygame.event.get():

            # closing game on clicking the red X
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


            # catching mouse down event
            if event.type == pygame.MOUSEBUTTONDOWN:
                print('event MOUSEBUTTONDOWn trigger')

                # Left mouse button event
                if event.button == 1:  
                    x, y = event.pos
                    x_row, y_col = y // SQUARE_SIZE,x // SQUARE_SIZE    
                    print("event.button == 1 trigger")
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                
                    
                    
                    for i, button in enumerate(buttons):
                        if button.collidepoint(x, y):
                            print(f"Button clicked: {i} ({i // COLS}, {i % COLS})")
                            # if there is selected square we need to clear 
                            # clear selected square and its movesa dn attacks when
                            # if(selected_square): 
                            #     print("if selected_square in MOUSEBUTTONDOWN trigger")
                            #     cancelSelectedSquareHighlight(screen, selected_square, piece, moves, attacks, attacks_pieces)
                            #     squares_to_update = joinSquaresToRefresh(selected_square, move_rect, attacks_rect)
                            #     selected_square = []
    
                            # checking if selected square belongs to current player
                            # if true render possible moves and attacks for sleected piece
                            if(cb.checkIfFieldHasSameColorASCurrentPlayer(x_row, y_col)):
                                selected_square = (x_row, y_col)
                                print("eh")
                                print(x_row, y_col)
                                print(res[x_row][y_col])
                                piece_in_square = res[x_row][y_col]
                                moves, attacks = cb.GetPossibleMoves(x_row, y_col)
                                
                                # chainging cursor to picked up piece
                                changeCursorToPiece(piece_in_square)
                                # changing color of selected square
                                highlightSquareWithPiece(screen, selected_square, piece_in_square)
                                
                                # drawing possible moves and atacks 
                                [highlightSquareAsMove(screen, c) for c in moves]
                                [highlightSquareAsAttack(screen, c) for c in attacks]

                                # adding squares for update
                                squares_to_update.append(getRectForSQ(selected_square))
                                squares_to_update+=transformListOfTuplesIntoRect(moves)
                                squares_to_update+=transformListOfTuplesIntoRect(attacks)
                                
            
            
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and selected_square!=[]:        
                    
                    x, y = event.pos
                    x_to, y_to = y // SQUARE_SIZE, x // SQUARE_SIZE
                    move_detected = False
                    print(f"Button unclicked: {i} ({i // COLS}, {i % COLS})")

                    # chaning cursor to simple hand
                    changeCursorToHand()

                    # checking if unlicked position corresponds to move
                    for pos in transformListOfTuplesIntoRect(moves):
                        if pos.collidepoint(x, y) and selected_square!=[]:
                            print('clicked on posible move')
                            move_detected = True

                    for pos in transformListOfTuplesIntoRect(attacks):
                        if pos.collidepoint(x, y) and selected_square!=[]:
                            print('clicked on posible attack')
                            move_detected = True
                        
                    if move_detected:

                        # clearing last turn highlisht
                        if(last_turn_des != None):
                            print("Clearing last turn highlights", last_turn_choosen_field, last_turn_des, piece_in_square)
                            clearSquare(screen, last_turn_choosen_field)
                            rednerPieceInSquare(screen, last_turn_des, last_turn_piece)
                            squares_to_update.append(getRectForSQ(last_turn_des))
                            squares_to_update.append(getRectForSQ(last_turn_choosen_field))

                        x_from,y_from = selected_square
                        last_turn_des = (x_to, y_to)
                        last_turn_choosen_field = selected_square

                        # move 
                        print("moving piece",piece_in_square, x_from, y_from, x_to, y_to)
                        cb.newMoveFromAtoB(x_from, y_from, x_to, y_to)

                        # clear squres for moves and rerender pieces on attacks
                        [clearSquare(screen, a) for a in moves]
                        for a in range(len(attacks)):
                            x_tmp, y_tmp = attacks[a][0],attacks[a][1]
                            rednerPieceInSquare(screen, (x_tmp, y_tmp), res[x_tmp][y_tmp])
                        
                        # highlight squares from and to
                        highlightSquare(screen, selected_square)
                        highlightSquareWithPiece(screen, last_turn_des, piece_in_square)
                        last_turn_choosen_field = selected_square
                        last_turn_piece = piece_in_square
                        
                        squares_to_update.append(getRectForSQ(selected_square))
                        squares_to_update+=transformListOfTuplesIntoRect(moves)
                        squares_to_update+=transformListOfTuplesIntoRect(attacks)
                        selected_square = []
                        move_detected = False

                    # when piece is dragged onto illegal spot
                    if(selected_square):
                        cancelSelectedSquareHighlight(screen, selected_square, piece_in_square, moves, attacks, attacks_pieces)
                        squares_to_update.append(getRectForSQ(selected_square))
                        squares_to_update+=transformListOfTuplesIntoRect(moves)
                        squares_to_update+=transformListOfTuplesIntoRect(attacks)
                        selected_square = []
                    
                    

            # for screen refreshing once on start                    
            if event.type in [pygame.WINDOWSHOWN, pygame.WINDOWENTER, pygame.WINDOWFOCUSGAINED, pygame.WINDOWRESTORED]:
                pygame.display.flip()

        if(refreshOnce == True): 
            print("refresh once")
            pygame.display.flip()
            refreshOnce = False
        if(squares_to_update):
            print("list to refresh:")
            for a in squares_to_update:
                print(a, "|row -",a[1]//SQUARE_SIZE,'col -',a[0]//SQUARE_SIZE)
                
            pygame.display.update(squares_to_update)   
            squares_to_update = []
            res = cb.returnBoard()
    

if __name__ == "__main__":
    main()

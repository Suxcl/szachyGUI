import pygame._view
from pygame import *
from random import *

import os
import sys
import platform
sys.path.append('modules')  # Access my module folder for importing

from menu import *

if platform.system() == 'Windows':
    os.environ['SDL_VIDEODRIVER'] = 'windib'    # Ensure compatability
os.environ['SDL_VIDEO_CENTERED'] = '1'  # Centre game window

# ############################################################################ #
# #    Worked on for 6:30                                                    # #
# ############################################################################ #

init()

screen = display.set_mode((600,600))

def reset_game():
    """Puts all of the pieces back"""

    global game_board, turn, wcastle, bcastle, wcaptured, bcaptured
    close_menu(win_menu)
    win_menu.event_off(5)
    win_menu.event_off(6)
    deselect_piece()
    turn = 1
    wcastle = 0
    bcastle = 0
    wcaptured = []
    bcaptured = []
    game_board[0] = 'R1'; game_board[7] = 'R1'; game_board[-1] = 'R2'; game_board[-8] = 'R2'
    game_board[1] = 'N1'; game_board[6] = 'N1'; game_board[-2] = 'N2'; game_board[-7] = 'N2'
    game_board[2] = 'B1'; game_board[5] = 'B1'; game_board[-3] = 'B2'; game_board[-6] = 'B2'
    game_board[4] = 'K1'; game_board[3] = 'Q1'; game_board[-4] = 'K2'; game_board[-5] = 'Q2'
    for i in range(8):
        game_board[8+i] = 'P1'
        game_board[48+i] = 'P2'
    for i in range(32):
        game_board[16+i] = None


def select_piece(location):
    """Attempts to select the piece at location"""

    global selected,moves,captures

    # Notes:
    # this function is so complicated because it finds where the newly selected piece can move and capture

    # Remove illegal selections
    if game_board[location] == None or game_board[location][1] != str(turn):
        return

    selected = location
    moves = []
    captures = []

    # Pawn for player 1
    if game_board[selected] == 'P1':
        if game_board[selected+8] == None:
            moves.append(selected+8)
            if selected//8 == 1 and game_board[selected+16] == None:
                moves.append(selected+16)
        if selected%8 != 0 and ((game_board[selected+7] != None and game_board[selected+7][1] == '2') or \
                                (game_board[selected-1] == 'P2' and en_passent == selected-1)):
            captures.append(selected+7)
        if selected%8 != 7 and ((game_board[selected+9] != None and game_board[selected+9][1] == '2') or \
                                (game_board[selected+1] == 'P2' and en_passent == selected+1)):
            captures.append(selected+9)

    # Pawn for player 2
    if game_board[selected] == 'P2':
        if game_board[selected-8] == None:
            moves.append(selected-8)
            if selected//8 == 6 and game_board[selected-16] == None:
                moves.append(selected-16)
        if selected%8 != 7 and ((game_board[selected-7] != None and game_board[selected-7][1] == '1') or \
                                (game_board[selected+1] == 'P1' and en_passent == selected+1)):
            captures.append(selected-7)
        if selected%8 != 0 and ((game_board[selected-9] != None and game_board[selected-9][1] == '1') or \
                                (game_board[selected-1] == 'P1' and en_passent == selected-1)):
            captures.append(selected-9)

    # Rook and half of Queen for both players
    if game_board[selected][0] in 'RQ':
        x,y = selected%8,selected//8

        for i in range(x+1,8,1):
            if game_board[i+y*8] == None:   # Check if no blocking piece
                moves.append(i+y*8)
            elif game_board[i+y*8][1] != str(turn): # Check if is attacking
                captures.append(i+y*8)
                break
            else:
                break

        for i in range(x-1,-1,-1):
            if game_board[i+y*8] == None:
                moves.append(i+y*8)
            elif game_board[i+y*8][1] != str(turn):
                captures.append(i+y*8)
                break
            else:
                break

        for i in range(y+1,8,1):
            if game_board[x+i*8] == None:
                moves.append(x+i*8)
            elif game_board[x+i*8][1] != str(turn):
                captures.append(x+i*8)
                break
            else:
                break

        for i in range(y-1,-1,-1):
            if game_board[x+i*8] == None:
                moves.append(x+i*8)
            elif game_board[x+i*8][1] != str(turn):
                captures.append(x+i*8)
                break
            else:
                break

    # Bishop and other half of Queen for both players
    if game_board[selected][0] in 'BQ':

        i = selected+7
        while (i-7)%8 != 0 and (i-7)//8 != 7:   # Check if valid move
            if game_board[i] == None:   # Check if no blocking piece
                moves.append(i)
            elif game_board[i][1] != str(turn): # Check if is attacking
                captures.append(i)
                break
            else:
                break
            i += 7

        i = selected+9
        while (i-9)%8 != 7 and (i-9)//8 != 7:
            if game_board[i] == None:
                moves.append(i)
            elif game_board[i][1] != str(turn):
                captures.append(i)
                break
            else:
                break
            i += 9

        i = selected-7
        while (i+7)%8 != 7 and (i+7)//8 != 0:
            if game_board[i] == None:
                moves.append(i)
            elif game_board[i][1] != str(turn):
                captures.append(i)
                break
            else:
                break
            i -= 7

        i = selected-9
        while (i+9)%8 != 0 and (i+9)//8 != 0:
            if game_board[i] == None:
                moves.append(i)
            elif game_board[i][1] != str(turn):
                captures.append(i)
                break
            else:
                break
            i -= 9

    # Knight for both players
    if game_board[selected][0] == 'N':
        x,y = selected%8,selected//8

        if x >= 2 and y <= 6:   # Check if valid move
            if game_board[(x-2)+(y+1)*8] == None:   # Check if no blocking piece
                moves.append((x-2)+(y+1)*8)
            elif game_board[(x-2)+(y+1)*8][1] != str(turn): # Check if is attacking
                captures.append((x-2)+(y+1)*8)
        if x >= 1 and y <= 5:
            if game_board[(x-1)+(y+2)*8] == None:
                moves.append((x-1)+(y+2)*8)
            elif game_board[(x-1)+(y+2)*8][1] != str(turn):
                captures.append((x-1)+(y+2)*8)

        if x <= 6 and y <= 5:
            if game_board[(x+1)+(y+2)*8] == None:
                moves.append((x+1)+(y+2)*8)
            elif game_board[(x+1)+(y+2)*8][1] != str(turn):
                captures.append((x+1)+(y+2)*8)
        if x <= 5 and y <= 6:
            if game_board[(x+2)+(y+1)*8] == None:
                moves.append((x+2)+(y+1)*8)
            elif game_board[(x+2)+(y+1)*8][1] != str(turn):
                captures.append((x+2)+(y+1)*8)

        if x <= 5 and y >= 1:
            if game_board[(x+2)+(y-1)*8] == None:
                moves.append((x+2)+(y-1)*8)
            elif game_board[(x+2)+(y-1)*8][1] != str(turn):
                captures.append((x+2)+(y-1)*8)
        if x <= 6 and y >= 2:
            if game_board[(x+1)+(y-2)*8] == None:
                moves.append((x+1)+(y-2)*8)
            elif game_board[(x+1)+(y-2)*8][1] != str(turn):
                captures.append((x+1)+(y-2)*8)

        if x >= 1 and y >= 2:
            if game_board[(x-1)+(y-2)*8] == None:
                moves.append((x-1)+(y-2)*8)
            elif game_board[(x-1)+(y-2)*8][1] != str(turn):
                captures.append((x-1)+(y-2)*8)
        if x >= 2 and y >= 1:
            if game_board[(x-2)+(y-1)*8] == None:
                moves.append((x-2)+(y-1)*8)
            elif game_board[(x-2)+(y-1)*8][1] != str(turn):
                captures.append((x-2)+(y-1)*8)

    # King for both players
    if game_board[selected][0] == 'K':
        x,y = selected%8,selected//8
        attacked = attacked_spaces(1+turn%2,game_board)

        if selected == 3 and wcastle%2 == 0 and \
           game_board[1] == None and game_board[2] == None and\
           not 1 in attacked and not 2 in attacked and not 3 in attacked:
            moves.append(1)
        if selected == 3 and -1 < wcastle < 2 and \
           game_board[4] == None and game_board[5] == None and game_board[6] == None and\
           not 3 in attacked and not 4 in attacked and not 5 in attacked:
            moves.append(5)

        if selected == 59 and bcastle%2 == 0 and \
           game_board[58] == None and game_board[57] == None and\
           not 57 in attacked and not 58 in attacked and not 59 in attacked:
            moves.append(57)
        if selected == 59 and -1 < bcastle < 2 and \
           game_board[60] == None and game_board[61] == None and game_board[62] == None and\
           not 59 in attacked and not 60 in attacked and not 61 in attacked:
            moves.append(61)

        if x >= 1 and y <= 6: # Check if valid move
            if game_board[(x-1)+(y+1)*8] == None:   # Check if no blocking piece
                moves.append((x-1)+(y+1)*8)
            elif game_board[(x-1)+(y+1)*8][1] != str(turn): # Check if is attacking
                captures.append((x-1)+(y+1)*8)
        if y <= 6:
            if game_board[x+(y+1)*8] == None:
                moves.append(x+(y+1)*8)
            elif game_board[x+(y+1)*8][1] != str(turn):
                captures.append(x+(y+1)*8)
        if x <= 6 and y <= 6:
            if game_board[(x+1)+(y+1)*8] == None:
                moves.append((x+1)+(y+1)*8)
            elif game_board[(x+1)+(y+1)*8][1] != str(turn):
                captures.append((x+1)+(y+1)*8)
        if x <= 6:
            if game_board[(x+1)+y*8] == None:
                moves.append((x+1)+y*8)
            elif game_board[(x+1)+y*8][1] != str(turn):
                captures.append((x+1)+y*8)
        if x <= 6 and y >= 1:
            if game_board[(x+1)+(y-1)*8] == None:
                moves.append((x+1)+(y-1)*8)
            elif game_board[(x+1)+(y-1)*8][1] != str(turn):
                captures.append((x+1)+(y-1)*8)
        if y >= 1:
            if game_board[x+(y-1)*8] == None:
                moves.append(x+(y-1)*8)
            elif game_board[x+(y-1)*8][1] != str(turn):
                captures.append(x+(y-1)*8)
        if x >= 1 and y >= 1:
            if game_board[(x-1)+(y-1)*8] == None:
                moves.append((x-1)+(y-1)*8)
            elif game_board[(x-1)+(y-1)*8][1] != str(turn):
                captures.append((x-1)+(y-1)*8)
        if x >= 1:
            if game_board[(x-1)+y*8] == None:
                moves.append((x-1)+y*8)
            elif game_board[(x-1)+y*8][1] != str(turn):
                captures.append((x-1)+y*8)

    # Find the player's king
    for i in range(64):
        if game_board[i] != None and game_board[i][0] == 'K' and game_board[i][1] == str(turn):
            break

    # See if a move allows the king to be taken
    t_moves = list(moves)
    for j in t_moves:
        t_game = list(game_board)
        t_game[j] = t_game[selected]
        t_game[selected] = None
        if game_board[selected][0] == 'K':
            i = j
        if i in attacked_spaces(1+turn%2,t_game):
            moves.remove(j)

    # See if a capture allows the king to be taken
    t_captures = list(captures)
    for j in t_captures:
        t_game = list(game_board)
        t_game[j] = t_game[selected]
        t_game[selected] = None
        if game_board[selected][0] == 'K':
            i = j
        if i in attacked_spaces(1+turn%2,t_game):
            captures.remove(j)

    board_buttons[selected].event_on(5)
    for i in moves:
        board_buttons[i].event_on(6)
    for i in captures:
        board_buttons[i].event_on(7)

def deselect_piece():
    """Deselects the selected piece"""

    global captures,moves,selected

    if selected != None:
        board_buttons[selected].event_off(5)
        for i in moves:
            board_buttons[i].event_off(6)
        for i in captures:
            board_buttons[i].event_off(7)

        captures = []
        moves = []
        selected = None

def move_piece(destination):
    """Moves the selected piece"""

    global game_board, en_passent, wcastle, bcastle, wcaptured, bcaptured


    if game_board[selected][0] == 'P':
        # En-passent rule activation
        if abs(destination-selected) in (7,9) and en_passent != None and abs(en_passent-destination) == 8:
            game_board[en_passent] = None

        # En-passent rule initiation
        en_passent = None
        if abs(destination-selected) == 16:
            en_passent = destination

        # Open the menu to select promotion
        if destination < 8 and turn == 2:
            open_menu(bpromote_menu)
        if destination > 55 and turn == 1:
            open_menu(wpromote_menu)

    # Deny castling to moved rooks
    if game_board[selected] == 'R1':
        if selected == 0:
            if wcastle == 2: wcastle = -1
            else:            wcastle = 1
        elif selected == 7:
            if wcastle == 1: wcastle = -1
            else:            wcastle = 2
    if game_board[selected] == 'R2':
        if selected == 56:
            if bcastle == 2: bcastle = -1
            else:            bcastle = 1
        elif selected == 63:
            if bcastle == 1: bcastle = -1
            else:            bcastle = 2

    # Activate castling move
    if game_board[selected][0] == 'K' and abs(destination-selected) == 2:
        if destination == 1:
            game_board[2] = 'R1'
            game_board[0] = None
        elif destination == 5:
            game_board[4] = 'R1'
            game_board[7] = None
        elif destination == 61:
            game_board[60] = 'R2'
            game_board[63] = None
        elif destination == 57:
            game_board[58] = 'R2'
            game_board[56] = None

    # Deny castling to moved king
    if game_board[selected] == 'K1':
        wcastle = -1
    if game_board[selected] == 'K2':
        bcastle = -1

    # Add captured piece to list of captured pieces
    if destination in captures:
        if turn == 1:
            if game_board[destination] == None:
                wcaptured.append("P")
            else:
                wcaptured.append(game_board[destination][0])
            wcaptured = sorted(wcaptured,key = lambda x: "PBNRQ".find(x))
        else:
            if game_board[destination] == None:
                bcaptured.append("P")
            else:
                bcaptured.append(game_board[destination][0])
            bcaptured = sorted(bcaptured,key = lambda x: "PBNRQ".find(x))

    game_board[destination] = game_board[selected]
    game_board[selected] = None

def attacked_spaces(player,board):
    """Returns which spaces a player is currently able to attack"""

    attacked = []

    for i in range(64):
        if board[i] == None:
            continue

        # Pawn for player 1
        if board[i] == 'P1' and player == 1:
            if i%8 != 0:
                attacked.append(i+7)
            if i%8 != 7:
                attacked.append(i+9)

        # Pawn for player 2
        if board[i] == 'P2' and player == 2:
            if i%8 != 7:
                attacked.append(i-7)
            if i%8 != 0:
                attacked.append(i-9)

        # Rook and half of Queen for both players
        if board[i][0] in 'RQ' and board[i][1] == str(player):
            x,y = i%8,i//8

            for j in range(x+1,8,1):
                attacked.append(j+y*8)
                if board[j+y*8] != None:
                    break

            for j in range(x-1,-1,-1):
                attacked.append(j+y*8)
                if board[j+y*8] != None:
                    break

            for j in range(y+1,8,1):
                attacked.append(x+j*8)
                if board[x+j*8] != None:
                    break

            for j in range(y-1,-1,-1):
                attacked.append(x+j*8)
                if board[x+j*8] != None:
                    break

        # Bishop and other half of Queen for both players
        if board[i][0] in 'BQ' and board[i][1] == str(player):

            j = i+7
            while (j-7)%8 != 0 and (j-7)//8 != 7:
                attacked.append(j)
                if board[j] != None:
                    break
                j += 7

            j = i+9
            while (j-9)%8 != 7 and (j-9)//8 != 7:
                attacked.append(j)
                if board[j] != None:
                    break
                j += 9

            j = i-7
            while (j+7)%8 != 7 and (j+7)//8 != 0:
                attacked.append(j)
                if board[j] != None:
                    break
                j -= 7

            j = i-9
            while (j+9)%8 != 0 and (j+9)//8 != 0:
                attacked.append(j)
                if board[j] != None:
                    break
                j -= 9

        # Knight for both players
        if board[i][0] == 'N' and board[i][1] == str(player):
            x,y = i%8,i//8

            if x >= 2 and y <= 6:
                attacked.append((x-2)+(y+1)*8)
            if x >= 1 and y <= 5:
                attacked.append((x-1)+(y+2)*8)

            if x <= 6 and y <= 5:
                attacked.append((x+1)+(y+2)*8)
            if x <= 5 and y <= 6:
                attacked.append((x+2)+(y+1)*8)

            if x <= 5 and y >= 1:
                attacked.append((x+2)+(y-1)*8)
            if x <= 6 and y >= 2:
                attacked.append((x+1)+(y-2)*8)

            if x >= 1 and y >= 2:
                attacked.append((x-1)+(y-2)*8)
            if x >= 2 and y >= 1:
                attacked.append((x-2)+(y-1)*8)

        if board[i][0] == 'K' and board[i][1] == str(player):
            x,y = i%8,i//8

            if x >= 1 and y <= 6:
                attacked.append((x-1)+(y+1)*8)
            if y <= 6:
                attacked.append(x+(y+1)*8)
            if x <= 6 and y <= 6:
                attacked.append((x+1)+(y+1)*8)
            if x <= 6:
                    attacked.append((x+1)+y*8)
            if x <= 6 and y >= 1:
                attacked.append((x+1)+(y-1)*8)
            if y >= 1:
                attacked.append(x+(y-1)*8)
            if x >= 1 and y >= 1:
                attacked.append((x-1)+(y-1)*8)
            if x >= 1:
                attacked.append((x-1)+y*8)

    return attacked

def is_checkmated():
    """Returns 1 if the player with the current turn to move is checkmated"""
    for i in range(64):
        select_piece(i)
        if moves+captures != []:
            deselect_piece()
            return 0
        deselect_piece()
    return 1


""" Game variables """
# Notes:
# selected is a number representing where the selected piece is
# moves is a list of where the selected piece can move
# captures is a list of where the selected piece can capture
# game_board is a list of every space on the board and says what piece exists there
# turn is a number either 1 or 2 representing whose turn it is

turn = 1
wcastle = 0
bcastle = 0
selected = None
moves = []
captures = []
wcaptured = []
bcaptured = []
game_board = [None for i in range(64)]
en_passent = None

""" Image Loading """
king1 = image.load("images/wking.png").convert_alpha()
king2 = image.load("images/bking.png").convert_alpha()
pawn1 = image.load("images/wpawn.png").convert_alpha()
pawn2 = image.load("images/bpawn.png").convert_alpha()
rook1 = image.load("images/wrook.png").convert_alpha()
rook2 = image.load("images/brook.png").convert_alpha()
queen1 = image.load("images/wqueen.png").convert_alpha()
queen2 = image.load("images/bqueen.png").convert_alpha()
bishop1 = image.load("images/wbishop.png").convert_alpha()
bishop2 = image.load("images/bbishop.png").convert_alpha()
knight1 = image.load("images/wknight.png").convert_alpha()
knight2 = image.load("images/bknight.png").convert_alpha()

""" Creation of game board """
# Notes:
# Event 5 represents a selected piece
# Event 6 represents a possible move for a piece
# Event 7 represents a possible capture of an enemy piece

font1 = font.Font('fonts/Alido.otf',18)
font2 = font.Font('fonts/LCALLIG.ttf',36)

win_bg = Surface((250,90))
win_bg.fill((0,0,0))
draw.rect(win_bg,(255,255,255),(5,5,240,80))

layer_black = Surface((50,50))
layer_black.fill((128,128,128))
layer_hovered = Surface((50,50))
layer_hovered.fill((0,0,255))
layer_selected = Surface((50,50))
layer_selected.fill((0,255,0))
layer_is_move = Surface((50,50),SRCALPHA)
layer_is_move.fill((0,0,255,85))
layer_is_capture = Surface((50,50))
layer_is_capture.fill((255,0,0))

new_bg = Surface((100,20))
new_bg.fill((255,0,0))
new_bg2 = Surface((100,20))
new_bg2.fill((0,0,255))

promote_layer = Surface((120,120))
promote_layer.fill((255,255,255))
draw.rect(promote_layer,(0,0,0),(5,5,110,110))
draw.rect(promote_layer,(255,255,255),(10,10,100,100))
draw.line(promote_layer,(0,0,0),(10,60),(110,60),5)
draw.line(promote_layer,(0,0,0),(60,10),(60,110),5)

# In-game GUI
game_menu = make_menu((0,0,800,800),'game',0)
open_menu(game_menu)

board_buttons = [Button((100+(i%8)*50,450-(i//8)*50,50,50),i,(0,)) for i in range(64)]

for i in range(64):
    if (i+i//8)%2 == 0:
        board_buttons[i].add_layer(layer_black,(0,0),(0,))

new_game = Button((2,2,50,20),'new',(0,))
new_game.add_layer(new_bg,(0,0),(2,))
new_game.add_text("Reset",font1,(0,0,0),(25,10),1,0,(0,))

quit_button = Button((548,2,50,20),'quit',(0,))
quit_button.add_layer(new_bg,(0,0),(2,))
quit_button.add_text("Quit",font1,(0,0,0),(25,10),1,0,(0,))

add_layer_multi(layer_hovered,(0,0),(2,-5,-6,-7),board_buttons)
add_layer_multi(layer_selected,(0,0),(5,),board_buttons)
add_layer_multi(layer_is_move,(0,0),(-5,6,-7),board_buttons)
add_layer_multi(layer_is_capture,(0,0),(-5,7),board_buttons)

add_objects(game_menu,board_buttons)
add_objects(game_menu,(new_game,quit_button))

# Win menu
win_menu = make_menu((175,270,250,90),'win',1)
win_menu.add_layer(win_bg,(0,0),(5,6))
win_menu.add_text("White wins!",font2,(0,0,0),(125,30),1,0,(5,))
win_menu.add_text("Black wins!",font2,(0,0,0),(125,30),1,0,(6,))
new_game2 = Button((10,60,100,20),'new',(0,))
new_game2.add_layer(new_bg,(0,0),(2,))
new_game2.add_layer(new_bg2,(0,0),(0,-2))
new_game2.add_text("New Game",font1,(255,255,255),(50,10),1,0,(0,))
win_menu.add_object(new_game2)
quit2 = Button((180,60,50,20),'quit',(0,))
quit2.add_layer(new_bg,(0,0),(2,))
quit2.add_layer(new_bg2,(0,0),(0,-2))
quit2.add_text("Quit",font1,(255,255,255),(25,10),1,0,(0,))
win_menu.add_object(quit2)


# Promotion menus
wqueen_btn = Button((10,10,50,50),'Q',(0,))
wknight_btn = Button((60,10,50,50),'N',(0,))
wrook_btn = Button((10,60,50,50),'R',(0,))
wbishop_btn = Button((60,60,50,50),'B',(0,))

bqueen_btn = Button((10,10,50,50),'Q',(0,))
bknight_btn = Button((60,10,50,50),'N',(0,))
brook_btn = Button((10,60,50,50),'R',(0,))
bbishop_btn = Button((60,60,50,50),'B',(0,))

add_layer_multi(layer_hovered,(0,0),(2,),(wqueen_btn,wknight_btn,wrook_btn,wbishop_btn,
                                          bqueen_btn,bknight_btn,brook_btn,bbishop_btn))

wqueen_btn.add_layer(queen1,(0,0),(0,))
wrook_btn.add_layer(rook1,(0,0),(0,))
wknight_btn.add_layer(knight1,(0,0),(0,))
wbishop_btn.add_layer(bishop1,(0,0),(0,))
bqueen_btn.add_layer(queen2,(0,0),(0,))
brook_btn.add_layer(rook2,(0,0),(0,))
bknight_btn.add_layer(knight2,(0,0),(0,))
bbishop_btn.add_layer(bishop2,(0,0),(0,))

wpromote_menu = make_menu((240,240,120,120),'wpromote',1)
wpromote_menu.add_layer(promote_layer,(0,0),(0,))
add_objects(wpromote_menu,(wqueen_btn,wknight_btn,wrook_btn,wbishop_btn))

bpromote_menu = make_menu((240,240,120,120),'bpromote',1)
bpromote_menu.add_layer(promote_layer,(0,0),(0,))
add_objects(bpromote_menu,(bqueen_btn,bknight_btn,brook_btn,bbishop_btn))

reset_game()

""" Main Loop """
# Notes:
# My loops run in three main steps:
#   1. Get inputs for each menu along with general inputs
#   2. Handle inputs for each menu and update all running systems
#   3. Draw all of the objects to the screen for each menu
#
# Using my menuing system I'm able to easily organize every GUI including the
# main game itself into these three steps.

running = 1
while running:
    """ STEP 1: Get inputs """
    chars = ''
    for evnt in event.get():
        if evnt.type == QUIT:
            running = 0
        elif evnt.type == KEYDOWN:
            if evnt.key == K_ESCAPE:
                running = 0
            else:
                chars += evnt.unicode

    lc,rc = mouse.get_pressed()[0:2]
    mx,my = mouse.get_pos()

    """ STEP 2: Handle inputs / update menus """

    update_menus(mx,my,lc,chars)

    if is_menu_open(wpromote_menu) or is_menu_open(bpromote_menu):  # Promotion menus
        for i in wpromote_menu.get_pressed():   # Check selection
            close_menu(wpromote_menu)
            game_board[c] = i+'1'
            deselect_piece()
            turn = 2
            if is_checkmated():
                open_menu(win_menu)
                win_menu.event_on(4)

        for i in bpromote_menu.get_pressed():   # Check selection
            close_menu(bpromote_menu)
            game_board[c] = i+'2'
            deselect_piece()
            turn = 1
            if is_checkmated():
                open_menu(win_menu)
                win_menu.event_on(5)

    elif is_menu_open(game_menu):
        # Handle the game board and game menu
        for c in game_menu.get_pressed():
            if c == 'new':      # Reset game button
                reset_game()
            elif c == 'quit':   # Exit game button
                running = 0
            else:
                if selected == None:    # Select piece that was clicked on
                    select_piece(c)
                else:
                    if selected == c:   # Deselect currently selected piece
                        deselect_piece()
                    else:
                        if c in moves or c in captures: # If the chosen square is an option
                            move_piece(c)

                            if not is_menu_open(wpromote_menu) and not is_menu_open(bpromote_menu):
                                deselect_piece()
                                turn = 1+turn%2
                                if is_checkmated():
                                    open_menu(win_menu)
                                    win_menu.event_on(5+turn%2)
                            else:
                                break

                        else:
                            deselect_piece()
                            select_piece(c)

    if is_menu_open(win_menu):
        for i in win_menu.get_pressed():
            if i == 'quit':
                running = 0
            elif i == 'new':
                reset_game()

    """ STEP 3: Draw menus """

    update_menu_images()

    if is_menu_open(game_menu):
        # Show which pieces are captured
        i = 0
        p = 0
        for piece in wcaptured:
            if piece == "P":
                if p == 0:
                    game_menu.blit(pawn2,(0,50))
                p += 1
            else:
                i += 50
            if piece == "B": game_menu.blit(bishop2,(0,50+i))
            if piece == "N": game_menu.blit(knight2,(0,50+i))
            if piece == "R": game_menu.blit(rook2,(0,50+i))
            if piece == "Q": game_menu.blit(queen2,(0,50+i))
        if p != 0:
            msg = font1.render(str(p),1,(255,255,255))
            game_menu.blit(msg,(20,68))

        i = 0
        p = 0
        for piece in bcaptured:
            if piece == "P":
                if p == 0:
                    game_menu.blit(pawn1,(550,50))
                p += 1
            else:
                i += 50
            if piece == "B": game_menu.blit(bishop1,(550,50+i))
            if piece == "N": game_menu.blit(knight1,(550,50+i))
            if piece == "R": game_menu.blit(rook1,(550,50+i))
            if piece == "Q": game_menu.blit(queen1,(550,50+i))
        if p != 0:
            msg = font1.render(str(p),1,(0,0,0))
            game_menu.blit(msg,(570,68))

        # Draw the pieces on the game board
        for i in range(64):
            if game_board[i] == 'P1':
                game_menu.blit(pawn1,(100+(i%8)*50,450-(i//8)*50))
            if game_board[i] == 'P2':
                game_menu.blit(pawn2,(100+(i%8)*50,450-(i//8)*50))
            if game_board[i] == 'K1':
                game_menu.blit(king1,(100+(i%8)*50,450-(i//8)*50))
            if game_board[i] == 'K2':
                game_menu.blit(king2,(100+(i%8)*50,450-(i//8)*50))
            if game_board[i] == 'Q1':
                game_menu.blit(queen1,(100+(i%8)*50,450-(i//8)*50))
            if game_board[i] == 'Q2':
                game_menu.blit(queen2,(100+(i%8)*50,450-(i//8)*50))
            if game_board[i] == 'R1':
                game_menu.blit(rook1,(100+(i%8)*50,450-(i//8)*50))
            if game_board[i] == 'R2':
                game_menu.blit(rook2,(100+(i%8)*50,450-(i//8)*50))
            if game_board[i] == 'B1':
                game_menu.blit(bishop1,(100+(i%8)*50,450-(i//8)*50))
            if game_board[i] == 'B2':
                game_menu.blit(bishop2,(100+(i%8)*50,450-(i//8)*50))
            if game_board[i] == 'N1':
                game_menu.blit(knight1,(100+(i%8)*50,450-(i//8)*50))
            if game_board[i] == 'N2':
                game_menu.blit(knight2,(100+(i%8)*50,450-(i//8)*50))

    screen.fill((255,255,255))
    draw.rect(screen,(0,0,0),(50,50,500,500))
    draw.rect(screen,(255,255,255),(100,100,400,400))
    draw_menus(screen)

    display.flip()
    time.wait(10)

quit()
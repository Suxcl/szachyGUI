import pygame
from classes.pieces_path import *
# c--- ustom cursor handling ---

def changeCursorToPiece(piece):
    print("changeCursorToPiece - changing curor to piece:",piece)
    piece_img_path = pieces_paths[piece]
    surf = pygame.image.load(piece_img_path).convert_alpha()
    cursor = pygame.cursors.Cursor((15,15), surf)
    pygame.mouse.set_cursor(cursor)

def changeCursorToHand():
    print("changeCursorToHand - changing curor to hand")
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

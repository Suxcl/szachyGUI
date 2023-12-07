import pygame
import sys

# Constants
IMG_SIZE = 60
ROWS, COLS = 8, 8
WIDTH, HEIGHT = IMG_SIZE*ROWS, IMG_SIZE*COLS

SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (118,150,86)
BLACK = (238,238,210)
GRAY = (169, 169, 169)
GREEN =(124,252,0)
SELECTED_COLOR = (0, 255, 0) 

def draw_chessboard(screen):
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            IMAGE = pygame.image.load("assets/pieces/bb.png").convert_alpha()
            # rect = IMAGE.get_rect()
            
            
            pygame.draw.rect(screen, color, rect)
            screen.blit(IMAGE,rect)



def highlighSquare(screen, selected_square):
    row = selected_square[0]
    col = selected_square[1]
    color = GREEN
    rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
    pygame.draw.rect(screen, color, rect)

def unhighlightSquare(screen, selected_square):
    row = selected_square[0]
    col = selected_square[1]
    color = WHITE if (row + col) % 2 == 0 else BLACK
    rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
    pygame.draw.rect(screen, color, rect)

def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chessboard with Buttons")
    draw_chessboard(screen) 


    clock = pygame.time.Clock()

    selected_square = None

    buttons = []
    for row in range(ROWS):
        for col in range(COLS):
            button_rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            buttons.append(button_rect)

    #od cursora
    cursor_img = pygame.image.load("assets/pieces/bb.png").convert_alpha()
    # pygame.mouse.set_visible(False)
    cursor_img_rect = cursor_img.get_rect()


    while True:
        for event in pygame.event.get():
            

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if(selected_square):
                    unhighlightSquare(screen, selected_square)
                if event.button == 1:  # Left mouse button
                    x, y = event.pos
                    for i, button in enumerate(buttons):
                        if button.collidepoint(x, y):

                            cursor_img_rect.center = pygame.mouse.get_pos()  # update position 
                            screen.blit(cursor_img, cursor_img_rect) 
                            # pygame.mouse.set_cursor(cursor_img)
                            selected_square = (y // SQUARE_SIZE,x // SQUARE_SIZE)
                            print(f"Button clicked: {i} ({i // COLS}, {i % COLS})")
        # screen.fill(GRAY)
        
        if(selected_square):
            highlighSquare(screen, selected_square)
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()

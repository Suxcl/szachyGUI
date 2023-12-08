# Simple pygame program

# Import and initialize the pygame library
import pygame
pygame.init()


positions = [
    # [0,0],[0,100],
    # [100,0],[100,100]
]
FIELD_SIZE = 60
for a in range(8):
    tmp = []
    for b in range(8):
        tmp.append([a*FIELD_SIZE,b*FIELD_SIZE])
    positions.append(tmp)


# Set up the drawing window
screen = pygame.display.set_mode([FIELD_SIZE*8,FIELD_SIZE*8])

# Run until the user asks to quit
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if b.collidepoint(pos):
                pass


    # Fill the background with white
    screen.fill((0,0,0))
    color = None
    size = 100
    counter = 0
    for a in range(len(positions)):
        for b in range(len(positions[a])):
            if  a%2 == b%2:
                color = (255,255,255)
            else: color = (0,0,0)

            screen.blit()
            # pygame.draw.rect(screen,color,(positions[a][b][0],positions[a][b][1],size,size))    
            # pygame.draw.rct

    
    
    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()





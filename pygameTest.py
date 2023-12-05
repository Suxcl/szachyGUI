# Simple pygame program

# Import and initialize the pygame library
import pygame
pygame.init()


positions = [
    [0,0],[0,100],
    [100,0],[100,100]
]

# Set up the drawing window
screen = pygame.display.set_mode([500, 500])

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))
    color = None
    size = 100
    for a in range(len(positions)):
        if a in [1,2]: 
            color = (10,10,100)
        else: color = (100,10,10)
        rct = pygame.rect(screen,color,(positions[a][0],positions[a][1],size,size))    
        pygame.draw.rct
    # Draw a solid blue circle in the center
    
    
    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
# importing the module
import pygame
# initialisation
pygame.init()
# setting up window size
display_width = 600
display_height = 600
 
# use python style variable names (lowercase)
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('checking hovers')
 
clock = pygame.time.Clock()
 
# load the font only once instead of every frame
font = pygame.font.SysFont('comicsans', 40)
 
# class name should be singular
 
 
class Button(pygame.sprite.Sprite):
    # 1) no need to have 4 parameters for position and size, use pygame.Rect instead
    # 2) let the Button itself handle which color it is
    # 3) give a callback function to the button so it can handle the click itself
    def __init__(self, color, color_hover, rect, callback, text='', outline=None):
        super().__init__()
        self.text = text
        # a temporary Rect to store the size of the button
        tmp_rect = pygame.Rect(0, 0, *rect.size)
 
        # create two Surfaces here, one the normal state, and one for the hovering state
        # we create the Surfaces here once, so we can simple built them and dont have
        # to render the text and outline again every frame
        self.org = self._create_image(color, outline, text, tmp_rect)
        self.hov = self._create_image(color_hover, outline, text, tmp_rect)
 
        # in Sprites, the image attribute holds the Surface to be displayed...
        self.image = self.org
        # ...and the rect holds the Rect that defines it position
        self.rect = rect
        self.callback = callback
 
    def _create_image(self, color, outline, text, rect):
        # function to create the actual surface
        # see how we can make use of Rect's virtual attributes like 'size'
        img = pygame.Surface(rect.size)
        if outline:
            # here we can make good use of Rect's functions again
            # first, fill the Surface in the outline color
            # then fill a rectangular area in the actual color
            # 'inflate' is used to 'shrink' the rect
            img.fill(outline)
            img.fill(color, rect.inflate(-4, -3))
        else:
            img.fill(color)
 
        # render the text once here instead of every frame
        if text != '':
            text_surf = font.render(text, 1, pygame.Color('black'))
            # again, see how easy it is to center stuff using Rect's attributes like 'center'
            text_rect = text_surf.get_rect(center=rect.center)
            img.blit(text_surf, text_rect)
        return img
 
    def update(self, events):
        # here we handle all the logic of the Button
        pos = pygame.mouse.get_pos()
        hit = self.rect.collidepoint(pos)
        # if the mouse in inside the Rect (again, see how the Rect class
        # does all the calculation for use), use the 'hov' image instead of 'org'
        self.image = self.hov if hit else self.org
        for event in events:
            # the Button checks for events itself.
            # if this Button is clicked, it runs the callback function
            if event.type == pygame.MOUSEBUTTONDOWN and hit:
                self.callback(self)
 
 
run = True
 
# we store all Sprites in a Group, so we can easily
# call the 'update' and 'draw' functions of the Buttons
# in the main loop
sprites = pygame.sprite.Group()
sprites.add(Button(pygame.Color('green'),
                   pygame.Color('red'),  # on hover color
                   # four parameters are position of rec (left,up,right,down) right and down cannot be zero
                   pygame.Rect(20, 100, 60, 60),
                   # //right these accor to display dimensions
                   # f1=pygame.font.SysFont('elephant',20)
                   lambda b: print(f"Button '{b.text}' was clicked"),
                   'Hover',
                   pygame.Color('black'),
 
                   ))
 
sprites.add(Button(pygame.Color('yellow'),
                   pygame.Color('red'),
                   pygame.Rect(300, 100, 200, 200),
                   lambda b: print(f"Click  me again!"),
                   'Another'))  # another button
 
screen.fill(pygame.Color('white'))

while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
 
    # update all sprites
    # it now doesn't matter if we have one or 200 Buttons
    sprites.update(events)
    # clear the screen
    
    # draw all sprites/Buttons
    sprites.draw(screen)
    pygame.display.update()
    # limit framerate to 60 FPS
    clock.tick(60)
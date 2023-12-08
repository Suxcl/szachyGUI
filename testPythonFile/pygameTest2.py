import pygame
import pygame_gui


pygame.init()

pygame.display.set_caption('Quick Start')

window_surface = pygame.display.set_mode((800, 600))

background = pygame.Surface((700, 500))
background.fill(pygame.Color('#ffffff'))

manager = pygame_gui.UIManager((800, 600))

hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (100, 100)),
                                            text='Say Hello',
                                            manager=manager)


hello_button2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 100), (100, 100)),
                                            text='SayHello2',
                                            manager=manager)


img = pygame.image.load("assets/pieces/bb.png")
shrek = pygame.image.load("assets/pieces/shrek.jpg")

clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == hello_button:
                print(event)
                print(event.ui_element)
                background.blit(img, (0,0))
            if event.ui_element == hello_button2:
                print('yooo')
                # window_surface.blit(img, (300, 300)) #blit
                background.blit(shrek, (300, 300)) #blit
    if hello_button.get_rect().collidepoint(pygame.mouse.get_pos()):
        print('yoooo')


        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()

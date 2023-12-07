import pygame

# ############################################################################ #
#                                                                              #
#   Explaining Events:                                                         #
#       Events are stored in menu objects in a list called "event_flags".      #
#       All images drawn onto the menu object must have a common event         #
#       to a currently activated event flag in order to be drawn.              #
#       If an image has a negative event and that event is in the event        #
#       flags then that image WILL NOT be drawn under any circumstances.       #
#                                                                              #
#   Typical Events:                                                            #
#       0 = always                                                             #
#       1 = disabled                                                           #
#       2 = hovering                                                           #
#       3 = selected                                                           #
#       4 = pressed                                                            #
#                                                                              #
#   Event Examples:                                                            #
#       - You have an entry with an image that has events (0, -3)              #
#       The above image will be drawn while the entry is not selected.         #
#                                                                              #
#       - You have a button with an image that has events (4, )                #
#       The above image will be drawn when the button is pressed.              #
#                                                                              #
# ############################################################################ #

# Creating constants for use with entrys and the "chars" parameter.
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
NUMBERS = "1234567890"
SYMBOLS = '''!@#$%^&*()~`_-+=:;<,>.?/|'"'''
ALWAYS = 0
DISABLED = 1
HOVERING = 2
SELECTED = 3
PRESSED = 4

menu_list = []      # List of all created menus

order_selected = [] # Order in which menus have been opened

class _menu_object:
    def __init__(self):
        self.id = ''
        self.layers = []
        self.changed = 1
        self.event_flags = []
        self.fill = None

    def add_text(self,text,font,colour,textrect,alignment,awrap,events):
        """Adds a layer of text. Can be aligned and textwrapped.
        events is a tuple of events during which this text will be displayed."""

        if awrap:
            lines = _text_wrap(text,font,textrect[2])
        else:
            lines = text.split('\n')

        y = font.size('A')[1]
        for i,line in enumerate(lines):
            if alignment == 0:
                self.layers.append((font.render(line,1,colour),(round(textrect[0]),round(textrect[1]+i*y)),events))

            elif alignment == 1:
                x = font.size(line)[0]
                self.layers.append((font.render(line,1,colour),(round(textrect[0]-x/2),round(textrect[1]-y*len(lines)/2+i*y)),events))

            elif alignment == 2:
                x = font.size(line)[0]
                self.layers.append((font.render(line,1,colour),(round(textrect[0]+textrect[2]-x),round(textrect[1]+i*y)),events))

            else: raise Exception("Alignment is 0 for left, 1 for centred and 2 for right.")

        self.changed = 1

    def toggle(self):
        """Changes the active state of this object."""
        self.toggle_event(1)
        self.changed = 1

    def get_id(self):
        return self.id

    def set_id(self,new_id):
        self.id = new_id

    def add_layer(self,layer,pos,events):
        """events is a tuple of events during which this layer will be displayed."""
        self.layers.append((layer,pos,events))
        self.changed = 1

    def toggle_event(self,event):
        """Switch the existance of a given event (can be a new undefined event)"""

        if event in self.event_flags:
            self.event_flags.remove(event)
        else:
            self.event_flags.append(event)

        self.changed = 1

    def event_off(self,event):
        """Turns off a given event."""

        if event in self.event_flags:
            self.event_flags.remove(event)
            self.changed = 1

    def event_on(self,event):
        """Turn on a given event."""

        if not event in self.event_flags:
            self.event_flags.append(event)
            self.changed = 1

    def set_fill(self,colour):
        self.fill = colour

class _menu(_menu_object):
    def __init__(self,rect,identity,always_on_top):
        """
        A menu on which widgets, images and text can be placed.
        Menus handle widgets allowing for user inputs in many different forms.
        Do not directly create a menu. Instead use the make_menu function.
        Menus should be handled per frame by the functions update_menus, update_menu_images and draw_menus."""

        self.x,self.y,self.w,self.h = rect
        self.id = identity
        self.always_on_top = always_on_top

        self.image = pygame.Surface((rect[2],rect[3]),pygame.SRCALPHA)
        self.image.fill((0,0,0,0))
        self.layers = []

        self.objects = []
        self.event_flags = []
        self.pressed_buttons = []

        self.changed = 1
        self.clicked = 0

    def update_image(self):
        self.changed = 0
        self.image.fill((0,0,0,0))
        for layer in self.layers:
            draw_img = 0
            for event in layer[2]:
                if event == 0 or event in self.event_flags:
                    draw_img = 1
                elif event < 0 and -event in self.event_flags:
                    draw_img = 0
                    break

            if draw_img:
                self.image.blit(layer[0],layer[1])

        for obj in self.objects:
            draw_obj = 0
            for event in obj.events:
                if event == 0 or event in self.event_flags:
                    draw_obj = 1
                elif event < 0 and -event in self.event_flags:
                    draw_obj = 0
                    break

            if draw_obj:
                if obj.changed: obj.update_image()
                self.image.blit(obj.image,(obj.x,obj.y))

    def add_object(self,m_object):
        self.objects.append(m_object)
        self.changed = 1

    def update_objects(self,mx,my,lc,char):
        """Updates enabled buttons by making them selected, pressed or changing their entry values."""
        self.pressed_buttons = []

        for obj in self.objects:

            update_obj = 0
            for event in obj.events:
                if event == 0 or event in self.event_flags:
                    update_obj = 1
                elif event < 0 and -event in self.event_flags:
                    update_obj = 0
                    break

            if not 1 in obj.event_flags and update_obj:     # ensures that the object is not disabled
                collide = (0 < mx-obj.x-self.x < obj.w and 0 < my-obj.y-self.y < obj.h)

                if collide: obj.event_on(2) # 2 is the hovered flag
                else: obj.event_off(2)
                obj.event_off(4)            # Clear all button presses

                if lc:      # Change selected / pressed flags
                    if collide:
                        if not self.clicked:
                            obj.event_on(3)     # 3 is the selected flag
                            obj.event_on(4)     # 4 is the pressed flag
                            self.pressed_buttons.append(obj.id) # Record that an object has been pressed
                    else:
                        obj.event_off(3)

                if obj.type == 'entry' and 3 in obj.event_flags:    # Update selected entries
                    obj.update_object(char)

            if obj.changed:
                self.changed = 1

        if lc and not self.clicked:
            self.clicked = 1
        elif self.clicked and not lc:
            self.clicked = 0

    def get_pressed(self):
        """Get the ID of all pressed buttons from the last call to update_objects"""
        return self.pressed_buttons

    def blit(self,surface,rect):
        """Draw arbitrary surface on the current menu image."""
        self.image.blit(surface,rect)
        self.changed = 1

    def move(self,pos):
        """Changes the position of the menu on the host surface."""
        self.x,self.y = pos

    def get_objects(self):
        """Returns the list of objects in this menu in the order that they were given to the menu."""
        return self.objects

    def get_object(self,identity):
        """Returns an object with given identity that is in this menu."""
        for obj in self.objects:
            if obj.id == identity:
                return obj

class Entry(_menu_object):
    def __init__(self,rect,identity,events,string,font,fcolour,textrect,align,awrap,chars,sensitive,maxlen):
        """
        Entrys can actively handle keyboard inputs.
        When an entry is selected and keyboard inputs are recieved, the entry will accumulate
        characters in its "string" variable as long as those characters are in the given "chars" variable.
        Entrys will also display what is in their "string" variable.
        font = pygame font object
        fcolour = 3 part tuple representing colour for font
        textrect = the rectangle in which the font will be displayed (x,y,w,h)
        align = the alignment for the text (0 = left, 1 = centre, 2 = right)
        awrap = boolean for weither or not to auto-wrap text
        chars = the characters that are allowed as input
        sensitive = boolean for weither or not to make displayed text into stars for security
        maxlen = the maximum number of characters that can be held"""

        self.type = 'entry'
        self.x,self.y,self.w,self.h = rect
        self.id = identity
        self.string = string
        self.font = font
        self.fcolour = fcolour
        self.textrect = textrect
        self.align = align
        self.autowrap = awrap
        self.allowed_chars = chars
        self.sensitive = sensitive
        self.maxlen = maxlen
        self.image = pygame.Surface((self.w,self.h),pygame.SRCALPHA)
        self.events = events

    def update_image(self):
        """Redraw the object's image."""
        self.changed = 0
        self.image.fill((0,0,0,0))
        for layer in self.layers:
            is_drawing = 0
            for event in layer[2]:
                if event in self.event_flags or event == 0:
                    is_drawing = 1
                if event < 0 and -event in self.event_flags:
                    is_drawing = 0
                    break
            if is_drawing:
                self.image.blit(layer[0],layer[1])
        if self.autowrap: lines = _text_wrap(self.string,self.font,self.textrect[2])
        else: lines = self.string.split('\n')
        y = self.font.size('A')[1]
        for i,line in enumerate(lines):
            if self.align == 0:
                if self.sensitive:
                    self.image.blit(self.font.render(''.join('*' for i in range(len(line))),1,self.fcolour),(self.textrect[0],self.textrect[1]+i*y))
                else:
                    self.image.blit(self.font.render(line,1,self.fcolour),(self.textrect[0],self.textrect[1]+i*y))
            elif self.align == 1:
                if self.sensitive:
                    x = self.font.size(''.join('*' for i in range(len(line))))[0]
                    self.image.blit(self.font.render(''.join('*' for i in range(len(line))),1,self.fcolour),((self.w-x)/2,(self.h-y*len(lines))/2+i*y))
                else:
                    x = self.font.size(line)[0]
                    self.image.blit(self.font.render(line,1,self.fcolour),((self.w-x)/2,(self.h-y*len(lines))/2+i*y))
            elif self.align == 2:
                if self.sensitive:
                    x = self.font.size(''.join('*' for i in range(len(line))))[0]
                    self.image.blit(self.font.render(''.join('*' for i in range(len(line))),1,self.fcolour),(self.w-x-self.textrect[0],self.textrect[1]+i*y))
                else:
                    x = self.font.size(line)[0]
                    self.image.blit(self.font.render(line,1,self.fcolour),(self.w-x-self.textrect[0],self.textrect[1]+i*y))
            else: raise Exception("Alignment is 0 for left, 1 for centred and 2 for right.")

    def update_object(self,char=''):
        """Update the string in the Entry with new characters."""
        if 3 in self.event_flags:
            for i in range(len(char)):
                if ord(char[i]) == pygame.K_BACKSPACE and self.string:
                    self.string = self.string[:-1]
                elif len(self.string) < self.maxlen or self.maxlen == 0:
                    if ord(char[i]) == pygame.K_RETURN:
                        self.string += '\n'
                    else:
                        if char[i] in self.allowed_chars:
                            self.string += char[i]
                self.changed = 1

    def set_text(self,text):
        self.changed = 1
        self.string = text

class Button(_menu_object):
    def __init__(self,rect,identity,events):
        """
        Buttons are super primative compared to other widgets.
        They share functionalities with every other widget and are comprised of a builtin update_image function.
        The Button widget is so empty because all of its necessary parts come strait from the base class that all widgets are derived from."""
        self.type = 'button'
        self.x,self.y,self.w,self.h = rect
        self.id = identity
        self.image = pygame.Surface((self.w,self.h),pygame.SRCALPHA)
        self.layers = []
        self.events = events
        self.changed = 1
        self.event_flags = []

    def update_image(self):
        """Redraw the Button's image."""
        self.changed = 0
        self.image.fill((0,0,0,0))
        for layer in self.layers:
            is_drawing = 0
            for event in layer[2]:
                if event in self.event_flags or event == 0:
                    is_drawing = 1
                if event < 0 and -event in self.event_flags:
                    is_drawing = 0
                    break
            if is_drawing:
                self.image.blit(layer[0],layer[1])



""" ----------------------------------------- """
""" End of classes, start of major functions. """
""" ----------------------------------------- """

def _text_wrap(text,font,width):
    """This will wrap text based on a given textbox width and font."""
    lines = text.split('\n')
    j = 0
    while j < len(lines):
        i = 0
        words = lines[j].split(' ')
        while i < len(words):
            line_size = font.size(' '.join(words[:i+1]))[0]
            if line_size > width:
                lines = lines[:j]+[' '.join(words[:i-1])]+[' '.join(words[i-1:])]+lines[j+1:]
                break
            i += 1
        j += 1

    return lines

def events_on(mobject,events):
    for i in events:
        mobject.event_on(i)
def events_off(mobject,events):
    for i in events:
        mobject.event_off(i)
def event_on_multi(event,mobjects):
    for i in mobjects:
        i.event_on(event)
def event_off_multi(event,mobjects):
    for i in mobjects:
        i.event_off(event)
def add_layer_multi(layer,pos,event,mobjects):
    for i in mobjects:
        i.add_layer(layer,pos,event)
def add_layers(layers,pos,event,mobject):
    for i in layers:
        mobject.add_layer(i,pos,event)
def add_objects(menu,objects):
    for i in objects:
        menu.add_object(i)

def make_menu(rect,identity,always_on_top):
    """Call this whenever you want to make a menu.
    Returns the menu object for referencing."""
    t_menu = _menu(rect,identity,always_on_top)
    t_menu.event_on(1)
    menu_list.append(t_menu)
    return t_menu

def update_menus(mx,my,lc,char):
    """Call this to update which menu is selected and to update objects on the selected menu."""
    if lc and menu_list[order_selected[-1]].always_on_top != 1:
        for i in order_selected:
            menu = menu_list[i]
            if menu.x < mx < menu.x+menu.w and menu.y < my < menu.y+menu.h:
                if order_selected[-1] != i:
                    order_selected.append(i)

    menu_list[order_selected[-1]].update_objects(mx,my,lc,char)

def close_menu(menu):
    """Call this to disable a menu."""
    menu.event_on(1)
    for i in range(len(menu_list)):
        if menu == menu_list[i]:
            while 1:
                try: order_selected.remove(i)
                except: break
            break

def open_menu(menu):
    """Call this to re-enable a disabled menu and bring it to the forefront."""
    menu.event_off(1)
    order_selected.append(menu_list.index(menu))

def update_menu_images():
    """Call this once before drawing menus to ensure that they are up to date"""
    for menu in menu_list:
        if menu.changed and not 1 in menu.event_flags:
            menu.update_image()

def draw_menus(surface):
    """Call this to draw menus onto the given surface.
    Remember to call update_menu_images first."""
    for i in order_selected:
        menu = menu_list[i]
        if not 1 in menu.event_flags:
            surface.blit(menu.image,(menu.x,menu.y,menu.w,menu.h))

def is_menu_open(menu):
    return not 1 in menu.event_flags and menu_list.index(menu) in order_selected
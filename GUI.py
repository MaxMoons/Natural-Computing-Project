from tkinter import *
import numpy as np


class GUI(Frame):
    '''
    Huidige idee:
    Maak een frame met een aantal knoppen daarboven;
    Air: Om pixels te wissen
    Stone: Om steen te plaatsen (waar water niet doorheen kan)
    Water: Om water te plaatsen
        Zelf alle tegels plaatsen of bijvoorbeeld ook een waterbron (i.e. een tegel die water genereert)
    Waterbron: Een tegel waarin water gegenereert wordt als er geen water in zit (als een soort waterval)
    Start animation: Begin het animeren nadat alles getekend is
    Animation speed: Snelheid waarmee de animatie loopt
        Aantal refreshes/sec?
    Stop animation (?): Stop de animatie

    Inputvakken voor parameters van de formules
    '''

    def __init__(self, root, **kw):
        super().__init__(**kw)
        self.root = root
        # Width and height of the canvas
        self.canvas_width, self.canvas_height = 600, 500
        self.frame_width, self.frame_height = 600, 100
        self.mode = 0
        
        # Amount of x and y pixels; y follows from height and pixel size as pixels are square
        self.x_pixels = 100
        self.pixel_size = self.canvas_width / self.x_pixels
        self.y_pixels = int(self.canvas_height / self.pixel_size)
        
        # Size of one pixel
        self.particle_size = 5
        
        self.root = Tk()
        self.root.title("Super awesome animatie")
        
        # Button panel frame stuff
        self.frame_width, self.frame_height = 600, 100
        self.frame = Frame(self.root, bg='grey')
        self.frame.pack(fill='x')
        Label(self.frame, text="Mode:", bg='grey').pack(side='left')
        self.modelabel = Label(self.frame, text="Default", bg='grey').pack(side='left')
        self.air_button = Button(self.frame, text='Delete')
        self.air_button.pack(side='left', padx=10)
        self.water_button = Button(self.frame, text='Water')
        self.water_button.pack(side='left', padx=10)
        self.stone_button = Button(self.frame, text='Stone')
        self.stone_button.pack(side='left', padx=10)
        
        self.start_button = Button(self.frame, text='Start simulation')
        self.start_button.pack(side='left', padx=60)
        self.stop_button = Button(self.frame, text='Stop simulation')
        self.stop_button.pack(side='left', padx=10)
        
        self.frame2 = Frame(self.root)
        self.frame2.pack(fill='x')
        
        Label(self.frame2, text="Animation speed:").pack(side=LEFT)
        self.speed_input = Entry(self.frame2, width=10)
        self.speed_input.pack(padx=10,side='left')
        self.speed_input.insert(0, "5")
        
        Label(self.frame2, text="Parameter1:").pack(side='left')
        self.Parameter1 = Entry(self.frame2, width=10)
        self.Parameter1.pack(padx=10,side='left')
        self.Parameter1.insert(0, "0")
        
        Label(self.frame2, text="Parameter2:").pack(side='left')
        self.Parameter2 = Entry(self.frame2, width=10)
        self.Parameter2.pack(padx=10,side='left')
        self.Parameter2.insert(0, "0")
        self.w = Canvas(self.root, width=self.canvas_width, height=self.canvas_height)
        self.w.bind("<Button-1>", leftclick)
        self.w.pack()
        
        self.create_grid()
    
    '''
    Deze functie heb ik van internet gehaald om een grid te tekenen
    Mijn idee was om deze functie te vervangen door draw_grid waarbij er alleen maar rectangles ipv lijnen getekend worden
    Hiermee krijg je wel een mooi idee over hoe er in het canvas getekend kan worden
    '''
    def create_grid(self):
        # vertical lines at an interval of "line_distance" pixel
        for x in range(self.particle_size, self.canvas_width, self.particle_size):
            self.w.create_line(x, 0, x, self.canvas_height, fill="gray80", width=0.15)
        # horizontal lines at an interval of "line_distance" pixel
        for y in range(self.particle_size, self.canvas_height, self.particle_size):
            self.w.create_line(0, y, self.canvas_width, y, fill="gray80", width=0.15)

    '''
    This function is called to draw a particle in the given coordinate when redrawing the entire grid
    It should be called from the mousehandler
    canvas is the space the particle should be drawn in.
    n is the type of particle that should be drawn (i.e. 0=air, 1=water, 2=stone)
    x, y are x and y coordinates (x1,y1) of the pixel
    pixel_size is the fixed pixel size that is used to determine x2 and y2
    tkinter colors: http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
    '''
    def draw_particle(self, x1, y1):
        # Gebruik self.particle size om uit x1,y1 de x2,y2 af te leiden
        # 2 = stone
        # A solid filled dark-gray rectangle (gray40?)
        if self.mode == 2:
            return True

        # 1 = water
        # A solid filled blue rectangle (DodgerBlue2?)
        elif self.mode == 1:
            return True

        # A rectangle with light-gray outline (gray80?) and no fill (snow?)
        # self.mode == 0
        else:
            return True
    
    
    '''
    Draw the entire grid based on the numbers stored in coords
    Gebruik draw_particle om iedere coordinaat te tekenen

    Het hele grid steeds opnieuw tekenen kan wat omslachtig zijn; misschien iets bedenken waarbij alleen de veranderde
    getallen opnieuw getekend worden (e.g. coordinatenstelsel van vorige iteratie meegeven en kijken of getal hetzelfde is?)
    '''
    def draw_grid(self, coords):
        for y in range(self.canvas_height):
            for x in range(self.canvas_width):
                self.draw_particle(coords[y][x], x*self.particle_size, y*self.particle_size)

    def delete_button_click(self):
        self.mode = 0

    def water_button_click(self):
        self.mode = 1

    def stone_button_click(self):
        self.mode = 2

    def change_label(self):
        data = self.air_button
        self.entryLabel.configure(text=data)


def leftclick(self,eventorigin):
    global x0, y0
    x0 = eventorigin.x
    y0 = eventorigin.y
    print(x0, y0)
    print("left")


if __name__ == "__main__":
    root = Tk()
    guiFrame = GUI(root)
    root.mainloop()

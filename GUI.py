import tkinter as tk
import Simulation as s
from PIL import Image, ImageTk
import Board as b


class GUI(tk.Frame):
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
        self.simulate = False
        self.number_of_iterations = 10
        self.animation_speed = 0.25
        self.watercolor = 'DodgerBlue2'
        self.stonecolor = 'gray40'
        self.line_startx = 0
        self.line_starty = 0
        self.line_endx = 0
        self.line_endy = 0
        self.gradient = 0
        self.stop_animation = True

        # Amount of x and y pixels; y follows from height and pixel size as pixels are square
        self.x_pixels = 100
        self.pixel_size = self.canvas_width / self.x_pixels
        self.y_pixels = int(self.canvas_height / self.pixel_size)

        # Size of one pixel
        self.particle_size = int(self.pixel_size)

        self.root = tk.Tk()
        self.root.title("Super awesome animatie")

        # Button panel frame stuff
        self.frame_width, self.frame_height = 600, 100
        self.frame = tk.Frame(self.root, bg='grey')
        self.frame.pack(fill='x')
        tk.Label(self.frame, text="Draw mode:", bg='grey').pack(side='left')
        self.modelabeltext = 'Delete'
        self.modelabel = tk.Label(self.frame, bg='grey', text=self.modelabeltext, width=10)
        self.modelabel.pack(side='left')
        self.air_button = tk.Button(self.frame, text='Delete')
        self.air_button.pack(side='left', padx=10)
        self.air_button.bind('<Button-1>', self.delete_button_click)
        self.water_button = tk.Button(self.frame, text='Water')
        self.water_button.pack(side='left', padx=10)
        self.water_button.bind('<Button-1>', self.water_button_click)
        self.stone_button = tk.Button(self.frame, text='Stone')
        self.stone_button.pack(side='left', padx=10)
        self.stone_button.bind('<Button-1>', self.stone_button_click)
        self.line_button = tk.Button(self.frame, text='Line')
        self.line_button.pack(side='left', padx=10)
        self.line_button.bind('<Button-1>', self.line_button_click)

        self.start_button = tk.Button(self.frame, text='Start simulation')
        self.start_button.pack(side='left', padx=50)
        self.start_button.bind('<Button-1>', self.start_button_click)

        self.stop_button = tk.Button(self.frame, text='Stop simulation')
        self.stop_button.pack(side='left', padx=10)
        self.stop_button.bind('<Button-1>', self.stop_button_click)

        self.frame2 = tk.Frame(self.root)
        self.frame2.pack(fill='x')

        tk.Label(self.frame2, text="Animation speed:").pack(side=tk.LEFT)
        self.speed_input = tk.Entry(self.frame2, width=10)
        self.speed_input.pack(padx=10, side='left')
        self.speed_input.insert(0, str(self.animation_speed))

        tk.Label(self.frame2, text="Gravitation:").pack(side='left')
        self.gravitation = tk.Entry(self.frame2, width=10)
        self.gravitation.pack(padx=10, side='left')
        self.gravitation.insert(0, "0")

        tk.Label(self.frame2, text="Formula:", bg='lightgrey').pack(side='left')
        self.formulalabeltext = "Convection-Diffusion"
        self.formulalabel = tk.Label(self.frame2, bg='lightgrey', text=self.formulalabeltext, width=17)
        self.formulalabel.pack(side='left')
        self.formula_button = tk.Button(self.frame2, text='Formula')
        self.formula_button.pack(side='left', padx=10)
        self.formula_button.bind('<Button-1>', self.formula_button_click)

        #self.Parameter2 = Entry(self.frame2, width=10)
        #self.Parameter2.pack(padx=10, side='left')
        #self.Parameter2.insert(0, "0")
        self.w = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height)
        self.w.bind("<Button-1>", self.leftclick)
        self.w.pack()
        self.initial_board = []
        self.rectangles = []
        self.new_tuples = []
        self.board = None
        # self.board = B.Board(self.canvas_width, self.canvas_height)
        # self.target_board = B.Board(self.canvas_width, self.canvas_height)
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

    def draw_element(self, x, y, val):
        x2 = x + self.pixel_size
        y2 = y + self.pixel_size

        if val == -1:
            r = self.w.create_rectangle(x, y, x2, y2, fill=self.stonecolor)
            self.rectangles.append(r)

        elif val == 1:
            r = self.w.create_rectangle(x, y, x2, y2, fill=self.watercolor)
            self.rectangles.append(r)

        # Used for water concentrations below 100%; adds transparency
        elif 0 < val < 1:
            alpha = int(val * 255)
            fill = root.winfo_rgb(self.watercolor) + (alpha,)
            image = Image.new('RGBA', (x2 - x, y2 - y), fill)
            self.rectangles.append(ImageTk.PhotoImage(image))
            self.w.create_image(x, y, image=self.rectangles[-1], anchor='nw')

        # Val = 0
        else:
            for r in self.rectangles:
                c = self.w.coords(r)
                if c[0] == x and c[1] == y:
                    print("Rectangle found!")
                    self.w.delete(r)
                    self.rectangles.remove(r)

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
        # Add the tuple to the tuples list.
        if self.mode == 2:
            r = self.w.create_rectangle(x1, y1, x1 + self.particle_size, y1 + self.particle_size, fill=self.stonecolor)
            self.rectangles.append(r)
            self.initial_board.append((x1, y1, self.mode))
            return True

        # 1 = water
        # A solid filled blue rectangle (DodgerBlue2?)
        # Add the tuple to the tuples list.
        elif self.mode == 1:
            r = self.w.create_rectangle(x1, y1, x1 + self.particle_size, y1 + self.particle_size, fill=self.watercolor)
            self.rectangles.append(r)
            self.initial_board.append((x1, y1, self.mode))
            return True

        # A rectangle with light-gray outline (gray80?) and no fill (snow?)
        # If there is a water or stone rectangle, remove it.
        elif self.mode == 0:
            for r in self.rectangles:
                c = self.w.coords(r)
                if c[0] == x1 and c[1] == y1:
                    print("Rectangle found!")
                    self.w.delete(r)
                    self.rectangles.remove(r)
                    return True
            return True

    '''
	For all water rectangles in the list of tuples of the current board, add 1 to the height of the water
	rectangle to let it drop 1 step. Save this in the list of new_tuples.
	'''

    def delete_button_click(self, event):
        print("Delete modus")
        self.modelabel.configure(text='Delete')
        self.mode = 0

    def water_button_click(self, event):
        print("Water modus")
        self.modelabeltext = 'Water'
        self.modelabel.configure(text='Water')
        self.mode = 1

    def line_button_click(self, event):
        print("Press for first point of line")
        self.mode = 3
		
    def stone_button_click(self, event):
        print("Stone modus")
        self.modelabel.configure(text='Stone')
        self.mode = 2

    def start_button_click(self, event):
        print("Start simulation")
        self.stop_animation = False
        self.animation_speed = self.speed_input.get()
        print("Animation speed = " + str(self.animation_speed))

        self.board = b.Board(self.rectangles, self.w, self.canvas_width, self.canvas_height, self.pixel_size)
        simulation = s.Simulation(canvas=self.w, canvas_width=self.canvas_width, canvas_height=self.canvas_height,
                                  rectangles=self.rectangles, animation_speed=self.animation_speed,
                                iterations=self.number_of_iterations, pixel_size=self.particle_size)
        self.rectangles = simulation.simulate()
        return True


    def stop_button_click(self, event):
        print("Stop simulation")
        # Used in simulation to stop an otherwise indefinitely running simulation
        self.stop_animation = True
        self.number_of_iterations = 0


    def formula_button_click(self, event):
        print("Hoi")
        if self.formulalabeltext == "Convection-Diffusion":
            self.formulalabeltext = "Navier–Stokes"
        else:
            self.formulalabeltext = "Convection-Diffusion"
        self.formulalabel.configure(text=self.formulalabeltext)
        return True

    '''
	Draw the entire grid based on the numbers stored in coords
	Gebruik draw_particle om iedere coordinaat te tekenen
	
	Het hele grid steeds opnieuw tekenen kan wat omslachtig zijn; misschien iets bedenken waarbij alleen de veranderde
	getallen opnieuw getekend worden (e.g. coordinatenstelsel van vorige iteratie meegeven en kijken of getal hetzelfde is?)
	'''
    # Set the start and end values of x and y to always catch the whole grid points that are clicked in.
    def set_coords_to_grid(self,gradient):
        if gradient > 0:
            for i in range(self.particle_size):
                if (self.line_startx - i) % self.particle_size == 0:
                    self.line_startx = self.line_startx - i
                if (self.line_endx - i) % self.particle_size == 0:
                    self.line_endx = self.line_endx - i + self.particle_size            
                if (self.line_starty - i) % self.particle_size == 0:
                    self.line_starty = self.line_starty - i
                if (self.line_endy - i) % self.particle_size == 0:
                    self.line_endy = self.line_endy - i + self.particle_size
	
    def drawline(self):
        #self.w.create_line( self.line_startx, self.line_starty, self.line_endx, self.line_endy)
        self.mode = 2
        xdifference = self.line_endx - self.line_startx
        ydifference = self.line_endy - self.line_starty
        self.gradient = ydifference/xdifference
        self.set_coords_to_grid(self.gradient)
        xdifference = self.line_endx - self.line_startx
        ydifference = self.line_endy - self.line_starty
        self.gradient = ydifference/xdifference
        print("xdifference = " + str(xdifference))
        if (self.gradient < 1 and self.gradient > 0) or (self.gradient > -1 and self.gradient < 0):
            for step in range(int(abs(xdifference))):
                if step%self.particle_size == 0:
                    self.draw_element(self.line_startx+step,self.line_starty+self.gradient*step,self.mode)
        else:
            self.gradient = xdifference/ydifference
            print("start x, y: " + str(self.line_startx) + " " + str(self.line_starty)) 
            print("end x, y: " + str(self.line_endx) + " " + str(self.line_endy)) 
            for step in range(int(abs(ydifference))):
                if step%self.particle_size == 0:
                    self.draw_element(self.line_startx+step*self.gradient, self.line_starty+step, self.mode)
        self.mode = 3
	
    """
    Deze functie verandert het beginpunt van de lijn als het nodig is. Er wordt namelijk altijd van links naar rechts getekend in drawline().
    """
    def minimizestart(self):
        temporaryx = 0
        temporaryy = 0
        if(self.line_startx > self.line_endx):
            temporaryx = self.line_startx
            self.line_startx = self.line_endx
            self.line_endx = temporaryx
            temporaryy = self.line_starty
            self.line_starty = self.line_endy
            self.line_endy = temporaryy
        print("start x,  y: " + str(self.line_startx) + ", " + str(self.line_starty))
        print("end x,  y: " + str(self.line_endx) + ", " + str(self.line_endy))

    def leftclick(self, eventorigin):
        global x0, y0
        x0 = eventorigin.x
        y0 = eventorigin.y
        linex1 = 0
        # Find the closest 'whole'-grid point
        grid_x = 0
        grid_y = 0
        for i in range(self.particle_size):
            if (x0 - i) % self.particle_size == 0:
                grid_x = x0 - i
        for j in range(self.particle_size):
            if (y0 - j) % self.particle_size == 0:
                grid_y = y0 - j
        # If draw line modus is on:
        if self.mode == 3:
            self.line_startx = x0
            self.line_starty = y0
            self.mode = 4
        elif self.mode == 4:
            self.line_endx = x0
            self.line_endy = y0
            self.mode = 3
            print("start x, y: " + str(self.line_startx) + " " + str(self.line_starty)) 
            print("end x, y: " + str(self.line_endx) + " " + str(self.line_endy)) 
            self.minimizestart()
            self.drawline()
        else:
            self.draw_element(grid_x, grid_y, self.mode)


if __name__ == "__main__":
    root = tk.Tk()
    guiFrame = GUI(root)
    root.mainloop()

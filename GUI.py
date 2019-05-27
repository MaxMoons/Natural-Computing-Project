from tkinter import *
import Simulation as s


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
        self.simulate = False
        self.number_of_iterations = 10
        self.animation_speed = 0.25
        self.watercolor = 'DodgerBlue2'
        self.stonecolor = 'gray40'

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
        self.modelabeltext = 'Delete'
        self.modelabel = Label(self.frame, bg='grey', text=self.modelabeltext)
        self.modelabel.pack(side='left')
        self.air_button = Button(self.frame, text='Delete')
        self.air_button.pack(side='left', padx=10)
        self.air_button.bind('<Button-1>', self.delete_button_click)
        self.water_button = Button(self.frame, text='Water')
        self.water_button.pack(side='left', padx=10)
        self.water_button.bind('<Button-1>', self.water_button_click)
        self.stone_button = Button(self.frame, text='Stone')
        self.stone_button.pack(side='left', padx=10)
        self.stone_button.bind('<Button-1>', self.stone_button_click)

        self.start_button = Button(self.frame, text='Start simulation')
        self.start_button.pack(side='left', padx=60)
        self.start_button.bind('<Button-1>', self.start_button_click)

        self.stop_button = Button(self.frame, text='Stop simulation')
        self.stop_button.pack(side='left', padx=10)
        self.stop_button.bind('<Button-1>', self.stop_button_click)

        self.frame2 = Frame(self.root)
        self.frame2.pack(fill='x')

        Label(self.frame2, text="Animation speed:").pack(side=LEFT)
        self.speed_input = Entry(self.frame2, width=10)
        self.speed_input.pack(padx=10, side='left')
        self.speed_input.insert(0, str(self.animation_speed))

        Label(self.frame2, text="Parameter1:").pack(side='left')
        self.Parameter1 = Entry(self.frame2, width=10)
        self.Parameter1.pack(padx=10, side='left')
        self.Parameter1.insert(0, "0")

        Label(self.frame2, text="Parameter2:").pack(side='left')

        self.Parameter2 = Entry(self.frame2, width=10)
        self.Parameter2.pack(padx=10, side='left')
        self.Parameter2.insert(0, "0")
        self.w = Canvas(self.root, width=self.canvas_width, height=self.canvas_height)
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
    """
	# Set the particle in our own grid. n is the type of particle.
	def set_particle_in_grid(self, x, y):
		for i in range (self.particle_size):
			for j in range (self.particle_size):
				self.grid[x+i][y+j] = self.mode
	"""

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
	Draw all the tuple that it gets. Function is based on the draw_particle function but now without
	adding or removing tuples from the tuples list, just drawing.
	'''

    def draw_tuple(self, tuple):
        x1 = tuple[0]
        y1 = tuple[1]
        n = tuple[2]
        # Gebruik self.particle size om uit x1,y1 de x2,y2 af te leiden
        # 2 = stone
        # A solid filled dark-gray rectangle (gray40?)
        if n == 2:
            self.w.create_rectangle(x1, y1, x1 + self.particle_size, y1 + self.particle_size, fill='gray40')
            return True

        # 1 = water
        # A solid filled blue rectangle (DodgerBlue2?)
        elif n == 1:
            r = self.w.create_rectangle(x1, y1, x1 + self.particle_size, y1 + self.particle_size, fill='DodgerBlue2')

            return True

        # A rectangle with light-gray outline (gray80?) and no fill (snow?)
        #
        elif n == 0:
            for r in self.w.winfo_children():
                coordinates = r.coords()
                self.w.create_rectangle(x1, y1, x1 + self.particle_size, y1 + self.particle_size, fill='snow',
                                        outline='gray80')
        else:
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

    def stone_button_click(self, event):
        print("Stone modus")
        self.modelabel.configure(text='Stone')
        self.mode = 2

    def start_button_click(self, event):
        print("Start simulation")
        self.animation_speed = self.speed_input.get()
        print("Animation speed = " + str(self.animation_speed))
        simulation = s.Simulation(canvas=self.w, canvas_width=self.canvas_width, canvas_height=self.canvas_height,
                                  rectangles=self.rectangles, animation_speed=self.animation_speed,
                                iterations=self.number_of_iterations, pixel_size=self.particle_size)
        self.rectangles = simulation.simulate()
        return True


    def stop_button_click(self, event):
        print("Stop simulation")
        self.number_of_iterations = 0

    '''
	Draw the entire grid based on the numbers stored in coords
	Gebruik draw_particle om iedere coordinaat te tekenen
	
	Het hele grid steeds opnieuw tekenen kan wat omslachtig zijn; misschien iets bedenken waarbij alleen de veranderde
	getallen opnieuw getekend worden (e.g. coordinatenstelsel van vorige iteratie meegeven en kijken of getal hetzelfde is?)
	'''

    def draw_grid(self, coords):
        for y in range(self.canvas_height):
            for x in range(self.canvas_width):
                self.draw_particle(coords[y][x], x * self.particle_size, y * self.particle_size)

    def leftclick(self, eventorigin):
        global x0, y0
        x0 = eventorigin.x
        y0 = eventorigin.y
        # print(x0, y0)
        # Find the closest 'whole'-grid point
        grid_x = 0
        grid_y = 0
        for i in range(self.particle_size):
            if (x0 - i) % self.particle_size == 0:
                grid_x = x0 - i
        for j in range(self.particle_size):
            if (y0 - j) % self.particle_size == 0:
                grid_y = y0 - j
        # print("Grid_x = " + str(grid_x))
        # print("Grid_y = " + str(grid_y))
        self.draw_particle(grid_x, grid_y)


if __name__ == "__main__":
    root = Tk()
    guiFrame = GUI(root)
    root.mainloop()

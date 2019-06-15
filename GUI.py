import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import Board as b
import Simulation as s


class GUI(tk.Frame):
    def __init__(self, root, n_pixels=100, **kw):
        super().__init__(**kw)
        # Width and height of the canvas
        self.canvas_width, self.canvas_height = 600, 500
        self.frame_width, self.frame_height = 600, 100
        self.mode = 0
        self.simulate = False
        self.animation_speed = 0.25
        self.watercolor = 'blue'
        self.stonecolor = 'gray40'
        self.simulator = s.Simulation()
        self.line_startx = 0
        self.line_starty = 0
        self.line_endx = 0
        self.line_endy = 0
        self.gradient = 0
        self.stop_animation = True

        # Amount of x and y pixels; y follows from height and pixel size as pixels are square
        self.x_pixels = n_pixels
        self.pixel_size = self.canvas_width // n_pixels
        self.y_pixels = self.canvas_height // self.pixel_size
        self.line_width = 15 // self.pixel_size

        self.root = root
        self.root.title("Convection-diffusion water flow simulation")

        # Button panel frame stuff
        self.frame_width, self.frame_height = 600, 100
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill='x')
        tk.Label(self.frame, text="Draw mode:").pack(side='left')
        self.modelabeltext = 'Delete'
        self.modelabel = tk.Label(self.frame, text=self.modelabeltext, width=7)
        self.modelabel.pack(side='left')
        self.air_button = tk.Button(self.frame, text='Delete')
        self.air_button.pack(side='left', padx=2)
        self.air_button.bind('<Button-1>', self.delete_button_click)
        self.water_button = tk.Button(self.frame, text='Water')
        self.water_button.pack(side='left', padx=2)
        self.water_button.bind('<Button-1>', self.water_button_click)
        self.stone_button = tk.Button(self.frame, text='Stone')
        self.stone_button.pack(side='left', padx=2)
        self.stone_button.bind('<Button-1>', self.stone_button_click)
        self.line_button = tk.Button(self.frame, text='Line')
        self.line_button.pack(side='left', padx=2)
        self.line_button.bind('<Button-1>', self.line_button_click)
        tk.Label(self.frame, text="% Water:").pack(side=tk.LEFT)
        self.water_input = tk.Entry(self.frame, width=4)
        self.water_input.pack(padx=10, side='left')
        self.water_input.insert(0, '100')

        self.start_button = tk.Button(self.frame, text='Start simulation')
        self.start_button.pack(side='left', padx=6)
        self.start_button.bind('<Button-1>', self.start_button_click)

        self.stop_button = tk.Button(self.frame, text='Stop simulation')
        self.stop_button.pack(side='left', padx=4)
        self.stop_button.bind('<Button-1>', self.stop_button_click)

        self.frame2 = tk.Frame(self.root)
        self.frame2.pack(fill='x')

        tk.Label(self.frame2, text="Animation speed:").pack(side=tk.LEFT)
        self.speed_input = tk.Entry(self.frame2, width=5)
        self.speed_input.pack(padx=3, side='left')
        self.speed_input.insert(0, str(self.animation_speed))

        tk.Label(self.frame2, text="Time step size:").pack(side=tk.LEFT)
        self.step_input = tk.Entry(self.frame2, width=5)
        self.step_input.pack(padx=3, side='left')
        self.step_input.insert(0, '10')

        tk.Label(self.frame2, text="Gravitation:").pack(side='left')
        self.gravitation = tk.Entry(self.frame2, width=5)
        self.gravitation.pack(padx=3, side='left')
        self.gravitation.insert(0, "5")

        self.formulalabeltext = "Convection-Diffusion"
        self.formulalabel = tk.Label(self.frame2, text=self.formulalabeltext, width=17)
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

        # One element = (rectangle, x1, y1)
        self.rectangles = []
        self.new_tuples = []
        self.board = None
        self.create_grid()

    def get_root(self):
        return self.root

    '''
	Deze functie heb ik van internet gehaald om een grid te tekenen
	Mijn idee was om deze functie te vervangen door draw_grid waarbij er alleen maar rectangles ipv lijnen getekend worden
	Hiermee krijg je wel een mooi idee over hoe er in het canvas getekend kan worden
	'''
    def create_grid(self):
        # vertical lines at an interval of "line_distance" pixel
        for x in range(0, self.canvas_width, self.pixel_size):
            self.w.create_line(x, 0, x, self.canvas_height, fill="gray80", width=0.15)

        # horizontal lines at an interval of "line_distance" pixel
        for y in range(0, self.canvas_height, self.pixel_size):
            self.w.create_line(0, y, self.canvas_width, y, fill="gray80", width=0.15)

    def draw_element(self, x, y, val):
        x2 = x + self.pixel_size
        y2 = y + self.pixel_size

        # Stone
        if val == -1:
            r = self.w.create_rectangle(x, y, x2, y2, fill=self.stonecolor, outline=self.stonecolor)
            self.rectangles.append((r, x, y))

        # 100% water
        elif val == 1:
            r = self.w.create_rectangle(x, y, x2, y2, fill=self.watercolor, outline=self.watercolor)
            self.rectangles.append((r, x, y))

        # <100% water; adds transparency
        elif 0 < val < 1:
            def create_rectangle(x1, y1, x2, y2, **kwargs):
                if 'alpha' in kwargs:
                    alpha = int(kwargs.pop('alpha') * 255)
                    fill = kwargs.pop('fill')
                    fill = self.root.winfo_rgb(fill) + (alpha,)
                    image = Image.new('RGBA', (x2 - x1, y2 - y1), fill)
                    img = ImageTk.PhotoImage(image)
                    self.w.create_image(x1, y1, image=img, anchor='nw')
                    self.rectangles.append((img, x, y))
            create_rectangle(x, y, x2, y2, fill='blue', alpha=val, outline="")

        # Nothing; val = 0, so remove that rectangle
        else:
            for r in self.rectangles:
                if r[1] == x and r[2] == y:
                    print("Rectangle found!")
                    self.w.delete(r[0])
                    self.rectangles.remove(r)


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
        self.modelabel.configure(text='Line')
        self.mode = 3

    def stone_button_click(self, event):
        print("Stone modus")
        self.modelabel.configure(text='Stone')
        self.mode = -1

    def start_button_click(self, event):
        print("Start simulation")
        self.stop_animation = False
        self.animation_speed = self.speed_input.get()
        print("Animation speed = " + str(self.animation_speed))
        self.board = b.Board(self.rectangles, self.w, self.canvas_width, self.canvas_height, self.pixel_size)
        self.simulator.simulate(board=self.board, formula=self.formulalabel, stones=self.board.stones)
        return True

    def stop_button_click(self, event):
        print("Stop simulation")
        # Used in simulation to stop an otherwise indefinitely running simulation
        # This value is returned from redraw board, which is called after every animation step, to notify simulation
        # of whether it should continue simulating or not
        self.stop_animation = True

    def formula_button_click(self, event):
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
    def set_coords_to_grid(self, gradient):
        if gradient > 0:
            for i in range(self.pixel_size):
                if (self.line_startx - i) % self.pixel_size == 0:
                    self.line_startx = self.line_startx - i
                if (self.line_endx - i) % self.pixel_size == 0:
                    self.line_endx = self.line_endx - i + self.pixel_size
                if (self.line_starty - i) % self.pixel_size == 0:
                    self.line_starty = self.line_starty - i
                if (self.line_endy - i) % self.pixel_size == 0:
                    self.line_endy = self.line_endy - i + self.pixel_size

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
                if step%self.pixel_size == 0:
                    self.draw_element(self.line_startx+step,self.line_starty+self.gradient*step, -1)
        else:
            self.gradient = xdifference/ydifference
            print("start x, y: " + str(self.line_startx) + " " + str(self.line_starty)) 
            print("end x, y: " + str(self.line_endx) + " " + str(self.line_endy)) 
            for step in range(int(abs(ydifference))):
                if step%self.pixel_size == 0:
                    self.draw_element(self.line_startx+step*self.gradient, self.line_starty+step, -1)
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
        for i in range(self.pixel_size):
            if (x0 - i) % self.pixel_size == 0:
                grid_x = x0 - i
        for j in range(self.pixel_size):
            if (y0 - j) % self.pixel_size == 0:
                grid_y = y0 - j
        # If draw line modus is on:
        if self.mode == 3:
            self.line_startx, self.line_starty = self.identify_pixel(x0, y0)
            self.mode = 4
        elif self.mode == 4:
            self.line_endx, self.line_endy = self.identify_pixel(x0, y0)
            self.mode = 3
            print("start x, y: " + str(self.line_startx) + " " + str(self.line_starty)) 
            print("end x, y: " + str(self.line_endx) + " " + str(self.line_endy)) 
            #self.minimizestart()
            #self.drawline()
            self.draw_stone_line()
        elif self.mode == 1:
            val = int(self.water_input.get())
            if val < 0:
                val = 0
            elif val > 100:
                val = 100
            self.draw_element(grid_x, grid_y, val/100)
        else:
            self.draw_element(grid_x, grid_y, self.mode)

    # This function is called from simulation; it is used to draw the entire representation of the board after 1 iteration
    def redraw_board(self, b):
        # Delete all non-stone (water) tiles, i.e. assume all water tiles change position/value
        for r in self.rectangles:
            if self.w.itemcget(r[0], "fill") != self.stonecolor:
                self.w.delete(r[0])
                self.rectangles.remove(r)

        # Draw new water tiles that were given by the representation
        # I.e. > 0 means it's water
        for y in range(self.canvas_height // self.pixel_size):
            for x in range(self.canvas_width // self.pixel_size):
                val = b.get_value(x, y)
                if val > 0:
                    self.draw_element(x, y, val)
        # Return stop_animation to notify Simulation of whether it should continue to simulate or not
        return self.stop_animation

    def draw_stone_line(self):
        x_step, y_step = self.get_steps()
        print(x_step, y_step)
        line = self.get_line_pixels(self.line_startx, self.line_starty, self.line_endx, self.line_endy, x_step, y_step)
        line = self.widen_line(line)
        for p in line:
            if not self.can_draw(p):
                line.remove(p)
        for p in line:
            self.draw_element(p[0], p[1], -1)

    # Is this pixel already drawn?
    def can_draw(self, p):
        for r in self.rectangles:
            if p[0] == r[1] and p[1] == r[2]:
                return False
        return True

    # Make sure the line is as wide as self.line_width dictates
    # Ensures the line is of a certain width in case the pixel_size is very small
    def widen_line(self, line):
        candidates = []
        for p in line:
            x_space = np.linspace(p[0]-(self.line_width//2)*self.pixel_size, p[0]+(self.line_width//2)*self.pixel_size, self.line_width)
            y_space = np.linspace(p[1]-(self.line_width//2)*self.pixel_size, p[1]+(self.line_width//2)*self.pixel_size, self.line_width)
            for x in x_space:
                for y in y_space:
                    if self.canvas_width-self.pixel_size >= x >= 0 and self.canvas_height-self.pixel_size >= y >= 0:
                        candidate = x, y
                        if candidate not in line and candidate not in candidates:
                            candidates.append(candidate)
        for c in candidates:
            line.append(c)
        return line

    def get_line_pixels(self, x1, y1, x2, y2, x_step, y_step):
        pixels = []
        # Set coords to pixel center rather than top-left corner
        x1 += self.pixel_size / 2
        y1 += self.pixel_size / 2
        x2 += self.pixel_size / 2
        y2 += self.pixel_size / 2
        if abs(x_step) == 1:
            while x1 != x2:
                pixel = self.identify_pixel(x1, y1)
                if pixel not in pixels:
                    pixels.append(pixel)
                x1 += x_step
                y1 += y_step
        else:
            while y1 != y2:
                pixel = self.identify_pixel(x1, y1)
                if pixel not in pixels:
                    pixels.append(pixel)
                x1 += x_step
                y1 += y_step
        return pixels

    # Identify the step sizes for finding the pixels within a drawn line
    # Return the 1-step as first argument, the other as second
    def get_steps(self):
        x_step, y_step = 1, 1
        if abs(self.line_startx-self.line_endx) >= abs(self.line_starty - self.line_endy):
            y_step = (self.line_endy - self.line_starty) / abs(self.line_startx - self.line_endx)
            if self.line_endx < self.line_startx:
                x_step = -1
        else:
            x_step = (self.line_endx - self.line_startx) / abs(self.line_starty - self.line_endy)
            if self.line_starty > self.line_endy:
                y_step = -1
        return x_step, y_step

    # Given an x and y coordinate, in which pixel am I?
    # i.e. get top-left corner of current pixel
    def identify_pixel(self, x, y):
        x, y = int(x), int(y)
        while x % self.pixel_size != 0:
            x -= 1
        while y % self.pixel_size != 0:
            y -= 1
        return x, y


if __name__ == "__main__":
    x_pixels = 150
    root = tk.Tk()
    gui = GUI(root, x_pixels)
    root = gui.get_root()
    root.mainloop()

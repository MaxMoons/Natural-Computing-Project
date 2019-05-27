from tkinter import *
import numpy as np
import time
import Board as B


class Simulation():
    def __init__(self, canvas, canvas_width, canvas_height, rectangles, animation_speed, iterations, pixel_size):
        self.canvas = canvas
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.rectangles = rectangles
        self.nextconfig = []
        self.animation_speed = animation_speed
        self.iterations = iterations
        self.watercolor = 'DodgerBlue2'
        self.stonecolor = 'gray40'
        self.pixel_size = pixel_size

    def simulate(self):
        iteration = 0
        while iteration < iterations:
            iteration += 1
            self.get_next_config()
			self.clear_canvas()
			self.draw_rectangles()
            # Bereken uit rectangles de posities van de nieuwe rectangles get_next_config
                # Sla iedere nieuwe rectangle op in next_config
            # Verwijder de huidige getekende rectangles clear_canvas
            # Teken de rectangles in next_config (draw_rectangles)
            # Sla next_config op als rectangles (update_lists)
            # Leeg de list van next_config (update_lists)

    '''
    Hierin wordt de configuratie van de volgende iteratie berekend
    '''
    def get_next_config(self):
		for i in range(len(self.rectangles)):
			if self.rectangles[i].iswater():
				self.move_rect(self.rectangles[i],"down")
			else:
				self.next_config.append(rectangles[i])

    '''
    Hier worden alle getekende rectangles verwijderd
    '''
    def clear_canvas(self):
        for r in self.rectangles:
            self.canvas.delete(r)
        self.rectangles = []
        return True

    '''
    Hier worden de nieuwe rectangles van de volgende configuratie getekend
    '''
    def draw_rectangles(self):
        for c in self.nextconfig:
            r = self.canvas.create_rectangle(c[0], c[1], c[0]+self.pixel_size, c[1]+self.pixel_size, fill=c[2])
            self.rectangles.append(r)
        self.nextconfig = []
        return True

    '''
    Hier worden de lijsten geupdate
    - rectangles wordt next_config
    - next_config wordt een lege list
    '''
    def update_lists(self):
		self.rectangles = self.next_config
		self.next_config = []



    # Plaats van de huidige rectangle de rectangle van de volgende stap in next_config
    def move_rect(self, rectangle, direction):
		if (direction == "down"):
			self.next_config.append((x1,y1+self.pixel_size,self.watercolor))
		elif (direction == "up"):
			self.next_config.append((x1,y1-self.pixel_size,self.watercolor))
		elif (direction == "right"):
			self.next_config.append((x1+self.pixel_size,y1,self.watercolor))
		elif (direction == "left"):
			self.next_config.append((x1-self.pixel_size,y1,self.watercolor))




    '''
    Iterate over every rectangle
    Determine per rectangle what its next position should be based on formulas, its element and its neighbours
    '''
    def next_step(self):
        next_config = []

        # Iterate over all rectangles;
        for r in self.rectangles:
            if iswater(r):
                return True

    def drop_water(self):
        remove = False
        tuple_to_remove = ((0, 0, 0))
        self.new_tuples = self.tuples
        for i in range(len(self.tuples)):
            if self.tuples[i][2] == 1:
                # Let the water rectangle drop
                self.new_tuples.append((self.tuples[i][0], self.tuples[i][1] + 5, 1))
                # Delete the water rectangle at current position
                self.new_tuples.remove(self.tuples[i])


    def iswater(self, rectangle):
        return self.canvas.itemcget(rectangle, "fill") == self.watercolor

    def isstone(self, rectangle):
        return self.canvas.itemcget(rectangle, "fill") == self.stonecolor
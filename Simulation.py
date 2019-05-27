from tkinter import *
import numpy as np
import time
import Board as B


class Simulation(canvas, canvas_width, canvas_height, pixels, animation_speed, iterations, pixel_size):
    def __init__(self, canvas, rectangles, animation_speed, iterations):
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
        return True

    '''
    Hier worden alle getekende rectangles verwijderd
    '''
    def clear_canvas(self):
        return True

    '''
    Hier worden de nieuwe rectangles van de volgende configuratie getekend
    '''
    def draw_rectangles(self):
        return True

    '''
    Hier worden de lijsten geupdate
    - rectangles wordt next_config
    - next_config wordt een lege list
    '''
    def update_lists(self):
        return True



    # Plaats van de huidige rectangle de rectangle van de volgende stap in next_config
    def move_rect(self, rectangle, direction):


    # Verwijder de oude getekende rectangles
    def remove_rects(self):


    # Teken de nieuwe configuratie
    def draw_rectangles(self):




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

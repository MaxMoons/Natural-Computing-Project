from tkinter import *
import numpy as np
import time
import Board as B


class Simulation(canvas, pixels, animation_speed, iterations. pixel_size):
    def __init__(self, canvas, rectangles, animation_speed, iterations):
        self.canvas = canvas
        self.rectangles = rectangles
        self.nextconfig = []
        self.animation_speed = animation_speed
        self.iterations = iterations
        self.watercolor = 'DodgerBlue2'
        self.stonecolor = 'gray40'
        self.pixel_size = pixel_size

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

    # calculate changes in grid for every step
    def next_step(self):
        self.drop_water()
        for i in range(len(self.new_tuples)):
            self.draw_tuple(self.new_tuples[i])
        self.tuples = self.new_tuples

    def simulation(self):
        for i in range(5):
            self.next_step()
            time.sleep(0.5)

    def iswater(self, rectangle):
        return self.canvas.itemcget(rectangle, "fill") == self.watercolor

    def isstone(self, rectangle):
        return self.canvas.itemcget(rectangle, "fill") == self.stonecolor

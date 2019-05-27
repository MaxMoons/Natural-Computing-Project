from tkinter import *
import numpy as np
import time
import Board as B


class Simulation(canvas, pixels, animation_speed, iterations. pixel_size):
    def __init__(self, canvas, rectangles, animation_speed, iterations):
        self.canvas = canvas
        self.rectangles = rectangles
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




    def iswater(self, rectangle):
        return self.canvas.itemcget(rectangle, "fill") == self.watercolor

    def isstone(self, rectangle):
        return self.canvas.itemcget(rectangle, "fill") == self.stonecolor

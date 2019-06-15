import tkinter as tk
import numpy as np
from time import sleep
import Board as b


class Simulation():
    def __init__(self):
        self.matrices = self.createMatrices()

    # NB Stones is aantal stenen in grid
    def simulate(self, board, formula, stones, parameters):
        return board

    def createMatrices(self):
        matrices = np.zeros((3,3,32), dtype=float)
        #Look at diffusion/NS matrices. Diagonal values DO NOT MATTER, thats why size 2**5=32
        
        return matrices
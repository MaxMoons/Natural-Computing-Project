import tkinter as tk
import numpy as np


class Board:
    def __init__(self, canvas_width, canvas_height, pixel_size):
        # Coordinate grid for drawing stuff; first index is y (vertical), second is x (horizontal)
        self.board = np.zeros((canvas_height//pixel_size, canvas_width//pixel_size), dtype=float)

    # 0 = nothing
    # 0-1 = water (i.e. 1 = 100% concentration)
    # -1 = stone
    def set_value(self, x, y, val):
        self.board[y][x] = val

    # Return the value of a particle in the grid
    def get_value(self, x, y):
        return self.board[y][x]

    def get_stone_amount(self):
        count = 0
        for r in self.board:
            for c in r:
                if c == -1:
                    count += 1
        return count

    # Return the 2D array
    def get_board(self):
        return self.board

    # Print the entire board
    def print_board(self):
        for row in self.board:
            print(row)

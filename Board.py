import tkinter as tk
import numpy as np


class Board:
    def __init__(self, rectangles, canvas, canvas_width, canvas_height, pixel_size):
        # Coordinate grid for drawing stuff; first index is y (vertical), second is x (horizontal)
        self.board = np.zeros((canvas_height//pixel_size, canvas_width//pixel_size), dtype=float)
        self.stones = self.set_initial_values(canvas, rectangles, pixel_size)

    # 0 = nothing
    # 0-1 = water (i.e. 1 = 100% concentration)
    # -1 = stone
    def set_value(self, x, y, val):
        self.board[y][x] = val

    # Return the value of a particle in the grid
    def get_value(self, x, y):
        return self.board[y][x][0]

    '''
    Copy the rectangles drawn before the simulation to the board as x,y values   
    '''
    def set_initial_values(self, canvas, rectangles, pixel_size):
        # Keep track of amount of stone tiles for simulator
        stones = 0
        for r in rectangles:
            coords = canvas.coords(r)
            # Color = water;
            if canvas.itemcget(r, "fill") == 'DodgerBlue2':
                self.set_value(r[1]//pixel_size, r[2]//pixel_size, 1.0)
            # Or stone;
            else:
                stones += 1
                self.set_value(int(r[1]//pixel_size), int(r[2]//pixel_size), -1.0)
        return stones

    def get_board(self):
        return self.board

    def print_board(self):
        for row in self.board:
            print(row)


if __name__ == "__main__":
    b = Board(None, None, 5, 5, 1)
    b.board[4][4][0] = 2
    b.board[2][3][0] = 2
    b.board[1][0][0] = 2
    print("Board b:")
    b.print_board()

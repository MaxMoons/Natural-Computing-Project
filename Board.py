import tkinter as tk
import numpy as np
import GUI as gui


class Board:
    def __init__(self, rectangles, canvas, canvas_width, canvas_height, pixel_size):
        # Coordinate grid for drawing stuff; first index is y (vertical), second is x (horizontal)
        self.canvas = canvas
        self.pixel_size = pixel_size
        self.board = np.zeros((canvas_height/pixel_size, canvas_width/pixel_size), dtype=float)
        self.set_initial_values(rectangles)



    # 0 = nothing
    # 0-1 = water (i.e. 1 = 100% concentration)
    # -1 = stone
    def set_value(self, x, y, val):
        coordinates = self.canvas.coords(rectangle)
        self.board[int(coordinates[1] / self.pixel_size)][int(coordinates[0] / self.pixel_size)] = val

    # Return the value of a particle in the grid
    def get_value(self, x, y):
        return self.board[y][x][0]

    '''
    Copy the rectangles drawn before the simulation to the board as x,y values   
    '''
    def set_initial_values(self, rectangles):
        for r in rectangles:
            coords = self.canvas.coords(r)
            color = self.canvas.itemcget(r, "fill")

            # Set to 100% water;
            if color == self.watercolor:
                self.board[coords[0]][coords[1]][0] = 1
            # Set to stone;
            else:
                self.board[coords[0]][coords[1]][0] = -1

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

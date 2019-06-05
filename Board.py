import tkinter as tk
import numpy as np
import GUI as gui

''''
Class that is used for defining the canvas in the GUI
Board is initialized as filled with zeros
Board can be used to draw the rectangles on the canvas


    
    TO-DO in GUI:
    When clicking the mouse to place a stone/water tile, store the coords and the value as a tuple (x,y,val) in a list
    When clicking the mouse to remove a stone/water tile, remove this tuple from the list
    When starting the simulation, use pass this list to define the initial drawn board
    After each time step, pass a list of tuples with altered tiles to update the board
'''


class Board:
    def __init__(self, rectangles, canvas, canvas_width, canvas_height, pixel_size):
        # Coordinate grid for drawing stuff; first index is y (vertical), second is x (horizontal)
        self.canvas = canvas
        self.board_width = canvas_width
        self.board_height = canvas_height
        self.pixel_size = pixel_size
        self.watercolor = 'DodgerBlue2'
        self.stonecolor = 'gray40'
        self.board = self.make_empty_board()

    # Make a list of lists containing lists set to 0
    # Each list on every position contains a value, x_velocity and y_velocity
    def make_empty_board(self):
        board = []
        for y in range(self.board_height):
            row = []
            for x in range(self.board_width):
                row.append([0, 0, 0])
            board.append(row)
        return board

    # 0 = nothing
    # 0-1 = water (i.e. 1 = 100% concentration)
    # 2 = stone
    def set_value(self, x, y, val):
        coordinates = self.canvas.coords(rectangle)
        self.board[int(coordinates[1] / self.pixel_size)][int(coordinates[0] / self.pixel_size)] = val

    # Set particle velocity on position x,y, coded in x and y direction
    # i.e. [vel_x, vel_y]
    def set_velocity(self, x, y, velocity):
        self.board[y][x][1] = velocity[0]
        self.board[y][x][2] = velocity[1]

    # Return the value of a particle in the grid
    def get_value(self, x, y):
        return self.board[y][x][0]

    # Return the velocity of this particle in the x and y direction
    def get_velocity(self, x, y):
        return self.board[y][x][1], self.board[y][x][2]

    '''
    Copy the rectangles drawn before the simulation to the board as x,y values   
    '''
    def set_initial_values(self):
        for r in rectangles:
            coords = self.canvas.coords(r)
            color = self.canvas.itemcget(r, "fill")

            # Set to 100% water;
            if color == self.watercolor:
                self.board[coords[0]][coords[1]][0] = 1
            # Set to stone;
            else:
                self.board[coords[0]][coords[1]][0] = 2


    '''
    Copies the board from this simulation board to target
    Used for creating a new board for the next time step in the simulation
    '''

    def copy_board(self, target):
        target.board = self.board
        target.board_width = self.board_width
        target.board_height = self.board_height

    '''
    Return the board as a list of tuples containing the coordinates that have value 1 or 2 (i.e. 0 values do not have to be drawn)
    '''

    def get_board(self):
        output = []
        for x in range(self.board_width):
            for y in range(self.board_height):
                if self.board[y][x] != 0:
                    output.append((x, y, self.board[y][x]))
        return output

    '''
    Compare the boards to see which values have to be changed.
    The values that have changed indicate which rectangles should be added or removed to make sure only tiles of which
    the values have been altered will be redrawn
    Output will be a list of tuples (x,y,val) where every tuple represents a tile that has been changed
    This output should contain ALL the tiles that have to be redrawn after a time step
    '''

    def get_changed_values(self, old_board):
        output = []
        for x in range(self.board_width):
            for y in range(self.board_height):
                if self.board[y][x] != old_board.board[y][x]:
                    output.append((x, y, self.board[y][x]))
        return output

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

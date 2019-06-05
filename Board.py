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
        self.board = np.zeros((canvas_height, canvas_width))
        self.canvas = canvas
        self.board = self.board.tolist()
        self.board_width = canvas_width
        self.board_height = canvas_height
        self.pixel_size = pixel_size
        self.watercolor = 'DodgerBlue2'
        self.stonecolor = 'gray40'

    def set_value(self, rectangle, val):
        coordinates = self.canvas.coords(rectangle)
        self.board[int(coordinates[1]/self.pixel_size)][int(coordinates[0]/self.pixel_size)] = val

    '''
    Tuples is a list of tuples (x, y, val)
    Used to copy the initial board after drawing the tiles    
    '''
    def set_board(self, tuples):
        for t in tuples:
            self.board[t[1]][t[0]] = t[2]

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
    b = Board(5, 5)
    b.set_value(4, 4, 2)
    b.set_value(1, 3, 2)
    b.set_value(2, 1, 2)
    print("Board b:")
    b.print_board()

    a = Board(5, 5)
    print("Board a:")
    a.print_board()

    print("Changed values:")
    values = b.get_changed_values(a)
    print(values)

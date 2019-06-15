import numpy as np
from time import sleep
import Board as b


class Simulation():
    def __init__(self, formula, stones, parameters):
        self.formula = formula
        self.stones = stones
        assert len(parameters)==3, "Wrong parameters given"
        self.sim_speed = float(parameters[0])
        self.time_step = float(parameters[1])
        self.gravitation = float(parameters[2])
        self.diffusion = np.asarray([[0,1,0],[1,-4,1],[0,1,0]])*self.time_step
        self.velocity = np.asarray([-1,0,1]).reshape(3,1)*self.gravitation*self.time_step

    def simulate(self, board):
        old_board = board.get_board
        old_balance = sum(old_board.flatten()) + self.stones
        
        #First Order Derivative
        fod = self.first_order_derivative(old_board)
        
        #Second Order Derivative
        sod = self.second_order_derivative(old_board)
        
        #Convolving velocity over FOD, DOES NOT WORK
        convection = self.conv1d(self.velocity, fod)
        
        #Convolving diffusion over SOD, DOES NOT WORK
        diffusion = self.conv2d(self.diffusion, sod)
        
        #Subtract two boards
        new_board = diffusion-convection
        new_balance = sum(new_board.flatten()) + self.stones
        assert np.abs(old_balance-new_balance)<1e10, "Mass has change, Critical error"
        
        return new_board
    
    def first_order_derivative(self, area):
        size_x = len(area)
        size_y = len(area[0])
        pad_area = np.pad(area,1,mode='constant', constant_values=0)
        new_area_x = np.zeros((size_x,size_y), dtype=float)
        new_area_y = np.zeros((size_x,size_y), dtype=float)
        
        for i in range(1,len(pad_area)-1):
            for j in range(1,len(pad_area[i])-1):
                new_area_x[j-1][i-1] = pad_area[i+1][j]-pad_area[i-1][j]                     
                new_area_y[j-1][i-1] = pad_area[i][j+1]-pad_area[i][j-1]
                
        return new_area_x + new_area_y
    
    def second_order_derivative(self, area):
        size_x = len(area)
        size_y = len(area[0])
        pad_area = np.pad(area,1,mode='constant', constant_values=0)
        new_area_x = np.zeros((size_x,size_y), dtype=float)
        new_area_y = np.zeros((size_x,size_y), dtype=float)
        
        for i in range(1,len(pad_area)-1):
            for j in range(1,len(pad_area[i])-1):
                new_area_x[j-1][i-1] = pad_area[i+1][j]+pad_area[i-1][j]-2*pad_area[i][j]                     
                new_area_y[j-1][i-1] = pad_area[i][j+1]+pad_area[i][j-1]-2*pad_area[i][j]
        return new_area_x + new_area_y
   
    def conv1d(self, kernel, area):
        size_y = len(kernel)+1   
        new_area = np.zeros((len(area),len(area[0])), dtype=float)
        pad_area = np.pad(area,1,mode='constant', constant_values=-1)
        
        for i in range(len(pad_area)-size_y):
            for j in range(1,len(pad_area[i])-2):
                if(pad_area[i+1][j]>0):    
                    if(pad_area[i][j]>0 and pad_area[i+2][j]>0):
                        new_area[i][j] += pad_area[i][j]*kernel[0][0]
                        new_area[i+1][j] += pad_area[i+1][j]*kernel[1][0]
                        new_area[i+2][j] += pad_area[i+2][j]*kernel[2][0]
                    elif(pad_area[i][j]>0 and pad_area[i+2][j]<0):
                        new_area[i][j] += pad_area[i][j]*kernel[0][0]
                        new_area[i+1][j] += pad_area[i+1][j]*kernel[2][0]
                    elif(pad_area[i][j]<0 and pad_area[i+2][j]>0):
                        new_area[i+1][j] += pad_area[i+1][j]*kernel[0][0]
                        new_area[i+2][j] += pad_area[i+1][j]*kernel[2][0]              
                
        return new_area
    
    def conv2d(self, kernel, area):
        size_x = len(kernel[0])
        size_y = len(kernel)        
        new_area = np.zeros((len(area),len(area[0])), dtype=float)
        pad_area = np.pad(area,1,mode='constant', constant_values=-1)
        
        for i in range(len(pad_area)-size_y):
            for j in range(len(pad_area[i])-size_x):
                if(pad_area[i+(size_y//2)][j+(size_x//2)]>0):
                    for l in range(size_y):
                        for k in range(size_x):                            
                            nr = [pad_area[i+(size_y//2)][0],pad_area[0][j+(size_x//2)],pad_area[i+(size_y//2)][size_x-1],pad_area[size_y-1][j+(size_x//2)]].count(-1)
                            if(pad_area[i+l][j+k]>=0 or not (l==size_y//2 and k==size_x//2)):
                                new_area[i+l][j+k] += pad_area[i+l][j+k]*kernel[l][k]
                    new_area[i+size_y//2][j+size_x//2] += (kernel[size_y//2][size_x//2]+nr*kernel[0][1])*pad_area[i+size_y//2][j+size_x//2]
                
        return new_area
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
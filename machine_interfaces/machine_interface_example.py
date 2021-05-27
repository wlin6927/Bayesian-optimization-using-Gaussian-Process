# -*- coding: iso-8859-1 -*-

import numpy as np

class machine_interface:
    """    
    This is the class that talks to the machine.

    To get it ready for a given machine, follow these steps. 
    The steps will start from the bottom of the script and work 
    upward so as to preserve referenced line numbers as you edit the code:

    1) On line 43, replace the expression to the right of the equal sign with 
    an expression that queries the machine and returns a float representing the current objective value
    2) At line 37, add expressions to set the machine control pvs to the position 
    called self.x -- Note: self.x is a 2-dimensional array of shape (1, ndim). 
    To get the values as a 1d-array, use self.x[0]
    3) On line 31, replace the expression to the right of the equal sign with an 
    expression that returns the current control pv values (i.e. the current x-position) f
    rom the machine as a 1-d array
    4) On line 29, replace the string to the right of the equal sign with 
    whatever you want to call your machine. The name is inconsequential, except that 
    you must not call it 'MultinormalInterface'
    5) At line 27, add any imports necessary for communicating with the machine in the 
    expressions you have added as a result of the steps above
    """
    def __init__(self, dev_ids, start_point = None):
        self.pvs = np.array(dev_ids)
        self.name = 'basic_multinormal' #name your machine interface. doesn't matter what you call it as long as it isn't 'MultinormalInterface'.
        if type(start_point) == type(None):
            current_x = np.zeros(len(self.pvs)) #replace with expression that reads current ctrl pv values (x) from machine
            self.setX(current_x)
        else: 
            self.setX(start_point)
            
    def gaussian(self, x, mu, sigma):
        return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sigma, 2.)))

    def add_gaussian2(self, x,mu1=2,std1=1,mu2=8,std2=3):
        return self.gaussian(x, mu1, std1) + self.gaussian(x,mu2,std2)

    def add_list(self, value_list):
        return sum([20*self.add_gaussian2(x) for x in value_list])

    def obj_func(self, x_list):
        #res = self.add_list(x_list) + 20 * np.sin(4*c1) + 20 * np.sin(2*c2)
        res = self.add_list(x_list)
        return res / 1e5

    def setX(self, x_new):
        self.x = np.array(x_new, ndmin=2)
        # add expressions to set machine ctrl pvs to the position called self.x 
        # Note: self.x is a 2-dimensional array of shape (1, ndim). 
        # To get the values as a 1d-array, use self.x[0]
        
    def getContext(self, time=0):
        self.c1 = time
        #self.c2 = time+1
        #return np.array([2 * np.sin(4*self.c1), 2 * np.sin(2*self.c2)])
        return np.array([np.sin(self.c1)])
        #return np.array([np.sin(time)])

    def getState(self, time=0):
        self.c1 = time
        #self.c2 = time+1
        
        objective_state = 5.0 * np.exp(-0.5*self.x[0].dot(np.eye(len(self.pvs))).dot(self.x[0].T)) + 0.001*np.random.normal() + np.sin(self.c1) #replace with expression that returns float representing current objective value
        
        #objective_state = self.obj_func(self.x[0])
        
        input = np.concatenate((self.x[0],self.getContext(time)))
        
        return np.array(input, ndmin = 2), np.array([[objective_state]])
    
 
    

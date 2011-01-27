'''
Created on 27/01/2011

@author: rogerio_bulha
'''

import math

from RSService import CRSService

class CRSDSS(CRSService):
    '''
    This class represents an actuator (differential steering system)
    '''
    def __init__(self,local_port):
        '''
        Constructor
        '''
        if local_port >= 49601 and local_port <= 49700:
            try:
                CRSService.__init__(self,'DSS',local_port,49580) #local_port from 49601 to 49700
            except:
                print 'CRSDSS - XML-RPC server fail'
            else:
                print 'CRSDSS - running'
        else:
            print 'CRSDSS - running out of ports'
        '''
        Properties
        '''
        self.X0  = 0
        self.Y0  = 0
        self.O0  = 0
        self.VR0 = 0
        self.VL0 = 0
        self.SR0 = 0
        self.SL0 = 0
        self.S0  = 0
        
        self.X = []
        self.Y = []
        self.O = []
        
        #load initial condition
        self.step_count = 1 #first step keep the initial values
        self.X.append(self.X0)
        self.Y.append(self.Y0)
        self.O.append(self.O0)
        
        self.wheel_radius = 0.03 #radios of the wheel in meters
        self.whell_axi_size = 0.15 #distance between whells in meters
        self.delta_time = 0.1 #delta time in sec.
        self.simulation_time = 0 #total simulated time in sec.
 
    def step(self):
        input = self.crsServer.PyRoboticStudio.input('DSS')
        if input and input.has_key('VR') and input.has_key('VL'): 
            self.SR0 = input['VR'] * self.delta_time
            self.SL0 = input['VL'] * self.delta_time
            self.S0  = (self.SR0 + self.SL0) / 2.0
            angle    = (self.SR0 + self.SL0) / self.whell_axi_size + self.O[self.step_count-1]
            self.O.append(angle)
            X = self.S0 * math.cos(angle) + self.X[self.step_count-1]
            self.X.append(X)
            Y = self.S0 * math.sin(angle) + self.Y[self.step_count-1]
            self.Y.append(Y)
            self.step_count = self.step_count + 1
            self.simulation_time = self.simulation_time + self.delta_time
            output = {}
            output['X'] = X
            output['Y'] = Y
            output['O'] = angle 
            self.crsServer.PyRoboticStudio.output(output)
        
if __name__ == '__main__':
    # Tester 
    try:    
        cService = CRSDSS(49601) 
    except:
        print 'CRSDSS - XML-RPC creation fail!'
    else:  
        cService.start()
        for loop in range(10):
            cService.step()
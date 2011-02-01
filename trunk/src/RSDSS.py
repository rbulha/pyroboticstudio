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
    def __init__(self,local_port,remote_port=49580):
        '''
        Constructor
        '''
        if local_port >= 49601 and local_port <= 49700:
            try:
                CRSService.__init__(self,'DSS',local_port,remote_port) #local_port from 49601 to 49700
            except:
                print 'CRSDSS - XML-RPC server fail'
            else:
                print 'CRSDSS - running'
        else:
            print 'CRSDSS - running out of ports'
        '''
        Properties
        '''
        self.data = {}
        
        self.data['X0']  = 0
        self.data['Y0']  = 0
        self.data['O0']  = 0
        self.data['VR0'] = 0
        self.data['VL0'] = 0
        self.data['SR0'] = 0
        self.data['SL0'] = 0
        self.data['S0']  = 0
        
        self.data['X'] = []
        self.data['Y'] = []
        self.data['O'] = []
        
        #load initial condition
        self.data['step_count'] = 1 #first step keep the initial values
        self.data['X'].append(self.data['X0'])
        self.data['Y'].append(self.data['Y0'])
        self.data['O'].append(self.data['O0'])
        
        self.data['wheel_radius']    = 0.03 #radios of the wheel in meters
        self.data['whell_axi_size']  = 0.20 #distance between whells in meters
        self.data['delta_time']      = 0.01 #delta time in sec.
        self.data['simulation_time'] = 0 #total simulated time in sec.
 
    def step(self):
        #data request
        self.data['input'] = self.crsClient.PyRoboticStudio.input(self.local_port,'DSS')
        if input and self.data['input'].has_key('VR') and self.data['input'].has_key('VL'): 
            self.data['SR0'] = self.data['input']['VR'] * self.self.data['delta_time']
            self.data['SL0'] = self.data['input']['VL'] * self.self.data['delta_time']
            self.data['S0']  = (self.data['SR0'] + self.data['SL0']) / 2.0
            angle    = (self.data['SR0'] + self.data['SL0']) / self.whell_axi_size + self.data['O'][self.data['step_count']-1]
            self.data['O'].append(angle)
            X = self.data['S0'] * math.cos(angle) + self.X[self.data['step_count']-1]
            self.X.append(X)
            Y = self.data['S0'] * math.sin(angle) + self.Y[self.data['step_count']-1]
            self.Y.append(Y)
            self.data['step_count'] = self.data['step_count'] + 1
            self.data['simulation_time'] = self.data['simulation_time'] + self.data['delta_time']
            output = {}
            output['X'] = X
            output['Y'] = Y
            output['O'] = angle 
            print 'output: ',output
            self.crsClient.PyRoboticStudio.output(self.local_port,'DSS',output)
        
if __name__ == '__main__':
    # Tester 
    try:    
        cService = CRSDSS(49601,49582) 
    except:
        print 'CRSDSS - XML-RPC creation fail!'
    else:  
        cService.start()
        for loop in range(10):
            cService.step()
            
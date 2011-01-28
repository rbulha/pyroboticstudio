'''
Created on 25/01/2011

@author: rogerio_bulha
'''

from RSClientServer import CRSServer
from RSClientServer import CRSClient

class CRSEngine(CRSServer):
    '''
    classdocs
    '''
    def __init__(self,local_port=49580):
        '''
        Constructor
        '''
        try:
            CRSServer.__init__(self,'localhost',self.local_port) 
        except:
            print 'CRSEngine fail creating the XML-RPC server'
        else:
            print 'CRSEngine server listening!!'
            self.register_function(self.WC_input, "PyRoboticStudio.input")
            self.register_function(self.WC_output, "PyRoboticStudio.output")
        '''
        Properties
        '''
        self.delta_time = 0.1 #delta time in sec.
        self.total_simulation_time = 120.0 #total time of the simulation in sec.
        self.local_port = local_port
        
    def WC_hello(self,param,port,sender='None'):
        print '[CRSEngine.WC_hello]: %s:%d:%s'%(param,port,sender) 
        host = 'http://localhost:%d' % port
        print host
        if sender.upper() == 'ENV':
            if not self.Clients.has_key('ENV'):
                self.Clients[sender] = CRSClient(host,'SERVER','1_0_0_0')
                return 1
            else:
                print '[CRSEngine.WC_hello]: Only one environment is permitted'
                return 0
        elif sender.upper() == 'ROBOT':
            robot_key = 'ROBOT-%05d'%port
            if not self.Clients.has_key(robot_key):
                self.Clients[robot_key] = CRSClient(host,robot_key,'1_0_0_0')
                return 1
            else:
                print '[CRSEngine.WC_hello]: This Robot is already registered'
                return 0            
    def WC_input(self,port,sender):
        print '[CRSEngine.WC_input]: ',sender
        return None
    def WC_output(self,port,sender,data):
        print '[CRSEngine.WC_output]: ',sender
        return 0                    

if __name__ == '__main__':
    # Tester 
    try:    
        cEngine = CRSEngine(49580) 
    except:
        print 'cEngine - XML-RPC Server creation fail!'
    else:    
        try:        
            cEngine.start()
            add, port = cEngine.GetServerInfo()
            print "cEngine - XML-RPC server running: %s::%d"%(add, port)
        except:
            print 'cEngine - XML-RPC Server register fail!'
        else:
            cEngine.join() #wait until running             

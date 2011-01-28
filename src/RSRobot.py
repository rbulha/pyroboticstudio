'''
Created on 26/01/2011

@author: rogerio_bulha
'''

from RSService import CRSService
from RSClientServer import CRSClient

class CRSRobot(CRSService):
    '''
    CRSRobot
    '''
    def __init__(self,local_port,remote_port=49580,ini_file='none.ini'):
        '''
        Constructor
        '''
        if local_port >= 49582 and local_port <= 49600:
            try:
                CRSService.__init__(self,'ROBOT',local_port,remote_port) #local_port from 49582 to 49600
            except:
                print 'CRSRobot - XML-RPC server fail'
            else:
                print 'CRSRobot - running'
        else:
            print 'CRSRobot - running out of ports'
    def WC_hello(self,param,port,sender='None'):
        host = 'http://localhost:%d' % port
        if sender.upper() == 'DSS':
            if not self.Clients.has_key('DSS'):
                self.Clients[sender.upper()] = CRSClient(host,'ROBOT','1_0_0_0')
                return 1
            else:
                print '[CRSRobot.WC_hello]: Only one DSS is permitted'
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
        cService = CRSRobot(49582,49580) 
    except:
        print 'CRSRobot - XML-RPC creation fail!'
    else:  
        cService.start()  
            
        
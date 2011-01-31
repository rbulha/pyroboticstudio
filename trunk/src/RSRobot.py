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
                print '[CRSRobot.__init__] - XML-RPC server fail'
            else:
                print '[CRSRobot.__init__] - running'
        else:
            print '[CRSRobot.__init__] - running out of ports'
        self.data = {}
        self.data['local'] = {}
        self.data['local']['VR'] = 0.2
        self.data['local']['VL'] = 0.42
            
    def WC_hello(self,param,port,sender='None'):
        host = 'http://localhost:%d' % port
        if sender.upper() == 'DSS':
            if not self.Clients.has_key('DSS'):
                self.Clients[sender.upper()] = CRSClient(host,'ROBOT','1_0_0_0')
                print '[CRSRobot.WC_hello]: Hello %s port=%d'%(sender,port)
                return 1
            else:
                print '[CRSRobot.WC_hello]: Only one DSS is permitted'
                return 0        
    def WC_input(self,port,sender):
        print '[CRSRobot.WC_input]: %s::%d'%(sender,port)
        if sender.upper() == 'DSS':
            return self.data['local']
        else:
            return None
    def WC_output(self,port,sender,data):
        #print '[CRSRobot.WC_output]: ',sender
        if sender.upper() == 'DSS':
            self.data['local']['X']=data['X']
            self.data['local']['Y']=data['Y']
            self.data['local']['O']=data['O']
            return 1
        return 0                    
           
if __name__ == '__main__':
    # Tester 
    try:    
        cService = CRSRobot(49582,49580) 
    except:
        print '[TESTER] CRSRobot - XML-RPC creation fail!'
    else:  
        cService.start()
        cService.join()  
            
        
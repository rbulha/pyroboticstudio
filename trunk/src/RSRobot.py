'''
Created on 26/01/2011

@author: rogerio_bulha
'''

from RSService import CRSService

class CRSRobot(CRSService):
    '''
    CRSRobot
    '''
    def __init__(self,local_port,ini_file='none.ini'):
        '''
        Constructor
        '''
        if local_port >= 49582 and local_port <= 49600:
            try:
                CRSService.__init__(self,'ROBOT',local_port,49580) #local_port from 49582 to 49600
            except:
                print 'CRSRobot - XML-RPC server fail'
            else:
                print 'CRSRobot - running'
        else:
            print 'CRSRobot - running out of ports'
            
if __name__ == '__main__':
    # Tester 
    try:    
        cService = CRSRobot(49582) 
    except:
        print 'CRSRobot - XML-RPC creation fail!'
    else:  
        cService.start()  
            
        
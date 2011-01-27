'''
Created on 25/01/2011

@author: rogerio_bulha
'''

from RSService import CRSService
from img2raw import CIMGSUPPORT

class CEnvironment(CRSService):
    '''
    classdocs
    '''
    def __init__(self,ini_file='none.ini'):
        '''
        Constructor
        '''
        
        self.terrain = None
        
        try:
            CRSService.__init__(self,'ENV',49581,49580)
        except:
            print 'CEnvironment - XML-RPC server fail'
        else:
            print 'CEnvironment - running'
    def LoadTerrain(self,file_name):        
        self.terrain = CIMGSUPPORT.BMP2RAW(file_name)
    def IsReady(self):
        if not self.terrain:
            return False
        else:
            return True    
if __name__ == '__main__':
    # Tester 
    try:    
        cEnv = CEnvironment() 
    except:
        print 'XML-RPC Environment creation fail!'
    else:  
        cEnv.start()  

            
              
            
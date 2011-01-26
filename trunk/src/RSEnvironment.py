'''
Created on 25/01/2011

@author: rogerio_bulha
'''

from RSService import CRSService

class CEnvironment(CRSService):
    '''
    classdocs
    '''
    def __init__(self,ini_file='none.ini'):
        '''
        Constructor
        '''
        try:
            CRSService.__init__(self,'ENV',49581,49580)
        except:
            print 'CEnvironment - XML-RPC server fail'
        else:
            print 'CEnvironment - running'

            
if __name__ == '__main__':
    # Tester 
    try:    
        cEnv = CEnvironment() 
    except:
        print 'XML-RPC Environment creation fail!'
    else:  
        cEnv.start()  

            
              
            
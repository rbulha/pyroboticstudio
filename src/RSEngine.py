'''
Created on 25/01/2011

@author: rogerio_bulha
'''

from RSClientServer import CRSServer

class CRSEngine(CRSServer):
    '''
    classdocs
    '''
    def __init__(self,local_port=49580):
        '''
        Constructor
        '''
        self.local_port = local_port
        try:
            CRSServer.__init__(self,'localhost',self.local_port) 
        except:
            print 'CRSEngine fail creating the XML-RPC server'
        else:
            print 'CRSEngine server listening!!'
                    
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

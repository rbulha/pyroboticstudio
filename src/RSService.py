'''
Created on 25/01/2011

@author: rogerio_bulha
'''

from RSClientServer import CRSClient
from RSClientServer import CRSServer

class CRSService(CRSServer):
    '''
    classdocs
    '''
    def __init__(self,service_name,local_port,remote_port):
        '''
        Constructor
        '''
        self.service_name = service_name
        self.local_port = local_port
        try:
            CRSServer.__init__(self,'localhost',local_port)
        except:
            print '[CRSService.__init__] %s fail creating the XML-RPC server port=%d'%(service_name,local_port)
            raise
        else:
            print '[CRSService.__init__]%s server listening port %d!!'%(service_name,local_port)
            self.register_function(self.WC_input, "PyRoboticStudio.input")
            self.register_function(self.WC_output, "PyRoboticStudio.output")
            self.register_function(self.WC_step, "PyRoboticStudio.step")
        try:
            self.remote_port = remote_port
            host = 'http://localhost:%d' % self.remote_port
            self.crsClient = CRSClient(host, service_name, '1_0_0_0')
        except:
            print '[CRSService.__init__] %s fail connecting to the server'%service_name
            raise
        else:
            print '[CRSService.__init__] %s connected!!'%service_name
            try:        
                if not self.crsClient.Hello(self.local_port):
                    print '[CRSService.__init__] %s - Hello not accepted.'%service_name
            except:
                print '[CRSService.__init__] XML-RPC hello fail!'
                raise
            else:
                print '[CRSService.__init__] %s - Initialization DONE.'%service_name
                        
    def WC_input(self,port,sender):
        print 'WC_input: ',sender
        return None
    def WC_output(self,port,sender,data):
        print 'WC_output: ',sender
        return 0
    def WC_step(self):
        print 'WC_step: '
        return 0
    
                    
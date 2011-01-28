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
        try:
            CRSServer.__init__('localhost',local_port)
            self.service_name = service_name
            self.local_port = local_port
        except:
            print '%s fail creating the XML-RPC server'%service_name
        else:
            print '%s server listening!!'%service_name
            self.register_function(self.WC_input, "PyRoboticStudio.input")
            self.register_function(self.WC_output, "PyRoboticStudio.output")
        try:
            self.remote_port = remote_port
            host = 'http://localhost:%d' % self.remote_port
            self.crsClient = CRSClient(host, service_name, '1_0_0_0')
        except:
            print '%s fail connecting to the server'%service_name
        else:
            print '%s connected!!'%service_name

        try:        
            if not self.crsClient.Hello(self.local_port):
                print '%s - Hello not accepted.'%service_name
        except:
            print 'XML-RPC hello fail!'
        else:
            print '%s - Initialization DONE.'%service_name
                    
    def WC_input(self,port,sender):
        print 'WC_input: ',sender
        return None
    def WC_output(self,port,sender,data):
        print 'WC_output: ',sender
        return 0
                    
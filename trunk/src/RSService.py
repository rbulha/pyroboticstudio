'''
Created on 25/01/2011

@author: rogerio_bulha
'''

from RSClientServer import CRSClient
from RSClientServer import CRSServer

class CRSService(object):
    '''
    classdocs
    '''
    def __init__(self,service_name,local_port,remote_port):
        '''
        Constructor
        '''
        self.service_name = service_name
        try:
            self.server_port = local_port
            self.crsServer = CRSServer('localhost',self.server_port) 
            self.crsServer.start()
        except:
            print '%s fail creating the XML-RPC server'%service_name
        else:
            print '%s server listening!!'%service_name
                    
        try:
            self.engine_server_port = remote_port
            host = 'http://localhost:%d' % self.engine_server_port
            self.crsClient = CRSClient(host, service_name, '1_0_0_0')
        except:
            print '%s fail connecting to the server'%service_name
        else:
            print '%s connected!!'%service_name

        try:        
            if not self.crsClient.Hello(self.server_port):
                print '%s - Hello not accepted.'%service_name
        except:
            print 'XML-RPC hello fail!'
        else:
            print '%s - Initialization DONE.'%service_name
    
    def start(self):
        '''
        Initiate service loop
        '''
        self.crsServer.join()
                    
'''
Created on 25/01/2011

@author: rogerio_bulha
'''
from xmlrpclib import ServerProxy, Error
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
from threading import Thread

class MyHandler(SimpleXMLRPCRequestHandler): 
    def do_POST(self):
        data = self.rfile.read(int(self.headers["content-length"]))
        response = self.server._marshaled_dispatch(
                data, getattr(self, '_dispatch', None) )
        self.send_response(200)
        self.send_header("Content-type", "text/xml")
        self.send_header("Content-length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)
        self.wfile.flush()

class CXMLRPCServer(Thread,SimpleXMLRPCServer):      
    def __init__(self, indentificador, host, port):
        '''Using fix port defined for the System302 = 12436'''
        Thread.__init__(self)
        SimpleXMLRPCServer.__init__(self,(host, port),MyHandler,logRequests=1)
        self.register_function(self.Ping, "PyRoboticStudio.ping")
        self.register_introspection_functions()    
        self.id = indentificador
        self.isRunning = True
        self.setDaemon(True)
    def GetServerInfo(self):  
        return self.socket.getsockname()
    def Ping(self):
        print 'CXMLRPCServer.ping'
        return 1    
    def ServerClose(self):
        print 'CXMLRPCServer.ServerClose'
        self.isRunning = False
    def handle_error(self, request, client_address):
        print 'CXMLRPCServer.handle_error from:', client_address
        print 'CXMLRPCServer.handle_error request: ', request
        return 1
    def handle_request(self):
        print 'CXMLRPCServer.handle_request'
        if self.isRunning:
            try:
                return SimpleXMLRPCServer.handle_request(self)
            except Error, v:
                print "[CXMLRPCServer.handle_request] Exception: %v, %v" % (Error, v)
                return 0    
        else:
            return 0    
    def verify_request(self, request, client_address):
        return SimpleXMLRPCServer.verify_request(self, request, client_address)
    def process_request(self, request, client_address):
        return SimpleXMLRPCServer.process_request(self, request, client_address)
    def server_close(self):
        print 'CXMLRPCServer.server_close'
        return SimpleXMLRPCServer.server_close(self)
    def finish_request(self, request, client_address):
        return SimpleXMLRPCServer.finish_request(self, request, client_address)
    def serve_forever(self):
        while self.isRunning: 
            self.handle_request()
        return 1    
    def run(self):
        self.serve_forever()
        return 1

class CRSClient(ServerProxy):
    def __init__(self, host, client_name, version='1_0_0_0'):
        self.version = version
        self.client_name = client_name
        if self.version == '1_0_0_0':
            try:
                ServerProxy.__init__(self,host,allow_none=True)
            except Error, v:
                print "CONNECTION ERROR", v        
        else:
            print 'Unsupported workspace' 
    def Ping(self):
        PingCW = 0
        try:
            PingCW = self.PyRoboticStudio.ping(self.client_name)
            print '\n Ping workspace: ', PingCW
        except Error, v:
            print "ERROR", v
        return PingCW  
    def Hello(self, port):
        try:
            print 'CRSClient - client_name=',self.client_name
            sStatus = self.PyRoboticStudio.hello(self.client_name,port,self.client_name)
            print '\n Hello: ',sStatus
            return sStatus
        except Error, v:
            print "ERROR", v
            return 0
    def Bye(self):
        try:
            print '\n Bye: ',self.PyRoboticStudio.bye(self.client_name,port,self.client_name)
        except Error, v:
            print "ERROR", v  
      
      
class CRSServer(CXMLRPCServer):
    '''
    XML RPC server register and manager all connections for the simulation engine.
    '''
    def __init__(self,host,port,ini_filename='none.txt'):
        '''
        Constructor
        '''
        CXMLRPCServer.__init__(self,0x001154,host,port)
        self.register_function(self.WC_close, "PyRoboticStudio.close")
        self.register_function(self.WC_hello, "PyRoboticStudio.hello")
        
        self.Clients = {}
        
    def WC_close(self,sender):
        print 'WC - Close: ',sender
        return 1
    def WC_hello(self,param,port,sender='None'):
        print 'WC - Hello: %s:%d:%s'%(param,port,sender) 
        host = 'http://localhost:%d' % port
        print host
        if sender.upper() == 'ENV':
            if not self.Clients.has_key('ENV'):
                self.Clients[sender] = CRSClient(host,'SERVER','1_0_0_0')
                return 1
            else:
                print 'Only one environment is permitted'
                return 0            
         
if __name__ == '__main__':
    # Tester 
    try:    
        cServerTester = CRSServer('localhost',49580) 
    except:
        print 'XML-RPC Server creation fail!'
    else:    
        try:        
            cServerTester.start()
            add, port = cServerTester.GetServerInfo()
            print "XML-RPC server running: %s::%d"%(add, port)
        except:
            print 'XML-RPC Server register fail!'
        else:
            cServerTester.join() #wait until running             
        
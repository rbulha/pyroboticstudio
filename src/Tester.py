'''
Created on 01/02/2011

@author: rogerio_bulha
'''
import unittest

from RSRobot    import CRSRobot
from RSEngine   import CRSEngine
from RSDSS      import CRSDSS

class Test_engine(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_robot(self):
        self.c_engine = CRSEngine(49580) 
        self.c_engine.start()
        host,port = self.c_engine.GetServerInfo()
        self.assertEqual(port, 49580, 'falha no server')
        self.assertEqual(host, '127.0.0.1', 'falha no server')

class Test_robot(unittest.TestCase):
    def setUp(self):
        self.c_engine = CRSEngine(49580) 
        self.c_engine.start()
    def tearDown(self):
        pass
    def test_robot(self):
        self.c_robot = CRSRobot(49582,49580)
        self.c_robot.start()
        host,port = self.c_robot.GetServerInfo()
        self.assertEqual(port, 49582, 'falha no server')
        self.assertEqual(host, '127.0.0.1', 'falha no server')

class Test_dss(unittest.TestCase):
    def setUp(self):
        self.c_engine = CRSEngine(49580) 
        self.c_engine.start()
        self.c_robot = CRSRobot(49582,49580)
        self.c_robot.start()
    def tearDown(self):
        pass
    def test_dss(self):
        self.c_dss = CRSDSS(49601,49582)    
        self.c_dss.start()
        host,port = self.c_dss.GetServerInfo()
        self.assertEqual(port, 49601, 'falha no server')
        self.assertEqual(host, '127.0.0.1', 'falha no server')

class Test_complete_session(unittest.TestCase):
    def setUp(self):
        self.c_engine = CRSEngine(49580) 
        self.c_engine.start()
    def tearDown(self):
        pass
    def test_complete(self):
        self.c_engine.RegisterService(CRSRobot, 49582, 49580)
        self.c_engine.RegisterService(CRSDSS, 49601, 49582)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_complete_session)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
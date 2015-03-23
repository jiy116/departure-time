import unittest
import xml.etree.ElementTree as ET
import json
import views

class TestFunctions(unittest.TestCase):
    
    def setUp(self):
        self.stopview = views.StopView()

    def testgetStops(self):
        reslist = []
        explist = ["15673","17757","15672","14954","15772"]
        stops = self.stopview.getStops(-122.42199, 37.7728799)
        for stop in stops:
            reslist.append(stop['stopid'])
        self.assertEqual(reslist,explist, 'Stops near by not match')

    def testgetResponse(self):
        pass
        
    def testgetRoutePreList(self):
        xml = ET.parse('test/data.xml')
        routeprelist = self.stopview.getRoutePreList(xml)
        self.assertEqual(len(routeprelist),3,'Number of routes not match')

        route_1 = {'routetag':'36','dirlist': \
        [{'timelist':[1222,2816,4496],'title':\
        'Outbound to The Mission District'}], \
        'hasdata':True}

        route_2 = {'routetag':'14','dirlist': \
        [{'timelist':[1447,1939,1939,2599,3259],'title':\
        'Inbound to Downtown'}],\
        'hasdata':True}

        route_3 = {'routetag':'49','dirlist':\
        [{'timelist':[311,875,1492,2152,2812],\
        'title':'Inbound to Fort Mason'}],\
        'hasdata':True}

        self.assertEqual(json.dumps(route_1), routeprelist[0].to_json(), \
            'parsed data not match')
        self.assertEqual(json.dumps(route_2), routeprelist[1].to_json(), \
            'parsed data not match')
        self.assertEqual(json.dumps(route_3), routeprelist[2].to_json(), \
            'parsed data not match')

    def testgetDirectionList(self):
        xml = ET.parse('test/predictions.xml')
        route = self.stopview.getDirectionList(xml)
        direction_1 = {'timelist':[889,2089,3349,4536], \
                       'title':'Outbound to the Richmond District'}
        direction_2 = {'timelist':[233,2159,2530,4098,5298], \
                       'title':'Inbound to Baker Beach'}
        self.assertEqual(len(route),2,'direction number not match')
        self.assertEqual(route[0].to_json(),json.dumps(direction_1), \
                        'direction date not match')
        self.assertEqual(route[1].to_json(),json.dumps(direction_2), \
                'direction date not match')

    def testgetTimeList(self):
        xml = ET.parse('test/direction.xml')
        timelist = self.stopview.getTimeList(xml)
        expected = [360,1602,2661,3861,5061]
        self.assertEqual(timelist,expected,'time list not match')

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFunctions)
    unittest.TextTestRunner(verbosity=2).run(suite)

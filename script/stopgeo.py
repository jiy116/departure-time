import urllib2
import logging
import xml.etree.ElementTree as ET

from mongoengine import *

BASE_URL = 'http://webservices.nextbus.com/service/publicXMLFeed?'
AGENT_URL = 'command=routeList&a=sf-muni'
STOP_URL = 'command=routeConfig&a=sf-muni&r='

connect('mydatabase')

class Stopgeo(Document):
    tag = StringField(max_length=255, required=True)
    stopid = StringField(max_length=255, required=True)
    title = StringField(required=True)
    location = PointField(required=True)

    mata = {'indexes':[('location','2dsphere')]}

def getRouteList():
    try:
        response = urllib2.urlopen(BASE_URL+AGENT_URL)
        response_xml = ET.fromstring(response.read())
        routeList = []
        for route in response_xml:
            route_info = route.attrib
            routeList.append(route_info['tag'])
        return routeList
    except Exception, e:
        logging.exception(e)
        return []

def addToDB(stopList):
    try:
        for stop in stopList:
            lon = float(stop['lon'])
            lat = float(stop['lat'])
            stopgeo = Stopgeo(tag=stop['tag'],       \
                              stopid=stop['stopId'], \
                              title=stop['title'],   \
                              location=[lon, lat])
            stopgeo.save()

    except Exception, e:
        logging.exception(e)
        Stopgeo.drop_collection()

def getStopList(routeList):
    try:
        stopList = []
        stopSet = set()
        for route in routeList:
            response = urllib2.urlopen(BASE_URL+STOP_URL+route)
            response_xml = ET.fromstring(response.read())

            route = response_xml[0]
            for stop in route.findall('stop'):
                if stop.attrib['tag'] not in stopSet:
                    stopList.append(stop.attrib)
                    stopSet.add(stop.attrib['tag'])
        return stopList
    except Exception, e:
        logging.exception(e)
        return []

def main():
    routeList = getRouteList()
    stopList = getStopList(routeList)
    addToDB(stopList)    

if __name__ == '__main__':
    main()
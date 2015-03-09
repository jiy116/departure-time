import urllib2
import logging
import xml.etree.ElementTree as ET
from pymongo import Connection

BASE_URL = 'http://webservices.nextbus.com/service/publicXMLFeed?'
AGENT_URL = 'command=routeList&a=sf-muni'
STOP_URL = 'command=routeConfig&a=sf-muni&r='


def getRouteList():
    try:
        response = urllib2.urlopen(BASE_URL+AGENT_URL)
        response_xml = ET.fromstring(response.read())
        routeList = []
        for route in response_xml:
            route_info = route.attrib
            routeList.append(route_info['tag'])

    except Exception, e:
        logging.exception(e)

    return routeList

def getStopList(routeList):
    try:
        stopList = []
        stopSet = set()
        for route in routeList:
            response = urllib2.urlopen(BASE_URL+STOP_URL+route)
            response_xml = ET.fromstring(response.read())

            route = response_xml[0]
            for stop in route.findall('stop'):
                if not stop.attrib['tag'] in stopSet:
                    stopList.append(stop.attrib)
                    stopSet.add(stop.attrib['tag'])

    except Exception, e:
        logging.exception(e)

    return stopList

def creatDB():
    try:
        con = Connection()
        db = con.mydatabase

        stop_collection = db.stop_collection
        stop_collection.remove()
        return stop_collection

    except Exception, e:
        logging.exception(e)


def addToDB(stop_collection,stopList):
    try:
        for stop in stopList:
            newstop = stopType(stop)
            stop_collection.insert(newstop)
	
	stop_collection.create_index([('loc', '2dsphere')])

    except Exception, e:
        logging.exception(e)

def stopType(stop):
    try:
        lat = float(stop['lat'])
        lon = float(stop['lon'])
        newstop = {'tag':stop['tag'],'title':stop['title'], \
                   'stopId':stop['stopId'],\
                   'loc':{'type': 'Point', 'coordinates':[lon, lat]}}

    except Exception, e:
        logging.exception(e)
    
    return newstop


def main():
    stop_collection = creatDB()
    routeList = getRouteList()
    stopList = getStopList(routeList)
    addToDB(stop_collection,stopList)


if __name__ == '__main__':
    main()


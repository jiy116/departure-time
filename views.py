import urllib2
import logging
import xml.etree.ElementTree as ET
from flask import Blueprint, request, redirect, render_template, url_for, jsonify
from flask.views import MethodView
from models import Stop, Stopgeo, Routepredictions, Direction

BASE_URL = 'http://webservices.nextbus.com/service/publicXMLFeed?'
PD_URL = 'command=predictions&a=sf-muni&stopId='
STOP_NUM = 5

nextbus = Blueprint('nextbus', __name__)

class StopView(MethodView):
    def get(self):
        lon = request.args.get('lon')
        lat = request.args.get('lat')
        stoplist = getStops(lon,lat)
        response = getResponse(stopList)
        return jsonify(**response)

    def getStops(self,lon, lat):
        stopList = Stopgeo.objects(location__near=[lon, lat])[:STOP_NUM]
        return stopList

    def getResponse(self,stopList):
        response = {}
        for stop in stopList:
            stopid = stop['stopid']
            stoptitle = stop['title']
            stop_routes_info = Stop.objects(stopid=stopid).to_json()
            if len(stop_routes_info) == 0:
                stop_routes_info = getStopInfo(stopid, stoptitle)
            response[stopid]=stop_routes_info

        return response

    def getStopInfo(self,stopid, stoptitle):
        try:
            response = urllib2.urlopen(BASE_URL+PD_URL+stopid)
            response_xml = ET.fromstring(response.read())
            routeprelist = getRoutePreList(response_xml)
            stop = Stop(stopid=stopid, 
                        title=stoptitle,
                        routeprelist=routeprelist)
            stop.save()
            #print stop.to_json()
            return stop.to_json()

        except Exception, e:
            logging.exception(e)

    def getRoutePreList(self,response_xml):
        routeprelist = []
        for predictions_xml in response_xml.findall('predictions'):
            dirlist = getDirectionList(predictions_xml)
            hasdata = False if len(dirlist)==0 else True
            predictions = Routepredictions(
                routetag = predictions_xml.get('routeTag'),
                hasdata = hasdata,
                dirlist = dirlist)
            routeprelist.append(predictions)
        return routeprelist

    def getDirectionList(self,predictions_xml):
        directionList = []
        for direction_xml in predictions_xml.findall('direction'):

            timelist = getTimeList(direction_xml)
            direction = Direction(title=direction_xml.get('title'),
                                timelist=timelist)
            directionList.append(direction)
        return directionList

    def getTimeList(self,direction_xml):
        timelist = []
        for prediction in direction_xml.iter('prediction'):
            timelist.append(int(prediction.attrib['seconds']))
        return timelist







findbus.add_url_rule('/findbus/',view_func=StopView.as)
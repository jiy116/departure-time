import urllib2
import logging
import json
import xml.etree.ElementTree as ET
from flask import Response, Blueprint, request, \
                redirect, render_template, url_for, jsonify
from flask.views import MethodView
from models import Stop, Stopgeo, Routepredictions, Direction

BASE_URL = 'http://webservices.nextbus.com/service/publicXMLFeed?'
PD_URL = 'command=predictions&a=sf-muni&stopId='
STOP_NUM = 5

nextbus = Blueprint('nextbus', __name__, template_folder='templates')

class HomeView(MethodView):
    def get(self):
        return render_template('index.html')

class StopView(MethodView):
    def get(self):
        try:
            lon = float(request.args.get('lon', ''))
            lat = float(request.args.get('lat', ''))
            stoplist = self.getStops(lon,lat)
            response = self.getResponse(stoplist)
            return Response(json.dumps(response),  mimetype='application/json')
        except Exception, e:
            logging.exception(e)
            return Response('Request data unavailable')

    def getStops(self, lon, lat):
        stoplist = Stopgeo.objects(location__near=[lon, lat])[:STOP_NUM]
        return stoplist

    def getResponse(self,stoplist):
        response = []
        for stop in stoplist:
            stopid = stop['stopid']
            stoptitle = stop['title']
            stop_routes_info = Stop.objects(stopid=stopid)
            if not stop_routes_info:
                stop_routes_info = self.getStopInfo(stopid, stoptitle)
            else:
                stop_routes_info = stop_routes_info[0].to_json()
            response.append(json.loads(stop_routes_info))

        return response

    def getStopInfo(self,stopid, stoptitle):
        try:
            response = urllib2.urlopen(BASE_URL+PD_URL+stopid)
            response_xml = ET.fromstring(response.read())
            routeprelist = self.getRoutePreList(response_xml)
            stop = Stop(stopid=stopid,
                        title=stoptitle,
                        routeprelist=routeprelist)
            stop.save()
            return stop.to_json()

        except Exception, e:
            logging.exception(e)

    def getRoutePreList(self,response_xml):
        routeprelist = []
        for predictions_xml in response_xml.findall('predictions'):
            dirlist = self.getDirectionList(predictions_xml)
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

            timelist = self.getTimeList(direction_xml)
            direction = Direction(title=direction_xml.get('title'),
                                timelist=timelist)
            directionList.append(direction)
        return directionList

    def getTimeList(self,direction_xml):
        timelist = []
        for prediction in direction_xml.iter('prediction'):
            timelist.append(int(prediction.attrib['seconds']))
        return timelist

nextbus.add_url_rule('/',view_func=HomeView.as_view('home'))
nextbus.add_url_rule('/stop.js',view_func=StopView.as_view('stop'))

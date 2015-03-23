from flask import url_for
from app import db
from datetime import datetime 

cache_time = 120   #seconds

class Stop(db.Document):
    created = db.DateTimeField(default=datetime.now)
    title = db.StringField(max_length=255, required=True)
    stopid = db.StringField(max_length=255, required=True, unique=True)
    routeprelist = db.ListField(db.EmbeddedDocumentField('Routepredictions'))

    meta = {'indexes':[
            'stopid',
            {
                'fields':['created'],
                'expireAfterSeconds': cache_time
            }
        ]
    }

#prediction information for one route
class Routepredictions(db.EmbeddedDocument):
    routetag = db.StringField(max_length=255, required=True)
    dirlist = db.ListField(db.EmbeddedDocumentField('Direction'))
    hasdata = db.BooleanField(required=True)
    
#prediction information for one direction of one route
class Direction(db.EmbeddedDocument):
    title = db.StringField(max_length=255, required=True)
    timelist = db.ListField(db.IntField())

#stop's geo information
class Stopgeo(db.Document):
    tag = db.StringField(max_length=255, required=True)
    stopid = db.StringField(max_length=255, required=True,unique=True)
    title = db.StringField(required=True)
    location = db.PointField(required=True)

    mata = {'indexes':[('location','2dsphere')]}
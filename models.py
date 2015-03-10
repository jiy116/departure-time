from flask import url_for
from app import db

class Stop(db.Document):
    title = db.StringField(max_length=255, required=True)
    timestamp = db.IntField(required = True)
    stopid = db.StringField(max_length=255, required=True)
    routepre = db.ListField(db.EmbeddedDocumentField('Routepre'))

    meta = {'indexes':['stopid']}

class Routepre(db.EmbeddedDocument):
    routetag = db.StringField(max_length=255, required=True)
    hasdata = db.BooleanField(required=True)
    pretime = db.ListField(db.IntField())

class Stopgeo(db.Document):
    tag = db.StringField(max_length=255, required=True)
    stopid = db.StringField(max_length=255, required=True)
    title = db.StringField(required=True)
    location = db.PointField(required=True)

    mata = {'indexes':[('location','2dsphere')]}

from base import db
from mongoengine import *

class Target(db.Document):
    target_id = db.StringField()
    primary_description = db.StringField()
    primary_type = db.StringField()
    alt_type = db.StringField()
    alt_description = db.StringField()

class TargetSet(db.Document):
    name = db.StringField()
    targets = db.ListField(db.ReferenceField(Target))

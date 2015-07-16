from base import db

class Experiment(db.Document):
    exp_uid = db.StringField()
    exp_key = db.StringField()
    perm_key = db.StringField()
    app_id = db.StringField()
    name = db.StringField()
    description = db.StringField()
    instructions = db.StringField()
    debrief = db.StringField()
    params = db.DictField()
    status = db.StringField(default="staging")
    target_set = db.ReferenceField('TargetSet')
    query_tries = db.IntField()
    query_duration = db.IntField()
    info  = db.DictField()

    # Use set's on any parameters that can be changed outside of a constructor.
    def set_status(self,status):
        self.status = status
        self.save()

        
    def set_exp_uid(self,exp_uid):
        self.exp_uid = exp_uid
        self.save()


    def set_exp_key(self,exp_key):
        self.exp_key = exp_key
        self.save()

    def set_perm_key(self,perm_key):
        self.perm_key = perm_key
        self.save()

    def set_info(self,info):
        self.info = info
        self.save()
    

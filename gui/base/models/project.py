from base import db

class Project( db.Document):
    name = db.StringField(max_length=255)
    description = db.StringField(max_length=255)
    users = db.ListField(db.ReferenceField('User'))
    experiments = db.ListField(db.ReferenceField('Experiment'))
    target_sets = db.ListField(db.ReferenceField('TargetSet'))

    def add_user(self,user):
        self.users.append(user)
        self.save()

    def add_experiment(self,experiment):
        self.experiments.append(experiment)
        self.save()

    def add_target_set(self, target_set):
        self.target_sets.append(target_set)
        self.save()

from base import db
import experiment
from flask.ext.login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Document, UserMixin):
    email = db.StringField(max_length=255, required=True)
    password = db.StringField(max_length=255)
    projects = db.ListField(db.ReferenceField('Project'))
    access_key_id = db.StringField(required=True)
    secret_access_key = db.StringField(required=True)
    aws_bucket_name = db.StringField(required=True)
    next_backend_global_host = db.StringField(required=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return self.email

    def __repr__(self):
        return '<User %r>' % self.email

    def add_project(self,project):
        self.projects.append(project)
        self.save()



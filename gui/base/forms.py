from flask_wtf import Form
from wtforms import (TextField,
                     PasswordField,
                     TextAreaField,
                     RadioField,
                     FileField,
                     SelectField,
                     BooleanField,
                     HiddenField,
                     FormField,
                     FieldList,
                     IntegerField,
                     validators)
from bson.objectid import ObjectId

class SecretForm(Form):
    access_key_id = TextField('Access Key ID',
                              validators = [validators.required()])
    secret_access_key = TextField('Secret Access Key',
                                  validators = [validators.required()])
    # bucket_name = TextField('Bucket',
    #                         validators = [validators.required()])
    # next_backend_global_host = TextField('Next Backend Host',
    #                         validators = [validators.required()])


class CreateAccountForm(Form):
    new_email = TextField('Email', validators=[validators.required()])
    new_password = PasswordField('Password', validators=[validators.required()])
    confirm_password = PasswordField('Confirm Password', validators=[validators.required()])

class LoginForm(Form):
    email = TextField('Email', validators=[validators.required()])
    password = PasswordField('Password', validators=[validators.required()])

    
class NewExperimentForm(Form):
    name = TextField('Experiment Name', validators=[validators.required()])
    description = TextAreaField('Description', validators=[validators.required()], default='Sorry! No description')
    instructions = TextAreaField('Instructions', validators=[validators.required()], default='Sorry! No instructions')
    debrief = TextAreaField('Debrief', validators=[validators.required()], default='Sorry! No debrief')
    # The coerce line coerces the object_id from the select form to an actual ObjectId
    target_set = SelectField('Target Set',coerce=ObjectId)   
    query_tries = IntegerField('queries',validators=[validators.required()], default=100)
    query_duration = IntegerField('duration (min)',validators=[validators.required()], default=60)
    
class NewProjectForm(Form):
    name = TextField('Project Name', validators=[validators.required()])
    description = TextAreaField('Description', validators=[validators.required()])
    #users = TextAreaField(u'Add Users', validators=[validators.required()]) #need to write custom validator
    # need to set up permissions for users eventually, also, need to figure out how to auto select users and submit a list
  
class ManageTargets(Form):
    target_id = HiddenField('not_set', validators=[validators.required()])
    target_type = SelectField('Target Type', coerce=int)
    primary_description = TextAreaField('Primary Description', validators=[validators.required()])
    alt_description = TextAreaField('Alternative Description', validators=[validators.required()])

class TargetSetForm(Form):
    name= TextField(u'Target Set Name', validators=[validators.required()])

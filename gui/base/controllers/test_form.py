from flask import Blueprint, Response, render_template, flash, request, redirect, url_for, session,jsonify
import json
from flask.ext.login import login_user, logout_user, login_required, current_user
from base.current import *
from base import cache
from base.forms import LoginForm, NewProjectForm
from base.models import User, Project
from wtforms import *
from wtforms.fields import *
from wtforms.widgets import *
from flask_wtf import Form
test_form = Blueprint('test_form', __name__)

class CustomWidget()

class CustomField(Field):
        widget = TextInput()


class CustomForm(Form):
        name  = TextField('Name')
        value = TextField('Value')
        custom = CustomField('Custom')

@test_form.route('/', methods=["POST","GET"])
def _test_form():
        form = CustomForm(name='a',value='b')
        print form, request.method
        if request.method=="POST":
                print form.name.data
                print form.value.data
                print form.custom.data
                
	return render_template('test_form.html', form=form)

from flask import Blueprint, Response, render_template, flash, request, redirect, url_for, session,jsonify
import json
from flask.ext.login import login_user, logout_user, login_required, current_user
from base.current import *
from base import cache
from base.forms import LoginForm, NewProjectForm
from base.models import User, Project

new_project = Blueprint('new_project', __name__)

@new_project.route('/', methods=["POST","GET"])
@login_required
def _new_project():
	form = NewProjectForm()
	if form.validate_on_submit():
	    name = form.name.data
	    description = form.description.data
            print "project count", Project.objects(name = name).count()
            if Project.objects(name = name).count() ==0:
                    project = Project(name=name, description=description)
                    project.save()
                    project.add_user(current_user.to_dbref())
                    current_user.add_project(project)
                    return redirect(url_for("project._project", project_id = project.id))
            else:
                    flash("Project name already exists")
                    
	return render_template('new_project.html', form=form)

import json

from flask import (Blueprint,
                   Response,
                   render_template,
                   flash,
                   request,
                   redirect,
                   url_for,
                   session,
                   jsonify)
from flask.ext.login import (login_user,
                             logout_user,
                             login_required,
                             current_user)
import base
from base import cache
from base.forms import LoginForm, NewExperimentForm, NewProjectForm
from base.models import User
from base.current import *

config = base.config
dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
@login_required
def _dashboard():
        if (not config.AWS_BUCKET_NAME or
            not config.AWS_ID or
            not config.AWS_KEY or
            not config.NEXT_BACKEND_GLOBAL_HOST):   
                return redirect(url_for('setup._setup'))
        else:
                return render_template('dashboard.html')

@dashboard.route('/edit_project/<project_id>', methods=["GET","POST"])
@login_required
def edit_project(project_id):
	# need to set current project before editing it
	set_project(project_id = project_id)
	return redirect(url_for('project.edit', project_id=project_id))

@dashboard.route('/delete_project/<project_id>', methods=["GET","POST"])
@login_required
def delete_project(project_id):
	# need to set current project before deleting it
	set_project(project_id = project_id)
	return redirect(url_for('project.delete', project_id=project_id))

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
import base.settings

config = base.settings.Config()
dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
@login_required
def _dashboard():
        if (not current_user.aws_bucket_name or
            not current_user.access_key_id or
            not current_user.secret_access_key or
            not current_user.next_backend_global_host):   
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

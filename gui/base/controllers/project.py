from flask import Blueprint, Response, render_template, flash, request, redirect, url_for, session,jsonify, _app_ctx_stack
import json
from flask.ext.login import login_user, logout_user, login_required, current_user

from base import cache
from base.forms import LoginForm, NewExperimentForm, NewProjectForm
from base.models import User, Target, TargetSet, Project
from base.current import *

project = Blueprint('project', __name__)


@project.route('/<project_id>')
@login_required
def _project(project_id):
    set_project(project_id = project_id)
    return render_template('project.html')

@project.route('/edit_project/<project_id>', methods=["GET","POST"])
@login_required
@project_required
def edit(project_id):
    set_project(project_id = project_id)
    form = NewProjectForm(obj=current_project)
    if form.validate_on_submit():
        current_project.update(set__name=form.name.data)
        current_project.update(set__description=form.description.data)
        return redirect(url_for('project._project', project_id=current_project.id))
    return render_template('edit_project.html', form=form)

@project.route('/delete/<project_id>', methods=["GET","POST"])
@login_required
@project_required
def delete(project_id):
    current_user.update(pull__projects=project_id)
    Project.objects(id=project_id)[0].delete()
    set_project()
    return redirect(url_for('dashboard._dashboard'))

@project.route('/manage_users')
@login_required
@project_required
def manage(project_id, expID):
    return render_template('manage_users.html')  

@project.route('/delete_experiment/<experiment_id>',methods=["GET","POST"])
@login_required
@project_required
def delete_experiment(experiment_id):
    set_experiment(experiment_id=experiment_id)
    return redirect(url_for('experiment.delete', experiment_id=experiment_id))

@project.route('/edit_experiment/<experiment_id>',methods=["GET","POST"])
@login_required
@project_required
def edit_experiment(experiment_id):
    set_experiment(experiment_id=experiment_id)
    return redirect(url_for('experiment.edit', experiment_id=experiment_id))

@project.route('/clone_experiment/<experiment_id>',methods=["GET","POST"])
@login_required
@project_required
def clone_experiment(experiment_id):
    set_experiment(experiment_id=experiment_id)
    return redirect(url_for('experiment.clone', experiment_id=experiment_id))
    

from flask import Blueprint, render_template, flash, request, redirect, url_for, session
from flask.ext.login import login_user, logout_user, login_required
from wtforms import TextField, PasswordField, TextAreaField, RadioField, FieldList, IntegerField, FormField, StringField, validators
from wtforms.compat import with_metaclass, iteritems, itervalues
from flask_wtf import Form

from base import cache
from base.forms import LoginForm, NewExperimentForm
from base.models import User
from base.current import *
from base.app_manager import app_manager

new_experiment = Blueprint('new_experiment', __name__)

@new_experiment.route('/')
@login_required
@project_required
def _new_experiment():
    # check to see if targets have been uploaded
    if len(current_project.target_sets) == 0:
        return render_template('no_targets.html')
    else:
        # targets have been uploaded, show new experiment page
        return render_template('new_experiment.html')

@new_experiment.route('/<app_id>',methods=["GET","POST"])
@login_required
@project_required
def new_experiment_details(app_id):

    # initialize form with base form of NewExperimentForm
    class NewExperimentForm_params(NewExperimentForm):
        pass

    # query the app_manager for app specific params
    app_resource = app_manager.get_app_resource(app_id)

    # This is an html string containing the necessary app params.
    app_params_template, app_params_form = app_resource.get_experiment_params()

    # associate app_params_form to form.params
    NewExperimentForm_params.params = FormField(app_params_form)
    form = NewExperimentForm_params()

    # Update the target set selections
    target_set_names = [target.name for target in current_project.target_sets]

    # Is exposing the target id a potential security hole?
    target_set_ids = [target.id for target in current_project.target_sets]
    form.target_set.choices = zip(target_set_ids, target_set_names)

    # check if form is validated
    if form.validate_on_submit():
        # do app specific processing, returns false if processing fails
        if form.params.process_experiment_params():
            name = form.name.data
            description = form.description.data
            instructions = form.instructions.data;
            debrief = form.debrief.data
            params  = form.params.data
            print "data", form.params.data
            target_set = form.target_set.data
            query_tries = form.query_tries.data
            query_duration = form.query_duration.data
            experiment = Experiment(
                name=name,
                description = description,
                instructions = instructions,
                debrief = debrief,
                app_id = app_id,
                params=params,
                target_set=target_set,
                query_tries = query_tries,
                query_duration = query_duration
            )
            experiment.save()


            # Add experiment to the current project
            current_project.add_experiment(experiment)
            return redirect(url_for('experiment._experiment', experiment_id=experiment.id))

    # render app params form template with the new composited form
    app_params_html = render_template(app_params_template, form=form.params)
    return render_template("new_experiment_details.html", form=form, app_params_html=app_params_html)


import csv, json, os, requests
from urlparse import urlparse
from bson.json_util import dumps
from flask import Blueprint, Response, render_template, flash, request, redirect, url_for, session,jsonify
from flask.ext.login import login_user, logout_user, login_required, current_user
from flask_wtf import Form
from wtforms import TextField, PasswordField, TextAreaField, RadioField, FieldList, IntegerField, FormField, validators
from werkzeug.local import Local

import base
from base import cache
from base.forms import LoginForm, NewExperimentForm, NewProjectForm
from base.models import User, Experiment
from base.current import *
from base.app_manager import app_manager

config = base.Config()
experiment = Blueprint('experiment', __name__)

@experiment.route('/<experiment_id>')
@login_required
@project_required
def _experiment(experiment_id):
    set_experiment(experiment_id=experiment_id)
    # Frontend base url needed for stats and widgets
    next_backend_url = "http://"+next_backend_global_host+":"+config.NEXT_BACKEND_GLOBAL_PORT
    # Frontend url needed for queries
    next_frontend_url = "http://"+config.NEXT_FRONTEND_GLOBAL_HOST+":"+config.NEXT_FRONTEND_GLOBAL_PORT
    # query the app_manager for app specific params
    app_resource = app_manager.get_app_resource(current_experiment.app_id)
    # This is an html string containing the necessary app dashboard.
    app_dashboard_html = app_resource.get_experiment_dashboard(current_experiment)
    return render_template('experiment.html',
                           experiment_id=experiment_id,
                           next_backend_url=next_backend_url,
                           next_frontend_url=next_frontend_url,
                           app_dashboard_html=app_dashboard_html)

@experiment.route('/clone/<experiment_id>',methods=["GET","POST"])
@login_required
@project_required
@experiment_required
def clone(experiment_id):
    set_experiment(experiment_id=experiment_id)
    # copy current experiment attributes
    app_id = current_experiment.app_id
    name = current_experiment.name + '_clone'
    description = current_experiment.description
    instructions = current_experiment.instructions
    debrief = current_experiment.debrief
    params  = current_experiment.params
    target_set = current_experiment.target_set
    # create new experiment object
    experiment = Experiment(name=name,
                            description = description,
                            instructions = instructions,
                            debrief = debrief,
                            app_id = app_id,
                            params=params,
                            target_set=target_set)
    experiment.save()
    # Add experiment to the current project
    current_project.add_experiment(experiment)
    return redirect(url_for('experiment.edit', experiment_id=experiment.id))

@experiment.route('/edit/<experiment_id>',methods=["GET","POST"])
@login_required
@project_required
@experiment_required
def edit(experiment_id):
    # initialize form with base form of NewExperimentForm
    class NewExperimentForm_params(NewExperimentForm):
        pass

    # query the app_manager for app specific params
    app_resource = app_manager.get_app_resource(current_experiment.app_id)

    # This is an html string containing the necessary app params.
    app_params_template, app_params_form = app_resource.get_experiment_params()

    # associate app_params_form to form.params
    NewExperimentForm_params.params = FormField(app_params_form)
    form = NewExperimentForm_params(obj=current_experiment)

    # render app params form template with the new composited form
    app_params_html = render_template(app_params_template, form=form.params)

    # Update the target set selections
    target_set_names = [target.name for target in current_project.target_sets]

    # Is exposing the target id a potential security hole?
    target_set_ids = [target.id for target in current_project.target_sets]
    form.target_set.choices = zip(target_set_ids, target_set_names)

    if form.validate_on_submit():
        # update all fields
        # Why do we use updates instead of saves?
        print form.params.data
        current_experiment.update(set__name=form.name.data)
        current_experiment.update(set__description=form.description.data)
        current_experiment.update(set__instructions=form.instructions.data)
        current_experiment.update(set__debrief = form.debrief.data)
        current_experiment.update(set__params=form.params.data)
        current_experiment.update(set__target_set=form.target_set.data)
        current_experiment.update(set__query_tries=form.query_tries.data)
        current_experiment.update(set__query_duration=form.query_duration.data)
        return redirect(url_for('experiment._experiment', experiment_id=current_experiment.id))

    return render_template("edit_experiment_details.html", form=form, app_params_html = app_params_html)


@experiment.route('/delete/<experiment_id>',methods=["GET","POST"])
@login_required
@project_required
@experiment_required
def delete(experiment_id):
    current_project.update(pull__experiments=experiment_id)
    Experiment.objects(id=experiment_id).delete()
    set_experiment()
    return redirect(url_for('project._project', project_id=current_project.id))

@experiment.route('/run_experiment/<experiment_id>')
@login_required
@project_required
@experiment_required
def run_experiment(experiment_id):
    # Get the appropriate app manager resource
    app_resource = app_manager.get_app_resource(current_experiment.app_id)
    # Run the experiment using this app resource
    url = "http://"+next_backend_global_host+":"+config.NEXT_BACKEND_GLOBAL_PORT+"/api/experiment"
    response_dict = app_resource.run_experiment(current_experiment, url)

    if 'exp_uid' in response_dict.keys() and 'exp_key' in response_dict.keys():
        current_experiment.set_exp_uid(response_dict['exp_uid'])
        current_experiment.set_exp_key(response_dict['exp_key'])
        current_experiment.set_perm_key(response_dict['perm_key'])
    else:
        flash("Failed to change experiment status to running.")
        return redirect(url_for('experiment._experiment', experiment_id = current_experiment.id))

    # Get the experiment info and store it in our current model
    response = requests.get(url+"/"+current_experiment.exp_uid+"/"+current_experiment.exp_key)
    current_experiment.set_info(eval(response.text))

    # Now that we have an exp_uid and exp_key, we can do the target mapping. This needs some error handling here.
    create_target_mapping_dict = {}
    create_target_mapping_dict['app_id'] = current_experiment.app_id
    create_target_mapping_dict['exp_uid'] = current_experiment.exp_uid
    create_target_mapping_dict['exp_key'] = current_experiment.exp_key

    # Do this more cleanly. The problem is that mongoengine fields can't be json serialized.
    create_target_mapping_dict['target_blob'] = [mongo_to_dict(doc) for doc in current_experiment.target_set.targets]
    url = "http://"+next_backend_global_host+":"+config.NEXT_BACKEND_GLOBAL_PORT+"/api/targets/createtargetmapping"
    response = requests.post(url,
                             json.dumps(create_target_mapping_dict),
                             headers={'content-type':'application/json'})
    # This should only be done if we can confirm that all the previous steps worked.
    current_experiment.set_status('running')
    return redirect(url_for('experiment._experiment', experiment_id = current_experiment.id))


@experiment.route('/get-temp-keys')
@login_required
@project_required
@experiment_required
def get_temp_keys():
    n = int(request.args.get("keys_count",0))
    # Use local links to to local request
    url = "http://"+next_backend_global_host+":"+config.NEXT_BACKEND_GLOBAL_PORT+"/api/temp-widget-keys"
    args = {
        'exp_uid':current_experiment.exp_uid,
        'exp_key':current_experiment.exp_key,
        'n': n,
        'tries': current_experiment.query_tries,
        'duration': current_experiment.query_duration
        }

    try:
        response = requests.post(url, json.dumps(args), headers={'content-type':'application/json'})
    except (requests.HTTPError, requests.ConnectionError) as e:
        print "Excepted in get_temp_key", e
        raise

    keys = eval(response.text)["keys"]
    # Use the global host and port since these are external links
    links = ["http://"+ config.NEXT_FRONTEND_GLOBAL_HOST+":"+str(config.NEXT_BACKEND_GLOBAL_PORT)+"/query/query_page/query_page/"+current_experiment.exp_uid+"/"+key for key in keys]
    return "\n".join(links),200, {'Content-Disposition':'attachment'}

@experiment.route('/get-participant-responses')
@login_required
@project_required
@experiment_required
def get_participant_responses():
    url = "http://"+next_backend_global_host+":"+config.NEXT_BACKEND_GLOBAL_PORT
    app_resource = app_manager.get_app_resource(current_experiment.app_id)
    participant_responses = app_resource.get_formatted_participant_data(current_experiment, url)
    return "\n".join(participant_responses), 200, {'Content-Disposition':'attachment', 'Content-Type': 'text/csv; charset=utf-8'}

@experiment.route('/get-embedding')
@login_required
@project_required
@experiment_required
def get_embedding():
    url = "http://"+next_backend_global_host+":"+config.NEXT_BACKEND_GLOBAL_PORT
    app_resource = app_manager.get_app_resource(current_experiment.app_id)
    embedding = app_resource.get_formatted_embedding_data(current_experiment,
                                                          url)
    print embedding

    return "\n".join(embedding), 200, {'Content-Disposition':'attachment', 'Content-Type': 'text/csv; charset=utf-8'}

#############################
# Some utility functions

def mongo_to_dict(doc):
    # This is a bit sloppy
    d = doc.to_mongo().to_dict()
    del d['_id']
    return d

@experiment.route('/query/<app_id>/<exp_uid>/<widget_key>')
def getquery(app_id, exp_uid, widget_key):
    # get experiment
    requested_experiment = Experiment.objects(exp_uid=exp_uid)[0]
    # query the app_manager for app specific params
    app_resource = app_manager.get_app_resource(requested_experiment.app_id)
    # This is an html string containing the necessary app dashboard.
    app_query_html = app_resource.get_query(
                            app_id=app_id,
                            exp_uid = exp_uid,
                            widget_key = widget_key)

    return app_query_html


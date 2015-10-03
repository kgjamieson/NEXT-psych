import sys
import datetime

from mongoengine import *
from flask import Blueprint, render_template, request, redirect, url_for
from flask.ext.login import login_required

from base.current import *
from base.settings import Config
from base.models import Target, TargetSet
from base.forms import ManageTargets, TargetSetForm




config = Config()
sys.path.extend('../../examples')
import examples.launch_experiment as launch_experiment

launch_experiment.generate_target_blob
targets = Blueprint('targets', __name__)

@targets.route('/manage',methods=["GET","POST"])
@login_required
@project_required
def manage():
    if request.method == 'POST':
        # Handle the primary targets first
        primary_file = request.files['primary_file']
        alt_file = request.files['alt_file']
        print primary_file.read().splitlines()
        name = request.form['name'] 
        if not name:
            flash('You must specify a unique target set name.')
            return render_template('manage_targets.html')
        
        primary_type = request.form['primary_type']
        alt_type  = 'text' if request.form['alt_type']=='None' else request.form['alt_type']
        
        target_set = TargetSet(name=name)
        target_list = launch_experiment.generate_target_blob(config.AWS_BUCKET_NAME,
                                                             config.AWS_ID,
                                                             config.AWS_KEY,
                                                             str(datetime.date.today()),
                                                             primary_file,
                                                             primary_type,
                                                             alt_file,
                                                             alt_type)['target_blob']
        for target in target_list:
            target = Target(target_id = target['target_id'],
                            primary_type = target['primary_type'],
                            primary_description = target['primary_description'],
                            alt_type = target['alt_type'],
                            alt_description = target['alt_description'])
            target.save()
            target_set.targets.append(target)
        # Save the target_set
        target_set.save()
        current_project.add_target_set(target_set)
    # Always return this page
    return render_template('manage_targets.html')

@targets.route('/edit/<target_set_id>',methods=["GET","POST"])
@login_required
@project_required
def edit(target_set_id):
    # get current target set
    target_set = TargetSet.objects(id=target_set_id)[0]
    # get form
    form = ManageTargets()
    # initialize the target types
    form.target_type.choices = [(1,'text'),(2,'image')]

    # edit target form
    if form.validate_on_submit():
        # get target id from form
        target_id = form.target_id.data
        # check if target id has not been set
        if target_id != 'none':
            # get the target to be edited
            target = Target.objects(id = target_id)[0]
            # update primary/alt descriptions
            target.update(set__primary_description=form.primary_description.data)
            target.update(set__alt_description=form.alt_description.data)
            # need to redefine target set before rendering template to update changes
            target_set = TargetSet.objects(id=target_set_id)[0]
            return render_template("edit_target_set.html", form=form, target_set_form=TargetSetForm(obj=target_set), target_set=target_set)

    return render_template("edit_target_set.html", form=form, target_set_form=TargetSetForm(obj=target_set), target_set=target_set)

@targets.route('/edit/target_set_name/<target_set_id>',methods=["GET","POST"])
@login_required
@project_required
def edit_target_set_name(target_set_id):
    # get current target set
    target_set = TargetSet.objects(id=target_set_id)[0]
    # get form
    target_set_form = TargetSetForm(request.form)

    if target_set_form.validate_on_submit():
        # get target id from form
        name = target_set_form.name.data
        # check if target id has not been set
        if len(name) > 0:
            # update name
            target_set.update(set__name=name)
            # need to redefine target set before rendering template to update changes
            target_set = TargetSet.objects(id=target_set_id)[0]
            # create new form object for editing targets
            # return render_template("edit_target_set.html", form=form, target_set_form=TargetSetForm(obj=target_set), target_set=target_set)

    return redirect(url_for('targets.edit', target_set_id=target_set_id))

@targets.route('/edit/delete_selected/<target_set_id>',methods=["GET","POST"])
@login_required
@project_required
def delete_selected(target_set_id):
    # getting all the targets that the user selects
    checked_items = request.values.getlist("targets")
    # loop through specified targets
    for target_id in checked_items:
        # get target from target id
        target = Target.objects(id = target_id)[0]
        # pull target from target set
        TargetSet.objects(id=target_set_id).update(pull__targets=target)
        # delete target object from mongo
        target.delete()

    # get updated target set
    target_set = TargetSet.objects(id=target_set_id)[0]

    return redirect(url_for('targets.edit', target_set_id=target_set.id))

@targets.route('/edit/delete_all/<target_set_id>',methods=["GET","POST"])
@login_required
@project_required
def delete_all(target_set_id):
    # remove target set from current project
    current_project.update(pull__target_sets=target_set_id)
    # delete target set from mongo
    TargetSet.objects(id=target_set_id).delete()

    return redirect(url_for('targets.manage'))


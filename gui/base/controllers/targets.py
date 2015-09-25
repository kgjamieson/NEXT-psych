from flask import Blueprint, render_template, flash, request, redirect, url_for, session
from flask.ext.login import login_user, logout_user, login_required
from wtforms import TextField, PasswordField, TextAreaField, RadioField, FieldList, IntegerField, FormField, StringField, validators, SelectField, HiddenField
from flask_wtf import Form

from base import cache
from base.forms import LoginForm, NewExperimentForm, ManageTargets, TargetSetForm
from base.models import User, Target, TargetSet
from base.current import *

from base.upload_manager import *
from boto.s3.connection import S3Connection
from boto.s3.key import Key

from StringIO import StringIO
from mongoengine import *
import os

targets = Blueprint('targets', __name__)

@targets.route('/manage',methods=["GET","POST"])
@login_required
@project_required
def manage():
    if request.method == 'POST':
        # Handle the zip file case first
        has_zip_file = False
        hosted_zip_file = request.files['hosted_zip_file']
        hosted_zip_file.seek(0, os.SEEK_END)
        if "hosted_zip_file" in request.files.keys() and hosted_zip_file.tell()!=0:
            has_zip_file = True
            hosted_zip_file = request.files['hosted_zip_file']

            # Dictionary mapping filename to object
            target_file_dict = zipfile_to_dictionary(hosted_zip_file)
            # Very basic consistency check
            #if len(target_list) != len(target_file_dict):
            #    flash("Inconsistent number of targets to images")
            #    return redirect(url_for('project.manage_targets'))

        hosted_csv_file = request.files['hosted_csv_file']

        # Parse the csv file into a list of dictionaries, one for each row
        target_list = csv_to_dict(hosted_csv_file, ["target_id", "primary_type", "alt_description"])

        # Create target set
        target_set = TargetSet(name=hosted_csv_file.filename)
        for target in target_list:
                # Get file object
            if has_zip_file == True:
                target_file = target_file_dict[target["target_id"]]
                bucket = get_AWS_bucket()
                target_url = upload_to_S3(bucket, str(current_project.id)+"_"+target["target_id"], StringIO(target_file))
                target = Target( target_id = target["target_id"],
                                 primary_type = target["primary_type"],
                                 primary_description = target_url,
                                 alt_type = "text",
                                 alt_description = target["alt_description"])
            else:
                target = Target( target_id = target["target_id"],
                                 primary_type = target["primary_type"],
                                 primary_description = target["target_id"],
                                 alt_type = "text",
                                 alt_description = target["alt_description"])
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


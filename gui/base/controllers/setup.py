import os
import random

import boto
from flask import (Blueprint,
                   render_template,
                   flash,
                   request,
                   redirect,
                   url_for,
                   session)
from flask.ext.login import login_required

import base
from base.forms import SecretForm


config = base.config
setup = Blueprint('setup', __name__)

@setup.route('/', methods=['GET','POST'])
@login_required
def _setup():
    form = SecretForm()
    if form.validate_on_submit():
        #config.AWS_ID = form.access_key_id.data
        os.environ['AWS_ACCESS_ID'] = form.access_key_id.data
        #config.AWS_KEY = form.secret_access_key.data
        os.environ['AWS_SECRET_ACCESS_KEY'] = form.secret_access_key.data
        #config.NEXT_BACKEND_GLOBAL_HOST = form.next_backend_global_host.data
        os.environ['NEXT_BACKEND_GLOBAL_HOST'] = form.next_backend_global_host
        gotbucket = False
        try:
            conn = boto.connect_s3(config.AWS_ID, config.AWS_KEY )
            while not gotbucket:
                bucket_uid = '%030x' % random.randrange(16**30)
                try:
                    newbucket = conn.create_bucket(bucket_uid)
                    gotbucket = True
                except boto.exception.S3CreateError, e:
                    pass
            os.environ['AWS_BUCKET_NAME'] = form.next_backend_global_host
            #config.AWS_BUCKET_NAME = bucket_uid
        except e:
            flash("Please check your aws credentials")
            return render_template('setup.html', form = SecretForm())
        return redirect(url_for('dashboard._dashboard'))
    return render_template('setup.html', form = form)
    # else:                       
    #     
        

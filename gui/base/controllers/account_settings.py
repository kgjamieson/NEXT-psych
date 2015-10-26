from flask import (Blueprint,
                   render_template,
                   flash, request,
                   redirect,
                   url_for,
                   session)
from flask.ext.login import login_required
from base.forms import SecretForm
import base

config = base.config
account_settings = Blueprint('account_settings', __name__)


@account_settings.route('/')
@login_required
def _account_settings():

    print config.NEXT_BACKEND_GLOBAL_HOST
    form = SecretForm()
    return render_template('account_settings.html', form = form)
    

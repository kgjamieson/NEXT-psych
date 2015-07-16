from flask import Blueprint, render_template, flash, request, redirect, url_for, session
from flask.ext.login import login_user, logout_user, login_required

from base import cache
from base.forms import LoginForm, NewExperimentForm
from base.models import User

account_settings = Blueprint('account_settings', __name__)


@account_settings.route('/')
@login_required
def _account_settings():
    return render_template('account_settings.html')

    

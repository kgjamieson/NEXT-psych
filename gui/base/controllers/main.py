from flask import Blueprint, render_template, flash, request, redirect, url_for, session
from flask.ext.login import login_user, logout_user, login_required

from base import cache
from base.forms import LoginForm, CreateAccountForm
from base.models import User, Experiment

main = Blueprint('main', __name__)

@main.route('/', methods=["GET", "POST"])
def home():
    return render_template('index.html', login_form=LoginForm(), create_form=CreateAccountForm())

@main.route('/login', methods=["POST"])
def login():
    login_form = LoginForm(request.form)
    if login_form.validate_on_submit():
        user = User.objects(email=login_form.email.data).first()
        if user and user.check_password(login_form.password.data):
            login_user(user)
            return redirect(request.args.get("next") or url_for('dashboard._dashboard'))
        else:
            flash("Login failed.", "login_error")
            # login is not valid
            return redirect('#create')
    return render_template('index.html', login_form=login_form, create_form=CreateAccountForm())
    

@main.route('/create', methods=["GET", "POST"])
def create():
    create_form = CreateAccountForm(request.form)
    if create_form.validate_on_submit():
        print "form data",create_form.new_email.data
        new_email = create_form.new_email.data
        new_password = create_form.new_password.data
        confirm_password = create_form.confirm_password.data
        print User.objects()
        if User.objects(email=new_email).count() == 0:
            if new_password == confirm_password:
                # Set the hashed password on the user.
                user = User(email=new_email)
                user.set_password(new_password)
                user.save()
                login_user(user, remember=True)
                return redirect(url_for('dashboard._dashboard'))
            else:
                flash("Passwords don't match!", "create_error")
                return redirect('#create')    
        else:
            flash("Username exists!", "create_error")
            return redirect('#create')
    # login form is not valid
    return render_template('index.html', login_form=LoginForm(), create_form=create_form)

@main.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    #session.clear()
    return redirect(url_for('main.home'))



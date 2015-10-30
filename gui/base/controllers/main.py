from flask import Blueprint, render_template, flash, request, redirect, url_for, session
from flask.ext.login import login_user, logout_user, login_required
from base.forms import LoginForm, CreateAccountForm
from base.models import User
from base.settings import Config

main = Blueprint('main', __name__)
config = Config()
@main.route('/', methods=["GET", "POST"])
def home():
    print "config.AUTHENTICATE {}".format(config.AUTHENTICATE)
    if config.AUTHENTICATE:
        return render_template('index.html',
                               login_form=LoginForm(),
                               create_form=CreateAccountForm())
    else:
        email = 'default'
        password = 'password'
        access_key_id = config.AWS_ID
        secret_access_key = config.AWS_KEY
        aws_bucket_name = config.AWS_BUCKET_NAME
        next_backend_global_host = config.NEXT_BACKEND_GLOBAL_HOST
        if not User.objects(email=email):
            user = User(email=email,
                        access_key_id=access_key_id,
                        secret_acces_key=secret_access_key,
                        aws_bucket_name=aws_bucket_name,
                        next_backend_global_host=next_backend_global_host)
            user.set_password(password)
            user.save()
        else:
            user = User.objects(email=email).first()
        login_user(user, remember=True)
        return redirect(url_for('dashboard._dashboard'))

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
    return render_template('index.html',
                           login_form=login_form,
                           create_form=CreateAccountForm())
    

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



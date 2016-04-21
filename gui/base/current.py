from functools import wraps
from flask import current_app, g, request, redirect, url_for, session, _app_ctx_stack, _request_ctx_stack
from werkzeug.local import LocalProxy
from models import User, Project, Experiment
from urlparse import urlparse

current_project = LocalProxy(lambda: _get_project())
current_experiment = LocalProxy(lambda: _get_experiment())
next_backend_global_host = LocalProxy(lambda: urlparse(request.url).hostname)

class Current(object):
    '''
    Manages the current project and experiment that a user is navigating. 
    
    Requires a project_loader: ::\n
    	@current.project_loader
    		def load_project(project_id):
    			return Project.objects(name = project_id)[0]


    '''
    def __init__(self, app=None, add_context_processor=True):
        self.project_callback = None
        self.experiment_callback = None
        if app is not None:
            self.init_app(app, add_context_processor)
        
    def init_app(self, app, add_context_processor=True):
        app.current = self
        if add_context_processor:
            app.context_processor(_project_context_processor)
            app.context_processor(_experiment_context_processor)

    def project_loader(self, loader):
        self.project_callback = loader

    def experiment_loader(self, loader):
        self.experiment_callback = loader

        
def set_project(project = None, project_id = None):
    '''
    Set's the project as the current project. 
    Either the project object or the project_id can be passed to this. 
    '''
    # Now add this project to the app context stack
    if not project == None:
        session['project_id'] = project.id
    elif not project_id == None:
        if current_app.current.project_callback == None:
            raise Exception("Please register a project loader method using the Current.project_loader decorator")
        session['project_id'] = project_id
    else:
        del session['project_id']
        # raise Exception(" Either project_id or project object must be provided")

def set_experiment(experiment = None, experiment_id = None):
    '''
    Set's the experiment as the current experiment. 
    Either the experiment object or the exp_uid can be passed to this. 
    '''
    # Now add this project to the app context stack
    if not experiment == None:
        session['experiment_id'] = experiment.id
    elif not experiment_id == None:
        if current_app.current.experiment_callback == None:
            raise Exception("Please register an experiment loader method using the Current.experiment_loader decorator")
        session["experiment_id"] = experiment_id
    else:
        del session["experiment_id"]
        # raise Exception(" Either experiment_id or experiment object must be provided")

    
def project_required(func):
    '''
    Decorator for a view to ensure that a project is active. If a project is not available, will kick the user to their dashboard.
    '''
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_project == None:
            # Eventually generalize this!!
            return redirect(url_for('dashboard._dashboard'))
        return func(*args, **kwargs)
    return decorated_view

def experiment_required(func):
    '''
    Decorator for a view to ensure that a project is active. If a project is not available, will kick the user to their dashboard.
    '''
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_experiment == None:
            # Eventually generalize this!!
            return redirect(url_for('dashboard._dashboard'))
        return func(*args, **kwargs)
    return decorated_view

def _project_context_processor():
    return dict(current_project=_get_project())

def _experiment_context_processor():
    return dict(current_experiment=_get_experiment())

def _get_project():
    if 'project_id' in session.keys():
        return current_app.current.project_callback(session['project_id'])
    else:
        return None

def _get_experiment():
    if 'experiment_id' in session.keys():
        return current_app.current.experiment_callback(session['experiment_id'])
    else:
        return None
    
    

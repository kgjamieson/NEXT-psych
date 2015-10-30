#! ../env/bin/python
import os

from flask import Flask
from flask.ext.cache import Cache
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.login import LoginManager
from flask_assets import Environment
from flask.ext.mongoengine import MongoEngine
from webassets.loaders import PythonLoader as PythonAssetsLoader

from base import assets
from base.settings import Config

config = Config()

# Setup flask cache
cache = Cache()

# Initialize flask assets
assets_env = Environment()

# Initialize debug toolbar
debug_toolbar = DebugToolbarExtension()

# Initialize Flask Login login manager
login_manager = LoginManager()
login_manager.login_view = "main.home"

# Initialize mongoengine db
db = MongoEngine()

from base.models import User, Project, Experiment
# import base.current
from base.current import Current
# Initialize current for current_experiment and current_project decorators
current = Current()

def create_app(object_name, env="prod"):
    """
    A flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Inputs:  ::\n
        object_name: the python path of the config object,
                     e.g. appname.settings.ProdConfig

        env: The name of the current environment, e.g. prod or dev
    """

    app = Flask(__name__)

    app.config.from_object(object_name)
    app.config['ENV'] = env
    
    # Init the cache
    cache.init_app(app)

    # Init debug toolbar
    debug_toolbar.init_app(app)

    # Init Mongo engine
    # mongoengine.connect(config.MONGODB_FRONTEND_DB_NAME, host=config.MONGODB_HOST, port=config.MONGODB_PORT)
    app.config['MONGODB_DB'] = config.MONGODB_FRONTEND_DB_NAME
    app.config['MONGODB_HOST'] = config.MONGODB_HOST
    app.config['MONGODB_PORT'] = config.MONGODB_PORT
    db.init_app(app)

    # Init login_manager
    login_manager.init_app(app)
    login_manager.login_view = "main.login"
    login_manager.refresh_view = "main.login"
    # Init current to track current project/experiment
    current.init_app(app)
    
    # Import and register the different asset bundles
    assets_env.init_app(app)
    assets_loader = PythonAssetsLoader(assets)
    for name, bundle in assets_loader.load_bundles().iteritems():
        assets_env.register(name, bundle)

    # register all the  blueprints
    from controllers import (
        main,
        error,
        dashboard,
        new_experiment,
        new_project,
        account_settings,
        project,
        experiment,
        targets,
        setup
    )
    
    app.register_blueprint(main)
    app.register_blueprint(error,url_prefix="/error")
    app.register_blueprint(dashboard,url_prefix="/dashboard")
    app.register_blueprint(new_experiment,url_prefix="/new_experiment")
    app.register_blueprint(new_project,url_prefix="/new_project")
    app.register_blueprint(account_settings,url_prefix="/account_settings")
    app.register_blueprint(project,url_prefix="/project")
    app.register_blueprint(experiment,url_prefix="/experiment")
    app.register_blueprint(targets,url_prefix="/targets")
    app.register_blueprint(setup,url_prefix="/setup")

    return app



@login_manager.user_loader
def load_user(userid):
    users = User.objects(email=userid)
    if len(users) >0:
        return users[0]
    return None

@current.project_loader
def load_project(project_id):
    projects  = Project.objects(id = project_id)
    if len(projects)>0:
        return projects[0]
    else:
        return None

@current.experiment_loader
def load_experiment(experiment_id):
    experiments = Experiment.objects(id = experiment_id)
    if len(experiments) > 0:
        return experiments[0]
    else:
        return None

if __name__ == '__main__':
    # Import the config for the proper environment using the shell var APPNAME_ENV
    env = os.environ.get('NEXT_FRONTEND_ENV', 'prod')
    app = create_app('base.settings.%sConfig' % env.capitalize(), env=env)
    app.run()



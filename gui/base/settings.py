import os
from pymongo import read_preferences

class Config(object):
    # Secret key for the cookies. Change in production.
    SECRET_KEY = 'secret'

    # Mongo DB settings.
    MONGODB_SETTINGS = {
        'db': 'next_frontend',
        'host': os.environ.get('MONGODB_PORT_27017_TCP_ADDR','localhost'),
        'port': int(os.environ.get('MONGODB_PORT_27017_TCP_PORT',27017)),
        'read_preference': read_preferences.ReadPreference.PRIMARY
    }

    # MongoDB info
    MONGODB_HOST = os.environ.get('MONGODB_PORT_27017_TCP_ADDR','localhost')
    MONGODB_PORT = int(os.environ.get('MONGODB_PORT_27017_TCP_PORT',27017))
    MONGODB_FRONTEND_DB_NAME = 'next_frontend'

    # AWS S3 info
    AWS_ID = os.environ.get('AWS_ACCESS_ID', None)
    AWS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', None)
    AWS_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME','next.discovery')

    # Local docker frontend base links (This is not set, therefor always is localhost, which is fine)
    NEXT_BACKEND_HOST = os.environ.get("NEXT_BACKEND_GLOBAL_HOST", 'localhost')
    NEXT_BACKEND_PORT = os.environ.get("NEXT_BACKEND_GLOBAL_PORT", "8000")
    
    # Global frontend base links. Used for widgets and stats calls.
    NEXT_BACKEND_GLOBAL_HOST = os.environ.get("NEXT_BACKEND_GLOBAL_HOST", 'localhost')
    NEXT_BACKEND_GLOBAL_PORT = os.environ.get("NEXT_BACKEND_GLOBAL_PORT", "8000")

    # Site ID and Key for Next Frontend Base.
    SITE_ID = '99eb2f19d5a303acc8fa1a6e9e05cd'
    SITE_KEY = '7c48d1b377889d9ec0322e1dcf7f39'

    AUTHENTICATE = False
    
class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../next_baseDB.db'
    CACHE_TYPE = 'simple'


class DevConfig(Config):
    # Config variables for the debug panel
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    DEBUG_TB_PANELS = ['flask.ext.mongoengine.panels.MongoDebugPanel']
    
    CACHE_TYPE = 'null'

    # This allows us to test the forms from WTForm
    WTF_CSRF_ENABLED = False

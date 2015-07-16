import base
import os
import logging
import sys

# Import the next_backend app from next_backend. 
env = os.environ.get('NEXT_FRONTEND_ENV', 'prod')
app = base.create_app('base.settings.%sConfig' % env.capitalize(), env=env)
    
# Log to standard out. Remember to turn off in production
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)


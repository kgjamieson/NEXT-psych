import os

def get_app_resource(app_id):
    """
    Returns an app_resource corresponding to this app_id

    Inputs: ::\n
    	(string) app_id: app identifier

    Outputs: ::\n
    	app_resource object
    
    """

    app_id = str(app_id) # sometimes input is unicode formatted which causes error
    path = 'base.app_manager'
    app_module = __import__(path+"."+app_id, fromlist=[app_id])
    app_class = getattr(app_module, app_id)
    return app_class()


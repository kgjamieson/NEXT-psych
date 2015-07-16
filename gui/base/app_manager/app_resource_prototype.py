class AppResourcePrototype:
    """
    AppResource
    Author: Lalit Jain

    Prototype class for an app resource. 
    """

    def get_experiment_params(self, args=None):
        """
        Return a form and a template with specific params for the new experiment form.
        """
        raise NotImplementedError
        
    def get_experiment_dashboard(self, args=None):
        """
        Return template with embedded widgets/plots/data for the dashboard.
        """
        raise NotImplementedError
    
    def get_formatted_participant_data(self, args=None):
        """
        Return formatted participant logs that are app specific.
        """
        raise NotImplementedError


    def run_experiment(self, current_experiment, args=None):
        """
        Run an initExp call on the frontend base level.
        """
        raise NotImplementedError

    def get_query(self, app_id, exp_uid, widget_key, args=None):
        """
        Render custom query for app type
        """
        raise NotImplementedError

    

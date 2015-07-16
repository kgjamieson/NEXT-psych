import csv, json, os, requests, sys
from wtforms import Form, FieldList, FloatField, FormField, TextField, IntegerField,  SelectField, validators, RadioField, FileField
from jinja2 import Environment, FileSystemLoader
import copy
from base.settings import Config
from base.app_manager.app_resource_prototype import AppResourcePrototype
from flask import render_template
from base.current import *
from base.models import Experiment

from base.upload_manager import *
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from StringIO import StringIO
import random, string

config = Config()
TEMPLATES_DIRECTORY = os.path.dirname(__file__)
loader = FileSystemLoader(TEMPLATES_DIRECTORY)
env = Environment(loader=loader)

class TupleBanditsPureExploration(AppResourcePrototype):
    """
    TupleBanditsPureExploration
    Author: Nick Glattard

    App resource for TupleBanditsPureExploration. 
    """

    def get_experiment_params(self, args=None):
        """
        Return a form and a template with specific params for the new experiment form.
        """
        alg_list = ['RandomSampling']
        # Alg row: follow this post: http://stackoverflow.com/questions/11402627/how-to-get-a-build-a-form-with-repeated-elements-well
        class AlgorithmDefinitionRowForm(Form):
            alg_label = TextField('Algorithm Label')
            alg_id = SelectField('Algorithm Id', choices=[(algorithm, algorithm) for algorithm in alg_list])
            alg_proportion = FloatField('Algorithm Proportion')
        
        class TupleBanditsPureExplorationForm(Form):            
            context_type = SelectField('Context Type', choices=[('text', 'Text'), ('image', 'Image')])
            context_image = FileField('Context Image')
            context_text = TextField('Context Text')
            k = IntegerField('Number of targets to choose from', default=4)
            failure_probability = FloatField('Confidence Level', validators=[validators.required()], default=0.95)
            algorithm_management = RadioField('Algorithm Management', 
                                                choices=[('fixed_proportions','Fixed Proportions'),
                                                        ('pure_exploration','Pure Exploration'),
                                                        ('explore_exploit','Explore Exploit')],
                                                default='fixed_proportions')
            participant_to_algorithm_management = RadioField('Participant to Algorithm Management', 
                                                                choices=[('one_to_many','One-to-many'),
                                                                          ('one_to_one','One-to-one')],
                                                                default='one_to_many')

            # process the experiment parameters
            def process_experiment_params(self):
                if self.context_type.data == 'image':
                    # is an image uploaded?
                    if self.context_image.data:
                        # upload image to s3
                        try:
                            f = self.context_image.data.read()
                            bucket = get_AWS_bucket()
                            random_name = ''.join(random.choice(string.ascii_uppercase) for i in range(12))
                            context_url = upload_to_S3(bucket, random_name, StringIO(f))
                            self.context_image.data = context_url
                        except Exception,e:
                            print e
                            return False
                    else:
                        self.context_type.data = 'none'
                else:
                    # check if empty string
                    if not self.context_text.data:
                        self.context_type.data = 'none'

                # return boolean of whether or not upload worked
                return True

            # List field of the rows of algorithm labels and alg id's
            alg_rows = FieldList(FormField(AlgorithmDefinitionRowForm))

        template = env.get_template("new_experiment_params.html")
        return template, TupleBanditsPureExplorationForm

    def get_experiment_dashboard(self, current_experiment, args=None):
        """
        Return template with embedded widgets/plots/data for the dashboard.
        """
        template = env.get_template("experiment_dashboard.html")
        html = render_template(template)
        return html
    
    def get_formatted_participant_data(self, current_experiment, args=None):
        """
        Return formatted participant logs that are app specific.
        """
        # WHY ARE WE LOOKING AT INDICES IN THIS FUNCTION???
        
        # Use frontend base local url
        url = "http://"+config.NEXT_BACKEND_GLOBAL_HOST+":"+config.NEXT_BACKEND_GLOBAL_PORT+"/api/experiment/"+current_experiment.exp_uid+"/"+current_experiment.exp_key+"/participants"
        try:
            response = requests.get(url)
            response_dict = eval(response.text)
        except (requests.HTTPError, requests.ConnectionError) as e:
            print "excepted e", e
            raise

        participant_responses = []
        participant_responses.append(",".join(["Participant Id", "Timestamp","Left","Right","Answer","Alg Label"]))
        for participant_id, response_list in response_dict['participant_responses'].iteritems():
            for response in response_list:
                line = [participant_id, response['timestamp_query_generated']]
                targets = {}
                for index in response['target_indices']:
                    targets[index['label']] = index
                    # Check for the index winner in this response
                    # Shouldn't there be a target_winner? This is weird.
                    if 'index_winner' in response.keys() and response["index_winner"] == index['index']:
                            target_winner = index
                # Append the left and right targets
                line.extend([targets['left']['target']['target_id'], targets['right']['target']['target_id']])
                # Append the index winner
                line.append(target_winner['target']['target_id'])
                # Append the alg_label
                line.append(response['alg_label'])
                participant_responses.append(",".join(line))
                
        return participant_responses   


    def run_experiment(self, current_experiment, args=None):
        """
        Run an initExp call on the frontend base level.
        """
        # Set up request dictionary for api initExp call
        initExp_dict = {}
        initExp_dict['app_id'] = current_experiment.app_id
        initExp_dict['site_id'] = config.SITE_ID
        initExp_dict['site_key'] = config.SITE_KEY
        initExp_dict['args'] = {}

        # Set up args for api initExp call
        initExp_dict['args']['instructions'] = current_experiment.instructions
        initExp_dict['args']['debrief'] = current_experiment.debrief
        initExp_dict['args']['n'] = len(current_experiment.target_set.targets)#current_experiment.params['n']
        # number of arms is denoted n, as well as expected key for target set init. This could be problematic.
        initExp_dict['args']['k'] = current_experiment.params['k']
        # initExp_dict['args']['num_targets'] = len(current_experiment.target_set.targets)
        initExp_dict['args']['failure_probability'] = current_experiment.params['failure_probability']
        initExp_dict['args']['participant_to_algorithm_management'] = current_experiment.params['participant_to_algorithm_management']
        initExp_dict['args']['alg_list'] = []
        initExp_dict['args']['algorithm_management_settings'] = {}
        initExp_dict['args']['algorithm_management_settings']['mode'] = current_experiment.params['algorithm_management']
        initExp_dict['args']['algorithm_management_settings']['params'] = {}
        initExp_dict['args']['algorithm_management_settings']['params']['context_type'] = current_experiment.params['context_type']
        initExp_dict['args']['algorithm_management_settings']['params']['context_image'] = current_experiment.params['context_image']
        initExp_dict['args']['algorithm_management_settings']['params']['context_text'] = current_experiment.params['context_text']
        initExp_dict['args']['algorithm_management_settings']['params']['proportions'] = []
        
        for alg in current_experiment.params['alg_rows']:
            params_dict = copy.deepcopy(alg)
            params_dict['params'] = {}
            params_dict['test_alg_label'] = 'Test'
            del params_dict['alg_proportion']
            initExp_dict['args']['alg_list'].append(params_dict)

            proportions_dict = {}
            proportions_dict['alg_label'] = alg['alg_label']
            proportions_dict['proportion'] = alg['alg_proportion']
            initExp_dict['args']['algorithm_management_settings']['params']['proportions'].append(proportions_dict)
        
        print initExp_dict

        # Make request  for initExp 
        try:
            url = "http://"+config.NEXT_BACKEND_GLOBAL_HOST+":"+config.NEXT_BACKEND_GLOBAL_PORT+"/api/experiment"
            response = requests.post(url,
                                     json.dumps(initExp_dict),
                                     headers={'content-type':'application/json'})
            response_dict = eval(response.text)
            
        except:
            exc_class, exc, tb = sys.exc_info()
            new_exc = Exception("%s. Error connecting to backend."%(exc or exc_class))
            raise new_exc.__class__,new_exc, tb

        return response_dict


    def get_query(self, app_id, exp_uid, widget_key, args=None):
        """
        Render custom query for app type
        """
        
        # Make this more flexible
        next_backend_url = "http://"+config.NEXT_BACKEND_GLOBAL_HOST+":"+config.NEXT_BACKEND_GLOBAL_PORT

        # pass in cookie dependent data
        requested_experiment = Experiment.objects(exp_uid=exp_uid)[0]
        query_tries = requested_experiment.query_tries
        debrief = requested_experiment.debrief
        instructions = requested_experiment.instructions
        context_type = requested_experiment.params['context_type']

        if context_type == 'image':
            context_content = requested_experiment.params['context_image']
        elif context_type == 'text':
            context_content = requested_experiment.params['context_text']
        else:
            context_content = 'none'

        template = env.get_template("query.html")

        return render_template(template, 
                                app_id=app_id, 
                                exp_uid = exp_uid, 
                                widget_key = widget_key, 
                                next_backend_url=next_backend_url,
                                query_tries = query_tries,
                                debrief = debrief,
                                instructions = instructions,
                                context_type=context_type,
                                context_content=context_content)



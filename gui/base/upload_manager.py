from boto.s3.connection import S3Connection
from boto.s3.key import Key
from base.settings import Config
import json
import csv
import zipfile

config = Config()

def upload_to_S3(bucket, key, file_object):
    """
    DESCRIPTION:
    Uploads a file object to a S3 instance

    Inputs: ::\n 
        bucket: S3 bucket we want to upload to
        key: the key to access the file in the bucket;
        file_object: the file that needs to be uploaded

    """   
    k = Key(bucket)
    k.key = key
    k.set_contents_from_file(file_object)
    k.set_acl('public-read')
    return k.generate_url(expires_in=0, query_auth=False, force_http=True)
    
def get_AWS_bucket():
    """
    DESCRIPTION:
    Creates a bucket for an S3 account 

    """
    conn = S3Connection(config.AWS_ID, config.AWS_KEY)

    #Maybe by default we should try to create bucket and then catch exception?
    #Also, migrate the bucket name to settings.Config
    bucket = conn.get_bucket(config.AWS_BUCKET_NAME)
    return bucket

def csv_to_dict(file,keys):
    """
    DESCRIPTION:
    Convers a csv file to a list of python dictionaries

    Inputs: ::\n 
        file: the csv file we want to convert to a dictionary
        keys: the list of keys to the dictionary i.e. the column
          headers of the csv file

    Outputs ::\n
        dictionary: the retuned list of dictionaries
    """   
    # reading in the csv file
    reader = csv.reader(file.read().splitlines(),quotechar='"', delimiter=',',skipinitialspace=True)
    
    # holds the final dictionary which the program returns
    result ={} 
    dictionary =[]
    count =0
    i=0

    for row in reader:
        if len(row)>0:
            count =0
            for col in row:
                result[keys[count]] = col
                count = count +1
            dictionary.append(result)
            result ={}    
        i = i+1

    return dictionary
    
def csv_to_json_object(file,keys):
    """
    DESCRIPTION:
    Converts a csv file into a json object

    Inputs: ::\n 
        file: the csv file we want to convert to a json object
        keys: the list of keys to the dictionary i.e. the column
          headers of the csv file

    Outputs: ::\n
        result: the retuned json object
    """
    return json.dumps(csv_to_dict(file,keys))

def zipfile_to_dictionary(file): 
    """
    DESCRIPTION:
    Takes in a zip file and returns a dictionary with the filenames
    as keys and file objects as values

    Inputs: ::\n 
        file: the concerned zip file
        
    Outputs: ::\n
        result: the retuned dictionary
    """
    
    listOfFiles= []
    dictionary ={}
    
    zf = zipfile.ZipFile(file)
    listOfFiles = zf.namelist() 
    for i in listOfFiles:
        f= zf.read(i)
        dictionary[i] = f
        
    return dictionary

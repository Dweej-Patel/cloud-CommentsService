from flask import Flask
import boto3
from dynamo_config import *

# Create the application server main class instance and call it 'application'
# Specific the path that identifies the static content and where it is.
application = Flask(__name__,
                    static_url_path='/static',
                static_folder='WebSite/static')

# Get the service resource.
dynamodbResource = boto3.resource('dynamodb',
                          aws_access_key_id=ACCESS_ID,
                          aws_secret_access_key=ACCESS_KEY)

# Instantiate a table resource object without actually
# creating a DynamoDB table. Note that the attributes of this table
# are lazy-loaded: a request is not made nor are the attribute
# values populated until the attributes
# on the table resource are accessed or its load() method is called.
table = dynamodbResource.Table('Comments')

from app import dynamodb

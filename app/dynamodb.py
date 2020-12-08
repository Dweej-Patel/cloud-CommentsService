import json

import uuid
from app import application, table
from flask import request, Response

# Setup and use the simple, common Python logging framework. Send log messages to the console.
# The application should get the log level out of the context. We will change later.
#

import os
import sys
import platform
import socket


cwd = os.getcwd()
sys.path.append(cwd)

print("*** PYHTHONPATH = " + str(sys.path) + "***")

import logging
from datetime import datetime

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()
logger.setLevel(logging.ERROR)


@application.route('/')
def hello_world():
    rsp = application.send_static_file('index.html')
    return rsp


# This function performs a basic health check. We will flesh this out.
@application.route("/api/health", methods=["GET"])
def health_check():

    pf = platform.system()

    rsp_data = { "status": "healthy", "time": str(datetime.now()),
                 "platform": pf,
                 "release": platform.release()
                 }

    if pf == "Darwin":
        rsp_data["note"]= "For some reason, macOS is called 'Darwin'"


    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)

    rsp_data["hostname"] = hostname
    rsp_data["IPAddr"] = IPAddr

    rsp_str = json.dumps(rsp_data)
    rsp = Response(rsp_str, status=200, content_type="application/json")
    return rsp

# Add new comment to table
@application.route("/api/comments", methods=["POST"])
def createComment():
    data = json.loads(request.data.decode())
    now = datetime.now()
    current_time = now.strftime('%Y-%m-%d %H:%M:%S')
    table.put_item(
       Item={
            'Comment_ID': str(uuid.uuid4()),
            'Comment_text': data['Comment_text'],
            'Email': data['Email'],
            'Datetime': current_time,
            'Tags': data['Tags'],
            'Version_ID': str(uuid.uuid4())
        }
    )
    rsp = 'new response created'
    return Response(rsp, status=201, content_type="application/text")

# Get a comment
@application.route("/api/comments/<comment_id>", methods=["GET"])
def getCommentByID(comment_id):
    response = table.get_item(
        Key={
            'Comment_ID': comment_id
        }
    )
    item = response['Item']
    return Response(json.dumps(item), status=200, content_type="application/json")

# Get item by email
@application.route("/api/comments", methods=["GET"])
def getCommentByQuery():
    emailQuery = request.args.get('Email')
    tagQuery = request.args.get('Tag')

    if emailQuery:
        return Response(json.dumps(getCommentByEmail(emailQuery)), status=200, content_type="application/json")
    elif tagQuery:
        return Response(json.dumps(getCommentByTag(tagQuery)), status=200, content_type="application/json")
    else:
        res = 'Invalid query string'
        return Response(res, status=400, content_type="application/text")


def getCommentByEmail(email):
    template = {'Email': email}
    fe = ' AND '.join(['{0}=:{0}'.format(k) for k, v in template.items()])
    ea = {':{}'.format(k): v for k, v in template.items()}
    # fe = Attr('Tag').contains(['25'])
    print(ea)
    result = table.scan(FilterExpression=fe,
                        ExpressionAttributeValues=ea)
    return result

# Get item by tag
def getCommentByTag(tag):
        expressionAttributes = dict()
        expressionAttributes[":tvalue"] = tag
        filterExpression = "contains(Tags, :tvalue)"

        result = table.scan(FilterExpression=filterExpression,
                            ExpressionAttributeValues=expressionAttributes)
        print(result)
        return result

# Update existing comment
@application.route("/api/comments", methods=["PUT"])
def updateItem():
    data = json.loads(request.data.decode())
    try:
        table.update_item(
            Key={
                'Comment_ID': data['Comment_ID']
            },
            UpdateExpression='SET Version_ID = :val1, Comment_text = :val2, Tags = :val3',
            ExpressionAttributeValues={
                ':val1': data['Version_ID'],
                ':val2': data['Comment_text'],
                ':val3': data['Tags']
            },
            ConditionExpression='Version_ID = :val1'
        )
        rsp = 'Comment updated successfully.'
        return Response(rsp, status=200, content_type="application/text")
    except:
        rsp = 'Comment update failed.'
        return Response(rsp, status=400, content_type="application/text")

# Get responses for given ID
@application.route("/api/comments/<comment_id>/responses", methods=["GET"])
def getResponses(comment_id):
    response = table.get_item(
        Key={
            'Comment_ID': comment_id
        },
        AttributesToGet=['Responses']

    )
    item = response['Item']
    return Response(json.dumps(item), status=200, content_type="application/json")

# Create responses for given ID
@application.route("/api/comments/<comment_id>/responses", methods=["POST"])
def addResponse(comment_id):
    data = json.loads(request.data.decode())
    Key={
        'Comment_ID': comment_id
    }
    dt = datetime.now()
    dts = dt.strftime('%Y-%m-%d %H:%M:%S')

    full_rsp={
        'Email': data['Email'],
        'Datetime': dts,
        'Responses': data['Response'],
        'Response_ID': str(uuid.uuid4()),
        'Version_ID': str(uuid.uuid4())
    }
    UpdateExpression='SET Responses = list_append(Responses, :i)'
    ExpressionAttributeValues={
        ':i': [full_rsp]
    }
    ReturnValues='UPDATED_NEW'

    table.update_item(
        Key=Key,
        UpdateExpression=UpdateExpression,
        ExpressionAttributeValues=ExpressionAttributeValues,
        ReturnValues=ReturnValues
    )
    rsp = 'Response added successfully.'
    return Response(rsp, status=201, content_type="application/text")




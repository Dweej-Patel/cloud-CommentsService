import uuid
from app import application
import boto3
from flask import Flask, request
from datetime import datetime

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Instantiate a table resource object without actually
# creating a DynamoDB table. Note that the attributes of this table
# are lazy-loaded: a request is not made nor are the attribute
# values populated until the attributes
# on the table resource are accessed or its load() method is called.
table = dynamodb.Table('Comments')

# Print out some data about the table.us-
# This will cause a request to be made to DynamoDB and its attribute
# values will be set based on the response.
# print(table.creation_date_time)

# Add new comment to table
@application.route("/api/comments", methods=["POST"])
def createComment():
    data = request.json()
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

# Get a comment
@application.route("/api/comments/<comment-id>", methods=["GET"])
def getCommentByID(comment_id):
    response = table.get_item(
        Key={
            'Comment_ID': comment_id
        }
    )
    item = response['Item']
    print(item)

# Get item by email
@application.route("/api/comments", methods=["GET"])
def getCommentByEmailOrTag():
    query = request.query_string().decode()
    print(query)
    queryRequests = query.split('&')
    for item in queryRequests:
        label = item.split('=')
        if label[0] == 'Email':
            return getCommentByEmail(label[1])
        elif label[0] == 'Tags':
            return getCommentByTag(label[1])
        else:
            res = 'Invalid query string'
            return res


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

def updateItem(id, version_id, comment, tags):
    try:
        table.update_item(
            Key={
                'Comment_ID': id
            },
            UpdateExpression='SET Version_ID = :val1, Comment_text = :val2, Tags = :val3',
            ExpressionAttributeValues={
                ':val1': version_id,
                ':val2': comment,
                ':val3': tags
            },
            ConditionExpression='Version_ID = :val1'
        )
    except:
        print('Version ID did not match')

def getResponses(id):
    response = table.get_item(
        Key={
            'Comment_ID': id
        },
        AttributesToGet=['Responses']

    )
    item = response['Item']
    print(item)

def addResponse(comment_id, email, response):
    Key={
        'Comment_ID': comment_id
    }
    dt = datetime.now()
    dts = dt.strftime('%Y-%m-%d %H:%M:%S')

    full_rsp={
        'Email': email,
        'Datetime': dts,
        'Response': response,
        'Response_ID': str(uuid.uuid4()),
        'Version_ID': str(uuid.uuid4())
    }
    UpdateExpression='SET Responses = list_append(Responses, :i)'
    ExpressionAttributeValues={
        ':i': [full_rsp]
    }
    ReturnValues='UPDATED_NEW'

    res = table.update_item(
        Key=Key,
        UpdateExpression=UpdateExpression,
        ExpressionAttributeValues=ExpressionAttributeValues,
        ReturnValues=ReturnValues
    )
    return res


# getCommentByEmail('dweejuschrist@faith.church')
# updateItem('1', '2', 'Lorem Ipsum', ['Dweejus', 'Is', 'Our', 'Lord', 'And', 'Savior'])
# addResponse('1', 'johnson@murphy.com', 'This is the second response')
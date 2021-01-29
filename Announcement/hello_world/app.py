import json
import boto3
from flask_lambda import FlaskLambda
from flask import request


app1 = FlaskLambda(__name__)
ddb = boto3.resource('dynamodb')
table = ddb.Table('AnnouncementsTable')

@app1.route('/test', methods=['GET'])
def index():
    return json_response({"message": "Hello, world!"})

@app1.route('/announcements', methods=['GET', 'POST'])
def put_list_announcements():
    if request.method == 'GET':
        return json_response(table.scan()['Items'])
    else:
        return json_response({"message": "student entry created"})


def json_response(data, response_code=200):
    return json.dumps(data), response_code, {'Content-Type': 'application/json'}
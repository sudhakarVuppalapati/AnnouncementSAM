import json
import boto3
from flask_lambda import FlaskLambda
from flask import request


app1 = FlaskLambda(__name__)

@app1.route('/test', methods=['GET'])
def index():
    return json_response({"message": "Hello, world!"})

@app1.route('/announcements', methods=['GET', 'POST'])
def put_list_students():
    if request.method == 'GET':
        return json_response({"message": "Hello, world!2222"})
    else:
        return json_response({"message": "student entry created"})


def json_response(data, response_code=200):
    return json.dumps(data), response_code, {'Content-Type': 'application/json'}
import json
import boto3
from flask_lambda import FlaskLambda
from flask import request


app1 = FlaskLambda(__name__)
dynamodb = boto3.resource("dynamodb", region_name="us-west-1")
table = dynamodb.Table("Announcements")

@app1.route('/test', methods=['GET'])
def index():
    return json_response({"message": "Hello, world!"})

@app1.route('/announcements', methods=['GET', 'POST'])
def put_list_announcements():
    if request.method == 'GET':
        response = table.scan()
        data = response['Items']
        print(data)
        return json_response(data)
    else:
        print("request.data  : ", request.data)
        json_object = json.loads(request.data)
        print(json_object["title"])
        table.put_item( Item= {"title": json_object["title"],"description":json_object["description"],"date":json_object["date"]})
        return json_response({"message": "student entry created"})


def json_response(data, response_code=200):
    return json.dumps(data), response_code, {'Content-Type': 'application/json'}
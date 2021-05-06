import json
import boto3
from flask_lambda import FlaskLambda
from flask import request


app1 = FlaskLambda(__name__)
dynamodb = boto3.resource("dynamodb", region_name="us-west-1")
table = dynamodb.Table("Announcements")
clientSNS = boto3.client('sns')

@app1.route('/announcements', methods=['GET'])
def listAnnouncements():
    if request.method == 'GET':
        response = table.scan()
        data = response['Items']
        print(data)
        return json_response(data)

@app1.route('/announcements', methods=['POST'])
def putAnnouncements():
    print("request.data  : ", request.data)
    json_object = json.loads(request.data)
    print(json_object["title"])
    table.put_item( Item= {"title": json_object["title"],"description":json_object["description"],"date":json_object["date"]})
    response = clientSNS.publish( TopicArn="arn:aws:sns:us-west-1:774142313059:AnnouncementsTopic", Message=request.data,  Subject='test')
    return json_response({"message": "announcements entry created"})

def json_response(data, response_code=200):
    return json.dumps(data), response_code, {'Content-Type': 'application/json'}
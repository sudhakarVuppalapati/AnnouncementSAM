import json
import boto3
from flask_lambda import FlaskLambda
from flask import request


app1 = FlaskLambda(__name__)
dynamodb = boto3.resource("dynamodb", region_name="us-west-1")
client = boto3.client('ssm')
TableNameParameter  =  client.get_parameter(Name='TableName',  WithDecryption= False)
TableNamevalue = TableNameParameter.get("Parameter").get("Value")
print(TableNameParameter.get("Parameter").get("Value"))
TopicArnParameter =  client.get_parameter(Name='TopicArn',  WithDecryption= False)
TopicArnvalue = TopicArnParameter.get("Parameter").get("Value")
print(TopicArnParameter.get("Parameter").get("Value"))

table = dynamodb.Table(TableNamevalue)
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
    title = json_object["title"] 
    description = json_object["description"]
    if not  title.strip():
        return json_response({"message": "announcements title should not be empty"},400)
    if not  description.strip():
        return json_response({"message": "announcements description should not be empty"},400)    
    print(json_object["title"])
    dbResponse = table.put_item( Item= {"title":  title,"description": description,"date":json_object["date"]})
    dbreturn = dbResponse.get("ResponseMetadata").get("HTTPStatusCode")
    print(dbreturn)
    print( dbreturn == 200)
    if dbreturn != 200 :
        return json_response({"message": "please can you check with your data something went worng with DynamoDB insert data"},dbreturn) 
    response = clientSNS.publish( TopicArn=TopicArnvalue, Message=request.data,  Subject='test')
    return json_response({"message": "announcements entry created"})

def json_response(data, response_code=200):
    return json.dumps(data), response_code, {'Content-Type': 'application/json'}
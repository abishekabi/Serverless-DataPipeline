import json
import logging
import boto3


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    # TODO implement
    
    print("*****myLambdaFunction Invoked*******", event['Records'][0]['dynamodb']['Keys'])
    # Get the service resource
    sqs = boto3.resource('sqs')
    
    # Get the queue
    queue = sqs.get_queue_by_name(QueueName='mySQSQueue')
    
    # Create a new message
    response = queue.send_message(MessageBody=str(event['Records'][0]['dynamodb']['Keys']))
    
    print("******* sent message to SNQ *******")
    # return {
    #     'statusCode': 200,
    #     'body': event['Records'][0]['dynamodb']['Keys']
    # }

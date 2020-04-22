import json
import logging
import boto3


logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('comprehend')

from botocore.exceptions import ClientError


def upload_file(body, bucket, object_name=None):
    """write a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = "output"

    # write to file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.put_object(Body=body, Bucket=bucket, Key=object_name)
        #response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True



def lambda_handler(event, context):
    
    input_data = event['Records'][0]['body']
    print("*****Producer LambdaFunction Invoked*******", input_data)
    
    input_string = eval(input_data)['name']['S']
    
    response = client.detect_sentiment(
        Text= input_string,
        LanguageCode='en'
    )
    
    response = [ {"Input String": input_string}, response ]
    print("*************AWS Comprehend Sentimental Analysis*********** ", response)
    
    # Perform the transfer
    # s3 = boto3.client('s3')
    # s3.upload_file('FILE_NAME', 'sentiment-analysis-out', 'OBJECT_NAME', Config=config)
    
    result = upload_file(str(response), 'sentiment-analysis-out', object_name="sentiment-output.txt")
    if(result == True):
        print("S3 write Success!")
    else:
        print("S3 write Failed!")
    
    # return {
    #     'statusCode': 200,
    #     'body': json.dumps('Hello from Lambda!')
    # }

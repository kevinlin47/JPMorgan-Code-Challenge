"""
This Code will be executed from AWS Lambda
When an object create event occurs from S3
Database is to be updated with the new data
provided from the data providers.
"""
import json
import urllib.parse
import boto3

s3 = boto3.client('s3')

def lambda_handler(event, context):
    print("Received event: " + event['Records'][0]['eventName'])
    print("Event receieved at: " + event['Records'][0]['eventTime'])

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    print("Object Key: " + key)

    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        print("CONTENT TYPE: " + response['ContentType'])
        return response['ContentType']
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
"""
This Code will be executed from AWS Lambda
When a object create event occurs from S3
Database is to be updated with the new data
provided from the data providers.
"""

def lambda_hander(Event, Context):
    #TODO
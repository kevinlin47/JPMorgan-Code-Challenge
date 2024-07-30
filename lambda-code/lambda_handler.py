"""
This Code will be executed from AWS Lambda
When an object create event occurs from S3
Database is to be updated with the new data
provided from the data providers.
"""
import json
import urllib.parse
import boto3

s3 = boto3.resource('s3')
dynamodb = boto3.client("dynamodb")

def lambda_handler(event, context):
    print("Received event: " + event['Records'][0]['eventName'])
    print("Event receieved at: " + event['Records'][0]['eventTime'])

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    print("Object Key: " + key)

    try:
        response = s3.Bucket(bucket).Object(key)
       
        movie_data = response.get()['Body'].read().decode('utf-8')
        json_data = json.loads(movie_data)

        # Cast and Genres will be stored as a List of Strings
        cast_members = []
        genres = []

        for cast in json_data[0]["cast"]:
          cast_members.append({"S": cast})

        for genre in json_data[0]["genres"]:
          genres.append({"S": genre})
        
        movie = {
          "Title"           : {'S': json_data[0]["title"]},
          "Year"            : {'N': str(json_data[0]["year"])},
          "Cast"            : {'L': cast_members},
          "Genres"          : {'L': genres},
          "Href"            : {'S': json_data[0]["href"]},
          "Extract"         : {'S': json_data[0]["extract"]},
          "Thumbnail"       : {'S': json_data[0]["thumbnail"]},
          "Thumbnail_width" : {'N': str(json_data[0]["thumbnail_width"])},
          "Thumbnail_height": {'N': str(json_data[0]["thumbnail_height"])}
        }

        print("The following movie data will be put into the database\n")
        print(movie)
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
    
    try:
      # If a movie with the given name already exists, it will be updated
      print("Executing database put_item\n")
      
      response = dynamodb.put_item(TableName='Movies', Item=movie, ReturnValues="ALL_OLD")

      if "Attributes" in response:
        print("Existing data for movie {} has been updated\n".format(json_data[0]["title"]))
        print("Old Attribute Values:\n")
        print(response["Attributes"])
      else:
        print("New movie {} has been added to the table {}".format(json_data[0]["title"], "Movies"))

    except Exception as e:
      print(e)
      print("Error when putting item into Table Movies")
      raise e
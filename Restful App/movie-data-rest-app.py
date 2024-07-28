"""
REST API Application for querying
movie data set
"""
from fastapi import FastAPI, HTTPException

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger(__name__)

class DynamoDB:
    def __init__(self, dyn_resource):
        """
        :param dyn_resource: A Boto3 DynamoDB resource.
        """
        self.dyn_resource = dyn_resource
        # The table variable is set during the scenario in the call to
        # 'exists' if the table exists. Otherwise, it is set by 'create_table'.
        self.table = None

    def exists(self, table_name):
        """
        Determines whether a table exists. As a side effect, stores the table in
        a member variable.

        :param table_name: The name of the table to check.
        :return: True when the table exists; otherwise, False.
        """
        try:
            table = self.dyn_resource.Table(table_name)
            table.load()
            exists = True
        except ClientError as err:
            if err.response["Error"]["Code"] == "ResourceNotFoundException":
                exists = False
            else:
                logger.error(
                    "Couldn't check for existence of %s. Here's why: %s: %s",
                    table_name,
                    err.response["Error"]["Code"],
                    err.response["Error"]["Message"],
                )
                raise
        else:
            self.table = table
        return exists

    def get_movie_by_title(self, title):
        """
        Gets movie data from the table for a specific movie.

        :param title: The title of the movie.
        :return: The data about the requested movie.
        """
        try:
            response = self.table.get_item(Key={"Title": title})
        except ClientError as err:
            logger.error(
                "Couldn't get movie %s from table %s. Here's why: %s: %s",
                title,
                self.table.name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:
            if "Item" in response:
                return response["Item"]
            else:
                raise HTTPException(status_code=404, detail="No movie found with the given movie_name")

def get_db_client():
    dyn_resource = boto3.resource("dynamodb")
    data_base = DynamoDB(dyn_resource)
    data_base.exists("Movies")

    return data_base

data_base = get_db_client()
app = FastAPI()

@app.get("/")
def root():
    return {"Movie Data Query":"RestAPI Application",
            "API Documentation found at endpoint" : "/docs#/"
    }

"""
Query movie database
Data can be queried by year, movie name, genre, or cast member
"""
@app.get("/movies/")
def get_movies(year: int  | None  = None, movie_name: str | None = None, cast_member: str | None = None, genre: str | None = None):
    if  year == None and movie_name == None and cast_member == None and genre == None:
        return {
            "message":     "No query parameters were given or parameter is invalid",
            "status_code": 200
        }
    
    if movie_name != None:
         # Gets movie data from the table for a specific movie.
         return data_base.get_movie_by_title(movie_name)
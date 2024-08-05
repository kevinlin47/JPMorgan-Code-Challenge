"""
REST API Application for querying
movie data set
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import boto3
from amazondax import AmazonDaxClient
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger(__name__)

class Message(BaseModel):
    message: str

class DynamoDB:
    def __init__(self, dyn_resource):
        """
        :param dyn_resource: A Boto3 DynamoDB resource.
        """
        self.dyn_resource = dyn_resource
        # The table variable is set during the scenario in the call to
        # 'exists' if the table exists.
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

    def set_dax_cache(self, dyn_dax_resource):
        """
        Configures DynamoDB resource to use DAX

        :param dyn_dax_resource: A DynamoDB Dax resource.
        :return: True when connection to DAX cluster is succesful; otherwise False
        """
        try:
            if self.table is None:
                logger.error(
                    "Table member variable has not been set yet"
                )
                return False
            
            table_name = self.table.table_name
            self.dyn_resource = dyn_dax_resource
            self.table = self.dyn_resource.Table(table_name)
            return True
        except ClientError as err:
            logger.error(
                    "%s: %s",
                    err.response["Error"]["Code"],
                    err.response["Error"]["Message"],
            )
            raise
            

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
                return JSONResponse(status_code=404, content={"message": "No movie found with the given movie_name=" + title})
    
    def get_movies_by_year(self, year):
        """
        Get movies from the table that match the given year

        :param year: The year the movie was released
        :return: Movie objects mathcing the requested year
        """
        try: 
            response = self.table.query(
                IndexName="Year-index",
                KeyConditionExpression=Key("Year").eq(year))
        except ClientError as err:
            logger.error(
                "Couldn't query for movies released in %s. Here's why: %s: %s",
                year,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:
            if response["Items"]:
                return response["Items"]
            else:
                return JSONResponse(status_code=404, content={"message": "No movie found with the given year=" + str(year)})

    def get_movies_by_cast_member(self, cast_member):
        """
        Get movies from the table that match the requested cast member

        :param cast_member: name of the cast member 
        :return: Movie objects mathcing the requested cast_member
        """
        movies = []
        scan_kwargs = {
                "FilterExpression": "contains(#Cast, :val)",
                "ExpressionAttributeNames": {
                    "#Cast": "Cast"
                },
                "ExpressionAttributeValues": {
                    ":val": cast_member
                }
            }
        try:
            done = False
            start_key = None
            while not done:
                if start_key:
                    scan_kwargs["ExclusiveStartKey"] = start_key

                response = self.table.scan(**scan_kwargs)
                movies.extend(response.get("Items", []))
                start_key = response.get("LastEvaluatedKey", None)
                done = start_key is None
        except ClientError as err:
            logger.error(
                "Couldn't scan for movies. Here's why: %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:
            if movies:
                return movies
            else:
                return JSONResponse(status_code=404, content={"message": "No movie found with the given cast_member=" + cast_member})
    
    def get_movies_by_genre(self, genre):
        """
        Get movies from the table that match the requested genre

        :param genre: movie genre
        :return: Movie objects mathcing the requested genre
        """
        movies = []
        scan_kwargs = {
                "FilterExpression": "contains(Genres, :val)",
                "ExpressionAttributeValues": {
                    ":val": genre
                }
            }
        try:
            done = False
            start_key = None
            while not done:
                if start_key:
                    scan_kwargs["ExclusiveStartKey"] = start_key

                response = self.table.scan(**scan_kwargs)
                movies.extend(response.get("Items", []))
                start_key = response.get("LastEvaluatedKey", None)
                done = start_key is None
        except ClientError as err:
            logger.error(
                "Couldn't scan for movies. Here's why: %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:
            if movies:
                return movies
            else:
                return JSONResponse(status_code=404, content={"message": "No movie found with the given genre=" + genre})

def get_db_client():
    dyn_resource = boto3.resource("dynamodb")
    data_base = DynamoDB(dyn_resource)
    data_base.exists("Movies")

    dyn_dax_resource  = AmazonDaxClient.resource(
    endpoint_url='dax://dax-movie-cluster-2.4tcfh6.dax-clusters.us-east-1.amazonaws.com')
    data_base.set_dax_cache(dyn_dax_resource)

    return data_base

def get_parameter_error_response(parameter):
        raise HTTPException(status_code=422, detail="No query parameter " + parameter + " was given or parameter is invalid")

data_base = get_db_client()
app = FastAPI()

@app.get("/")
def root():
    return {"Movie Data Query":"RestAPI Application",
            "API Documentation found at endpoint" : "/docs#/"
    }

@app.get("/healthcheck")
def health_check():
    return {
        "Health Check": "Passed"
    }

@app.get("/readiness")
def readiness_check():
    return data_base.get_movie_by_title("Venom")

"""
Query movie database by movie name
"""
@app.get("/movies/title/", responses={404: {"model": Message}})
def get_movies_by_title(movie_name: str | None = None):
    if  movie_name == None or movie_name == "":
        return get_parameter_error_response("movie_name")
    
    return data_base.get_movie_by_title(movie_name)

"""
Query movie database by year
"""
@app.get("/movies/year/", responses={404: {"model": Message}})
def get_movies_by_year(year: int | None = None):
    if year == None:
        return get_parameter_error_response("year")

    return data_base.get_movies_by_year(year)

"""
Query movie database by cast member
"""
@app.get("/movies/cast/", responses={404: {"model": Message}})
def get_movies_by_cast_member(cast_member: str | None = None):
    if cast_member == None or cast_member == "":
        return get_parameter_error_response("cast_member")
    
    return data_base.get_movies_by_cast_member(cast_member)

"""
Query movie database by genre
"""
@app.get("/movies/genre/", responses={404: {"model": Message}})
def get_movies_by_genre(genre: str | None = None):
    if genre == None or genre == "":
        return get_parameter_error_response("genre")

    return data_base.get_movies_by_genre(genre)
FROM python:3.10

WORKDIR /code

COPY App/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r /code/requirements.txt

COPY ./App /code/App

CMD ["fastapi", "run", "App/movie-data-rest-app.py", "--port", "80"]
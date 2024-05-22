# Notes

Notes is a Flask application that enables users to store, retrieve, update and delete their notes using a simple API. The notes are stored in a database and consist of a title and a body. Each note is associated with an owner that created the note and is allowed to view, modify, and delete it.

## Development and testing

The development and testing can be done from within the virtual environment with installed requirements.

### Create and activate virtual environment

```sh
python3 -m venv .venv
source .venv/bin/activate
```

### Install requirements

```sh
pip3 install -r requirements.txt
```

### Run tests

```sh
python3 -m pytest
```

### Run flask development server

```sh
flask --app 'app:create_app("development")' run
```

## Production deployment

Production deployment can utilize the provided Dockerfile that runs the Notes app using the gunicorn WSGI server. Before running, the `SECRET_KEY` and `DATABASE_URI` environmental variables should be defined e.g. in a `.env` file.

### Build docker image

```sh
docker build -t notes-image .
```

### Run image

```sh
docker run --env-file=.env -d -p 8000:8000 notes-image
```

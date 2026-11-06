FROM python:3

WORKDIR /usr/src/notes-flask-app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY app ./app
COPY migrations ./migrations
COPY config.py .
COPY docker-entrypoint.sh .

ENV FLASK_APP="app:create_app(\"production\")"

RUN chmod +x docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]

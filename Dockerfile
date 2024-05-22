FROM python:3

WORKDIR /usr/src/notes-flask-app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY app ./app
COPY config.py .

CMD [ "gunicorn", "-b", "0.0.0.0", "app:create_app(\"production\")" ]

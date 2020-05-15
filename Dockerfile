FROM python:3.8-alpine

RUN adduser -D raven

WORKDIR /home/ravenraffle

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

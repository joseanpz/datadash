FROM python:3.6-alpine3.8

# FROM tiangolo/uvicorn-gunicorn:python3.6-alpine3.8

# LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"

COPY requirements.txt /tmp
RUN apk add --no-cache --virtual .build-deps libffi-dev gcc libc-dev make \
    && pip install -r /tmp/requirements.txt \
    && apk del .build-deps gcc libc-dev make
    # && apk add --no-cache pkgconfig python3-dev openssl-dev libffi-dev musl-dev make gcc

#COPY Pipfile* /tmp
#RUN cd /tmp && pipenv lock --requirements > requirements.txt
RUN ls -la




COPY start.sh /start.sh
RUN chmod +x /start.sh

COPY gunicorn_conf.py /gunicorn_conf.py

COPY start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

RUN ls -la
COPY app /app/app
WORKDIR /app/
RUN touch __init__.py
RUN pwd && ls -la

ENV PYTHONPATH=/usr

EXPOSE 80

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn
CMD ["/start.sh"]

# FROM tiangolo/uvicorn-gunicorn:python3.7

# LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"

# RUN pip install fastapi

# COPY ./app /app

# FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
#
#RUN pip install
#celery~=4.3
#passlib[bcrypt]
#tenacity
#requests
#emails
#"fastapi>=0.47.0"
#"uvicorn>=0.11.1"
#gunicorn
#pyjwt
#python-multipart
#email_validator
#jinja2
#psycopg2-binary
#alembic
#SQLAlchemy

# For development, Jupyter remote kernel, Hydrogen
# Using inside the container:
# jupyter lab --ip=0.0.0.0 --allow-root --NotebookApp.custom_display_url=http://127.0.0.1:8888
#ARG env=prod
#RUN bash -c "if [ $env == 'dev' ] ; then pip install jupyterlab ; fi"
#EXPOSE 8888

#COPY ./app /app
#WORKDIR /app/
#
#ENV PYTHONPATH=/app
#
#EXPOSE 80
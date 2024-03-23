FROM python:3
RUN apt-get update
RUN apt-get -y install libldap2-dev libsasl2-dev
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r /code/requirements.txt
COPY . /code/


## Installiere automatisch fork von Django-oauth-toolkit https://github.com/RitchiS99/django-oauth-toolkit
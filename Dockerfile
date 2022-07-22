FROM python:3
RUN apt-get update
RUN apt-get -y install libldap2-dev libsasl2-dev
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
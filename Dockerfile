# pull official base image
FROM python:3.8-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
  apt-get install -y \
    netcat sox flite

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
RUN pip install git+https://github.com/sacovo/feincms3-meta.git@7be48fee3cbc3b11b3e05723fa3e7e59d9ec92e4 --upgrade

# copy project
COPY . /usr/src/app/

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

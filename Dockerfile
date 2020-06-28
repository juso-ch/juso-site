# pull official base image
FROM python:3.8-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
  apt-get install -y \
    netcat

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
RUN pip install git+https://github.com/sacovo/feincms3-meta.git@5e02cb1576485d5f87ee3d51cdb254c1a6e6050c --upgrade

# copy project
COPY . /usr/src/app/

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

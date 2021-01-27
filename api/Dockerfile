# Dockerfile
# pull official base image
FROM python:3.9-slim

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install gcc -y
RUN apt-get install musl-dev -y
RUN apt-get install wget -y


# install dependencies
RUN pip install --upgrade pip
RUN pip install Django
RUN pip install django-cors-headers
# RUN pip install -r requirements.txt

RUN pip install requests
RUN pip install clickhouse-driver
RUN pip install asyncio
RUN pip install pymongo
RUN pip install pandas
RUN pip install paramiko
# copy project
# RUN wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1SEDg_HJRCUarff1YMRXCHjv7mJhdrXFy' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1SEDg_HJRCUarff1YMRXCHjv7mJhdrXFy" -O /usr/src/app/dataset.csv && rm -rf /tmp/cookies.txt
COPY . .
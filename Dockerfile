FROM python:3.10

ADD . /opt/konnsearch
WORKDIR /opt/konnsearch

RUN pip install .

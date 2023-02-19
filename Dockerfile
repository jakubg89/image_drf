FROM python:3.10

RUN pip install -U pip && apt-get update

WORKDIR /api/
COPY requirements.txt /api/
RUN pip install -r requirements.txt

COPY . /api

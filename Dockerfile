FROM python:3.9
WORKDIR /api
COPY requirements.txt /api/
RUN pip install -r requirements.txt
COPY . /api

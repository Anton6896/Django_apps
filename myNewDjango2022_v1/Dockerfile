FROM python:3

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN mkdir -p /opt/app
WORKDIR /opt/app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

ADD ./core .
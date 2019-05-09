FROM python:3-alpine

RUN apk update && apk add py3-pip
RUN pip install pika --upgrade

WORKDIR /
RUN mkdir orquestrator

WORKDIR orquestrator
COPY orquestrator/. .

CMD python queue_worker.py

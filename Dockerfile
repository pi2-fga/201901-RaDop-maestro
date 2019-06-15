FROM python:3-alpine

WORKDIR /app

RUN apk update && apk add --no-cache py3-pip
# RUN pip install pika --upgrade

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src/ /app/

CMD python3 main.py

FROM python:3.8.13-slim-bullseye

LABEL maintener="Michael Loukeris"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER=1


RUN apt-get update && apt-get -y upgrade && apt-get install -y nano

COPY ./requirements.txt ./requirements.txt

RUN set -eux \
 && pip install --no-cache-dir --user --upgrade pip \
 && pip install --no-cache-dir --user -r requirements.txt

RUN mkdir /code

WORKDIR /code

COPY . .

CMD [ "python", "consumer.py" ]

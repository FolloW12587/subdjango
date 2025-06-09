# FROM python:3.10
FROM python:3.10.0-alpine

RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    python3-dev \
    build-base

WORKDIR /app

# EXPOSE 8000


COPY requirements.txt requirements.txt

RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt

COPY . .
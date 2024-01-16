FROM arm64v8/python:3.10-alpine3.15

ENV APP_PATH /app

RUN apk update \
    && apk add --no-cache bash
#        curl \
#        wget \
#        build-base \
#        git \
#        openssh-client \
#        libffi-dev \
#        zip \
#        unzip \
#        ca-certificates \
#        openblas-dev

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install --system --deploy

RUN mkdir -p ${APP_PATH}

WORKDIR ${APP_PATH}
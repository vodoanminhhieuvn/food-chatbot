FROM python:3.8.13-bullseye AS BASE

RUN apt-get update \
  && apt-get --assume-yes --no-install-recommends install \
  build-essential \
  curl \
  git \
  jq \
  libgomp1 \
  vim

WORKDIR /app

# upgrade pip version
RUN pip3 install --no-cache-dir --upgrade pip

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

ADD config.yml config.yml
ADD domain.yml domain.yml
ADD credentials.yml credentials.yml
ADD endpoints.yml endpoints.yml
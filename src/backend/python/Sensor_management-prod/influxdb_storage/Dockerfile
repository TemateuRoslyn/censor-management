FROM python:3.8.10 AS build

# app building
WORKDIR /app

# outils pour kafka (ajouter)
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get -y upgrade
RUN apt-get -y install wget
RUN wget https://github.com/edenhill/librdkafka/archive/v1.2.0.tar.gz && tar xvzf v1.2.0.tar.gz && cd librdkafka-1.2.0/ && ./configure && make && make install && ldconfig


COPY ./ressources/requirements.txt /app/
RUN python -m venv venv
RUN /app/venv/bin/pip install -r requirements.txt

FROM build

# arguments
ARG DEBUG
ARG HOST
ARG PORT

# env variables
ENV debug $DEBUG
ENV host $HOST
ENV port $PORT

# app source code copiying
COPY ./src/ /app

# run the app
EXPOSE 5004
CMD ["/app/venv/bin/python", "app.py"]






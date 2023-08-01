FROM python:3.8.10 AS build

# app building...
WORKDIR /app
COPY ./requirements.txt /app/
RUN python -m venv venv
RUN /app/venv/bin/pip install -r requirements.txt

FROM build

# arguments
ARG DEBUG
ARG HOST
ARG PORT
ARG API_ADDR

# env variables
ENV debug $DEBUG
ENV host $HOST
ENV port $PORT
ENV api_addr $API_ADDR

# copiying app sources
COPY ./src/ /app

# run
EXPOSE 8085
CMD ["/app/venv/bin/python", "app.py"]
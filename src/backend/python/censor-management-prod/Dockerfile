FROM python:3.8.10 AS build

# app building
WORKDIR /app
COPY ./requirements.txt /app/
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
EXPOSE 8000
CMD ["/app/venv/bin/python", "app.py"]
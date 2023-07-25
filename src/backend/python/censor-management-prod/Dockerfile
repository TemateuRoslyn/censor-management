FROM python:3.8.10 AS build

# app building
WORKDIR /app
COPY ./requirements.txt /app/
RUN python -m venv venv
RUN /app/venv/bin/pip install -r requirements.txt

FROM build

# env variables
ENV debug false
ENV host 127.0.0.1
ENV port 8000

# app source code copiying
COPY ./src/ /app

# run the app
EXPOSE 8000
CMD ["/app/venv/bin/python", "app.py"]
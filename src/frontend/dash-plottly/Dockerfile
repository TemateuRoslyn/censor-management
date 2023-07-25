FROM python:3.8.10 AS build

# app building...
WORKDIR /app
COPY ./requirements.txt /app/
RUN python -m venv venv
RUN /app/venv/bin/pip install -r requirements.txt

FROM build

# env variables
ENV debug false
ENV host 0.0.0.0
ENV port 8085
ENV api_addr 127.0.0.1:8000

# copiying app sources
COPY ./src/ /app

# run
EXPOSE 8085
CMD ["/app/venv/bin/python", "app.py"]
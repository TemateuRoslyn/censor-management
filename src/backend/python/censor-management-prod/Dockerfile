FROM python:3.10 as dev

WORKDIR /work

FROM dev as runtime
WORKDIR /app

COPY ./requirements.txt /app/
RUN pip install -r /app/requirements.txt

COPY ./src/ /app/
ENV FLASK_APP=app.py

CMD flask run -h 0.0.0 -p 5004
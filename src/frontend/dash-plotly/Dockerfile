FROM python:3.10 AS build

ENV DASH_DEBUG_MODE True
WORKDIR /
# COPY ./requirements.txt /app/
RUN set -ex && \
    pip install -r requirements.txt

FROM python:3.10

WORKDIR /
# COPY ./app /app

EXPOSE 4000

CMD ["python", "src/app/app.py"]
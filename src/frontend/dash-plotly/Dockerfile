FROM python:3.10 AS dev

WORKDIR /

ENV DASH_DEBUG_MODE True

FROM python:3.10

COPY ./requirements.txt /
RUN pip install -r /requirements.txt

COPY ./src /app/

EXPOSE 8085

CMD ["python", "app/run.py"]
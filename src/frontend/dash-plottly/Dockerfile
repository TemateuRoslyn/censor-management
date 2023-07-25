FROM python:3.10 AS build

WORKDIR /app
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

FROM build

COPY ./src/ /app
EXPOSE 8085
CMD ["python", "app.py"]
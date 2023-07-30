#!/bin/sh

cd ./../../../../src/backend/python/Sensor_management-prod/influxdb_storage
docker build -t dscdatasmart/api_influxdb:latest .


# docker tag fcf0d9be9aa5 localhost:32000/censor-backend:latest
# docker push localhost:32000/censor-backend 


#!/bin/sh

cd ./../../../../src/backend/python/Sensor_management-prod/mongodb_storage
docker build -t dscdatasmart/api_mongodb:latest .


# docker tag fcf0d9be9aa5 localhost:32000/censor-backend:latest
# docker push localhost:32000/censor-backend 


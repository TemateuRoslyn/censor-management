#!/bin/sh

cd ./../../../../src/backend/python/Sensor_management-prod/usb_storage
docker build -t dscdatasmart/api_usb:latest .


# docker tag fcf0d9be9aa5 localhost:32000/censor-backend:latest
# docker push localhost:32000/censor-backend 


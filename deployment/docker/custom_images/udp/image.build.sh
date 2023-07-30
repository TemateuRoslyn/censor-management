#!/bin/sh

cd ./../../../../src/backend/python/Sensor_management-prod/udp_packets
docker build -t dscdatasmart/api_udp:latest .


# docker tag fcf0d9be9aa5 localhost:32000/censor-backend:latest
# docker push localhost:32000/censor-backend 


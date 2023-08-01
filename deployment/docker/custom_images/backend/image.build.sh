#!/bin/sh

cd ./../../../../src/backend/python/censor-management-prod
docker build -t dscdatasmart/censor-backend:latest .


# docker tag fcf0d9be9aa5 localhost:32000/censor-backend:latest
# docker push localhost:32000/censor-backend 


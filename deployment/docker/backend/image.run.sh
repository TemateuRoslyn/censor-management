#!/bin/sh

cd ./../../../src/backend/python/censor-management-prod
docker build -t softmaes/censor-backend:latest .

cd ./app

docker build . -t merritz-app
docker run -it -p 5004:5004 merritz-app
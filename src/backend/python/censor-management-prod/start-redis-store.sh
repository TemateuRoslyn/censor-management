
# remember to update above in configs!

# docker network create redis

cd ./storage/

# docker run -d --name redis-stack -p 6379:6379 redis/redis-stack-server:latest


#redis-0
docker run -d --rm --name redis-0 -v ${PWD}/redis-0:/etc/redis/ redis redis-server /etc/redis/redis.conf
docker exec -it redis-0 redis-cli


# #redis-1
# docker run -d --rm --name redis-1 -v ${PWD}/redis-1:/etc/redis/ redis redis-server /etc/redis/redis.conf

# #redis-2
# docker run -d --rm --name redis-2 -v ${PWD}/redis-2:/etc/redis/ redis redis-server /etc/redis/redis.conf

# # sentinel-0
# docker run -d --rm --name sentinel-0 -v ${PWD}/sentinel-0:/etc/redis/ redis redis-server /etc/redis/sentinel.conf --sentinel

# # sentinel-1
# docker run -d --rm --name sentinel-1 -v ${PWD}/sentinel-1:/etc/redis/ redis redis-sentinel /etc/redis/sentinel.conf

# # sentinel-2
# docker run -d --rm --name sentinel-2 -v ${PWD}/sentinel-2:/etc/redis/ redis redis-sentinel /etc/redis/sentinel.conf
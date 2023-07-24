# models/accelerometre1.py

import redis,json,random

liste = [94016, 80014, 60659, 10011]

redis_cli = redis.Redis(host='redis',port=6379)


class Accelerometre1:
    def __init__(self):
        self.humidity = 0
        self.listTime = 0
        self.temperature = 0
        self.time = 0

    def set_next(self):
        self.time += 1
        self.listTime = self.time
        self.temperature = random.uniform(-5,100)
        self.humidity = random.uniform(-5,100)
        redis_cli.rpush('temperatures',self.temperature)
        redis_cli.rpush('humidity',self.humidity)
        redis_cli.rpush('time',self.time)
        return True

    def get_next(self,cycle):
        length = len(redis_cli.lrange('temperatures',0,-1))
        if length < 101:
            temps_bytes = redis_cli.lrange('temperatures',0,(length -1))
            postal_codes_bytes = redis_cli.lrange('humidity',0,(length -1))
            times_bytes = redis_cli.lrange('time',0,(length -1))
            return {
                    "temperature": list(map(lambda x:json.loads(x),temps_bytes)), 
                    "time": list(map(lambda x:json.loads(x),times_bytes)), 
                    "humidity":list(map(lambda x:json.loads(x),postal_codes_bytes))
                }
        else:
            temps_bytes = redis_cli.lrange('temperatures',(length -100),(length -1))
            postal_codes_bytes = redis_cli.lrange('humidity',(length -100),(length -1))
            times_bytes = redis_cli.lrange('time',(length -100),(length -1))
            return {
                    "temperature": list(map(lambda x:json.loads(x),temps_bytes)), 
                    "time": list(map(lambda x:json.loads(x),times_bytes)), 
                    "humidity":list(map(lambda x:json.loads(x),postal_codes_bytes))
                }

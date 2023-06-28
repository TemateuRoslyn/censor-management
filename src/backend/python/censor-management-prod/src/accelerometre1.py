# models/accelerometre1.py

import redis,json,random

liste = [94016, 80014, 60659, 10011]

redis_cli = redis.Redis(host='172.17.0.2',port=6379)


class Accelerometre1:
    def __init__(self):
        self.postal_codes = 0
        self.temperature = 0
        self.time = 0

    def set_next(self):
        self.time += 1
        self.postal_codes = liste[random.randint(0,(len(liste)-1))]
        self.temperature = random.uniform(-5,100)
        redis_cli.rpush('temperatures',self.temperature)
        redis_cli.rpush('postal_codes',self.postal_codes)
        redis_cli.rpush('time',self.time)
        return True

    def get_next(self):
        length = len(redis_cli.lrange('temperatures',0,-1))
        if length < 101:
            temps_bytes = redis_cli.lrange('temperatures',0,(length -1))
            postal_codes_bytes = redis_cli.lrange('postal_codes',0,(length -1))
            times_bytes = redis_cli.lrange('time',0,(length -1))
            return {
                    "temperature": list(map(lambda x:json.loads(x),temps_bytes)), 
                    "time": list(map(lambda x:json.loads(x),times_bytes)), 
                    "code":list(map(lambda x:json.loads(x),postal_codes_bytes))
                }
        else:
            temps_bytes = redis_cli.lrange('temperatures',(length -100),(length -1))
            postal_codes_bytes = redis_cli.lrange('postal_codes',(length -100),(length -1))
            times_bytes = redis_cli.lrange('time',(length -100),(length -1))
            return {
                    "temperature": list(map(lambda x:json.loads(x),temps_bytes)), 
                    "time": list(map(lambda x:json.loads(x),times_bytes)), 
                    "code":list(map(lambda x:json.loads(x),postal_codes_bytes))
                }

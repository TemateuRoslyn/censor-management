# models/accelerometre1.py

import json,random, math as m



class Accelerometre1:
    def __init__(self):
        self.humidity = []
        self.temperature = []
        self.time = 0
        self.listTime = []

    def set_next(self):
        self.time += 1
        self.listTime.append(self.time)
        self.humidity.append(random.uniform(-5,100))
        self.temperature.append(random.uniform(-5,100))
        return True

    def get_next(self,cycle:float):
        length = len(self.listTime)
        cycle = m.floor(cycle*length/100)
        print(cycle)
        if length < cycle:
            temps_bytes = range(0,(length -1))
            humidity_bytes = range(0,(length -1))
            times_bytes = range(0,(length -1))
            return {
                    "temperatures": list(map(lambda x:self.temperature[x],temps_bytes)), 
                    "humidites":list(map(lambda x:self.humidity[x],humidity_bytes)),
                    "times": list(map(lambda x:self.listTime[x],times_bytes)), 
                }
        else:
            temps_bytes = range(abs((length -cycle)),(length -1))
            humidity_bytes = range(abs((length -cycle)),(length -1))
            times_bytes = range(abs((length -cycle)),(length -1))
            return {
                    "temperatures": list(map(lambda x:self.temperature[x],temps_bytes)), 
                    "humidites":list(map(lambda x:self.humidity[x],humidity_bytes)),
                    "times": list(map(lambda x:self.listTime[x],times_bytes)), 
                }
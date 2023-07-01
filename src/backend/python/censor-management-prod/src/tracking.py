# models/accelerometre1.py

import json,random, math as m, geopy



class Tracker:
    def __init__(self):
        self.city = []
        self.lat = []
        self.lon = []
        self.state = []

    def set_next(self,city, state, lat, lon):
        self.city.append(city)
        self.state.append(state)
        self.lat.append(float(lat) + random.uniform(0.000122,0.000889))
        self.lon.append(float(lon) + random.uniform(0.000122,0.000889))

    def get_next(self):
        return {
                "city": list(self.city), 
                "state":list(self.state),
                "lat": list(self.lat), 
                "lon": list(self.lon), 
            }
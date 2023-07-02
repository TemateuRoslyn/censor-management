# models/accelerometre1.py

import random


class Accelerometre2:
    def __init__(self):
        self.postal_codes = [94016, 80014, 60659, 10011]
        self.current_temp = 50
        self.max_temp = 100
        self.min_temp = 0
        self.nom_capteur = "Accelerometre No 2"

    def get_next(self):
        if random.random() >= 0.5:
            if self.current_temp + 1 <= self.max_temp:
                self.current_temp += 1
        elif self.current_temp - 1 >= self.min_temp:
            self.current_temp -= 1
        return {
            "postal_code": self.postal_codes[0],
            "capteur_name": self.nom_capteur,
            "time ": self.current_temp,
        }

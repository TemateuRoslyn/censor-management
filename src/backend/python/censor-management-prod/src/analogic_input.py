import random


class AnalogicInput:
    def __init__(self) -> None:
        self.taille = 1

    def get_value(self):
        etats = [random.choice([True, False]) for _ in range(self.taille)]
        etat = random.choice(etats)
        valeur = random.uniform(0, 10)

        return {
            "etat": etat,
            "valeur": round(0 if etat == False else valeur, 2),
        }

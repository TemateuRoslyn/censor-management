import pandas as pd

"""Je crée ici un petit DataFrame que je vais afficher dans le tableau"""
datas = {
    "ID": [0, 1, 2, 3, 4],
    "Capteur": ["Capteur 0", "Capteur 1", "Capteur 2", "Capteur 3", "Capteur 4"],
    "Unité": ["C/M", "KG", "M", "C", "M"],
    "Valeur": [10, 2, 0.5, 4, 6],
}

data_frame = pd.DataFrame(datas)

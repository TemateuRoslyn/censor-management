import pandas as pd

"""Je crée ici un petit DataFrame que je vais afficher dans le tableau"""
datas = {
    "ID": [0, 1, 2, 3, 4],
    "Capteur": ["Capteur 0", "Capteur 1", "Capteur 2", "Capteur 3", "Capteur 4"],
    "Unité": ["C/M", "KG", "M", "C", "M"],
    "Valeur": [10, 2, 0.5, 4, 6],
}

data_frame = pd.DataFrame(datas)

""" Un petit DataFrame pour la liste des enregistrements"""

datas_enregistrement = {
    "ID": [000, 1, 2, 3, 4, 5, 6],
    "Capteur": [
        "Capteur 1",
        "Entrée analogique 0",
        "Entrée analogique 1",
        "Entrée analogique 2",
        "Entrée analogique 0",
        "Entrée analogique 1",
        "Entrée analogique 2",
    ],
    "Début": [
        "06/06/2021",
        "07/07/2021",
        "06/06/2021",
        "07/07/2021",
        "07/07/2021",
        "06/06/2021",
        "07/07/2021",
    ],
    "Fin": [
        "06/06/2021",
        "07/07/2021",
        "06/06/2021",
        "07/07/2021",
        "07/07/2021",
        "06/06/2021",
        "07/07/2021",
    ],
    "Durée": [1, 2, 3, 4, 9, 5, 6],
}

data_frame_enregistrement = pd.DataFrame(datas_enregistrement)

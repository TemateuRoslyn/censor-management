import json
import pandas as pd

# Liste pour stocker les objets JSON extraits
liste_json = []

# Supposons que vous ayez une liste "values" contenant des chaînes JSON
values = [
    '{"values": {"nom": "John", "age": 30}}',
    '{"values": {"nom": "Alice", "age": 25}}',
    '{"values": {"nom": "Bob", "age": 35}}',
]

# Parcourez la liste "values" et extrayez les objets JSON
for value in values:
    json_values = json.loads(value)
    liste_json.append(json_values["values"])

# Transformez la liste de dictionnaires en un DataFrame avec Pandas
df = pd.DataFrame(liste_json)

# Affichez le DataFrame
print(df)

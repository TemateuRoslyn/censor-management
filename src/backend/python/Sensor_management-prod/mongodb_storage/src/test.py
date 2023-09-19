import pandas as pd 
from pymongo import MongoClient
from pprint import pprint
import json

uri = "mongodb://root:admin@192.168.3.87:27017"

# Transformation des données en un Pandas 
data_frame = pd.read_csv("Donnees_completes_25_8_2023 9_39_30_index_0.csv")

client = MongoClient(uri)
database = client["DB_ALL"] 
collection = database["datas"] 

for index, row in data_frame.iterrows(): 
   data_dict = row.to_dict()
   result = collection.insert_one(data_dict)

print("La fin")
client.close()
from pymongo import MongoClient

class MongoDBHandler:
    def __init__(self, db_name, host='localhost', port=27017):
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]

    def insert_one(self, collection_name, data):
        try:
            collection = self.db[collection_name]
            result = collection.insert_one(data)
            return result.inserted_id
        except Exception as e:
            print(f"Erreur lors de l'insertion dans la collection {collection_name}: {e}")
            return None

    def find(self, collection_name, query=None):
        try:
            collection = self.db[collection_name]
            if query:
                return collection.find(query)
            else:
                return collection.find()
        except Exception as e:
            print(f"Erreur lors de la recherche dans la collection {collection_name}: {e}")
            return None

    def update_one(self, collection_name, query, update_data):
        try:
            collection = self.db[collection_name]
            result = collection.update_one(query, {'$set': update_data})
            return result.modified_count
        except Exception as e:
            print(f"Erreur lors de la mise à jour dans la collection {collection_name}: {e}")
            return 0

    def delete_one(self, collection_name, query):
        try:
            collection = self.db[collection_name]
            result = collection.delete_one(query)
            return result.deleted_count
        except Exception as e:
            print(f"Erreur lors de la suppression dans la collection {collection_name}: {e}")
            return 0

    def close(self):
        self.client.close()
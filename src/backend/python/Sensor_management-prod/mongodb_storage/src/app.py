import threading
import numpy as np
import pandas as pd

from flask import Flask, jsonify, request
from datetime import datetime as Date
from redis import Redis
from mongodb import MongoDBHandler

app = Flask(__name__)




STOP_INSERT_DATA =[False]

def process_messages(item: dict, sample_size : int = 1000, format_time : str = "%d-%m-%y %H:%M:%S.%f"):
    """
       process message reads from redis   

       Parameters
       ----------
       item : message from redis
       sample_size : number of sample reads per channel in one time
       format_time : format time


       Return
       ------
            msg : dict
    """

    t1 = Date.fromisoformat(item['time_start'])
    t2 = Date.fromisoformat(item['time_stop'])

    delta = (t2-t1)/sample_size

    data ={}
   
    t = [ val for val in np.arange(t1,t2+delta, delta).tolist()]
    
    if len(t) > sample_size:
        data['timestamp'] =[val.strftime(format_time) for val in t[0:sample_size]]
    elif len(t) < sample_size:
        tmp = t[-1]
        while(len(t) < sample_size):
            tmp += delta
            t.append(tmp)
        data['timestamp'] = [val.strftime(format_time) for val in t]
    else:
        data['timestamp'] = [val.strftime(format_time) for val in t]
   

    channels = np.asarray(item['channels'].split(), dtype=str)

    for ch in channels :
        data[ch] = np.asarray(item[ch][1:-2].split(), dtype=float).tolist()

  
    msg ={}

    msg['value'] = data
    msg['sample_rate'] = int(item['sample_rate'])
    msg['time_start'] = t1
    msg['time_stop'] = t2
    msg['channels'] = channels.__str__()
  

    return msg


def insert_data_into_mongodb(stop_event, redis:Redis, mongo : MongoDBHandler, config):

    lastid = '0'
    check_backlog = False 

    while not stop_event[0]:

        items = []

        if check_backlog : 

            items = redis.xreadgroup(groupname=config['group'], consumername='C_mongodb',block=10, count=100, streams={config['stream']:lastid} )

        else :
                    
            items = redis.xreadgroup(groupname=config['group'], consumername='C_mongodb',block=10, count=100, streams={config['stream']:'>'} )


        if items == None :

            pass

        else :

            check_backlog = True if len(items[0][1]) > 0 else False

            for elt in items[0][1] :

                _, item = elt

                data = process_messages(item=item, sample_size=int(config['sample']), format_time=f"%{config['day']}-%{config['month']}-%{config['year']} %{config['hour']}:%{config['minute']}:%{config['seconds']}.%{config['milliseconds']}")

                mongo.insert_one(collection_name=config['collection_name'], data=data)
               

            lastid = items[0][1][-1][0]
       

        


# Route pour écrire des données dans InfluxDB
@app.route('/api/writeloop', methods=['POST'])
def api_write_to_mongodb():

    try:

        data = request.get_json()

        redis_conn = Redis(host=data.get('host'), port=int(data.get('port')), decode_responses=True)

        mongo = MongoDBHandler(host=data.get('url'), db_name=data.get('db'))

        if len(redis_conn.xinfo_groups(data.get('stream'))==0):

                redis_conn.xgroup_create(name=data.get('stream'), groupname=data.get('group'), id=0)

        config = {}
        config['day'] = data.get('day')
        config['month'] = data.get('month')
        config['year'] = data.get('year')
        config['hour'] = data.get('hour')
        config['minute'] = data.get('minute')
        config['seconds'] = data.get('seconds')
        config['milliseconds'] = data.get('milliseconds')
        config['sample'] = data.get('sample')
        config['group'] = data.get('group')
        config['stream'] = data.get('stream')
        config['collection_name'] = data.get('collection_name')

        # Créez un thread pour la tâche en arrière-plan
        background_thread = threading.Thread(target=insert_data_into_mongodb, args=(STOP_INSERT_DATA, redis_conn, mongo, config))
        # Démarrez le thread en arrière-plan
        background_thread.start()


        background_thread.join()

        redis_conn.close()
        mongo.close()

    except Exception as ex:
        print(f"Error : {ex}")



# Route pour écrire des données dans InfluxDB
@app.route('/api/stopwriteloop', methods=['GET'])
def api_stop_write_to_mongodb(): 

    STOP_INSERT_DATA[0] = True 

    return jsonify({'return': "Stop de la sauvegarde"}), 200 


# Route pour rechercher des données dans MongoDB
@app.route('/api/find', methods=['POST'])
def find_data():
    try:
        data = request.get_json()
        collection_name = data.get('collection_name')
        query = data.get('query')

        mongo_handler = MongoDBHandler(host=data.get('url'), db_name=data.get('db'))

        if collection_name:
            results = mongo_handler.find(collection_name=collection_name, query=query)
            mongo_handler.close()
            return jsonify({'results': [result for result in results]}), 200
        else:
            mongo_handler.close()
            return jsonify({'error': 'La collection doit être spécifiée dans le corps de la requête JSON.'}), 400

    except Exception as e:
        return jsonify({'error': 'Une erreur s\'est produite lors du traitement de la requête.'}), 500
    


# Route pour mettre à jour des données dans MongoDB
@app.route('/api/update', methods=['POST'])
def update_data():
    try:
        data = request.get_json()
        collection_name = data.get('collection_name')
        query = data.get('query')
        update_data = data.get('update_data')

        mongo_handler = MongoDBHandler(host=data.get('url'), db_name=data.get('db'))


        if collection_name and query and update_data:
            updated_count = mongo_handler.update_one(collection_name=collection_name, query=query, update_data=update_data)
            mongo_handler.close()
            return jsonify({'message': f'{updated_count} documents mis à jour dans MongoDB.'}), 200
        else:
            mongo_handler.close()
            return jsonify({'error': 'La collection, la requête (query) et les données de mise à jour (update_data) doivent être spécifiées dans le corps de la requête JSON.'}), 400

    except Exception as e:
        return jsonify({'error': 'Une erreur s\'est produite lors du traitement de la requête.'}), 500
    


# Route pour supprimer des données dans MongoDB
@app.route('/api/delete', methods=['POST'])
def delete_data():
    try:
        data = request.get_json()
        collection_name = data.get('collection_name')
        query = data.get('query')

        mongo_handler = MongoDBHandler(host=data.get('url'), db_name=data.get('db'))


        if collection_name and query:
            deleted_count = mongo_handler.delete_one(collection_name=collection_name, query=query)
            mongo_handler.close()
            return jsonify({'message': f'{deleted_count} documents supprimés de MongoDB.'}), 200
        else:
            mongo_handler.close()
            return jsonify({'error': 'La collection et la requête (query) doivent être spécifiées dans le corps de la requête JSON.'}), 400

    except Exception as e:
        return jsonify({'error': 'Une erreur s\'est produite lors du traitement de la requête.'}), 500









# # Configuration de la base de données MongoDB
# MONGODB_URL = "mongodb://localhost:27017"
# MONGODB_DB_NAME = "mydatabase"

# # Créer une instance de la classe MongoDBHandler
# mongo_handler = MongoDBHandler(db_name=MONGODB_DB_NAME, url=MONGODB_URL)


# # Route pour insérer des données dans MongoDB
# @app.route('/api/insert', methods=['POST'])
# def insert_data():
#     try:
#         data = request.get_json()
#         collection_name = data.get('collection_name')
#         data_to_insert = data.get('data')

#         if collection_name and data_to_insert:
#             inserted_id = mongo_handler.insert_one(collection_name=collection_name, data=data_to_insert)
#             if inserted_id:
#                 return jsonify({'message': 'Données insérées avec succès dans MongoDB.', 'inserted_id': str(inserted_id)}), 201
#             else:
#                 return jsonify({'error': 'Erreur lors de l\'insertion des données dans MongoDB.'}), 500
#         else:
#             return jsonify({'error': 'La collection et les données doivent être spécifiées dans le corps de la requête JSON.'}), 400

#     except Exception as e:
#         return jsonify({'error': 'Une erreur s\'est produite lors du traitement de la requête.'}), 500
    


# # Route pour rechercher des données dans MongoDB
# @app.route('/api/find', methods=['POST'])
# def find_data():
#     try:
#         data = request.get_json()
#         collection_name = data.get('collection_name')
#         query = data.get('query')

#         if collection_name:
#             results = mongo_handler.find(collection_name=collection_name, query=query)
#             return jsonify({'results': [result for result in results]}), 200
#         else:
#             return jsonify({'error': 'La collection doit être spécifiée dans le corps de la requête JSON.'}), 400

#     except Exception as e:
#         return jsonify({'error': 'Une erreur s\'est produite lors du traitement de la requête.'}), 500
    


# # Route pour mettre à jour des données dans MongoDB
# @app.route('/api/update', methods=['POST'])
# def update_data():
#     try:
#         data = request.get_json()
#         collection_name = data.get('collection_name')
#         query = data.get('query')
#         update_data = data.get('update_data')

#         if collection_name and query and update_data:
#             updated_count = mongo_handler.update_one(collection_name=collection_name, query=query, update_data=update_data)
#             return jsonify({'message': f'{updated_count} documents mis à jour dans MongoDB.'}), 200
#         else:
#             return jsonify({'error': 'La collection, la requête (query) et les données de mise à jour (update_data) doivent être spécifiées dans le corps de la requête JSON.'}), 400

#     except Exception as e:
#         return jsonify({'error': 'Une erreur s\'est produite lors du traitement de la requête.'}), 500
    


# # Route pour supprimer des données dans MongoDB
# @app.route('/api/delete', methods=['POST'])
# def delete_data():
#     try:
#         data = request.get_json()
#         collection_name = data.get('collection_name')
#         query = data.get('query')

#         if collection_name and query:
#             deleted_count = mongo_handler.delete_one(collection_name=collection_name, query=query)
#             return jsonify({'message': f'{deleted_count} documents supprimés de MongoDB.'}), 200
#         else:
#             return jsonify({'error': 'La collection et la requête (query) doivent être spécifiées dans le corps de la requête JSON.'}), 400

#     except Exception as e:
#         return jsonify({'error': 'Une erreur s\'est produite lors du traitement de la requête.'}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
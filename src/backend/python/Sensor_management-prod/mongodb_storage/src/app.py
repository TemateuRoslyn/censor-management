import threading
import numpy as np
import pandas as pd
import os

from flask import Flask, jsonify, request
from datetime import datetime as Date
from redis import Redis
from mongodb import MongoDBHandler

# Lire la valeur des variables d'environnement
debug_val = os.getenv("debug")  # La variable "debug" sera soit True ou False (str)
host_val = os.getenv("host")    # La variable "host" contiendra l'adresse (str)
port_val = os.getenv("port")    # La variable "port" contiendra le port (str)


# Convertir le port en nombre (integer)
try:
    port_val = int(port_val)
except ValueError:
    print("Erreur : le port n'est pas un entier valide.")
    
if debug_val == "true":
    debug_val = True
else:
    debug_val = False


app = Flask(__name__)




STOP_INSERT_DATA =[False]
BACKGROUND_THREAD = None

STOP_INSERT_DATA_ALL =[False]
BACKGROUND_THREAD_ALL = None

def quering(data):

    query = {}
    query['time_start'] = {'$gte':Date.fromisoformat(data['time_start'])}
    # query['time_stop'] = {'$lte':Date.fromisoformat(data['time_start'])}

    return query

def process_ai_messages(item: dict, sample_size : int = 1000, format_time : str = "%d-%m-%y %H:%M:%S.%f"):
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


def insert_data_ai_into_mongodb(stop_event, redis:Redis, mongo : MongoDBHandler, config):

    global STOP_INSERT_DATA

    try:
        
        lastid = '0-0'
        check_backlog = True

        lis = redis.xinfo_groups(config['stream'])

        if len(lis)!=0:
            for elt in lis:
                if elt['name']==config['group']:
                    lastid = elt['last-delivered-id']

        while not STOP_INSERT_DATA[0]:

            items = []

            if check_backlog : 

                items = redis.xreadgroup(groupname=config['group'], consumername='C_mongodb',block=10, count=10, streams={config['stream']:lastid} )

            else :
                        
                items = redis.xreadgroup(groupname=config['group'], consumername='C_mongodb',block=10, count=10, streams={config['stream']:'>'} )


            if (items == None) or (len(items[0][1])==0) :

                check_backlog = False if (len(items[0][1]) == 0) else True

            else :
                                
                for elt in items[0][1] :

                    id, item = elt

                    data = process_ai_messages(item=item, sample_size=int(config['sample_size']), format_time=f"%{config['day']}-%{config['month']}-%{config['year']} %{config['hour']}:%{config['minute']}:%{config['seconds']}.%{config['milliseconds']}")

                    mongo.insert_one(collection_name=config['collection_name'], data=data)

                    redis.xack(config['stream'],config['group'],id)
             
                lastid = items[0][1][-1][0]

        redis.close()
        mongo.close()
    except Exception as ex:
        print(f"Erreur {ex}")

def read_items_from_redis(redis, stream, group, consumer='consumer_i', block=1, count=1):

      
    items = []

                           
    items = redis.xreadgroup(groupname=group, consumername=consumer,block=block, count=count, streams={stream:'>'} )

    
    if (len(items)== 0)or (items == None):

        return None
    
    elif (len(items[0][1])==0):

        return None

    else :            

        data = []

                
        for elt in items[0][1] :

            id, item = elt

            data.append(item)

            redis.xack(stream, group, id)

        return data

def insert_data_all_into_mongodb(stop_event, redis:Redis, mongo : MongoDBHandler, config):

    global STOP_INSERT_DATA_ALL

    try:
        
        # lastid = '0-0'
        # check_backlog = True

        # lis = redis.xinfo_groups(config['stream'])

        # if len(lis)!=0:
        #     for elt in lis:
        #         if elt['name']==config['group']:
        #             lastid = elt['last-delivered-id']

        while not STOP_INSERT_DATA_ALL[0]:

            items = read_items_from_redis(redis=redis, stream=config['stream'], group=config['group'], consumer='C_mongodb_all')

            if (items == None) :

                pass

            else :
                
                item = items[0]

                # pprint.pprint(item)

                data = {}

                channels =[elt.replace("'", "") for elt in np.asarray(item['columns'][1:-2].split(", "), dtype=str).tolist()]

                # print(channels)

                for ch in channels :
                    
                    if (ch =='udp') or (ch =='timestamp'):

                        data[ch] = np.asarray([None if (elt=='nan')  else elt.replace("'","") for elt in item[ch][1:-1].split(", ")], dtype=str).tolist()

                    else:

                        data[ch] = np.asarray([None if (elt=='nan')  else elt.replace("'","") for elt in item[ch][1:-1].split(", ")], dtype=float).tolist()

                    
                message = {}
                message['time_start'] = str(item['timestart'])
                message['time_stop'] = str(item['timestop'])
                message['rate'] = int(item['rate'])
                message['values'] = data
                message['channels'] = channels


                mongo.insert_one(collection_name=config['collection_name'], data=message)


        redis.close()
        mongo.close()
    except Exception as ex:
        print(f"Erreur {ex}")
       
       
@app.route('/api/usb/find_session', methods=['GET'])
def find_session():

    try:

        data = request.get_json()
        # collection_name = data.get('collection_name')
        # query = data.get('query')
        #mongo_handler = MongoDBHandler(host=data.get('url'), db_name=data.get('db'))
        mongo_handler = MongoDBHandler(host=data.get('url'), db_name=data.get('db'), usename=data.get('username'), password=data.get('password'))

        if data.get('collection_name') is not None:
            
            results = mongo_handler.find(collection_name=data.get('collection_name'), query=quering(data.get('query')))
            # mongo_handler.close()
            return jsonify({'results': [result for result in results]}), 200
        else:
            mongo_handler.close()
            return jsonify({'error': 'La collection doit être spécifiée dans le corps de la requête JSON.'}), 400

    except Exception as e:

        return jsonify({'Message': f"Une erreur sur la sauvegarde dans MongoDB :  {e}."}), 500
        
@app.route('/api/usb/save_session', methods=['POST'])
def save_session():

    try:

        data = request.get_json()

        mongo = MongoDBHandler(host=data.get('url'), db_name=data.get('db'), usename=data.get('username'), password=data.get('password'))

        message = {}

        message["start_session"] = data.get("start_session")

        message["end_session"] = data.get("end_session")

        message["description"] = data.get("description")

        mongo.insert_one(collection_name=data['collection_name'], data=message)
        

    except Exception as e:

        return jsonify({'Message': f"Une erreur sur la sauvegarde de la session dans MongoDB :  {e}."}), 500



# Route pour écrire des données dans InfluxDB
@app.route('/api/write_loop', methods=['POST'])
def api_write_to_mongodb():
    global BACKGROUND_THREAD

    try:

        data = request.get_json()

        redis_conn = Redis(host=data.get('host'), port=int(data.get('port')), decode_responses=True)

        mongo = MongoDBHandler(host=data.get('url'), db_name=data.get('db'), usename=data.get('username'), password=data.get('password'))

        # if len(redis_conn.xinfo_groups(data.get('stream')))==0:

        #         redis_conn.xgroup_create(name=data.get('stream'), groupname=data.get('group'), id=0)

        list_group = redis_conn.xinfo_groups(data.get('stream'))

        if len(list_group)==0:

                redis_conn.xgroup_create(name=data.get('stream'), groupname=data.get('group'), id=0)
        else:

            create = True

            for elt in list_group:

                if data.get('group') == elt['name'] :

                    create=False
                    
            if create :

                redis_conn.xgroup_create(name=data.get('stream'), groupname=data.get('group'), id=0)

        config = {}
        config['day'] = data.get('day')
        config['month'] = data.get('month')
        config['year'] = data.get('year')
        config['hour'] = data.get('hour')
        config['minute'] = data.get('minute')
        config['seconds'] = data.get('seconds')
        config['milliseconds'] = data.get('milliseconds')
        config['sample_size'] = data.get('sample_size')
        config['group'] = data.get('group')
        config['stream'] = data.get('stream')
        config['collection_name'] = data.get('collection_name')

        # Créez un thread pour la tâche en arrière-plan
        BACKGROUND_THREAD = threading.Thread(target=insert_data_ai_into_mongodb, args=(STOP_INSERT_DATA, redis_conn, mongo, config))
        # Démarrez le thread en arrière-plan
        BACKGROUND_THREAD.start()

        return jsonify({'Message': f"Début de la sauvegarde dans MongoDB"}), 200
    
    except Exception as e:
        redis_conn.close()
        mongo.close()
        return jsonify({'Message': f"Une erreur sur la sauvegarde dans MongoDB :  {e}."}), 500




# Route pour écrire des données dans InfluxDB
@app.route('/api/stop_write_loop', methods=['GET'])
def api_stop_write_to_mongodb():

    global STOP_INSERT_DATA 
    global BACKGROUND_THREAD

    try:

        STOP_INSERT_DATA[0] = True 

        BACKGROUND_THREAD.join()

        return jsonify({'Message': "Stop de la sauvegarde dans MongoDB"}), 200
    
    except Exception as ex:
        return jsonify({'Message': f"Un problème à l'arret : {ex}"}), 500 
    

# Route pour écrire des données dans InfluxDB
@app.route('/api/write_loop_all', methods=['POST'])
def api_write_all_to_mongodb():
    global BACKGROUND_THREAD_ALL

    try:

        data = request.get_json()

        redis_conn = Redis(host=data.get('host'), port=int(data.get('port')), decode_responses=True)

        mongo = MongoDBHandler(host=data.get('url'), db_name=data.get('db'), usename=data.get('username'), password=data.get('password'))

        # if len(redis_conn.xinfo_groups(data.get('stream')))==0:

        #         redis_conn.xgroup_create(name=data.get('stream'), groupname=data.get('group'), id=0)

        list_group = redis_conn.xinfo_groups(data.get('stream'))

        if len(list_group)==0:

                redis_conn.xgroup_create(name=data.get('stream'), groupname=data.get('group'), id=0)
        else:

            create = True

            for elt in list_group:

                if data.get('group') == elt['name'] :

                    create=False
                    
            if create :

                redis_conn.xgroup_create(name=data.get('stream'), groupname=data.get('group'), id=0)

        config = {}
        config['group'] = data.get('group')
        config['stream'] = data.get('stream')
        config['collection_name'] = data.get('collection_name')

        # Créez un thread pour la tâche en arrière-plan
        BACKGROUND_THREAD_ALL = threading.Thread(target=insert_data_all_into_mongodb, args=(STOP_INSERT_DATA, redis_conn, mongo, config))
        # Démarrez le thread en arrière-plan
        BACKGROUND_THREAD_ALL.start()

        return jsonify({'Message': f"Début de la sauvegarde(all) dans MongoDB"}), 200
    
    except Exception as e:
        redis_conn.close()
        mongo.close()
        return jsonify({'Message': f"Une erreur sur la sauvegarde(all) dans MongoDB :  {e}."}), 500




# Route pour écrire des données dans InfluxDB
@app.route('/api/stop_write_loop_all', methods=['GET'])
def api_stop_write_all_to_mongodb():

    global STOP_INSERT_DATA_ALL 
    global BACKGROUND_THREAD_ALL

    try:

        STOP_INSERT_DATA_ALL[0] = True 

        BACKGROUND_THREAD_ALL.join()

        return jsonify({'Message': "Stop de la sauvegarde(all) dans MongoDB"}), 200
    
    except Exception as ex:
        return jsonify({'Message': f"Un problème à l'arret (all) : {ex}"}), 500 



# Route pour rechercher des données dans MongoDB
@app.route('/api/find', methods=['POST'])
def find_data():
    try:
        data = request.get_json()
        # collection_name = data.get('collection_name')
        # query = data.get('query')

        #mongo_handler = MongoDBHandler(host=data.get('url'), db_name=data.get('db'))
        mongo_handler = MongoDBHandler(host=data.get('url'), db_name=data.get('db'), usename=data.get('username'), password=data.get('password'))

        if data.get('collection_name') is not None:
            
            results = mongo_handler.find(collection_name=data.get('collection_name'), query=quering(data.get('query')))
            # mongo_handler.close()
            return jsonify({'results': [result for result in results]}), 200
        else:
            mongo_handler.close()
            return jsonify({'error': 'La collection doit être spécifiée dans le corps de la requête JSON.'}), 400

    except Exception as e:
        return jsonify({'error': f"Une erreur s\'est produite lors du traitement de la requête. {e}"}), 500
    


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
    from waitress import serve
    
    if debug_val :
        app.run(
        debug=debug_val, 
        host=host_val,
        port=port_val, 
        )
    else :
        serve(
            app, 
            host=host_val, 
            port=port_val
            )

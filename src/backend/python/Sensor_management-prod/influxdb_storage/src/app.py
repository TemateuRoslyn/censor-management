import threading
import numpy as np
import pandas as pd
import os

from flask import Flask, jsonify, request
from datetime import datetime as Date
from influxdb_client import Point
from influxdb import InfluxDBHandler
from redis import Redis


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


# # Configuration de la base de données InfluxDB
# INFLUXDB_URL = "http://localhost:8086"
# INFLUXDB_TOKEN = "YOUR_AUTH_TOKEN"
# INFLUXDB_ORG = "YOUR_ORG"
# INFLUXDB_BUCKET = "YOUR_BUCKET"

# # Créer une instance de la classe InfluxDBHandler
# influx_handler = InfluxDBHandler(
#     url=INFLUXDB_URL,
#     token=INFLUXDB_TOKEN,
#     org=INFLUXDB_ORG,
#     bucket=INFLUXDB_BUCKET
# )

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


def insert_data_into_influxdb(stop_event, redis:Redis, influx : InfluxDBHandler, config):

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

                point = Point("measurement_channel").tag("channel", "ai")

                for key in data.keys():

                     point.field(key, data[key].__str__())

                influx.write_api.write(bucket=config['bucket'], org=config['org'], record=point)

            lastid = items[0][1][-1][0]
       

        


# Route pour écrire des données dans InfluxDB
@app.route('/api/writeloop', methods=['POST'])
def api_write_to_influxdb():

    try:

        data = request.get_json()

        redis_conn = Redis(host=data.get('host'), port=int(data.get('port')), decode_responses=True)

        influx = InfluxDBHandler(url=data.get('url'), token=data.get('token'), org=data.get('org'))

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
        config['group'] = data.get('group')
        config['stream'] = data.get('stream')
        config['sample'] = data.get('sample')
        config['org'] = data.get('org')
        config['bucket'] = data.get('bucket')

        # Créez un thread pour la tâche en arrière-plan
        background_thread = threading.Thread(target=insert_data_into_influxdb, args=(STOP_INSERT_DATA, redis_conn, influx, config))
        # Démarrez le thread en arrière-plan
        background_thread.start()


        background_thread.join()

    except Exception as ex:
        print(f"Error : {ex}")



# Route pour écrire des données dans InfluxDB
@app.route('/api/stopwriteloop', methods=['GET'])
def api_stop_write_to_influxdb(): 

    STOP_INSERT_DATA[0] = True 

    return jsonify({'return': "Stop de la sauvegarde"}), 200      


# Route pour effectuer une requête sur InfluxDB
@app.route('/api/query', methods=['POST'])
def query_influxdb():
    try:
        data = request.get_json()
        query = data.get('query')
        influx_handler = InfluxDBHandler(url=data.get('url'), token=data.get('token'), org=data.get('org'))

        if query:
            result = influx_handler.query_data(query=query)
            influx_handler.close()
            return jsonify(result), 200
        else:
            influx_handler.close()
            return jsonify({'error': 'La requête doit être spécifiée dans le corps de la requête JSON.'}), 400

    except Exception as e:
        return jsonify({'error': 'Une erreur s\'est produite lors du traitement de la requête.'}), 500
    





# # Route pour écrire des données dans InfluxDB
# @app.route('/api/write', methods=['POST'])
# def write_to_influxdb():
#     try:
#         data = request.get_json()
#         measurement = data.get('measurement')
#         tags = data.get('tags', {})
#         fields = data.get('fields', {})

#         if measurement and fields:
#             success = influx_handler.write_data(measurement=measurement, tags=tags, fields=fields)
#             if success:
#                 return jsonify({'message': 'Données écrites avec succès dans InfluxDB.'}), 201
#             else:
#                 return jsonify({'error': 'Erreur lors de l\'écriture des données.'}), 500
#         else:
#             return jsonify({'error': 'Les données doivent contenir une mesure (measurement) et des champs (fields).'}), 400

#     except Exception as e:
#         return jsonify({'error': 'Une erreur s\'est produite lors du traitement de la requête.'}), 500

# # Route pour effectuer une requête sur InfluxDB
# @app.route('/api/query', methods=['POST'])
# def query_influxdb():
#     try:
#         data = request.get_json()
#         query = data.get('query')

#         if query:
#             result = influx_handler.query_data(query=query)
#             return jsonify(result), 200
#         else:
#             return jsonify({'error': 'La requête doit être spécifiée dans le corps de la requête JSON.'}), 400

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

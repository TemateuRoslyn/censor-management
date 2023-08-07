import threading
import json
import os 
import requests

from flask import request,jsonify, Flask
from redis import Redis, RedisError
from argparse import ArgumentParser, FileType
from configparser import ConfigParser


app = Flask(__name__)



if __name__ == '__main__':

    # Lire la valeur des variables d'environnement
    debug_val = os.getenv("debug", "true")  # La variable "debug" sera soit True ou False (str)
    host_val = os.getenv("host", "127.0.0.1")    # La variable "host" contiendra l'adresse (str)
    port_val = os.getenv("port", 5000)    # La variable "port" contiendra le port (str)


    # Convertir le port en nombre (integer)
    try:
        port_val = int(port_val)
    except ValueError:
        print("Erreur : le port n'est pas un entier valide.")
        
    if debug_val == "true":
        debug_val = True
    else:
        debug_val = False

    config_parser = ConfigParser()

    config_parser.read(os.getenv("CONFIG_PATH", "../ressources/configs.ini"))

    config_ai = dict(config_parser['Config_ai'])

    config_di = dict(config_parser['Config_di'])

    config_do = dict(config_parser['Config_do'])

    config_ci = dict(config_parser['Config_ci'])

    config_co = dict(config_parser['Config_co'])

    config_redis = dict(config_parser['Redis'])

    config_mongodb = dict(config_parser['Mongodb'])

    config_influxdb = dict(config_parser['Influxdb'])

    config_usb = dict(config_parser['Usb'])

    config_api_mongodb = dict(config_parser['Api_mongodb'])

    config_api_ni = dict(config_parser['Api_ni'])

    config_api_usb = dict(config_parser['Api_usb'])

    config_api_udp = dict(config_parser['Api_udp'])




    STOP_EVENT_COLLECT_UDP = [False]

    try:

        data_ai = {
                    'stream': "stream_chan_ai",#str(config_redis.get('stream')),
                    'host': config_redis.get('host'),
                    'port': config_redis.get('port'),
                    'period': config_ai.get('period'),
                    'rate': config_ai.get('rate'),
                    'buffer_size': config_ai.get('buffer_size'),
                    'sample_size': config_ai.get('sample_size'),
                    'device': config_ai.get('device'),
                    'channels': ["ai0", "ai1", "ai2", "ai3", "ai4", "ai5", "ai6", "ai7"]
                    }
        
        data_di = {
                    'stream': "stream_chan_di",#str(config_redis.get('stream')),
                    'host': config_redis.get('host'),
                    'port': config_redis.get('port'),
                    'period': config_di.get('period'),
                    'rate': config_di.get('rate'),
                    'buffer_size': config_di.get('buffer_size'),
                    'sample_size': config_di.get('sample_size'),
                    'device': config_di.get('device'),
                    'lines': config_di.get('lines'),
                    'num_di': "0"
                    }
        

        data_do = {
                    'stream': "stream_chan_do",#str(config_redis.get('stream')),
                    'host': config_redis.get('host'),
                    'port': config_redis.get('port'),
                    'period': config_do.get('period'),
                    'rate': config_do.get('rate'),
                    'buffer_size': config_do.get('buffer_size'),
                    'sample_size': config_do.get('sample_size'),
                    'device': config_do.get('device'),
                    'lines': config_do.get('lines'),
                    'num_di': "0"
                    }
        
        data_ci = {
                    'stream': "stream_chan_ci",#str(config_redis.get('stream')),
                    'host': config_redis.get('host'),
                    'port': config_redis.get('port'),
                    'period': config_ci.get('period'),
                    'rate': config_ci.get('rate'),
                    'buffer_size': config_ci.get('buffer_size'),
                    'sample_size': config_ci.get('sample_size'),
                    'device': config_ci.get('device'),
                    'channel': "ctr1"
                    }
        
        data_co = {
                    'stream': "stream_chan_co",#str(config_redis.get('stream')),
                    'host': config_redis.get('host'),
                    'port': config_redis.get('port'),
                    'period': config_co.get('period'),
                    'rate': config_co.get('rate'),
                    'buffer_size': config_co.get('buffer_size'),
                    'sample_size': config_co.get('sample_size'),
                    'device': config_co.get('device'),
                    'channel': "ctr1"
                    }
        


        print(data_ai)
        api_url_ni_ai = f"{config_api_ni.get('endpoint')}/api/read_ai_loop_to_redis"

                # # Créez un thread pour la tâche en arrière-plan
                # ni_thread_ai = threading.Thread(target=request_post, args=(api_url_ni_ai, data_to_ni_ai))
                # # Démarrez le thread en arrière-plan
                # ni_thread_ai.start()
        api_url_ai = f"{config_api_ni.get('endpoint')}/api/read_ai_to_redis"

        api_url_ai_stop = f"{config_api_ni.get('endpoint')}/api/stop_read_ai_to_redis"


        api_url_di = f"{config_api_ni.get('endpoint')}/api/read_di"

        api_url_ci = f"{config_api_ni.get('endpoint')}/api/read_ci"
            
        # response = requests.post(api_url_ai, json=data_to_ni_ai)

        try:
            # Faire une requête POST sécurisée avec les données
            response = requests.post(api_url_di, json=data_di)
            # response = requests.get(api_url_ai_stop)

            while response.status_code == 200:

                resp = response.json()

                print(f"ret :{resp['data']}")

                # t="{'time': '2023-08-02T05:22:44.390720', 'values': [False]}"

                # print(f"js : {json.loads(t)}")

                data = resp['data']

                print(f"{data}")

                if data['values'][0]:
                     break

                response = requests.post(api_url_di, json=data_di)

            # Vérifier si la requête a réussi
            if response.status_code == 200:
                data = response.json()  # Si la réponse de l'API est au format JSON
                print("Données reçues :", data)
            else:
                print(f"Échec de la requête : {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête : {e}")

    except Exception as e:
         print(f"{e}")



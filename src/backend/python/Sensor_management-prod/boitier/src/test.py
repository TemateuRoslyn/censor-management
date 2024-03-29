import threading
import time
import json
import os 
import requests

from datetime import datetime as Date
from flask import request,jsonify, Flask
from redis import Redis, RedisError
from argparse import ArgumentParser, FileType
from configparser import ConfigParser


app = Flask(__name__)

def get_pression(url, data):

    resp = requests.post(url, json=data)

    while resp.status_code == 200:

        r = resp.json()['data']

        if r['values'][0]:
            break

        resp = requests.post(url, json=data)
    
    return True

def send_requests_post(stop_event, url, data):
     
    requests.post(url, json=data)

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

        # Liste des données par API

        data_ai = {
                    'stream': config_ai.get('stream'),#str(config_redis.get('stream')),
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
                    'stream': config_di.get('stream'),#str(config_redis.get('stream')),
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
                    'stream': config_ci.get('stream'),
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
                    'stream': "stream_chan_co",
                    'host': config_redis.get('host'),
                    'port': config_redis.get('port'),
                    'period': config_co.get('period'),
                    'rate': config_co.get('rate'),
                    'buffer_size': config_co.get('buffer_size'),
                    'sample_size': config_co.get('sample_size'),
                    'device': config_co.get('device'),
                    'channel': "ctr1"
                    }
        
        data_mongo_ai = {
                    'stream': config_ai.get('stream'),
                    'host': config_redis.get('host'),
                    'port': config_redis.get('port'),
                    'period': config_ai.get('period'),
                    'rate': config_ai.get('rate'),
                    'buffer_size': config_ai.get('buffer_size'),
                    'sample_size': config_ai.get('sample_size'),
                    'device': config_ai.get('device'),
                    'month': config_ai.get('month'),
                    'year': config_ai.get('year'),
                    'hour': config_ai.get('hour'),
                    'minute': config_ai.get('minute'),
                    'seconds': config_ai.get('seconds'),
                    'milliseconds': config_ai.get('milliseconds'),
                    'group': config_ai.get('group'),
                    'collection_name': config_ai.get('collection_name'),
                    'url':config_mongodb.get('url'),
                    'db':config_mongodb.get('db'),
                    'username':config_mongodb.get('username'),
                    'password':config_mongodb.get('password'),
                    'channels': ["ai0", "ai1", "ai2", "ai3", "ai4", "ai5", "ai6", "ai7"]
                    }
        data_mongo_di = {
                    'stream': config_di.get('stream'),
                    'host': config_redis.get('host'),
                    'port': config_redis.get('port'),
                    'period': config_di.get('period'),
                    'rate': config_di.get('rate'),
                    'buffer_size': config_di.get('buffer_size'),
                    'sample': config_di.get('sample_size'),
                    'device': config_di.get('device'),
                    'lines': config_di.get('lines'),
                    'month': config_di.get('month'),
                    'year': config_di.get('year'),
                    'hour': config_di.get('hour'),
                    'minute': config_di.get('minute'),
                    'seconds': config_di.get('seconds'),
                    'milliseconds': config_di.get('milliseconds'),
                    'group': config_ai.get('group'),
                    'collection_name': config_di.get('collection_name'),
                    'url':config_mongodb.get('url'),
                    'db':config_mongodb.get('db'),
                    'num_di': 0
                    }
        data_mongo_ci = {
                    'stream': config_ci.get('stream'),#str(config_redis.get('stream')),
                    'host': config_redis.get('host'),
                    'port': config_redis.get('port'),
                    'period': config_ci.get('period'),
                    'rate': config_ci.get('rate'),
                    'buffer_size': config_ci.get('buffer_size'),
                    'sample': config_ci.get('sample_size'),
                    'device': config_ci.get('device'),
                    'month': config_ci.get('month'),
                    'year': config_ci.get('year'),
                    'hour': config_ci.get('hour'),
                    'minute': config_ci.get('minute'),
                    'seconds': config_ci.get('seconds'),
                    'milliseconds': config_ci.get('milliseconds'),
                    'group': config_ci.get('group'),
                    'collection_name': config_ci.get('collection_name'),
                    'url':config_mongodb.get('url'),
                    'db':config_mongodb.get('db'),
                    'channel': "ctr1"
                    }
        
        # query = {
        #     'time_start': "2023-08-02 21:23:47.453"
        #     # 'time_stop': "2023-08-02 21:23:48.124"
        #     }
        
        # data_mongo_find_ai = {
        #             'collection_name': config_ai.get('collection_name'),
        #             'url':config_mongodb.get('url'),
        #             'db':config_mongodb.get('db'),
        #             'username':config_mongodb.get('username'),
        #             'password':config_mongodb.get('password'),
        #             'query':query
        #             }
        
        data_usb = {
                    'stream': config_ci.get('stream'),#str(config_redis.get('stream')),
                    'host': config_redis.get('host'),
                    'port': config_redis.get('port'),
                    'mount_dir': config_usb.get('mount_dir'),
                    'source_dir': config_usb.get('source_dir'),
                    'usb_mount_path': config_usb.get('usb_mount_path')
                    }


        # Liste des endpoint
        api_url_ni_ai = f"{config_api_ni.get('endpoint')}/api/read_ai_to_redis"
        
        # api_url_ai = f"{config_api_ni.get('endpoint')}/api/read_ai_to_redis"

        api_url_ai_stop = f"{config_api_ni.get('endpoint')}/api/stop_read_ai_to_redis"

        api_url_ai_loop = f"{config_api_ni.get('endpoint')}/api/read_ai_loop_to_redis"

        api_url_ai_stop_loop = f"{config_api_ni.get('endpoint')}/api/stop_read_ai_loop_to_redis"

        api_url_di = f"{config_api_ni.get('endpoint')}/api/read_di"

        api_url_ci = f"{config_api_ni.get('endpoint')}/api/read_ci"

        api_url_mongo_ai = f"http://127.0.0.1:5005/api/write_loop"

        api_url_mongo_ai_stop = f"http://127.0.0.1:5005/api/stop_write_loop"

        api_url_mongo_find = f"http://127.0.0.1:5005/api/find"
            
        # response = requests.post(api_url_ai, json=data_to_ni_ai)


        try:

            # stop_event = threading.Event()

            # tr1 = threading.Thread(target=send_requests_post, args=(stop_event, api_url_ai_loop, data_ai,))

            # tr2 = threading.Thread(target=send_requests_post, args=(stop_event, api_url_mongo_ai, data_mongo_ai,))
           
            if get_pression(url=api_url_di, data=data_di):

                """ 
                response = requests.post(api_url_ai_loop, json=data_ai)

                # Vérifier si la requête a réussi
                if response.status_code == 200:
                    data = response.json()  # Si la réponse de l'API est au format JSON
                    print("Données reçues :", data)
                else:
                    print(f"Échec de la requête : {response.status_code} - {response.text}")

                time.sleep(1)         """        

                response = requests.post(api_url_mongo_find, json=data_mongo_find_ai)

                # Vérifier si la requête a réussi
                if response.status_code == 200:
                    data = response.json()  # Si la réponse de l'API est au format JSON
                    print("Données reçues :", data)
                else:
                    print(f"Échec de la requête : {response.status_code} - {response.text}") 
                

                """ response = requests.post(api_url_mongo_ai, json=data_mongo_ai)

                # Vérifier si la requête a réussi
                if response.status_code == 200:
                    data = response.json()  # Si la réponse de l'API est au format JSON
                    print("Données reçues :", data)
                else:
                    print(f"Échec de la requête : {response.status_code} - {response.text}") """
                
            
            time.sleep(10)
            

            if get_pression(url=api_url_di, data=data_di):

                """ #AI
                response = requests.get(api_url_ai_stop_loop)

                # Vérifier si la requête a réussi
                if response.status_code == 200:
                    data = response.json()  # Si la réponse de l'API est au format JSON
                    print("Données reçues :", data)
                else:
                    print(f"Échec de la requête : {response.status_code} - {response.text}")

                time.sleep(2)

                #MongoDB
                response = requests.get(api_url_mongo_ai_stop)

                # Vérifier si la requête a réussi
                if response.status_code == 200:
                    data = response.json()  # Si la réponse de l'API est au format JSON
                    print("Données reçues :", data)
                else:
                    print(f"Échec de la requête : {response.status_code} - {response.text}") """
                
            


            

        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête : {e}")

    except Exception as e:
         print(f"{e}")



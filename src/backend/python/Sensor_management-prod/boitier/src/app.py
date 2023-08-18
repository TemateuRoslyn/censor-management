import threading
import time
import json
import os 
import requests

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
    host_val = os.getenv("host", "0.0.0.0")    # La variable "host" contiendra l'adresse (str)
    port_val = os.getenv("port", 5006)    # La variable "port" contiendra le port (str)


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

    config_file = dict(config_parser['File'])

    config_api_mongodb = dict(config_parser['Api_mongodb'])

    config_api_ni = dict(config_parser['Api_ni'])

    config_api_usb = dict(config_parser['Api_usb'])

    config_api_udp = dict(config_parser['Api_udp'])

    config_api_file = dict(config_parser['Api_file'])




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
                    'lines': "port0/line",#config_do.get('lines'),
                    'num_do': "1:4"
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
                    'host': 'redis', #config_redis.get('host'),
                    'port': config_redis.get('port'),
                    'period': config_ai.get('period'),
                    'rate': config_ai.get('rate'),
                    'buffer_size': config_ai.get('buffer_size'),
                    'sample_size': config_ai.get('sample_size'),
                    'device': config_ai.get('device'),
                    'day': config_ai.get('day'),
                    'month': config_ai.get('month'),
                    'year': config_ai.get('year'),
                    'hour': config_ai.get('hour'),
                    'minute': config_ai.get('minute'),
                    'seconds': config_ai.get('seconds'),
                    'milliseconds': config_ai.get('milliseconds'),
                    'group': config_ai.get('group'),
                    'collection_name': config_ai.get('collection_name'),
                    'url':'mongo', #config_mongodb.get('url'),
                    'db': config_mongodb.get('db'),
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
                    'sample_size': config_di.get('sample_size'),
                    'device': config_di.get('device'),
                    'lines': config_di.get('lines'),
                    'day': config_ai.get('day'),
                    'month': config_di.get('month'),
                    'year': config_di.get('year'),
                    'hour': config_di.get('hour'),
                    'minute': config_di.get('minute'),
                    'seconds': config_di.get('seconds'),
                    'milliseconds': config_di.get('milliseconds'),
                    'group': config_ai.get('group'),
                    'collection_name': config_di.get('collection_name'),
                    'url': config_mongodb.get('url'),
                    'db':config_mongodb.get('db'),
                    'username':config_mongodb.get('username'),
                    'password':config_mongodb.get('password'),
                    'num_di': 0
                    }
        data_mongo_ci = {
                    'stream': config_ci.get('stream'),#str(config_redis.get('stream')),
                    'host': config_redis.get('host'),
                    'port': config_redis.get('port'),
                    'period': config_ci.get('period'),
                    'rate': config_ci.get('rate'),
                    'buffer_size': config_ci.get('buffer_size'),
                    'sample_size': config_ci.get('sample_size'),
                    'device': config_ci.get('device'),
                    'day': config_ai.get('day'),
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
                    'username':config_mongodb.get('username'),
                    'password':config_mongodb.get('password'),
                    'channel': "ctr1"
                    }
        
        data_usb = {
                    'source_dir': config_usb.get('source_dir')
                    # 'usb_mount_path': config_usb.get('usb_mount_path')
                    }
        
        data_file = {
                    'stream': config_ai.get('stream'),#str(config_redis.get('stream')),
                    'host': config_redis.get('host'),
                    'port': config_redis.get('port'),
                    'day': config_ai.get('day'),
                    'month': config_ci.get('month'),
                    'year': config_ci.get('year'),
                    'hour': config_ci.get('hour'),
                    'minute': config_ci.get('minute'),
                    'seconds': config_ci.get('seconds'),
                    'milliseconds': config_ci.get('milliseconds'),
                    'sample_size': config_ai.get('sample_size'),
                    'folder_path': config_file.get('folder_path'),
                    'max_file': config_file.get('max_file'),
                    'group': config_file.get('group')
                    }


        # Liste des endpoints
        api_url_ni_ai = f"{config_api_ni.get('endpoint')}/api/read_ai_to_redis"
        
        api_url_ai_stop = f"{config_api_ni.get('endpoint')}/api/stop_read_ai_to_redis"

        api_url_ai_loop = f"{config_api_ni.get('endpoint')}/api/read_ai_loop_to_redis"

        api_url_ai_stop_loop = f"{config_api_ni.get('endpoint')}/api/stop_read_ai_loop_to_redis"

        api_url_di = f"{config_api_ni.get('endpoint')}/api/read_di"

        api_url_ci = f"{config_api_ni.get('endpoint')}/api/read_ci"

        api_url_do_flashes = f"{config_api_ni.get('endpoint')}/api/write_do_flashes"

        api_url_do_stop_flashes = f"{config_api_ni.get('endpoint')}/api/stop_flashes"

        api_url_mongo_write = f"{config_api_mongodb.get('endpoint')}/api/write_loop"

        api_url_mongo_stop_write = f"{config_api_mongodb.get('endpoint')}/api/stop_write_loop"

        api_url_mongo_find = f"{config_api_mongodb.get('endpoint')}/api/find"

        api_url_file_write = f"{config_api_file.get('endpoint')}/api/write_folder"

        api_url_file_stop_write = f"{config_api_file.get('endpoint')}/api/stop_write_folder"

        api_url_usb_find = f"{config_api_usb.get('endpoint')}/api/usb/find"
        
        api_url_usb_copy = f"{config_api_usb.get('endpoint')}/api/usb/copy_files"
            


        try:

            data_do['state'] = "start"

            response = requests.post(api_url_do_flashes, json=data_do)

                # Vérifier si la requête a réussi
            if response.status_code == 200:
                data = response.json()  # Si la réponse de l'API est au format JSON
                print("Données reçues :", data)
            else:
                print(f"Échec de la requête : {response.status_code} - {response.text}")

            time.sleep(1) 

            #Usb  
            response = requests.get(api_url_usb_find)

            # Vérifier si la requête a réussi
            if response.status_code == 200:

                data_do['state'] = "USB"

                response = requests.post(api_url_do_flashes, json=data_do)

                    # Vérifier si la requête a réussi
                if response.status_code == 200:
                    data = response.json()  # Si la réponse de l'API est au format JSON
                    print("Données reçues :", data)
                else:
                    print(f"Échec de la requête : {response.status_code} - {response.text}")
            else:
                print(f"Échec de la requête : {response.status_code} - {response.text}")
      

            time.sleep(1)

            if get_pression(url=api_url_di, data=data_di):

                
                response = requests.post(api_url_ai_loop, json=data_ai)

                # Vérifier si la requête a réussi
                if response.status_code == 200:
                    data = response.json()  # Si la réponse de l'API est au format JSON
                    print("Données reçues :", data)
                else:
                    print(f"Échec de la requête : {response.status_code} - {response.text}")

                time.sleep(1)                 
                

                response = requests.post(api_url_mongo_write, json=data_mongo_ai)

                # Vérifier si la requête a réussi
                if response.status_code == 200:
                    data = response.json()  # Si la réponse de l'API est au format JSON
                    print("Données reçues :", data)
                else:
                    print(f"Échec de la requête : {response.status_code} - {response.text}")

                
                response = requests.post(api_url_file_write, json=data_file)

                # Vérifier si la requête a réussi
                if response.status_code == 200:
                    data = response.json()  # Si la réponse de l'API est au format JSON
                    print("Données reçues :", data)
                else:
                    print(f"Échec de la requête : {response.status_code} - {response.text}")

                
                data_do['state'] = "record"

                response = requests.post(api_url_do_flashes, json=data_do)

                    # Vérifier si la requête a réussi
                if response.status_code == 200:
                    data = response.json()  # Si la réponse de l'API est au format JSON
                    print("Données reçues :", data)
                else:
                    print(f"Échec de la requête : {response.status_code} - {response.text}")

                
            
            time.sleep(10)
            

            if get_pression(url=api_url_di, data=data_di):

                #AI
                response = requests.get(api_url_ai_stop_loop)

                # Vérifier si la requête a réussi
                if response.status_code == 200:
                    data = response.json()  # Si la réponse de l'API est au format JSON
                    print("Données reçues :", data)
                else:
                    print(f"Échec de la requête : {response.status_code} - {response.text}")

                time.sleep(2)

                #MongoDB
                response = requests.get(api_url_mongo_stop_write)

                # Vérifier si la requête a réussi
                if response.status_code == 200:
                    data = response.json()  # Si la réponse de l'API est au format JSON
                    print("Données reçues :", data)
                else:
                    print(f"Échec de la requête : {response.status_code} - {response.text}")

                #File
                response = requests.get(api_url_file_stop_write)

                # Vérifier si la requête a réussi
                if response.status_code == 200:
                    data = response.json()  # Si la réponse de l'API est au format JSON
                    print("Données reçues :", data)
                else:
                    print(f"Échec de la requête : {response.status_code} - {response.text}") 
                
                #Stop flashes
                response = requests.get(api_url_do_stop_flashes)

                # Vérifier si la requête a réussi
                if response.status_code == 200:
                    data = response.json()  # Si la réponse de l'API est au format JSON
                    print("Données reçues :", data)
                else:
                    print(f"Échec de la requête : {response.status_code} - {response.text}") 


                #Usb  
                response = requests.get(api_url_usb_find)

                # Vérifier si la requête a réussi
                if response.status_code == 200:

                    data = response.json()  # Si la réponse de l'API est au format JSON

                    print("Données reçues :", data)

                    data_usb['usb_mount_path'] = data['usb_mount_path']

                    #flashes
                    data_do['state'] = "wait_usb"

                    response = requests.post(api_url_do_flashes, json=data_do)

                        # Vérifier si la requête a réussi
                    if response.status_code == 200:
                        data = response.json()  # Si la réponse de l'API est au format JSON
                        print("Données reçues :", data)
                    else:
                        print(f"Échec de la requête : {response.status_code} - {response.text}")


                    #Usb copy

                    response = requests.post(api_url_usb_copy, json=data_usb)

                    # Vérifier si la requête a réussi
                    if response.status_code == 200:

                        data = response.json()  # Si la réponse de l'API est au format JSON
                        print("Données reçues :", data)
                        
                    else:
                        print(f"Échec de la requête : {response.status_code} - {response.text}")

                    
                    #Stop flashes
                    response = requests.get(api_url_do_stop_flashes)

                    # Vérifier si la requête a réussi
                    if response.status_code == 200:
                        data = response.json()  # Si la réponse de l'API est au format JSON
                        print("Données reçues :", data)
                    else:
                        print(f"Échec de la requête : {response.status_code} - {response.text}") 

                    #Mode USB
                    data_do['state'] = "USB"

                    response = requests.post(api_url_do_flashes, json=data_do)

                        # Vérifier si la requête a réussi
                    if response.status_code == 200:
                        data = response.json()  # Si la réponse de l'API est au format JSON
                        print("Données reçues :", data)
                    else:
                        print(f"Échec de la requête : {response.status_code} - {response.text}")


                else:
                    print(f"Échec de la requête : {response.status_code} - {response.text}")
      
           

        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête : {e}")

    except Exception as e:
         print(f"{e}")



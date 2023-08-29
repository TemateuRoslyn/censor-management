import threading
import time
import os
import pprint
import requests 

from datetime import datetime as Date
from flask import request,jsonify, Flask
from redis import Redis, RedisError
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from udp_protocol import UDPHandler

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

#################################################### Config #########################################################

config_parser = ConfigParser()

config_parser.read(os.getenv("CONFIG_PATH", "../ressources/configs.ini"))

config_ai = dict(config_parser['Config_ai'])

config_di = dict(config_parser['Config_di'])

config_do = dict(config_parser['Config_do'])

config_ci = dict(config_parser['Config_ci'])

config_co = dict(config_parser['Config_co'])

config_all = dict(config_parser['Config_all'])

config_redis = dict(config_parser['Redis'])

config_mongodb = dict(config_parser['Mongodb'])

config_influxdb = dict(config_parser['Influxdb'])

config_usb = dict(config_parser['Usb'])

config_file = dict(config_parser['File'])

config_udp = dict(config_parser['Udp'])

config_api_mongodb = dict(config_parser['Api_mongodb'])

config_api_ni = dict(config_parser['Api_ni'])

config_api_usb = dict(config_parser['Api_usb'])

config_api_udp = dict(config_parser['Api_udp'])

config_api_file = dict(config_parser['Api_file'])

config_api_all = dict(config_parser['Api_all'])
############################################################################################################################################



########################################################## Data for post ####################################################################

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
        
data_di_dir = {
                    'stream': "stream_chan_di_dir",
                    'host': config_redis.get('host'),
                    'port': config_redis.get('port'),
                    'period': config_di.get('period'),
                    'sample_size': config_di.get('sample_size'),
                    'device': config_di.get('device'),
                    'lines': config_di.get('lines'),
                    'sleep':0.001,
                    'num_di': "7"

                    } 
        
data_di_vit = {
                    'stream': "stream_chan_di_vit",
                    'host': config_redis.get('host'),
                    'port': config_redis.get('port'),
                    'period': config_di.get('period'),
                    'sample_size': config_di.get('sample_size'),
                    'device': config_di.get('device'),
                    'lines': config_di.get('lines'),
                    'sleep':0.001,
                    'num_di': "6"

                    } 
        
data_di_syn = {
                    'stream': "stream_chan_di_syn",
                    'host': config_redis.get('host'),
                    'port': config_redis.get('port'),
                    'period': config_di.get('period'),
                    'sample_size': config_di.get('sample_size'),
                    'device': config_di.get('device'),
                    'lines': config_di.get('lines'),
                    'sleep':0.001,
                    'num_di': "5"

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
        
data_udp = {
                    'stream': config_udp.get('stream'),
                    'host': config_redis.get('host'),
                    'port': config_redis.get('port'),
                    'ip_port':config_udp.get('ip_port')
                    }
        
data_all = {

            'host': config_redis.get('host'),
            'port': config_redis.get('port'),
            'day': config_ai.get('day'),
            'month': config_ai.get('month'),
            'year': config_ai.get('year'),
            'hour': config_ai.get('hour'),
            'minute': config_ai.get('minute'),
            'seconds': config_ai.get('seconds'),
            'milliseconds': config_ai.get('milliseconds'),
            'sample_size': config_ai.get('sample_size'),
            'group': config_all.get('group'),
            'stream': config_all.get('stream'),
            'stream_ai': config_ai.get('stream'),
            'stream_dir': data_di_dir.get('stream'),
            'stream_vit': data_di_vit.get('stream'),
            'stream_syn': data_di_syn.get('stream'),
            'stream_udp': config_udp.get('stream') 

            }
        
data_mongo_all = {

            'db': config_all.get('db'),
            'group': config_all.get('group'),
            'collection_name': config_all.get('collection_name'),
            'stream': config_all.get('stream'),
            'url':'mongo', #config_mongodb.get('url'),
            'host': 'redis', #config_redis.get('host'),
            'port': config_redis.get('port'),
            'username': config_mongodb.get('username'),
            'password': config_mongodb.get('password'),
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
                    'username': config_mongodb.get('username'),
                    'password': config_mongodb.get('password'),
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
        
data_file_all = {

                    'stream': config_all.get('stream'),#str(config_redis.get('stream')),
                    'host': config_redis.get('host'),
                    'port': config_redis.get('port'),
                    'sample_size': config_ai.get('sample_size'),
                    'folder_path': config_file.get('folder_path2'),
                    'max_file': config_file.get('max_file'),
                    'group': config_file.get('group')

                    }

############################################################################################################################################





############################################################collecte AI ####################################################################

api_url_ai_loop = f"{config_api_ni.get('endpoint')}/api/read_ai_loop_to_redis"

api_url_ai_stop_loop = f"{config_api_ni.get('endpoint')}/api/stop_read_ai_loop_to_redis"
############################################################################################################################################





#############################################################Flashes #######################################################################

api_url_do_flashes = f"{config_api_ni.get('endpoint')}/api/write_do_flashes"

api_url_do_stop_flashes = f"{config_api_ni.get('endpoint')}/api/stop_flashes"
#############################################################################################################################################





############################################################### USB #########################################################################

api_url_usb_find = f"{config_api_usb.get('endpoint')}/api/usb/find"
        
api_url_usb_copy = f"{config_api_usb.get('endpoint')}/api/usb/copy_files"
#############################################################################################################################################






############################################################# File All ######################################################################

api_url_file_write_all = f"{config_api_file.get('endpoint')}/api/write_folder_all"

api_url_file_stop_write_all = f"{config_api_file.get('endpoint')}/api/stop_write_folder_all"
#############################################################################################################################################






############################################################# MongoDB All ###################################################################

api_url_mongo_write_all = f"{config_api_mongodb.get('endpoint')}/api/write_loop_all"

api_url_mongo_stop_write_all = f"{config_api_mongodb.get('endpoint')}/api/stop_write_loop_all"
##############################################################################################################################################






########################################################### Collecte All ######################################################################

api_url_all_stop = f"{config_api_all.get('endpoint')}/api/stop_write_to_redis"

api_url_all_loop = f"{config_api_all.get('endpoint')}/api/write_to_redis"
################################################################################################################################################





############################################################## UDP #############################################################################

api_url_udp_stop = f"{config_api_udp.get('endpoint')}/api/stop_read_packets_loop"

api_url_udp_loop = f"{config_api_udp.get('endpoint')}/api/read_packets_loop"
################################################################################################################################################






############################################################## Direction ########################################################################

api_url_di_dir_loop = f"{config_api_ni.get('endpoint')}/api/read_di_dir_loop_to_redis"

api_url_di_dir_stop_loop = f"{config_api_ni.get('endpoint')}/api/stop_read_di_dir_loop_to_redis"
#################################################################################################################################################






################################################################## Vitesse ######################################################################

api_url_di_vit_loop = f"{config_api_ni.get('endpoint')}/api/read_di_vit_loop_to_redis"

api_url_di_vit_stop_loop = f"{config_api_ni.get('endpoint')}/api/stop_read_di_vit_loop_to_redis"
#################################################################################################################################################





############################################################## synchronisation ##################################################################

api_url_di_syn_loop = f"{config_api_ni.get('endpoint')}/api/read_di_syn_loop_to_redis"

api_url_di_syn_stop_loop = f"{config_api_ni.get('endpoint')}/api/stop_read_di_syn_loop_to_redis"
#################################################################################################################################################
            

def get_pression(url, data):

    resp = requests.post(url, json=data)

    while resp.status_code == 200:

        r = resp.json()['data']

        if r['values'][0]:
            break

        resp = requests.post(url, json=data)
    
    return True




def api_post(api_url, data):

    try:

        response = request.post(api_url, json=data)

        if response.status_code == 200:

            return jsonify({"status" : response.status_code,"values" : response.json()})
        
        else:

            return jsonify({"status" : response.status_code,"values" : f"Echec de la requêtte : {response.status_code} - {response.text}"})
        

    except requests.exceptions.RequestException as e:

        return jsonify({"status" : response.status_code,"values":f"Exception level : {e}"})
    

def api_get(api_url):

    try:

        response = request.get(api_url)

        if response.status_code == 200:

            return jsonify({"status" : response.status_code,"values" : response.json()})
        
        else:

            return jsonify({"status" : response.status_code,"values" : f"Echec de la requêtte : {response.status_code} - {response.text}"})
        

    except requests.exceptions.RequestException as e:

        return jsonify({"status" : response.status_code,"values":f"Exception level : {e}"})








STOP_EVENT_COLLECT_UDP = [False]
BACKGROUND_UDP=None

STOP_EVENT_COLLECT = [False]
BACKGROUND=None

app = Flask(__name__)



    

def collect_data(stop_event,udp:UDPHandler, redis: Redis, config):
    global STOP_EVENT_COLLECT

    while not STOP_EVENT_COLLECT[0]:

        message = {}
        message['udp'] =  udp.receive_packet()
        message['timestamp'] = Date.utcnow().isoformat(sep=" ")
       

        redis.xadd(name=config.get('stream'), fields=message)
    
    udp.close()    
    redis.close()

    
def collect_data_from_udp(stop_event,udp:UDPHandler, redis: Redis, config):
    global STOP_EVENT_COLLECT_UDP

    while not STOP_EVENT_COLLECT_UDP[0]:

        message = {}
        message['udp'] =  udp.receive_packet()
        message['timestamp'] = Date.utcnow().isoformat(sep=" ")         

        redis.xadd(name=config.get('stream'), fields=message)

        if 'START' in data_udp.split(';'):

            # Collect data from AI

            data = api_post(api_url_ai_loop, json=data_ai)

            pprint.pprint(data)


            # Collect datas Direction
                      
            data = api_post(api_url_di_dir_loop, json=data_di_dir)           
            
            pprint.pprint(data)

            # Collect datas Vitesse
                
            data = api_post(api_url_di_vit_loop, json=data_di_vit)

            pprint.pprint(data)

            print(f"Data :{data}")

            # Collect datas synchronisation
            
            data = api_post(api_url_di_syn_loop, json=data_di_syn)

            pprint.pprint(data)                
            

            # Flashes record

            data_do['state'] = "record"

            data = api_post(api_url_do_flashes, json=data_do)

            pprint.pprint(data)

                      

        elif 'STOP' in data_udp.split(';'):

            # STOP Collect data from AI

            data = api_get(api_url_ai_stop_loop)

            pprint.pprint(data)


            # STOP Collect datas Direction
                      
            data = api_get(api_url_di_dir_stop_loop)           
            
            pprint.pprint(data)


            # STOP Collect datas Vitesse
                
            data = api_get(api_url_di_vit_stop_loop)

            pprint.pprint(data)


            # STOP Collect datas synchronisation
            
            data = api_get(api_url_di_syn_stop_loop)

            pprint.pprint(data)


                
            #Stop flashes

            data = api_get(api_url_do_stop_flashes)

            pprint.pprint(data)            


            # Get Usb  

            response = api_get(api_url_usb_find)

            # Vérifier si la requête a réussi
            if response['status'] == 200:

                pprint.pprint(response)

                data_usb['usb_mount_path'] = response['values']['usb_mount_path']

                # Flashes wait copy to usb

                data_do['state'] = "wait_usb"

                data = api_post(api_url_do_flashes, json=data_do)

                pprint.pprint(data)
                
                # Copy files to USB

                response = api_post(api_url_usb_copy, json=data_usb)

                pprint.pprint(response)
                    
                #Stop flashes

                response = api_get(api_url_do_stop_flashes)
            
                pprint.pprint(response)

                    
                #Mode USB
                data_do['state'] = "USB"

                response = api_post(api_url_do_flashes, json=data_do)

                pprint.pprint(response)
                 

            else:

                pprint.pprint(response)

            STOP_EVENT_COLLECT_UDP[0] = True

            break
              

        elif 'INIT' in data_udp.split(';'):

            #Start 
            data_do['state'] = "start"

            response = api_post(api_url_do_flashes, json=data_do)

            pprint.pprint(response)

            # Usb  Mode
            response = api_get(api_url_usb_find)

            # Vérifier si la requête a réussi
            if response['status'] == 200:

                data_do['state'] = "USB"

                response = api_post(api_url_do_flashes, json=data_do)

                pprint.pprint(response)

            else:

                pprint.pprint(response)


        elif 'EVENT' in data_udp.split(';'):

            pass

        elif 'HDR' in data_udp.split(';'):

            pass

        else:

            pass




@app.route('/api/read_UDP_packets_loop', methods=['POST'])
def api_read_udp():

    try:
        # Récupérer les données JSON de la requête POST
        data = request.get_json()

        # Vérifier si les données sont valides (vous pouvez ajouter plus de validation ici)
        if 'host' not in data or 'port' not in data:
            return jsonify({'error': f"Les données doivent contenir l'adresse ip du serveur et le port."}), 400

        udp = UDPHandler(target_ip = data['host'], target_port= int(data['port']))


        # Créez un thread pour la tâche en arrière-plan
        BACKGROUND_UDP = threading.Thread(target=collect_data_from_udp, args=(STOP_EVENT_COLLECT_UDP, udp))
        # Démarrez le thread en arrière-plan
        BACKGROUND_UDP.start()


        BACKGROUND_UDP.join()


        # Répondre avec un message de succès
        return jsonify({'message': 'Données ajoutées avec succès.'}), 200

    except Exception as e:
        return jsonify({'error': 'Une erreur s\'est produite lors du traitement de la requête.'}), 500
    

@app.route('/api/read_packets_loop', methods=['POST'])
def api_read():

    global BACKGROUND

    try:
        # Récupérer les données JSON de la requête POST
        data = request.get_json()

        # # Vérifier si les données sont valides (vous pouvez ajouter plus de validation ici)
        # if 'host' not in data or 'port' not in data:
        #     return jsonify({'error': f"Les données doivent contenir l'adresse ip du serveur et le port."}), 400
        redis_conn = Redis(host=data.get('host'), port=int(data.get('port')))

        udp = UDPHandler(target_port= int(data['ip_port']))

        config = {}
        config['stream'] = data.get('stream')


        # Créez un thread pour la tâche en arrière-plan
        BACKGROUND = threading.Thread(target=collect_data, args=(STOP_EVENT_COLLECT, udp, redis_conn, config))
        # Démarrez le thread en arrière-plan
        BACKGROUND.start()

        # Répondre avec un message de succès
        return jsonify({'message': 'Données (UDP) ajoutées avec succès.'}), 200

    except Exception as e:
        return jsonify({'error': 'Une erreur s\'est produite lors du traitement de la requête.'}), 500

# Route pour écrire des données dans InfluxDB
@app.route('/api/stop_read_packets_loop', methods=['GET'])
def api_stop_write_to_mongodb():

    global STOP_EVENT_COLLECT 
    global BACKGROUND

    try:

        STOP_EVENT_COLLECT[0] = True 

        BACKGROUND.join()

        return jsonify({'Message': "Stop de la sauvegarde(udp)"}), 200
    
    except Exception as ex:
        return jsonify({'Message': f"Un problème à l'arret (udp) : {ex}"}), 500 


# Route pour envoyer et recevoir un paquet UDP
@app.route('/api/udp', methods=['POST'])
def udp_communication():
    try:
        data = request.get_json()
        action = data.get('action')
        udp_handler = UDPHandler(target_ip=data.get('host') , target_port=int(data.get('port')))

        if action == 'send':
            message = data.get('message')
            if message:
                udp_handler.send_packet(data=message)
                udp_handler.close()
                return jsonify({'message': 'Paquet UDP envoyé avec succès.'}), 200
            else:
                return jsonify({'error': 'Le message doit être spécifié dans le corps de la requête JSON.'}), 400
        elif action == 'receive':
            received_data = udp_handler.receive_packet()
            if received_data:
                udp_handler.close()
                return jsonify({'data': received_data}), 200
            else:
                udp_handler.close()
                return jsonify({'error': 'Aucune donnée reçue.'}), 404
        else:
            return jsonify({'error': 'L\'action spécifiée n\'est pas valide.'}), 400

    except Exception as e:
        return jsonify({'error': 'Une erreur s\'est produite lors du traitement de la requête.'}), 500


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


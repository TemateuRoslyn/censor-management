import threading
import os
import requests 

from flask import request,jsonify, Flask
from redis import Redis, RedisError
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from udp_protocol import UDPHandler

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

config_parser = ConfigParser()

config_parser.read(os.environ["CONFIG_PATH"])

config = dict(config_parser['Config'])

config_redis = dict(config_parser['Redis'])

config_mongodb = dict(config_parser['Mongodb'])

config_influxdb = dict(config_parser['Influxdb'])

config_usb = dict(config_parser['Usb'])

config_api_mongodb = dict(config_parser['Api_mongodb'])

config_api_ni = dict(config_parser['Api_ni'])

config_api_usb = dict(config_parser['Api_usb'])

config_api_udp = dict(config_parser['Api_udp'])


app = Flask(__name__)


STOP_EVENT_COLLECT_UDP = [False]

def request_post(api_url, data):

    try:
        response = request.post(api_url, json=data)

        if response.status_code == 200:
            return jsonify({"Données reçues" : response.json()})

    except requests.exceptions.RequestException as e:
        return f"Erreur lors de la requête : {e}"



    
def collect_data_from_udp(stop_event,udp:UDPHandler):

    while not stop_event[0]:

        data_udp =  udp.receive_packet()

        if 'START' in data_udp.split(';'):

            try:

                data_to_ni_ai = {
                    'stream': "stream_chan_ai",#str(config_redis.get('stream')),
                    'host': config_redis.get('host'),
                    'port': config_redis.get('port'),
                    'period': config.get('period'),
                    'rate': config.get('rate'),
                    'buffer_size': config.get('buffer_size'),
                    'sample_size': config.get('sample_size'),
                    'device': config.get('device'),
                    'channels': ["ai0", "ai1", "ai2", "ai3", "ai4", "ai5", "ai6", "ai7"]
                    }
                
                api_url_ni_ai = f"{config_api_ni.get('endpoint')}/api/read_ai_loop_to_redis"

                # Créez un thread pour la tâche en arrière-plan
                ni_thread_ai = threading.Thread(target=request_post, args=(api_url_ni_ai, data_to_ni_ai))
                # Démarrez le thread en arrière-plan
                ni_thread_ai.start()


            except requests.exceptions.RequestException as e:
                print(f"Erreur lors de la requête : {e}")
            

        elif 'STOP' in data_udp.split(';'):

            request.get()

            stop_event[0]=True

        elif 'INIT' in data_udp.split(';'):

            request.get()

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
        background_thread = threading.Thread(target=collect_data_from_udp, args=(STOP_EVENT_COLLECT_UDP, udp,))
        # Démarrez le thread en arrière-plan
        background_thread.start()


        background_thread.join()


        # Répondre avec un message de succès
        return jsonify({'message': 'Données ajoutées avec succès.'}), 201

    except Exception as e:
        return jsonify({'error': 'Une erreur s\'est produite lors du traitement de la requête.'}), 500
    

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


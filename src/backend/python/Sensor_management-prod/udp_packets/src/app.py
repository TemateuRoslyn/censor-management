import threading
from flask import request,jsonify, Flask
from redis import Redis, RedisError
from udp_packets import UDPHandler

app = Flask(__name__)


STOP_EVENT_COLLECT_UDP = [False]


    
def collect_data_from_udp(stop_event,udp:UDPHandler):

    while not stop_event[0]:

        data_udp =  udp.receive_packet()

        if 'START' in data_udp.split(';'):

            request.post()

        elif 'STOP' in data_udp.split(';'):

            request.get()

            stop_event[0]=True

        elif 'INIT' in data_udp.split(';'):

            request.get()

        else:

            pass




@app.route('/api/read_UDP_packets', methods=['POST'])
def api_read_udp():

    try:
        # Récupérer les données JSON de la requête POST
        data = request.get_json()

        # Vérifier si les données sont valides (vous pouvez ajouter plus de validation ici)
        if 'host_udp' not in data or 'port_udp' not in data:
            return jsonify({'error': f"Les données doivent contenir l'adresse ip du serveur et le port."}), 400

        udp = UDPHandler(target_ip = data['host_udp'], target_port= int(data['port_udp']))


        # Créez un thread pour la tâche en arrière-plan
        background_thread = threading.Thread(target=collect_data_from_udp, args=(STOP_EVENT_COLLECT_UDP, udp,))
        # Démarrez le thread en arrière-plan
        background_thread.start()


        background_thread.join()


        # Répondre avec un message de succès
        return jsonify({'message': 'Données ajoutées avec succès.'}), 201

    except Exception as e:
        return jsonify({'error': 'Une erreur s\'est produite lors du traitement de la requête.'}), 500

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5001)
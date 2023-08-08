import numpy as np
import time
import threading
import os

from json import JSONEncoder
from flask import Flask, jsonify, request
from redis import Redis, RedisError
from ni_channels import ChannelsAI, ChannelCI, ChannelCO, ChannelDI, ChannelDO

# Lire la valeur des variables d'environnement
debug_val = os.getenv("debug", "true")  # La variable "debug" sera soit True ou False (str)
host_val = os.getenv("host", "0.0.0.0")    # La variable "host" contiendra l'adresse (str)
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


app = Flask(__name__)

STOP_EVENT_COLLECT_CHAN_AI = [False]
CHANGE_STATE_CHAN_DO = [False]
BACKGROUND_THREAD_AI = None
BACKGROUND_THREAD_DO = None
BACKGROUND_THREAD_REDIS = None
QUEUE_AI = []


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)
    
def collect_data_from_chan_ai(stop_event,channel_ai:ChannelsAI, collect_time: float = 10.0):

    global QUEUE_AI
    global STOP_EVENT_COLLECT_CHAN_AI
   
    if collect_time > 0 :

        start = time.process_time()

        while (time.process_time() - start) <= collect_time :

            QUEUE_AI.append(channel_ai.read_datas())
        
        channel_ai.close_task()

    elif collect_time < 0 :

        while not STOP_EVENT_COLLECT_CHAN_AI[0]:

            QUEUE_AI.append(channel_ai.read_datas())

        channel_ai.close_task()

    else:
        raise(f"Le temps de collect est null {collect_time}")
    
def data_to_redis(stop_event,obj_redis:Redis, stream:str, channels):

    global QUEUE_AI
    global STOP_EVENT_COLLECT_CHAN_AI

    while not STOP_EVENT_COLLECT_CHAN_AI[0] or (len(QUEUE_AI) > 0):

        if len(QUEUE_AI) > 0 :

            data = {}  
            
            samples = QUEUE_AI.pop(0)          

            tab = np.array(samples['values'])

            i = 0
            for ch in channels:
                data[ch] = tab[i,:].__str__()
                i+=1
            
            data['time_start'] = samples['time_start']
            data['time_stop'] = samples['time_stop']
            data['sample_rate'] = str(samples['sample_rate'])
            data['channels'] = ' '.join(samples['channels'])

            obj_redis.xadd(name=stream, fields=data)
    
    obj_redis.close()

def flashes(change_state, channel_do:ChannelDO, state, off_state, period=0.25):
    global CHANGE_STATE_CHAN_DO

    while not CHANGE_STATE_CHAN_DO[0]:

        channel_do.write_data(state)

        time.sleep(period)

        channel_do.write_data(off_state)

        time.sleep(period)

    channel_do.close_task()



@app.route('/api/read_ai_loop_to_redis', methods=['POST'])
def api_read_ai_loop_to_redis():
    # Assurez-vous d'avoir correctement configuré la connexion à Redis dans cette route
    global QUEUE_AI
    global BACKGROUND_THREAD_AI
    global BACKGROUND_THREAD_REDIS

    try:

        data = request.get_json()

        stream_chan_ai = data.get('stream')
        redis_host = data.get('host')
        redis_port = int(data.get('port'))
        collect_time = float(data.get('period'))
        rate = int(data.get('rate'))
        buffer_size = int(data.get('buffer_size'))
        sample_per_chan = int(data.get('sample_size'))
        device= data.get('device')
        channels =data.get('channels')

        obj_chan = ChannelsAI(rate=rate, buffer_size=buffer_size, sample_per_chan=sample_per_chan, device=device, channels=channels)

        obj_chan.init_task()

        obj_redis = Redis(host=redis_host, port=redis_port)


        # Créez un thread pour la tâche en arrière-plan
        BACKGROUND_THREAD_AI = threading.Thread(target=collect_data_from_chan_ai, args=(STOP_EVENT_COLLECT_CHAN_AI, obj_chan, collect_time))
        # Démarrez le thread en arrière-plan
        BACKGROUND_THREAD_AI.start()

        time.sleep(2)

        BACKGROUND_THREAD_REDIS = threading.Thread(target=data_to_redis, args=(STOP_EVENT_COLLECT_CHAN_AI, obj_redis,stream_chan_ai, channels ))

        BACKGROUND_THREAD_REDIS.start()            

        return jsonify({'Message': f"Début de la collecte"}), 200
    
    except Exception as e:
        obj_redis.close()
        obj_chan.close_task()
        return jsonify({'Message': f"Une erreur s\'est produite lors du traitement de la requete :  {e} ."}), 500




@app.route('/api/stop_read_ai_loop_to_redis', methods=['GET'])
def api_stop_read_ai_loop_to_redis():

    global STOP_EVENT_COLLECT_CHAN_AI
    global BACKGROUND_THREAD_AI
    global BACKGROUND_THREAD_REDIS

    try:

        STOP_EVENT_COLLECT_CHAN_AI[0]=True
        BACKGROUND_THREAD_AI.join()
        BACKGROUND_THREAD_REDIS.join()

        return jsonify({'message': f"Arrêt de la collecte des AI en boucle"}), 200
    except Exception as ex:
        return jsonify({'message': f"Un problème à l'arret : {ex}"}), 500


@app.route('/api/read_ai_to_redis', methods=['POST'])
def api_read_ai_to_redis():
    # Assurez-vous d'avoir correctement configuré la connexion à Redis dans cette route

    try:

        data = request.get_json()

        stream_chan_ai = data.get('stream')
        redis_host = data.get('host')
        redis_port = int(data.get('port'))
        rate = int(data.get('rate'))
        buffer_size = int(data.get('buffer_size'))
        sample_per_chan = int(data.get('sample_size'))
        device = data.get('device')
        channels =data.get('channels')

        obj_chan = ChannelsAI(rate=rate, buffer_size=buffer_size, sample_per_chan=sample_per_chan, device=device, channels=channels)

        obj_chan.init_task()

        obj_redis = Redis(host=redis_host, port=redis_port)

        obj_chan.read_datas()

        last_id = 0

        while len(obj_chan.queue) > 0 :

            data = {}

            samples = obj_chan.queue.pop(0)

            tab = np.array(samples['values'])

            i = 0
            for ch in channels:
                data[ch] = tab[i,:].__str__()
                i+=1
            
            data['time_start'] = samples['time_start']
            data['time_stop'] = samples['time_stop']
            data['sample_rate'] = str(samples['sample_rate'])
            data['channels'] = ' '.join(samples['channels'])

            last_id = obj_redis.xadd(name=stream_chan_ai, fields=data)

        obj_chan.close_task()

        return jsonify({"id": f"{last_id}"}), 200
    
    except Exception as e:
        obj_chan.close_task()
        return jsonify({'error': f"Une erreur s\'est produite lors du traitement de la requête : \n {e} ."}), 500





@app.route('/api/read_ai', methods=['POST'])
def api_read_ai():
    # Assurez-vous d'avoir correctement configuré la connexion à Redis dans cette route

    try:

        data = request.get_json()

        rate = int(data.get('rate'))
        buffer_size = int(data.get('buffer_size'))
        sample_per_chan = int(data.get('sample_size'))
        device=str(data.get('device'))
        channels =data.get('channels')

        obj_chan = ChannelsAI(rate=rate, buffer_size=buffer_size, sample_per_chan=sample_per_chan, device=device, channels=channels)

        obj_chan.init_task()

        samples = obj_chan.read_datas()
        
        obj_chan.close_task()
        

        return jsonify({'data': f"{samples}"}), 200
    
    except Exception as e:
        return jsonify({'error': f"Une erreur s\'est produite lors du traitement de la requête : \n {e} ."}), 500



@app.route('/api/read_di', methods=['POST'])
def api_read_di():

    try :

        data = request.get_json()

        obj_chan = ChannelDI(lines=data.get('lines'), device=data.get('device'), num_di=data.get('num_di'), sample_size=int(data.get('sample_size')))

        obj_chan.init_task()

        data = obj_chan.read_data()

        obj_chan.close_task()

        return jsonify({'data': data}) , 200
    
    except Exception as e:
        return jsonify({'error': 'Une erreur s\'est produite lors du traitement de la requête.'}), 500
    

@app.route('/api/write_do', methods=['POST'])
def api_write_do():

    try :

        data = request.get_json()

        obj_chan = ChannelDO(lines=data.get('lines'), device=data.get('device'), num_do=data.get('num_do'))

        obj_chan.init_task()

        t = obj_chan.write_data(data=data.get('value'))

        obj_chan.close_task()

        return jsonify({'write': f"{t}"}) , 200
    
    except Exception as e:
        return jsonify({'error': f"Une erreur s\'est produite lors du traitement de la requête : \n {e} ."}), 500


@app.route('/api/write_do_flashes', methods=['POST'])
def api_write_do_flashes():
    global BACKGROUND_THREAD_DO

    try :

        data = request.get_json()

        obj_chan = ChannelDO(lines=data.get('lines'), device=data.get('device'), num_do=data.get('num_do'))

        obj_chan.init_task()

        if (data.get('state') == "record") or (data.get('state') == "Record"):

            BACKGROUND_THREAD_DO = threading.Thread(target=flashes, args=(CHANGE_STATE_CHAN_DO, obj_chan,[True,True,True,False], [False,False,True,False],))
            BACKGROUND_THREAD_DO.start()

            return jsonify({"Message": f"Changement d'état à {data.get('state')}"}), 200
        
        elif (data.get('state') == "wait_usb") or (data.get('state') == "Wait_USB"):

            BACKGROUND_THREAD_DO = threading.Thread(target=flashes, args=(CHANGE_STATE_CHAN_DO, obj_chan,[True,True,True,True], [True,True,False,False],))
            BACKGROUND_THREAD_DO.start()

            return jsonify({"Message": f"Changement d'état à {data.get('state')}"}), 200
        
        elif (data.get('state') == "Stop") or (data.get('state') == "stop"):

            obj_chan.write_data([True,True,True,True])

            obj_chan.close_task()

            return jsonify({"Message": f"Changement d'état à {data.get('state')}"}), 200
        
        elif (data.get('state') == "start") or (data.get('state') == "start"):

            obj_chan.write_data([True,False,False,False])

            obj_chan.close_task()

            return jsonify({"Message": f"Changement d'état à {data.get('state')}"}), 200
        
        elif (data.get('state') == "usb") or (data.get('state') == "USB"):

            obj_chan.write_data([True,False,True,False])

            obj_chan.close_task()

            return jsonify({"Message": f"Changement d'état à {data.get('state')}"}), 200
        
        elif (data.get('state') == "pb") or (data.get('state') == "pb"):

            obj_chan.write_data([False,True,True,False])

            obj_chan.close_task()

            return jsonify({"Message": f"Changement d'état à {data.get('state')}"}), 200
        
        else :
            return jsonify({'State': f"{data.get('state')}"}) , 200
    
    except Exception as e:
        return jsonify({'error': f"Une erreur s\'est produite lors du traitement de la requête : \n {e} ."}), 500


@app.route('/api/stop_flashes', methods=['GET'])
def api_stop_flashes():

    global BACKGROUND_THREAD_DO
    global CHANGE_STATE_CHAN_DO

    try:

        CHANGE_STATE_CHAN_DO[0] = True
        BACKGROUND_THREAD_DO.join()

        return jsonify({'message': f"stop flashes"}), 200
    except Exception as ex:
        return jsonify({'message': f"Un problème à l'arret du flashes : {ex}"}), 500


@app.route("/api/read_ci", methods=['POST'])
def api_read_ci():
    try:

        data = request.get_json()

        obj_chan = ChannelCI(channel=data.get('channel'), device=data.get('device'), sample_size=data.get('sample_size'))

        if data.get('type') == "pulse_freq" :

            obj_chan.init_task_pulse_freq()

        elif data.get('type') == "pulse_ticks" :

            obj_chan.init_task_pulse_ticks()

        elif data.get('type') == "pulse_time" :

            obj_chan.init_task_pulse_time()
        
        elif data.get('type') == "period" :

            obj_chan.init_task_period()

        elif data.get('type') == "freq" :

            obj_chan.init_task_freq()
        
        elif data.get('type') == "two_edge" :

            obj_chan.init_task_two_edge()

        elif data.get('type') == "gps_timestamp" :

            obj_chan.init_task_gps_timestamp()

        elif data.get('type') == "pulse" :

            obj_chan.init_task_pulse()

        elif data.get('type') == "semi_period" :

            obj_chan.init_task_semi_period()
        
        else :

            return jsonify({'error': 'Le type de compteur doit être spécifiée dans le corps de la requête JSON.'}), 400
        
        data = obj_chan.read_data()

        obj_chan.close_task()

        return jsonify({'data': f"{data}"}), 200

    except Exception as e:

        return jsonify({'error': f"Une erreur s\'est produite lors du traitement de la requête : \n {e} ."}), 500

 

# @app.route("/api/read_ci_to_redis", methods=['POST'])
# def api_read_ci_to_redis():
#     try:

#         data = request.get_json()

#         obj_chan = ChannelCI(channel=data.get('channel'), device=data.get('device'), sample_size=data.get('sample'))

#         if data.get('type') == "pulse_freq" :

#             obj_chan.init_task_pulse_freq()

#         elif data.get('type') == "pulse_ticks" :

#             obj_chan.init_task_pulse_ticks()

#         elif data.get('type') == "pulse_time" :

#             obj_chan.init_task_pulse_time()
        
#         elif data.get('type') == "period" :

#             obj_chan.init_task_period()

#         elif data.get('type') == "freq" :

#             obj_chan.init_task_freq()
        
#         elif data.get('type') == "two_edge" :

#             obj_chan.init_task_two_edge()

#         elif data.get('type') == "gps_timestamp" :

#             obj_chan.init_task_gps_timestamp()
        
#         else :

#             return jsonify({'error': 'Le type de compteur doit être spécifiée dans le corps de la requête JSON.'}), 400
        
#         data = obj_chan.read_data()


#         obj_chan.close_task()

#         return jsonify({'data': data}), 200

#     except Exception as e:

#         return jsonify({'error': f"Une erreur s\'est produite lors du traitement de la requête : \n {e} ."}), 500


@app.route("/api/read_ci_to_redis", methods=['POST'])
def api_read_ci_to_redis():
    try:

        data = request.get_json()

        obj_chan = ChannelCI(channel=data.get('channel'), device=data.get('device'), sample_size=data.get('sample_size'))

        obj_redis = Redis(host=data.get('host'), port=int(data.get('port')))

        if data.get('type') == "pulse_freq" :

            obj_chan.init_task_pulse_freq()

        elif data.get('type') == "pulse_ticks" :

            obj_chan.init_task_pulse_ticks()

        elif data.get('type') == "pulse_time" :

            obj_chan.init_task_pulse_time()
        
        elif data.get('type') == "period" :

            obj_chan.init_task_period()

        elif data.get('type') == "freq" :

            obj_chan.init_task_freq()
        
        elif data.get('type') == "two_edge" :

            obj_chan.init_task_two_edge()

        elif data.get('type') == "gps_timestamp" :

            obj_chan.init_task_gps_timestamp()

        elif data.get('type') == "pulse" :

            obj_chan.init_task_pulse()

        elif data.get('type') == "semi_period" :

            obj_chan.init_task_semi_period()
        
        else :

            return jsonify({'error': 'Le type de compteur doit être spécifiée dans le corps de la requête JSON.'}), 400
        
        data = obj_chan.read_data()

        last_id = obj_redis.xadd(name=data.get('stream'), fields=data)

        obj_chan.close_task()

        return jsonify({'id': f"{last_id}", 'data': f"{data}"}), 200

    except Exception as e:

        return jsonify({'error': f"Une erreur s\'est produite lors du traitement de la requête : \n {e} ."}), 500


@app.route("/api/write_co", methods=['POST'])
def api_write_co():
    try:

        data = request.get_json()

        obj_chan = ChannelCO(channel=data.get('channel'), device=data.get('device'), sample_size=data.get('sample_size'))

        if data.get('type') == "pulse_freq" :

            obj_chan.init_task_pulse_freq()
            obj_chan.write_data_CtrFreq(freq=float(data.get('freq')))

        elif data.get('type') == "pulse_ticks" :

            obj_chan.init_task_pulse_ticks()
            obj_chan.write_data_CtrTick(high_tick=float(data.get('high_tick')), low_tick=float(data.get('low_tick')))

        elif data.get('type') == "pulse_time" :

            obj_chan.init_task_pulse_time()
            obj_chan.write_data_CtrTime(high_time=float(data.get('high_time')), low_time=float(data.get('low_time')))
                
        else :

            return jsonify({'error': 'Le type de compteur doit être spécifiée dans le corps de la requête JSON.'}), 400
        
       
        obj_chan.close_task()

        return jsonify({'data': f"{data}"}), 200

    except Exception as e:

        return jsonify({'error': f"Une erreur s\'est produite lors du traitement de la requête : \n {e} ."}), 500


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

    









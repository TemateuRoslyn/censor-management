import pandas as pd
import numpy as np
import time
import threading

from json import JSONEncoder
from flask import Flask, jsonify, request
from redis import Redis, RedisError
from ni_channels import ChannelsAI, ChannelCI, ChannelCO, ChannelDI, ChannelDO

app = Flask(__name__)

STOP_EVENT_COLLECT_CHAN_AI = [False]


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)
    
def collect_data_from_chan_ai(stop_event,channel_ai:ChannelsAI, collect_time: float = 10.0):

   
    if collect_time > 0 :

        start = time.process_time()

        while (time.process_time() - start) <= collect_time :

            channel_ai.read_datas()

    elif collect_time < 0 :

        while not stop_event[0]:

            channel_ai.read_datas()

    else:
        raise(f"Le temps de collect est null {collect_time}")



@app.route('/api/read_data_chan_ai_to_redis_get', methods=['GET'])
def api_read_data_chan_ai_to_redis_get():
    # Assurez-vous d'avoir correctement configuré la connexion à Redis dans cette route
    stream_chan_ai = str(request.args.get('stream',default="stream_chan_ai"))
    redis_host = str(request.args.get('host',default="127.0.0.1"))
    redis_port = int(request.args.get('port', 6973))
    collect_time = float(request.args.get('period', 1.0))
    rate = int(request.args.get('rate', 15000))
    buffer_size = int(request.args.get('buffer_size', 1000000))
    sample_per_chan = int(request.args.get('sample_size', 1000))
    device=str(request.args.get('device',default="Dev1"))
    channels = request.args.getlist('channels', default=["ai0", "ai1", "ai2", "ai3", "ai4", "ai5", "ai6", "ai7"])

    obj_chan = ChannelsAI(rate=rate, buffer_size=buffer_size, sample_per_chan=sample_per_chan, device=device, channels=channels)

    obj_chan.init_task()

    obj_redis = Redis(host=redis_host, port=redis_port)


    # Créez un thread pour la tâche en arrière-plan
    background_thread = threading.Thread(target=collect_data_from_chan_ai, args=(STOP_EVENT_COLLECT_CHAN_AI, obj_chan, collect_time))
    # Démarrez le thread en arrière-plan
    background_thread.start()

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

    
    background_thread.join()

    return jsonify({'id': last_id})



@app.route('/api/read_ai_loop_to_redis', methods=['POST'])
def api_read_ai_loop_to_redis():
    # Assurez-vous d'avoir correctement configuré la connexion à Redis dans cette route

    try:

        data = request.get_json()

        stream_chan_ai = str(data.get('stream'))
        redis_host = str(data.get('host'))
        redis_port = int(data.get('port'))
        collect_time = float(data.get('period'))
        rate = int(data.get('rate'))
        buffer_size = int(data.get('buffer_size'))
        sample_per_chan = int(data.get('sample_size'))
        device=str(data.get('device'))
        channels =data.get('channels')

        obj_chan = ChannelsAI(rate=rate, buffer_size=buffer_size, sample_per_chan=sample_per_chan, device=device, channels=channels)

        obj_chan.init_task()

        obj_redis = Redis(host=redis_host, port=redis_port)


        # Créez un thread pour la tâche en arrière-plan
        background_thread = threading.Thread(target=collect_data_from_chan_ai, args=(STOP_EVENT_COLLECT_CHAN_AI, obj_chan, collect_time))
        # Démarrez le thread en arrière-plan
        background_thread.start()

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
        
        background_thread.join()

        return jsonify({'id': last_id}), 200
    
    except Exception as e:
        return jsonify({'error': f"Une erreur s\'est produite lors du traitement de la requête : \n {e} ."}), 500




@app.route('/api/stop_read_ai_loop_to_redis', methods=['GET'])
def api_stop_read_ai_loop_to_redis():

    STOP_EVENT_COLLECT_CHAN_AI[0]=True


@app.route('/api/read_ai_to_redis', methods=['POST'])
def api_read_ai_to_redis():
    # Assurez-vous d'avoir correctement configuré la connexion à Redis dans cette route

    try:

        data = request.get_json()

        stream_chan_ai = str(data.get('stream'))
        redis_host = str(data.get('host'))
        redis_port = int(data.get('port'))
        rate = int(data.get('rate'))
        buffer_size = int(data.get('buffer_size'))
        sample_per_chan = int(data.get('sample_size'))
        device=str(data.get('device'))
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

        return jsonify({'id': last_id}), 200
    
    except Exception as e:
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
        

        return jsonify({'data': samples}), 200
    
    except Exception as e:
        return jsonify({'error': f"Une erreur s\'est produite lors du traitement de la requête : \n {e} ."}), 500



@app.route('/api/read_di', methods=['POST'])
def api_read_di():

    try :

        data = request.get_json()

        obj_chan = ChannelDI(lines=data.get('lines'), device=data.get('device'), num_di=data.get('num_di'), sample_size=int(data.get('sample')))

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

        obj_chan = ChannelDO(lines=data.get('lines'), device=data.get('device'), num_di=data.get('num_di'))

        obj_chan.init_task()

        t = obj_chan.write_data(data=data.get('value'))

        obj_chan.close_task()

        return jsonify({'write': t}) , 200
    
    except Exception as e:
        return jsonify({'error': f"Une erreur s\'est produite lors du traitement de la requête : \n {e} ."}), 500


@app.route("/api/read_ci", methods=['POST'])
def api_read_ci():
    try:

        data = request.get_json()

        obj_chan = ChannelCI(channel=data.get('channel'), device=data.get('device'), sample_size=data.get('sample'))

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

        return jsonify({'data': data}), 200

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

        obj_chan = ChannelCI(channel=data.get('channel'), device=data.get('device'), sample_size=data.get('sample'))

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

        return jsonify({'id': last_id, 'data': data}), 200

    except Exception as e:

        return jsonify({'error': f"Une erreur s\'est produite lors du traitement de la requête : \n {e} ."}), 500


@app.route("/api/write_co", methods=['POST'])
def api_write_co():
    try:

        data = request.get_json()

        obj_chan = ChannelCO(channel=data.get('channel'), device=data.get('device'), sample_size=data.get('sample'))

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

        return jsonify({'data': data}), 200

    except Exception as e:

        return jsonify({'error': f"Une erreur s\'est produite lors du traitement de la requête : \n {e} ."}), 500


if __name__ == '__main__':

    from waitress import serve
    debug = True

    if debug :
        app.run(host='0.0.0.0', port=5000, debug=debug)
    else :
        serve(app, host='0.0.0.0', port=5000)
    









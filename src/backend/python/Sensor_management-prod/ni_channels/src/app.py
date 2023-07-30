import pandas as pd
import numpy as np
import time
import os
import threading

from json import JSONEncoder
from flask import Flask, jsonify, request
from redis import Redis, RedisError
from ni_channels import ChannelsAI

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



@app.route('/api/read_data_chan_ai_to_redis', methods=['POST'])
def api_read_data_chan_ai_to_redis():
    # Assurez-vous d'avoir correctement configuré la connexion à Redis dans cette route

    data = request.get_json()

    stream_chan_ai = str(data['stream'])
    redis_host = str(data['host'])
    redis_port = int(data['port'])
    collect_time = float(data['period'])
    rate = int(data['rate'])
    buffer_size = int(data['buffer_size'])
    sample_per_chan = int(data['sample_size'])
    device=str(data['device'])
    channels =data['channels']

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




@app.route('/api/stop_read_data_chan_ai_to_redis', methods=['GET'])
def api_stop_read_data_chan_ai_to_redis():

    STOP_EVENT_COLLECT_CHAN_AI[0]=True





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    









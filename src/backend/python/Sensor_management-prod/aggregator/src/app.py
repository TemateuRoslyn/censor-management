import os
import threading
import pandas as pd
import numpy as np

from flask import Flask, request, jsonify
from datetime import datetime as Date
from redis_stream import RedisStreamReader
from redis import Redis



# Lire la valeur des variables d'environnement
debug_val = os.getenv("debug","true")  # La variable "debug" sera soit True ou False (str)
host_val = os.getenv("host","0.0.0.0")    # La variable "host" contiendra l'adresse (str)
port_val = os.getenv("port",5007)    # La variable "port" contiendra le port (str)


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

STOP_INSERT_DATA = [False]
BACKGROUND_THREAD = None

def process_messages_stream_ai(item: dict, sample_size : int = 1000, format_time : str = "%d-%m-%y %H:%M:%S.%f"):
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

def last_delivery_id(redis, stream, group):

    lastid='0-0'

    lis = redis.xinfo_groups(stream)

    if len(lis)!=0:
        for elt in lis:
            if elt['name']==group:
                lastid = elt['last-delivered-id']

    return lastid


def save_data_to_mongo_and_folder(stop_event, redisReader:RedisStreamReader, config):

    global STOP_INSERT_DATA

    try:
        i = 0
        df_ai = None
        df_udp = None
        df_ci = None
        df_di = None
        time_start = None
        time_stop = None
        rate = None
        line_nb = 0

        
        while not STOP_INSERT_DATA[0] or (df != None):

            items = redisReader.read_one_streams()

            if (items == None) or (len(items[0][1])==0) :

                check_backlog = False if (len(items[0][1]) == 0) else True

            else :
                
                for stream, mesg_list in items:

                    if stream == config['stream_ai']:

                        id, item = mesg_list

                        if len(item)>0:

                            data = process_messages_stream_ai(item=item, sample_size=int(config['sample_size']), format_time=f"%{config['day']}-%{config['month']}-%{config['year']} %{config['hour']}:%{config['minute']}:%{config['seconds']}.%{config['milliseconds']}")

                            if df_ai is not None:

                                time_stop = data['time_stop']
                                df_ai= pd.concat([df_ai, pd.DataFrame(data['value'])], ignore_index=True)

                            else:

                                time_start = data['time_start']
                                time_stop = data['time_stop']
                                rate = data['sample_rate']
                                df_ai = pd.DataFrame(data['value'])


                    elif(stream == config['stream_ci']):

                        id, item = mesg_list

                        if len(item)>0:

                            if df_ci is not None:

                                df_ci= pd.concat([df_ci, pd.DataFrame(item)], ignore_index=True)

                            else:

                                df_ci = pd.DataFrame(item)
                    
                    elif(stream == config['stream_di']):

                        id, item = mesg_list

                        if len(item)>0:

                            if df_di is not None:

                                df_di= pd.concat([df_di, pd.DataFrame(item)], ignore_index=True)

                            else:

                                df_di = pd.DataFrame(item)

                    elif(stream == config['stream_udp']):

                        id, item = mesg_list

                        if len(item)>0:

                            if df_udp is not None:

                                df_udp= pd.concat([df_udp, pd.DataFrame(item)], ignore_index=True)

                            else:

                                df_udp = pd.DataFrame(item)

                    elif(stream == config['stream_sync1']):

                        id, item = mesg_list

                        if len(item)>0:

                            if df_sync1 is not None:

                                df_sync1 = pd.concat([df_sync1, pd.DataFrame(item)], ignore_index=True)

                            else:

                                df_sync1 = pd.DataFrame(item)

                    elif(stream == config['stream_sync2']):

                        id, item = mesg_list

                        if len(item)>0:

                            if df_sync2 is not None:

                                df_sync2 = pd.concat([df_sync2, pd.DataFrame(item)], ignore_index=True)

                            else:

                                df_sync2 = pd.DataFrame(item)

                    elif(stream == config['stream_sync3']):

                        id, item = mesg_list

                        if len(item)>0:

                            if df_sync3 is not None:

                                df_sync3 = pd.concat([df_sync3, pd.DataFrame(item)], ignore_index=True)

                            else:

                                df_sync3 = pd.DataFrame(item)

                    else:

                        pass

            df = df_ai.merge(df_ci, on=['timestamp'], how='outer')
            df = df.merge(df_di, on=['timestamp'], how='outer')
            df = df.merge(df_udp, on=['timestamp'], how='outer')
            df = df.merge(df_sync1, on=['timestamp'], how='outer')
            df = df.merge(df_sync2, on=['timestamp'], how='outer')
            df = df.merge(df_sync3, on=['timestamp'], how='outer')

            message = {}

            message['values'] = df
            message['rate'] = rate
            message['timestart'] = time_start
            message['timestop'] = time_stop

            redisReader.write(stream=config['stream'], data=message)
        
        redisReader.close()                   
                 
    except Exception as ex:
        print(f"Erreur {ex}")



# Route pour écrire des données dans InfluxDB
@app.route('/api/write_to_redis', methods=['POST'])
def api_write_to_redis_loop():
    global BACKGROUND_THREAD

    try:

        data = request.get_json()

        stream = [data.get('stream_ai'),data.get('stream_ci'),data.get('stream_di'),data.get('stream_udp')]

        redis_reader = RedisStreamReader(redis_host=data.get('host'), redis_port=int(data.get('port')), consumer_group=data.get('group'),stream_name=stream)

        redis_reader.create_consumer_group()

        config = {}
        config['day'] = data.get('day')
        config['month'] = data.get('month')
        config['year'] = data.get('year')
        config['hour'] = data.get('hour')
        config['minute'] = data.get('minute')
        config['seconds'] = data.get('seconds')
        config['milliseconds'] = data.get('milliseconds')
        config['sample_size'] = data.get('sample_size')
        config['group'] = data.get('group')
        config['stream'] = data.get('stream')
        config['stream_ci'] = data.get('stream_ci')
        config['stream_ai'] = data.get('stream_ai')
        config['stream_di'] = data.get('stream_di')
        config['stream_udp'] = data.get('stream_udp')
        config['stream_sync1'] = data.get('stream_sync1')
        config['stream_sync2'] = data.get('stream_sync2')
        config['stream_sync3'] = data.get('stream_sync3')
        # config['max_file'] = data.get('max_file')

        # Créez un thread pour la tâche en arrière-plan
        BACKGROUND_THREAD = threading.Thread(target=save_data_to_mongo_and_folder, args=(STOP_INSERT_DATA, redis_reader,config))
        # Démarrez le thread en arrière-plan
        BACKGROUND_THREAD.start()

        return jsonify({'Message': f"Début de la sauvegarde dans fichier"}), 200
    
    except Exception as e:
        redis_reader.close()
        return jsonify({'Message': f"Une erreur sur la sauvegarde dans fichier :  {e}."}), 500



# Route pour écrire des données dans InfluxDB
@app.route('/api/stop_write_to_redis', methods=['GET'])
def api_stop_write_to_redis_loop():

    global STOP_INSERT_DATA 
    global BACKGROUND_THREAD

    try:

        STOP_INSERT_DATA[0] = True 

        BACKGROUND_THREAD.join()

        return jsonify({'Message': "Stop de la sauvegarde"}), 200
    
    except Exception as ex:
        return jsonify({'Message': f"Un problème à l'arret : {ex}"}), 500 




import os
import json
import threading
import pandas as pd
import numpy as np
import pprint

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

def calibration(x,offset,sensibilite):

    return (x+offset)/sensibilite

def read_items_from_redis(redis, stream, group, consumer='consumer_i', block=1, count=1):

      
    items = []

                           
    items = redis.xreadgroup(groupname=group, consumername=consumer,block=block, count=count, streams={stream:'>'} )

    
    # pprint.pprint(items)


    if (len(items)== 0)or (items == None):

        return None
    
    elif (len(items[0][1])==0):

        return None

    else :            

        data = []

                
        for elt in items[0][1] :

            id, item = elt

            data.append(item)

            redis.xack(stream, group, id)

        return data


def write_to_redis(stop_event, redisReader:RedisStreamReader, config):

    global STOP_INSERT_DATA

    try:
        i = 0
        df = None
        df_ai = None
        df_udp = None
        df_dir = None
        df_vit = None
        df_syn = None
        time_start = None
        time_stop = None
        rate = None
        line_nb = 0

        
        while not STOP_INSERT_DATA[0] or (df != None):

            # AI 0-7
            l = read_items_from_redis(redis=redisReader.redis_conn, stream=config['stream_ai'], group=config['group'], consumer='consumer_ai')

            

            if l==None:

                df_ai = pd.DataFrame(columns=['timestamp','ai0', 'ai1', 'ai2', 'ai3', 'ai4', 'ai5', 'ai6', 'ai7'])

            else:

                data = process_messages_stream_ai(item=l[0], sample_size=int(config['sample_size']), format_time=f"%Y-%m-%d %H:%M:%S.%f")
                
                time_stop = data['time_stop']
                time_start = data['time_start']
                rate = data['sample_rate']                
                df_ai = pd.DataFrame(data['value'])

                df_ai['ai0'] = df_ai['ai0'].apply(lambda x : calibration(x,offset=0,sensibilite=0.079863))
                df_ai['ai1'] = df_ai['ai1'].apply(lambda x : calibration(x,offset=-0.001,sensibilite=0.080607))
                df_ai['ai2'] = df_ai['ai2'].apply(lambda x : calibration(x,offset=-0.007,sensibilite=0.080243))
                df_ai['ai3'] = df_ai['ai3'].apply(lambda x : calibration(x,offset=-0.004,sensibilite=0.080366))
                df_ai['ai4'] = df_ai['ai4'].apply(lambda x : calibration(x,offset=-0.003,sensibilite=0.080154))
                df_ai['ai5'] = df_ai['ai5'].apply(lambda x : calibration(x,offset=-0.002,sensibilite=0.080917))

            print(f"ai") 

            # Synchro
            l = read_items_from_redis(redis=redisReader.redis_conn, stream=config['stream_syn'], group=config['group'], consumer='consumer_syn')

            if l==None:

                df_syn = pd.DataFrame(columns=['timestamp','Synchron'])

            else:
                              
                df_syn = pd.DataFrame([l[0]],columns=['timestamp','Synchron'])

            print(f"syn")

            # Direction
            l = read_items_from_redis(redis=redisReader.redis_conn, stream=config['stream_dir'], group=config['group'], consumer='consumer_dir')

            if l==None:

                df_dir = pd.DataFrame(columns=['timestamp','Direction'])

            else:
                              
                df_dir = pd.DataFrame([l[0]],columns=['timestamp','Direction'])

            print(f"dir")

            # Vitesse
            l = read_items_from_redis(redis=redisReader.redis_conn, stream=config['stream_vit'], group=config['group'], consumer='consumer_vit')

            if l==None:

                df_vit = pd.DataFrame(columns=['timestamp','Vitesse'])

            else:
                              
                df_vit = pd.DataFrame([l[0]],columns=['timestamp','Vitesse'])

            print(f"Vit")
            

            # UDP
            l = read_items_from_redis(redis=redisReader.redis_conn, stream=config['stream_udp'], group=config['group'], consumer='consumer_udp')

            if l==None:

                df_udp = pd.DataFrame(columns=['timestamp','udp'])

            else:

                df_udp = pd.DataFrame([l[0]], columns=['timestamp','udp'])

            print(f"udp")
                
            

            df = df_ai.merge(df_syn, on=['timestamp'], how='outer')
            df = df.merge(df_dir, on=['timestamp'], how='outer')
            df = df.merge(df_vit, on=['timestamp'], how='outer')
            df = df.merge(df_udp, on=['timestamp'], how='outer')

            # df.replace('nan', None, inplace=True) 

            print(f"df")

            print(df) 

            message = {}

            for cols in df.columns.to_list():

                message[cols] = df[cols].to_list().__str__()          
                    
            message['rate'] = rate.__str__()
            message['timestart'] = time_start.__str__()
            message['timestop'] = time_stop.__str__()
            message['columns'] = df.columns.to_list().__str__()

            # pprint.pprint(message)

            redisReader.write(stream=config['stream'], data=message)

            df = None
            df_ai = None
            df_udp = None
            df_dir = None
            df_vit = None
            df_syn = None
        
        redisReader.close()                   
                 
    except Exception as ex:
        print(f"Erreur {ex}")



# Route pour écrire des données dans InfluxDB
@app.route('/api/write_to_redis', methods=['POST'])
def api_write_to_redis_loop():
    global BACKGROUND_THREAD

    try:

        data = request.get_json()

        stream = [data.get('stream_ai'),data.get('stream_dir'),data.get('stream_vit'),data.get('stream_syn'),data.get('stream_udp'), data.get('stream')]

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
        config['stream_ai'] = data.get('stream_ai')
        config['stream_dir'] = data.get('stream_dir')
        config['stream_vit'] = data.get('stream_vit')
        config['stream_syn'] = data.get('stream_syn')
        config['stream_udp'] = data.get('stream_udp')

        # Créez un thread pour la tâche en arrière-plan
        BACKGROUND_THREAD = threading.Thread(target=write_to_redis, args=(STOP_INSERT_DATA, redis_reader,config))
        # Démarrez le thread en arrière-plan
        BACKGROUND_THREAD.start()

        return jsonify({'Message': f"écriture dans dans stream_all"}), 200
    
    except Exception as e:
        redis_reader.close()
        return jsonify({'Message': f"Une erreur au niveau de l'ecriture dans stream_all :  {e}."}), 500



# Route pour écrire des données dans InfluxDB
@app.route('/api/stop_write_to_redis', methods=['GET'])
def api_stop_write_to_redis_loop():

    global STOP_INSERT_DATA 
    global BACKGROUND_THREAD

    try:

        STOP_INSERT_DATA[0] = True 

        BACKGROUND_THREAD.join()

        return jsonify({'Message': "Stop écriture dans stream_all"}), 200
    
    except Exception as ex:
        return jsonify({'Message': f"Un problème à stopper l'écriture dans stream_all : {ex}"}), 500 



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
import os
import threading
import pandas as pd
import numpy as np
import pprint

from flask import Flask, request, jsonify
from datetime import datetime as Date
from redis_stream import RedisStreamReader
from redis import Redis

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

    pprint.pprint(lis)

    if len(lis)!=0:
        for elt in lis:
            if elt['name']==group:
                lastid = elt['last-delivered-id']

    return lastid

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


import json


if __name__ == '__main__':

    stream = ['stream_chan_ai', 'stream_chan_di_vit', 'stream_chan_di_dir', 'stream_udp', 'stream_all', 'stream_chan_di_syn']

    redis_reader = RedisStreamReader(redis_host='127.0.0.1', redis_port=6379, consumer_group='aggr_all',stream_name=stream)

    # item = redis_reader.read_one_streams()

    # item = read_items_from_redis(redis_reader.redis_conn,stream=stream[0], group='aggr_all')

    # pprint.pprint(item)

    i=0

    while i < 2:

        t = last_delivery_id(redis_reader.redis_conn, stream=stream[5],group='aggr_all')

        print(redis_reader.redis_conn.xlen(stream[5]))

        item = read_items_from_redis(redis_reader.redis_conn, stream=stream[5], group='aggr_all',consumer='consumer_vit')

        pprint.pprint(item)

        # item = item[0]

        # data = json.loads(data)

        # pprint.pprint(data)

        # print(item)

        # df = pd.DataFrame(eval(data))

        # print(df)

        # df = pd.DataFrame({'col1': [1, 2],'col2': [0.5, 0.75]})

        # tab = df.to_numpy()

        # data = {}

        # i=0

        # for cols in df.columns.to_list():

        #     data[cols] = tab[i].tolist().__str__()

        ##########################################################meerge######################################################################

        # data = {}

        # channels =[elt.replace("'", "") for elt in np.asarray(item['columns'][1:-2].split(", "), dtype=str).tolist()]

        # print(channels)

        # for ch in channels :

        #     if (ch =='udp') or (ch =='timestamp'):

        #         data[ch] = np.asarray([None if (elt=='nan')  else elt.replace("'","") for elt in item[ch][1:-1].split(", ")], dtype=str).tolist()

        #     else:

        #         data[ch] = np.asarray([None if (elt=='nan')  else elt for elt in item[ch][1:-1].split(", ")], dtype=float).tolist()



        # # pprint.pprint(data)

        # time_start = str(item['timestart'])
        # print(time_start)
        # time_stop = str(item['timestop'])
        # print(time_stop)

        # rate = int(item['rate'])

        # print(rate)

        # print(pd.DataFrame(data))



        # print(f"{df.columns.to_list()}")

        # print(f"{df['col1'].to_list()}")

        # print(f"{df.to_numpy()}")

        i+=1

from redis import Redis
from datetime import datetime as Date
import numpy as np
import pandas as pd
import pprint

def process_messages(item: dict, sample_size : int = 1000, format_time : str = "%d-%m-%y %H:%M:%S.%f"):
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
    print(f"{t1}")
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



if __name__=='__main__' :

    lastid = '0-0'
    check_backlog = True

    redis = Redis(host='127.0.0.1',port=6379, decode_responses=True)

    lis = redis.xinfo_groups("stream_all")

    if len(lis)!=0:

        for elt in lis:

            if elt['name']=='mongo_ai':
                lastid = elt['last-delivered-id']

    len_r = redis.xlen("stream_all")

    print(f"{lis}")

    print(f"len stream : {len_r}")

    stream = {'stream_chan_ai': '0-0', 'stream_chan_ci': '0-0', 'stream_chan_di': '0-0', 'stream_udp': '0-0', 'stream_all': '0-0'}

    messages = redis.xreadgroup(groupname='aggr_all', consumername='c1', streams={'stream_all':'>'}, count=1, block=0)

    pprint.pprint(messages[0][1]['values'])

    df = pd.DataFrame.from_dict(messages['values'])

    print(df)

    # while True:

    #     items = []

    #     if check_backlog : 

    #         items = redis.xreadgroup(groupname="mongo_ai", consumername='C_mongodb',block=10, count=100, streams={'stream_chan_ai':lastid} )

    #     else :
                        
    #         items = redis.xreadgroup(groupname="mongo_ai", consumername='C_mongodb',block=10, count=100, streams={'stream_chan_ai':'>'} )


    #     if (items == None) or (len(items[0][1])==0):

    #         check_backlog = False if (len(items[0][1]) == 0) else True

    #     else :            

                
    #         for elt in items[0][1] :

    #             _, item = elt

    #             print(f"Debut")

    #             print(f"{item}")

    #             data = process_messages(item=item, sample_size=1000, format_time="%d-%m-%y %H:%M:%S.%f")

    #             print(f"Insert")

    #             print(f"{data}")

    #             print(f"Fin insert")
                

    #         lastid = items[0][1][-1][0]
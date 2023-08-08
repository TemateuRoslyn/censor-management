import os
import threading
import pandas as pd
import numpy as np

from flask import Flask, request, jsonify
from datetime import datetime as Date
from file_manager import PandasFileManager, FolderManager
from redis import Redis



# Lire la valeur des variables d'environnement
debug_val = os.getenv("debug","true")  # La variable "debug" sera soit True ou False (str)
host_val = os.getenv("host","0.0.0.0")    # La variable "host" contiendra l'adresse (str)
port_val = os.getenv("port",5005)    # La variable "port" contiendra le port (str)


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


def insert_data_into_folder(stop_event, redis:Redis, folder : FolderManager, config):

    global STOP_INSERT_DATA

    try:
        
        lastid = '0-0'
        check_backlog = True 
        i = 0
        df = None
        time_start = None
        time_stop = None
        rate = None
        line_nb = 0

        lis = redis.xinfo_groups(config['stream'])

        if len(lis)!=0:
            for elt in lis:
                if elt['name']==config['group']:
                    lastid = elt['last-delivered-id']

        while not STOP_INSERT_DATA[0] or (df != None):

            items = []

            if check_backlog : 

                items = redis.xreadgroup(groupname=config['group'], consumername='C_Folder',block=10, count=10, streams={config['stream']:lastid} )

            else :
                        
                items = redis.xreadgroup(groupname=config['group'], consumername='C_Folder',block=10, count=10, streams={config['stream']:'>'} )

            

            if (items == None) or (len(items[0][1])==0) :

                check_backlog = False if (len(items[0][1]) == 0) else True

            else :

                line_nb += int(config['sample_size'])*len(items[0][1])
                
                for elt in items[0][1] :

                    id, item = elt

                    data = process_messages(item=item, sample_size=int(config['sample_size']), format_time=f"%{config['day']}-%{config['month']}-%{config['year']} %{config['hour']}:%{config['minute']}:%{config['seconds']}.%{config['milliseconds']}")

                    if df is not None:
                        time_stop = data['time_stop']
                        df= pd.concat([df, pd.DataFrame(data['value'])], ignore_index=True)
                    else:
                        time_start = data['time_start']
                        time_stop = data['time_stop']
                        rate = data['sample_rate']
                        df = pd.DataFrame(data['value'])

                    redis.xack(config['stream'],config['group'],id)
                                
                lastid = items[0][1][-1][0]

                if (line_nb >= int(config['max_file'])) or not STOP_INSERT_DATA[0]:
                    
                    date = Date.now()

                    name_file =f"Donnees_{date.day}_{date.month}_{date.year} {date.hour}_{date.minute}_{date.second}_index_{i}.csv"

                    i+=1

                    file_w = PandasFileManager(file_path=f"{folder.folder_path}/{name_file}")

                    comments = f"Start : {time_start} \n Stop : {time_stop} \n Rate : {rate}"

                    file_w.write_csv(df,comments)
                

        redis.close()
    except Exception as ex:
        print(f"Erreur {ex}")


# Route pour écrire des données dans InfluxDB
@app.route('/api/write_folder', methods=['POST'])
def api_write_to_folder():
    global BACKGROUND_THREAD

    try:

        data = request.get_json()

        redis_conn = Redis(host=data.get('host'), port=int(data.get('port')), decode_responses=True)

        folder = FolderManager(folder_path=data.get('folder_path'))

        folder.create_folder()

        list_group = redis_conn.xinfo_groups(data.get('stream'))

        if len(list_group)==0:

                redis_conn.xgroup_create(name=data.get('stream'), groupname=data.get('group'), id=0)
        else:

            create = True

            for elt in list_group:

                if data.get('group') == elt['name'] :

                    create=False

            if create :

                redis_conn.xgroup_create(name=data.get('stream'), groupname=data.get('group'), id=0)


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
        config['max_file'] = data.get('max_file')

        # Créez un thread pour la tâche en arrière-plan
        BACKGROUND_THREAD = threading.Thread(target=insert_data_into_folder, args=(STOP_INSERT_DATA, redis_conn, folder, config))
        # Démarrez le thread en arrière-plan
        BACKGROUND_THREAD.start()

        return jsonify({'Message': f"Début de la sauvegarde dans fichier"}), 200
    
    except Exception as e:
        redis_conn.close()
        return jsonify({'Message': f"Une erreur sur la sauvegarde dans fichier :  {e}."}), 500



# Route pour écrire des données dans InfluxDB
@app.route('/api/stop_write_folder', methods=['GET'])
def api_stop_write_to_folder():

    global STOP_INSERT_DATA 
    global BACKGROUND_THREAD

    try:

        STOP_INSERT_DATA[0] = True 

        BACKGROUND_THREAD.join()

        return jsonify({'Message': "Stop de la sauvegarde"}), 200
    
    except Exception as ex:
        return jsonify({'Message': f"Un problème à l'arret : {ex}"}), 500 




# Route pour lire le contenu du fichier CSV
@app.route('/api/read_csv', methods=['POST'])
def read_csv():
    data = request.get_json()
    csv_file_manager = PandasFileManager(data.get('file'))
    df = csv_file_manager.read_csv()
    if df is not None:
        return df.to_json(orient='records')
    else:
        return jsonify({'message': 'Le fichier n\'existe pas'}), 404

# Route pour écrire le contenu dans le fichier CSV
@app.route('/api/write_csv', methods=['POST'])
def write_csv():

    data = request.get_json()

    if data:

        df = pd.DataFrame(data['value'])

        csv_file_manager = PandasFileManager(data.get('file'))

        csv_file_manager.write_csv(df)

        return jsonify({'message': 'Données écrites dans le fichier CSV avec succès'})
    
    else:

        return jsonify({'message': 'Le contenu doit être fourni'}), 400

# Les méthodes read_excel() et write_excel() sont identiques à celles de la classe précédente.

# Route pour lire le contenu du fichier Excel
@app.route('/api/read_excel', methods=['GET'])
def read_excel():
    excel_file_manager = PandasFileManager("data.xlsx")
    df = excel_file_manager.read_excel()
    if df is not None:
        return df.to_json(orient='records')
    else:
        return jsonify({'message': 'Le fichier n\'existe pas'}), 404

# Route pour écrire le contenu dans le fichier Excel
@app.route('/api/write_excel', methods=['POST'])
def write_excel():
    data = request.get_json()
    if data:
        df = pd.DataFrame(data)
        excel_file_manager = PandasFileManager("data.xlsx")
        excel_file_manager.write_excel(df)
        return jsonify({'message': 'Données écrites dans le fichier Excel avec succès'})
    else:
        return jsonify({'message': 'Le contenu doit être fourni'}), 400
    

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


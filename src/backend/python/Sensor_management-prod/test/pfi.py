# import nidaqmx
# import time

# from nidaqmx.constants import LineGrouping

# # Définir le nom de la carte d'acquisition (à adapter en fonction de votre configuration)
# device_name = 'Dev1'
# pfi = "PFI1"

# # Créer une tâche de sortie numérique
# with nidaqmx.Task() as task:
#     # Ajouter une tâche de sortie numérique sur le connecteur PFI0
#     task.do_channels.add_do_chan(f"{device_name}/{pfi}",line_grouping=LineGrouping.CHAN_PER_LINE)
#     while True:
#         # Écrire des valeurs numériques (0 ou 1) sur le connecteur PFI0
#         data = True #[0, 1, 0, 1]  # Exemple de valeurs à écrire
#         task.write(data)
        
#         print(f"Données écrites sur le connecteur {pfi}.")

#         time.sleep(1)


# import nidaqmx

# # Nom de l'appareil
# device_name = "Dev1"

# # Configurer les canaux PFI comme compteurs
# counter_channels = ["PFI0", "PFI1", "PFI2", "PFI3"]

# # Créer une tâche
# with nidaqmx.Task() as task:
#     # Ajouter les canaux PFI comme compteurs
#     for channel_name in counter_channels:
#         counter_channel = task.ci_channels.add_ci_count_edges_chan(f"{device_name}/{channel_name}")
#         counter_channel.ci_count_edges_term = "/Dev1/PFI9"  # Utilisez le signal de référence approprié
    
#     # Démarrer la tâche pour commencer la comptage
#     task.start()

#     # Lire les valeurs de comptage
#     while True:
#         counter_values = task.read()
#         print("Valeurs de comptage :", counter_values)

import nidaqmx

def count_edges(task, num_edges):

    with task:
        data = task.read(number_of_samples_per_channel=num_edges)
        rising_edges = 0
        falling_edges = 0

        for elt in data:
            if elt:
                rising_edges+=1
            else:
                falling_edges+=1

        return rising_edges, falling_edges

def main():

    channel_name = "PFI9"  # Nom du canal PFI que vous souhaitez compter
    num_edges = 1       # Nombre de flancs à compter

    with nidaqmx.Task() as task:

        task.di_channels.add_di_chan(f"/Dev1/PFI9")
        task.start()

        while True: 
            rising_edges, falling_edges = count_edges(task, num_edges)
            
            print("Nombre de montées (flancs montants) détectées : {}".format(rising_edges))
            print("Nombre de descentes (flancs descendants) détectées : {}".format(falling_edges))

        task.close()

if __name__ == "__main__":

    main()

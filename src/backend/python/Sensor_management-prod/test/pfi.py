import nidaqmx

# Définir le nom de la carte d'acquisition (à adapter en fonction de votre configuration)
device_name = 'Dev1'
pfi = "PFI5"

# Créer une tâche de sortie numérique
with nidaqmx.Task() as task:
    # Ajouter une tâche de sortie numérique sur le connecteur PFI0
    task.do_channels.add_do_chan(f"{device_name}/{pfi}")
    
    # Écrire des valeurs numériques (0 ou 1) sur le connecteur PFI0
    data = True #[0, 1, 0, 1]  # Exemple de valeurs à écrire
    task.write(data)
    
    print(f"Données écrites sur le connecteur {pfi}.")
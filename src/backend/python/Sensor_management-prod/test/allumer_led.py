import nidaqmx

def allumer_leds():
    with nidaqmx.Task() as task:
        # Ajouter les sorties P0.1 à P0.4 à la tâche
        task.do_channels.add_do_chan("Dev1/port0/line1:4")

         # Configurer les sorties comme des sorties numériques
        task.start()  # Démarrer la tâche

        
        # Configurer les sorties comme des sorties numériques
        task.write([False, True, True, True])  # Allumer les LEDS branchées sur P0.1 à P0.4

if __name__ == "__main__":
    try:

        print(f"Tension de réference")
        # local_sys = nidaqmx.system.System.local()
        # volt_ref = local_sys.fetch_do_voltage_ref_level()
        # print(f"{volt_ref}")
        allumer_leds()
        print("LEDs allumées avec succès.")
    except nidaqmx.DaqError as e:
        print("Erreur lors de l'allumage des LEDs :", e)

import pprint
import psutil
import re
import pyudev


def convert_bytes(bytes):
    # Convertir les octets en format lisible (Go, Mo, Ko, etc.)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024


expression=r"^/dev/sd[c-z]{1,2}[0-9]+$"


cle_usb_trouvee = False
chemin_cle_usb = ''
        
partitions = psutil.disk_partitions()

print(f"Partition :")
pprint.pprint(partitions)

for partition in partitions :
    pprint.pprint(partition)
    # if 'removable' in partition.opts and 'noauto' not in partition.opts :
    if re.match(expression,partition.device):
        cle_usb_trouvee = True
        chemin_cle_usb = partition.mountpoint
        
        print(f"########################################################################################################")
        print(f"Path : {chemin_cle_usb}\n")
        usage = psutil.disk_usage(partition.mountpoint)
        print(f"Espace total: {convert_bytes(usage.total)}")
        print(f"Espace Utilisé: {convert_bytes(usage.used)}")
        print(f"Taux d'utilisation: {convert_bytes(usage.percent)}%")
        print(f"-----------------------------------------------------")
        break






   

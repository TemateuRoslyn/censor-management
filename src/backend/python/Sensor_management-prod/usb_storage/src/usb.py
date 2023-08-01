import shutil
import psutil
import os
import re
from pyudev import Context, Monitor


class USBHandler:
    def __init__(self, mount_dir='/mnt/usb', expression=r"^/dev/sd[c-z]{1,2}[0-9]+$"):
        self.context = Context()
        self.monitor = Monitor.from_netlink(self.context)
        self.monitor.filter_by(subsystem='block', device_type='partition')
        self.mount_dir = mount_dir
        self.expression = expression

    def mount_usb(self, device_path):
        try:
            os.makedirs(self.mount_dir, exist_ok=True)
            os.system(f"mount {device_path} {self.mount_dir}")
            print(f"Clé USB montée à {self.mount_dir}")
        except Exception as e:
            print(f"Erreur lors du montage de la clé USB : {e}")

    def unmount_usb(self):
        try:
            os.system(f"umount {self.mount_dir}")
            print(f"Clé USB démontée")
        except Exception as e:
            print(f"Erreur lors du démontage de la clé USB : {e}")

    def find_usb(self):

        cle_usb_trouvee = False
        chemin_cle_usb = ''
        
        partitions = psutil.disk_partitions()
        for partition in partitions :
            print(f"Partition : {partition}")
            # if 'removable' in partition.opts and 'noauto' not in partition.opts :
            if re.match(self.expression,partition.device):
                cle_usb_trouvee = True
                chemin_cle_usb = partition.mountpoint
                break
        return cle_usb_trouvee, chemin_cle_usb

    def start_monitoring(self):
        for device in self.monitor:
            if device.action == 'add':
                print("Clé USB insérée.")
                self.mount_usb(device.device_node)
            elif device.action == 'remove':
                print("Clé USB retirée.")
                self.unmount_usb()



class USBFileCopier:
    def __init__(self, source_dir, usb_mount_path):
        self.source_dir = source_dir
        self.usb_mount_path = usb_mount_path

    def copy_files_to_usb(self):
        # Vérifier si le chemin du répertoire source existe
        if not os.path.exists(self.source_dir):
            print(f"Le répertoire source '{self.source_dir}' n'existe pas.")
            return False

        # Vérifier si le chemin du point de montage de la clé USB existe
        if not os.path.exists(self.usb_mount_path):
            print(f"Le point de montage USB '{self.usb_mount_path}' n'existe pas.")
            return False

        # Copier les fichiers du répertoire source vers la clé USB
        try:
            for file_name in os.listdir(self.source_dir):
                file_path = os.path.join(self.source_dir, file_name)
                if os.path.isfile(file_path):
                    shutil.copy(file_path, self.usb_mount_path)
                    print(f"Copié '{file_name}' vers la clé USB.")
            return True
        except Exception as e:
            print(f"Une erreur s'est produite lors de la copie des fichiers : {e}")

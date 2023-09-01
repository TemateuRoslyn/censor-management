import os
from configparser import ConfigParser

config_parser = ConfigParser()

config_parser.read(os.getenv("CONFIG_PATH", "./configs.ini"))


################## USB ##########################

config_api_usb = dict(config_parser["Api_usb"])


api_url_usb_find = f"{config_api_usb.get('endpoint')}/api/usb/find"

api_url_usb_find_all = f"{config_api_usb.get('endpoint')}/api/usb/find_all"  # retourne toute les clés usb connecte

api_url_usb_usage = f"{config_api_usb.get('endpoint')}/api/usb/usage"  # retourne le pourcentage d'utilisation d'un périphérique

api_url_usb_copy = f"{config_api_usb.get('endpoint')}/api/usb/copy_files"

import os
from configparser import ConfigParser

############## Initialisation du Config Parser #############

config_parser = ConfigParser()

config_parser.read(os.getenv("CONFIG_PATH", "./configs.ini"))


################## USB ##########################

config_api_usb = dict(config_parser["Api_usb"])


api_url_usb_find = f"{config_api_usb.get('endpoint')}/api/usb/find"

api_url_usb_find_all = f"{config_api_usb.get('endpoint')}/api/usb/find_all"  # retourne toute les clés usb connecte

api_url_usb_usage = f"{config_api_usb.get('endpoint')}/api/usb/usage"  # retourne le pourcentage d'utilisation d'un périphérique

api_url_usb_copy = f"{config_api_usb.get('endpoint')}/api/usb/copy_files"


##################### AI ############################

config_api_ni = dict(config_parser["Api_ni"])

api_ni_read_all = f"{config_api_ni.get('endpoint')}/api/read_ai"

#################### Config AI ########################

ni_config = dict(config_parser["Config_ai"])

host = ni_config.get("host")
port = ni_config.get("port")
period = ni_config.get("period")
rate = ni_config.get("rate")
buffer_size = ni_config.get("buffer_size")
sample_size = ni_config.get("sample_size")
device = ni_config.get("device")
channels = ["ai0", "ai1", "ai2", "ai3", "ai4", "ai5", "ai6", "ai7"]


################### Sauvegardes datas ##################

config_mongo = dict(config_parser["Api_mongo"])

api_url_mongo_find_all = f"{config_mongo.get('endpoint')}/api/find"
api_url_mongo_find_session = f"{config_mongo.get('endpoint')}/api/find_session"


config_mongo_param = dict(config_parser["Config_mongo"])

mongo_url = config_mongo_param.get("url")
mongo_db = config_mongo_param.get("db")
mongo_username = config_mongo_param.get("username")
mongo_password = config_mongo_param.get("password")
mongo_collection_name = config_mongo_param.get("collection_name")
session_name = config_mongo_param.get("session_name")

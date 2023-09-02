import os
import dash
from dash import Dash
import dash_auth
import dash

from libs.shell import mount_app
from services.request import get_request

# Lire la valeur des variables d'environnement
debug_val = os.getenv("debug")  # La variable "debug" sera soit True ou False (str)
host_val = os.getenv("host")  # La variable "host" contiendra l'adresse (str)
port_val = os.getenv("port")  # La variable "port" contiendra le port (str)

# Convertir le port en nombre (integer)
try:
    port_val = int(port_val)
except ValueError:
    print("Erreur : le port n'est pas un entier valide.")

if debug_val == "true":
    debug_val = True
else:
    debug_val = False


scripts = [
    "https://cdnjs.cloudflare.com/ajax/libs/dayjs/1.10.8/dayjs.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/dayjs/1.10.8/locale/ru.min.js",
    "https://www.googletagmanager.com/gtag/js?id=G-4PJELX1C4W",
    "https://media.ethicalads.io/media/client/ethicalads.min.js",
]

app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    use_pages=True,
    external_scripts=scripts,
    title="Data Logger.",
    update_title="Logger...",
)

VALID_USERNAME_PASSWORD_PAIRS = {"demo": "demo"}

# value = get_request(
#     "https://b471-2a01-e0a-3b2-a7f0-9ec6-7757-e1c7-e484.ngrok-free.app/api/usb/find_all"
# )
# print(value)

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS,
)

app.layout = mount_app(
    dash.page_registry.values(),
)

server = app.server

if __name__ == "__main__":
    app.run_server(
        debug=debug_val,
        host=host_val,
        port=port_val,
    )

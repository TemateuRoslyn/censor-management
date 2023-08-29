import os

from flask import Flask, jsonify, request
from usb import USBHandler, USBFileCopier

# Lire la valeur des variables d'environnement
debug_val = os.getenv(
    "debug", "true"
)  # La variable "debug" sera soit True ou False (str)
host_val = os.getenv("host", "0.0.0.0")  # La variable "host" contiendra l'adresse (str)
port_val = os.getenv("port", 5003)  # La variable "port" contiendra le port (str)


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


# Route pour le taux d'usage
@app.route("/api/usb/usage", method=["POST"])
def usb_usage():
    data = request.get_json()
    usb_handler = USBHandler()

    try:
        data = usb_handler.usage(data.get("mount_dir"))

        return jsonify({"values": data}), 200

    except Exception as e:
        return jsonify({"Echec": e}), 500


# Route pour démarrer la détection et le montage d'une clé USB
@app.route("/api/usb/start_monitoring", methods=["POST"])
def start_usb_monitoring():
    data = request.get_json()
    usb_handler = USBHandler(mount_dir=data.get("mount_dir"))
    try:
        usb_handler.start_monitoring()
        return (
            jsonify(
                {"message": "Démarrage de la détection et du montage des clés USB."}
            ),
            200,
        )
    except Exception as e:
        return (
            jsonify(
                {
                    "error": "Une erreur s'est produite lors du démarrage de la détection des clés USB."
                }
            ),
            500,
        )


# Route pour démarrer la détection et le montage d'une clé USB
@app.route("/api/usb/find", methods=["GET"])
def find_usb():
    # data = request.get_json()
    usb_handler = USBHandler()
    try:
        present, mount = usb_handler.find_usb()

        if present and mount:
            return (
                jsonify(
                    {
                        "usb_present": present,
                        "usb_mount_path": mount,
                        "message": "Démarrage de la détection et du montage des clés USB.",
                    }
                ),
                200,
            )

        return (
            jsonify(
                {
                    "usb_present": present,
                    "usb_mount_path": mount,
                    "message": "Démarrage de la détection et du montage des clés USB.",
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "error": "Une erreur s'est produite lors du démarrage de la détection des clés USB."
                }
            ),
            500,
        )


# Route pour démarrer la détection et le montage d'une clé USB
@app.route("/api/usb/find_all", methods=["GET"])
def find_all_usb():
    # data = request.get_json()
    usb_handler = USBHandler()
    try:
        present, list = usb_handler.find_all_usb()

        return (
            jsonify(
                {
                    "usb_present": present,
                    "usb_mount_paths": list,
                    "message": "Démarrage de la détection et du montage des clés USB.",
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "error": "Une erreur s'est produite lors du démarrage de la détection des clés USB."
                }
            ),
            500,
        )


# Route pour démonter une clé USB
@app.route("/api/usb/unmount", methods=["POST"])
def unmount_usb():
    data = request.get_json()
    usb_handler = USBHandler(mount_dir=data.get("mount_dir"))
    try:
        usb_handler.unmount_usb()
        return jsonify({"message": "Clé USB démontée avec succès."}), 200
    except Exception as e:
        return (
            jsonify(
                {"error": "Une erreur s'est produite lors du démontage de la clé USB."}
            ),
            500,
        )


# Route pour copier les fichiers vers la clé USB
@app.route("/api/usb/copy_files", methods=["POST"])
def copy_files_to_usb():
    data = request.get_json()
    usb_file_copier = USBFileCopier(
        source_dir=data.get("source_dir"), usb_mount_path=data.get("usb_mount_path")
    )
    try:
        success = usb_file_copier.copy_files_to_usb()
        if success:
            return (
                jsonify({"message": "Copie des fichiers vers la clé USB réussie."}),
                200,
            )
        else:
            return (
                jsonify(
                    {
                        "error": "Une erreur s'est produite lors de la copie des fichiers vers la clé USB."
                    }
                ),
                500,
            )
    except Exception as e:
        return (
            jsonify(
                {"error": "Une erreur s'est produite lors du traitement de la requête."}
            ),
            500,
        )


if __name__ == "__main__":
    from waitress import serve

    if debug_val:
        app.run(
            debug=debug_val,
            host=host_val,
            port=port_val,
        )
    else:
        serve(app, host=host_val, port=port_val)

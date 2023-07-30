from flask import Flask, jsonify, request
from usb import USBHandler, USBFileCopier

app = Flask(__name__)


# Route pour démarrer la détection et le montage d'une clé USB
@app.route('/api/usb/start_monitoring', methods=['POST'])
def start_usb_monitoring():
    data = request.get_json()
    usb_handler = USBHandler(mount_dir=data.get('mount_dir'), expression=data.get('expression'))
    try:
        usb_handler.start_monitoring()
        return jsonify({'message': 'Démarrage de la détection et du montage des clés USB.'}), 200
    except Exception as e:
        return jsonify({'error': 'Une erreur s\'est produite lors du démarrage de la détection des clés USB.'}), 500

# Route pour démonter une clé USB
@app.route('/api/usb/unmount', methods=['POST'])
def unmount_usb():
    data = request.get_json()
    usb_handler = USBHandler(mount_dir=data.get('mount_dir'), expression=data.get('expression'))
    try:
        usb_handler.unmount_usb()
        return jsonify({'message': 'Clé USB démontée avec succès.'}), 200
    except Exception as e:
        return jsonify({'error': 'Une erreur s\'est produite lors du démontage de la clé USB.'}), 500
    
# Route pour copier les fichiers vers la clé USB
@app.route('/api/usb/copy_files', methods=['POST'])
def copy_files_to_usb():
    data = request.get_json()
    usb_file_copier = USBFileCopier(source_dir=data.get('mount_dir'), usb_mount_path=data.get('usb_mount_path'))
    try:
        success = usb_file_copier.copy_files_to_usb()
        if success:
            return jsonify({'message': 'Copie des fichiers vers la clé USB réussie.'}), 200
        else:
            return jsonify({'error': 'Une erreur s\'est produite lors de la copie des fichiers vers la clé USB.'}), 500
    except Exception as e:
        return jsonify({'error': 'Une erreur s\'est produite lors du traitement de la requête.'}), 500
    

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5001)


import pandas as pd
import os

class FolderManager:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def create_folder(self):
        try:
            os.makedirs(self.folder_path, exist_ok=True)
            print(f"Dossier '{self.folder_path}' créé avec succès.")
        except Exception as e:
            print(f"Erreur lors de la création du dossier : {e}")

    def delete_folder(self):
        try:
            os.rmdir(self.folder_path)
            print(f"Dossier '{self.folder_path}' supprimé avec succès.")
        except FileNotFoundError:
            print(f"Le dossier '{self.folder_path}' n'existe pas.")
        except Exception as e:
            print(f"Erreur lors de la suppression du dossier : {e}")

    def list_files(self):
        try:
            files = os.listdir(self.folder_path)
            print(f"Contenu du dossier '{self.folder_path}':")
            for file in files:
                print(file)
        except FileNotFoundError:
            print(f"Le dossier '{self.folder_path}' n'existe pas.")
        except Exception as e:
            print(f"Erreur lors de la liste des fichiers : {e}")

    def move_file(self, source_file, destination_folder):
        try:
            os.makedirs(destination_folder, exist_ok=True)
            destination_path = os.path.join(destination_folder, os.path.basename(source_file))
            os.rename(source_file, destination_path)
            print(f"Fichier déplacé de '{source_file}' vers '{destination_path}' avec succès.")
        except FileNotFoundError:
            print(f"Le fichier '{source_file}' n'existe pas.")
        except Exception as e:
            print(f"Erreur lors du déplacement du fichier : {e}")


class PandasFileManager:
    
    def __init__(self, file_path):
        self.file_path = file_path

    def read_csv(self):
        try:
            df = pd.read_csv(self.file_path)
            return df
        except FileNotFoundError:
            print(f"Le fichier '{self.file_path}' n'existe pas.")
            return None
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier CSV : {e}")
            return None

    def write_csv(self, dataframe,comments=None):

        try:
            if comments :

                with open(self.file_path, 'w') as file:
                    # Écrire les commentaires
                    file.write(f"# {comments}\n")

                    st = ",".join(dataframe.columns.tolist())

                    file.write(f"{st}\n")

                    dataframe.to_csv(file,index=False,header=False)

            else:

                dataframe.to_csv(self.file_path, index=False, header=True)

            print(f"Données écrites dans le fichier '{self.file_path}' avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'écriture des données dans le fichier CSV : {e}")

    def read_excel(self, sheet_name=0):
        try:
            df = pd.read_excel(self.file_path, sheet_name=sheet_name)
            return df
        except FileNotFoundError:
            print(f"Le fichier '{self.file_path}' n'existe pas.")
            return None
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier Excel : {e}")
            return None

    def write_excel(self, dataframe, sheet_name='Sheet1'):
        try:
            with pd.ExcelWriter(self.file_path, mode='a', engine='openpyxl') as writer:
                dataframe.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"Données écrites dans le fichier '{self.file_path}' avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'écriture des données dans le fichier Excel : {e}")

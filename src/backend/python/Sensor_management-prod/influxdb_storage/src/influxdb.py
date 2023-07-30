from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

class InfluxDBHandler:
    def __init__(self, url, token, org, bucket):
        self.client = InfluxDBClient(url=url, token=token, org=org)
        self.bucket = bucket
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def write_data(self, measurement, tags, fields):
        try:
            point = Point(measurement).tag(**tags).field(**fields)
            self.write_api.write(bucket=self.bucket, record=point)
            return True
        except Exception as e:
            print(f"Erreur lors de l'écriture des données : {e}")
            return False

    def query_data(self, query):
        try:
            result = self.client.query_api().query(org=self.client.org, query=query)
            return result
        except Exception as e:
            print(f"Erreur lors de la requête : {e}")
            return None

    def close(self):
        self.client.close()
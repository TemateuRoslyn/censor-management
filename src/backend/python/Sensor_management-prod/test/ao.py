import nidaqmx
import time

class AnalogOutputChannel:
    def __init__(self, device_name, channel_name):
        self.device_name = device_name
        self.channel_name = channel_name
        self.task = nidaqmx.Task()
        self.ao_channel = self.task.ao_channels.add_ao_voltage_chan(f"{self.device_name}/{self.channel_name}")
        
    def write_voltage(self, voltage):
        try:
            self.task.write(voltage)
            print(f"Voltage {voltage} V written to channel {self.channel_name}")
        except Exception as e:
            print(f"Error writing voltage: {e}")
            
    def close(self):
        self.task.close()

# Exemple d'utilisation de la classe
if __name__ == "__main__":
    device_name = "BNC-2110/Dev1"  # Nom de l'appareil
    channel_name = "ao0"  # Nom du canal de sortie analogique
    
    ao_channel = AnalogOutputChannel(device_name, channel_name)
    
    voltage_to_write = 5.5 #[5.5, 2.5]  # Tension en volts

    i =0

    while True :

        ao_channel.write_voltage(voltage_to_write)

        time.sleep(2)

        i+=1

        if i>20:
            break
    
    ao_channel.close()
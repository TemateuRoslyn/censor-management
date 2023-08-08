import socket

class UDPHandler:
    def __init__(self, target_ip='0.0.0.0', target_port=55000):
        self.target_ip = target_ip
        self.target_port = target_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((target_ip,target_port))

    def send_packet(self, data):
        try:
            self.socket.sendto(data.encode(), (self.target_ip, self.target_port))
            print(f"Packet sent to {self.target_ip}:{self.target_port}")
        except Exception as e:
            print(f"Error sending packet: {e}")

    def receive_packet(self, buffer_size=1024):
        try:
            #self.socket.bind((self.target_ip, self.target_port))
            print(f"{self.socket}")
            data, address = self.socket.recvfrom(buffer_size)
            print(f"Packet received from {address[0]}:{address[1]}")
            return data.decode()
        except Exception as e:
            print(f"Error receiving packet: {e}")
            return None

    def close(self):
        self.socket.close()

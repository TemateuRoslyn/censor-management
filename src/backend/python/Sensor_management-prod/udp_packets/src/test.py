from udp_protocol import UDPHandler


if __name__=='__main__':

	udp = UDPHandler(target_ip='0.0.0.0', target_port=55000)

	while True:
		print(f"packet en attente")

		data = udp.receive_packet()
   
		print(f"{data}")

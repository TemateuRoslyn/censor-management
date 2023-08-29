from udp_protocol import UDPHandler

import pandas as pd


if __name__=='__main__':

	# udp = UDPHandler(target_ip='0.0.0.0', target_port=55000)

	# while True:
	# 	print(f"packet en attente")

	# 	data = udp.receive_packet()
   
	# 	print(f"{data}")

	a = {
		'timestamp':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21],
		'ai0': [elt for elt in range(20,41)],
		'ai1': [elt for elt in range(60,81)],
		'ai2': [elt for elt in range(120,141)]
	}

	b = {
		'timestamp':[1,2,3,4,5,6,7,8,9,15,16,17,18,24,25],
		'udp': [elt for elt in range(20,35)]
	}

	c = {
		'timestamp':[25,26,32,41,50,66,72,81,92,98],
		'tor1': [elt for elt in range(20,30)],
		'tor2': [elt for elt in range(20,30)]
	}

	# print(f"{a}\n")
	# print(f"{b}\n")
	# print(f"{c}")

	a_pd = pd.DataFrame(a)

	b_pd =pd.DataFrame(b)

	c_pd =pd.DataFrame(c)

	ab_pd = a_pd.merge(b_pd, on=['timestamp'], how='outer')

	ac_pd = a_pd.merge(c_pd, on=['timestamp'], how='outer')

	# print(f"{a_pd.head()}\n")

	# print(f"{b_pd.head()}\n")

	# print(f"{c_pd.head()}\n")

	# print(f"{ab_pd}\n")

	# print(f"{ab_pd.fillna(method='ffill')}\n")


	print(f"{ac_pd}\n")

	print(f"{ac_pd.fillna(method='ffill')}\n")

	ac_pd = ac_pd.fillna(method='ffill')
	ac_pd = ac_pd.fillna(method='bfill')

	print(f"Dict {ac_pd.to_dict('list').__str__()}")

	udp = UDPHandler(target_port=55000)

	print(f"data : {udp.receive_packet()}")

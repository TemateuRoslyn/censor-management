"""Example of AI raw operation."""
import pprint
import time

import nidaqmx

pp = pprint.PrettyPrinter(indent=4)

with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai7")

    task.start()

    print("Print real data : ")

    while True:

        data = task.read(number_of_samples_per_channel=1)
        pp.pprint(data)
        time.sleep(10)

    # in_stream = task.in_stream

    # print("1 Channel 1 Sample Read Raw: ")
    # data = in_stream.read(number_of_samples_per_channel=1)
    # pp.pprint(data)

    # print("1 Channel N Samples Read Raw: ")
    # data = in_stream.read(number_of_samples_per_channel=8)
    # pp.pprint(data)

    
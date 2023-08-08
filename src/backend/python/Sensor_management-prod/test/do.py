"""Example for writing digital signal."""
import nidaqmx
import time
from nidaqmx.constants import LineGrouping

def flashes(event, task, data, period=0.25, off_state = [False,False,False,False]):

    while event:

        task.write(data)

        time.sleep(period)

        task.write(off_state)

        time.sleep(period)



with nidaqmx.Task() as task:
    task.do_channels.add_do_chan(
        "Dev1/port0/line1:4", line_grouping=LineGrouping.CHAN_PER_LINE
    )

    task.start()

    l = [[0,0,0,0],[0,0,0,1],[0,0,1,0],[0,0,1,1],[0,1,0,0],[0,1,0,1],[0,1,1,0],[0,1,1,1],[1,0,0,0],[1,0,0,1],[1,0,1,0],[1,0,1,1],[1,1,0,0],[1,1,0,1],[1,1,1,0],[1,1,1,1]]

    lb = [[True,True,True,True],[True,True,True,False],[True,True,False,True],[True,True,False,False],[True,False,True,True],[True,False,True,False],[True,False,False,True],[True,False,False,False],[False,True,True,True]]

    # for elt in lb:

    #     print(f"{elt}")

    #     print(task.write(elt))


    #     time.sleep(3)

    data=[True,True,True,False]

    flashes(True, task, data, period=0.25, off_state=[False,False,True,False])

    
    # while True :

    #     try:
    #         print("N Lines 1 Sample Boolean Write (Error Expected): ")
    #         print(task.write([True, True, True, True]))

    #         #print(task.write([False, False, False, False]))
    #     except nidaqmx.DaqError as e:
    #         print(e)

    # print("1 Channel N Lines 1 Sample Unsigned Integer Write: ")
    # print(task.write(8))

    # print("1 Channel N Lines N Samples Unsigned Integer Write: ")
    # print(task.write([1, 2, 4, 8], auto_start=True))
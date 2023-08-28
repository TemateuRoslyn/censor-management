import nidaqmx
import threading
import time
from nidaqmx.constants import LineGrouping

event_pfi1 = [False]
event_pfi2 = [False]
event_pfi3 = [False]


def send_events(event, chan, period):
    

    with nidaqmx.Task() as task:

        task.do_channels.add_do_chan(
            chan, line_grouping=LineGrouping.CHAN_PER_LINE
        )
        
        task.start()

        while not event[0]:

            task.write(True)

            time.sleep(period)

            task.write(False)

            time.sleep(period)

        task.close()

if __name__ == "__main__":


    t1 = threading.Thread(target=send_events,args=(event_pfi1,"/Dev1/PFI1",0.05 ))
    t2 = threading.Thread(target=send_events,args=(event_pfi2,"/Dev1/PFI2",1 ))
    t3 = threading.Thread(target=send_events,args=(event_pfi3,"/Dev1/PFI3",0.03 ))

    t1.start()
    t2.start()
    t3.start()

    time.sleep(120)

    event_pfi1[0] = True
    event_pfi2[0] = True
    event_pfi3[0] = True

    t1.join()
    t2.join()
    t3.join()



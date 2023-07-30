
import nidaqmx
from nidaqmx.constants import AcquisitionType, Edge, LineGrouping
from nidaqmx.types import CtrTime, CtrTick, CtrFreq
from datetime import datetime as Date


class ChannelsAI:

    def __init__(self):
        self.rate = 10000
        self.buffer_size = 1000000
        self.sample_per_chan = 1000
        self.sample_mode = AcquisitionType.CONTINUOUS
        self.active_edge = Edge.RISING
        self.device = "Dev1"
        self.channels = ["ai0", "ai1", "ai2", "ai3", "ai4", "ai5", "ai6", "ai7"]
        self.collect_time = 10.0
        self.task = None
        self.queue = []

    def __init__(self, rate=10000, buffer_size=1000000, sample_per_chan=1000,
                 sample_mode=AcquisitionType.CONTINUOUS, active_edge=Edge.RISING,
                 device="Dev1", channels=["ai0", "ai1", "ai2", "ai3", "ai4", "ai5", "ai6", "ai7"],
                 collect_time=10.0):
        self.rate = rate
        self.buffer_size = buffer_size
        self.sample_per_chan = sample_per_chan
        self.sample_mode = sample_mode
        self.active_edge = active_edge
        self.device = device
        self.channels = channels
        self.collect_time = collect_time
        self.task = None
        self.queue = []

    
    def init_task (self):

        task = nidaqmx.Task()

        for ch in self.channels : 
            task.ai_channels.add_ai_voltage_chan(f"{self.device}/{ch}")

        task.timing.cfg_samp_clk_timing(self.rate,active_edge=self.active_edge, sample_mode=self.sample_mode,samps_per_chan=self.buffer_size)

        self.task = task

        self.task.start()

        return self.task
    

    def close_task(self):

        self.task.close()

    def get_data(self):
        return self.queue

    def clear_queue(self):
        self.queue = []
    

    def read_datas(self):

        if self.task == None :

            self.init_task()
        

        message = {}

        message ['time_start'] = Date.now().isoformat()               

        message ['values'] = self.task.read(number_of_samples_per_channel=self.sample_per_chan)

        message ['time_stop'] = Date.now().isoformat()

        message ['sample_rate'] = self.rate

        message['channels'] = self.channels

        self.queue.append(message)

        return message
    

    

class ChannelDI:

    def __init__(self) -> None:

        self.lines = "/port0/line"
        self.device = "Dev1"
        self.num_di = "0-7"
        self.sample_size = 1
        self.grouping = LineGrouping.CHAN_PER_LINE
        self.task = None

    
    def init_task(self):

        task = nidaqmx.Task()
        
        task.di_channels.add_di_chan(lines=f"{self.device}{self.lines}{self.num_di}", line_grouping=self.grouping)

        self.task = task

        self.task.start()

        return task
        

    def read_data(self):        

        samples = {}
        
        samples['time'] = Date.now().isoformat()            

        samples['values'] = self.task.read(number_of_samples_per_channel=self.sample_size)

        return samples
    


class ChannelDO:

    def __init__(self) -> None:

        self.lines = "/port0/line"
        self.device = "Dev1"
        self.num_do = "0-7"
        self.grouping = LineGrouping.CHAN_FOR_ALL_LINES

    
    def init_task(self):

        task = nidaqmx.Task()
        
        task.do_channels.add_do_chan(lines=f"{self.device}{self.lines}{self.num_do}", line_grouping=self.grouping)

        self.task = task

        self.task.start()

        return task

    def write_data(self, data):

        t = self.task.write(data=data)

        return t
    


class ChannelCI:

    def __init__(self) -> None:

        self.channels = ["ctr0"]
        self.device = "Dev1"
        self.sample_size = 1
        self.task = None


    def init_task(self):

        task = nidaqmx.Task()
        
        task.ci_channels.add_ci_pulse_chan_freq(counter=f"{self.device}/{self.channels[0]}")

        self.task = task

        self.task.start()

        return task
        

    def read_data(self):        

        samples = {}
        
        samples['time'] = Date.now().isoformat()            

        samples['values'] = self.task.read(number_of_samples_per_channel=self.sample_size)

        return samples
    



class ChannelCO:

    def __init__(self) -> None:

        self.channels = ["ctr1", "ctr2"]
        self.device = "Dev1"
        self.sample_size = 1
        self.low_time = 0.01
        self.high_time = 0.01
        self.sample_mode = AcquisitionType.CONTINUOUS
        self.task = None

    def init_task_time(self):

        task = nidaqmx.Task()
        
        task.co_channels.add_co_pulse_chan_time(counter=f"{self.device}/{self.channels[0]}", low_time=self.low_time, high_time=self.high_time)

        task.timing.cfg_implicit_timing(sample_mode=self.sample_mode)

        self.task = task

        self.task.start()

        return task
    
    def init_task_freq(self):

        task = nidaqmx.Task()
        
        task.co_channels.add_co_pulse_chan_freq(counter=f"{self.device}/{self.channels[0]}")

        self.task = task

        self.task.start()

        return task
    
    def init_task_tick(self):

        task = nidaqmx.Task()
        
        task.co_channels.add_co_pulse_chan_ticks(counter=f"{self.device}/{self.channels[0]}")

        self.task = task

        self.task.start()

        return task

    def write_data_CtrTime(self):

        sample = CtrTime(high_time=0.001, low_time=0.002)

        self.task.write(sample)

    def write_data_CtrFreq(self):

        sample = CtrFreq(freq=0.1)

        self.task.write(sample)

    def write_data_CtrTick(self):

        sample = CtrTick(high_tick=0.01, low_tick=0.02)

        self.task.write(sample)





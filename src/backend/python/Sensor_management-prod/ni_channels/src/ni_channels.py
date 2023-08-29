
import nidaqmx
from nidaqmx.constants import AcquisitionType, Edge, LineGrouping
from nidaqmx.types import CtrTime, CtrTick, CtrFreq
from datetime import datetime as Date


class ChannelsAI:

    def __init__(self):
        self.rate = 10000
        self.buffer_size = 268435455
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
        self.queue = []
        self.task.close()

    def get_data(self):
        return self.queue

    def clear_queue(self):
        self.queue = []
    

    def read_datas(self):

        if self.task == None :

            self.init_task()
        

        message = {}

        message ['time_start'] = Date.utcnow().isoformat(sep=" ")               

        message ['values'] = self.task.read(number_of_samples_per_channel=self.sample_per_chan)

        message ['time_stop'] = Date.utcnow().isoformat(sep=" ")

        message ['sample_rate'] = self.rate

        message['channels'] = self.channels

        self.queue.append(message)

        return message
    
class ChannelsAO:

    def __init__(self):
        self.rate = 10000
        self.device = "Dev1"
        self.channels = ["ao0", "ao1"]
        self.collect_time = 10.0

    def __init__(self, rate=10000, device="Dev1", channels=["ao0", "ao1"]):
        self.rate = rate
        self.device = device
        self.channels = channels
        self.task = None

    
    def init_task (self):

        task = nidaqmx.Task()

        for ch in self.channels : 
            task.ai_channels.add_ai_voltage_chan(f"{self.device}/{ch}")

        task.timing.cfg_samp_clk_timing(self.rate)

        self.task = task

        return self.task
    

    def write_voltage(self, voltage):

        try:

            self.task.write(voltage)

            print(f"Voltage {voltage} V written to channel {self.channels}")

        except Exception as e:

            print(f"Error writing voltage: {e}")
    

    def close_task(self):

        self.task.close()

    

    

class ChannelDI:

    def __init__(self) -> None:

        self.lines = "/port0/line"
        self.device = "Dev1"
        self.num_di = "0-7"
        self.sample_size = 1
        self.grouping = LineGrouping.CHAN_PER_LINE
        self.task = None

    def __init__(self, lines, device, num_di, sample_size):

        self.lines = lines
        self.device = device
        self.num_di = num_di
        self.sample_size = sample_size
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

        samples['values'] = self.task.read(number_of_samples_per_channel=self.sample_size)
        
        samples['time'] = Date.utcnow().isoformat(sep=" ") 

        return samples
    
    def close_task(self):

        self.task.close()
    


class ChannelDO:

    def __init__(self) -> None:

        self.lines = "port0/line"
        self.device = "Dev1"
        self.num_do = "0:7"
        self.grouping = LineGrouping.CHAN_PER_LINE
        self.task = None

    def __init__(self, lines, device, num_do):

        self.lines = lines
        self.device = device
        self.num_do = num_do
        self.grouping = LineGrouping.CHAN_PER_LINE
        self.task = None

    
    def init_task(self):

        task = nidaqmx.Task()

        lines=f"{self.device}/{self.lines}{self.num_do}"

        print(lines)
        
        task.do_channels.add_do_chan(lines=f"{self.device}/{self.lines}{self.num_do}", line_grouping=self.grouping)

        self.task = task

        self.task.start()

        return task

    def write_data(self, data):

        t = self.task.write(data=data)

        return t
    
    def close_task(self):

        self.task.close()
    


class ChannelCI:

    def __init__(self) -> None:

        self.channel = "ctr0"
        self.device = "Dev1"
        self.sample_size = 1
        self.task = None

    def __init__(self, channel, device, sample_size):

        self.channel = channel
        self.device = device
        self.sample_size = sample_size
        self.task = None


    def init_task_pulse_freq(self):

        task = nidaqmx.Task()
        
        task.ci_channels.add_ci_pulse_chan_freq(counter=f"{self.device}/{self.channel}")

        self.task = task

        self.task.start()

        return task
    

    def init_task_pulse_ticks(self):

        task = nidaqmx.Task()
        
        task.ci_channels.add_ci_pulse_chan_ticks(counter=f"{self.device}/{self.channel}")

        self.task = task

        self.task.start()

        return task
    

    def init_task_pulse_time(self):

        task = nidaqmx.Task()
        
        task.ci_channels.add_ci_pulse_chan_time(counter=f"{self.device}/{self.channel}")

        self.task = task

        self.task.start()

        return task
    


    def init_task_period(self):

        task = nidaqmx.Task()
        
        task.ci_channels.add_ci_period_chan(counter=f"{self.device}/{self.channel}")

        self.task = task

        self.task.start()

        return task
    

    def init_task_freq(self):

        task = nidaqmx.Task()
        
        task.ci_channels.add_ci_freq_chan(counter=f"{self.device}/{self.channel}")

        self.task = task

        self.task.start()

        return task
    

    def init_task_two_edge(self):

        task = nidaqmx.Task()
        
        task.ci_channels.add_ci_two_edge_sep_chan(counter=f"{self.device}/{self.channel}")

        self.task = task

        self.task.start()

        return task
    

    def init_task_gps_timestamp(self):

        task = nidaqmx.Task()
        
        task.ci_channels.add_ci_gps_timestamp_chan(counter=f"{self.device}/{self.channel}")

        self.task = task

        self.task.start()

        return task
    
    def init_task_pulse(self):
    
        task = nidaqmx.Task()
        
        task.ci_channels.add_ci_pulse_width_chan(counter=f"{self.device}/{self.channel}")

        self.task = task

        self.task.start()

        return task
    
    def init_task_semi_period(self):
    
        task = nidaqmx.Task()
        
        task.ci_channels.add_ci_semi_period_chan(counter=f"{self.device}/{self.channel}")

        self.task = task

        self.task.start()

        return task
        

    def read_data(self):        

        samples = {}          

        samples['values'] = self.task.read(number_of_samples_per_channel=self.sample_size)
        
        samples['time'] = Date.utcnow().isoformat()  

        return samples
    
    def close_task(self):

        self.task.close()
    



class ChannelCO:

    def __init__(self) -> None:

        self.channel = "ctr1"
        self.device = "Dev1"
        self.sample_size = 1
        self.low_time = 0.01
        self.high_time = 0.01
        self.sample_mode = AcquisitionType.CONTINUOUS
        self.task = None

    def init_task_pulse_time(self):

        task = nidaqmx.Task()
        
        task.co_channels.add_co_pulse_chan_time(counter=f"{self.device}/{self.channel}", low_time=self.low_time, high_time=self.high_time)

        task.timing.cfg_implicit_timing(sample_mode=self.sample_mode)

        self.task = task

        self.task.start()

        return task
    
    def init_task_pulse_freq(self):

        task = nidaqmx.Task()
        
        task.co_channels.add_co_pulse_chan_freq(counter=f"{self.device}/{self.channel}")

        self.task = task

        self.task.start()

        return task
    
    def init_task_pulse_tick(self):

        task = nidaqmx.Task()
        
        task.co_channels.add_co_pulse_chan_ticks(counter=f"{self.device}/{self.channel}")

        self.task = task

        self.task.start()

        return task

    def write_data_CtrTime(self, high_time, low_time):

        sample = CtrTime(high_time=high_time, low_time=low_time)

        self.task.write(sample)

        return sample

    def write_data_CtrFreq(self, freq):

        sample = CtrFreq(freq=freq)

        self.task.write(sample)

        return sample

    def write_data_CtrTick(self, high_tick, low_tick):

        sample = CtrTick(high_tick=high_tick, low_tick=low_tick)

        self.task.write(sample)

        return sample

    def close_task(self):

        self.task.close()





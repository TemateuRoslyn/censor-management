import redis

class RedisStreamReader:
    def __init__(self, stream_name,redis_host='localhost', redis_port=6379, consumer_group='mygroup', consumer_name='myconsumer'):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.streams = stream_name
        self.consumer_group = consumer_group
        self.consumer_name = consumer_name
        self.redis_conn = redis.Redis(host=self.redis_host, port=self.redis_port, decode_responses=True)
    
    def create_consumer_group(self):

        if type(self.streams)=="str":
            try:
                self.redis_conn.xgroup_create(self.streams, self.consumer_group, id='0', mkstream=True)
                print(f"Consumer group '{self.consumer_group}' created.")
            except redis.exceptions.ResponseError as e:
                if "BUSYGROUP Consumer Group name already exists" in str(e):
                    print(f"Consumer group '{self.consumer_group}' already exists.")
                else:
                    print(f"Error creating consumer group: {e}")

        else:
            for stream in self.streams:
                try:
                    self.redis_conn.xgroup_create(stream, self.consumer_group, id='0', mkstream=True)
                    print(f"Consumer group '{self.consumer_group}' created.")
                except redis.exceptions.ResponseError as e:
                    if "BUSYGROUP Consumer Group name already exists" in str(e):
                        print(f"Consumer group '{self.consumer_group}' already exists.")
                    else:
                        print(f"Error creating consumer group: {e}")

    
    def read_stream(self):
        try:

            if type(self.streams)=="str":
                while True:
                    messages = self.redis_conn.xreadgroup(groupname=self.consumer_group, consumername=self.consumer_name,
                                                        streams={self.stream_name: '>'}, count=1, block=0)
                    for _, message in messages:
                        message_id = message[0]
                        message_data = message[1]
                        print(f"Message ID: {message_id}, Message Data: {message_data}")
            else:
                while True:
                # Prepare the streams for xreadgroup in the format ('stream_name', '>')
                    streams_with_start = [(stream, '>') for stream in self.streams]
                    
                    messages = self.redis_conn.xreadgroup(groupname=self.consumer_group, consumername=self.consumer_name,
                                                        streams=streams_with_start, count=1, block=0)
                    for stream_name, message_list in messages:
                        message_id = message_list[0][0]
                        message_data = message_list[0][1]
                        print(f"Stream: {stream_name}, Message ID: {message_id}, Message Data: {message_data}")
        
        except KeyboardInterrupt:
            print("Stream reading stopped by user.")

    def last_delivery_id(self, stream):

        lastid='>'

        lis = self.redis_conn.xinfo_groups(stream)

        if len(lis)!=0:
            for elt in lis:
                if elt['name']==self.consumer_group:
                    lastid = elt['last-delivered-id']

        return lastid

    
    def read_one_streams(self):
        try:
            # Prepare the streams and last-delivered IDs for xreadgroup
            streams_with_start = {}
            for stream in self.streams:
                streams_with_start[f"{stream}"] = self.last_delivery_id(stream)

                
            # last_delivered_ids = {stream: '>' for stream in self.streams}
            print(f"{streams_with_start}")  
            messages = self.redis_conn.xreadgroup(groupname=self.consumer_group, consumername=self.consumer_name,
                                                      streams=streams_with_start, count=1, block=0)
            if messages is not None:

                for stream_name, message_list in messages:

                    if len(message_list)>0:

                        if len(message_list[0])>0:
                            message_id = message_list[0][0]
                            # message_data = message_list[0][1]
                            # last_delivered_ids[stream_name] = message_id
                            # print(f"Stream: {stream_name}, Message ID: {message_id}, Message Data: {message_data}")
                            # Acknowledge the message
                            self.redis_conn.xack(stream_name, self.consumer_group, message_id)
                            print(f"Message ID {message_id} acknowledged.")

            return messages
        except KeyboardInterrupt:
            print("Stream reading stopped by user.")
    
    def write(self, stream, data):

        self.redis_conn.xadd(stream, data)

    def close(self):
        self.redis_conn.close()
    


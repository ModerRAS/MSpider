import json
from multiprocessing import Process

import zmq

from Config import MaxQueueLength


class MessageQueue(Process):
    def __init__(self, InsideCode, ServerPort: int = 5555, name: str = "MessageQueue"):
        Process.__init__(self)
        self.__name__ = name
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://0.0.0.0:" + str(ServerPort))
        self.queue = {}
        self.InsideCode = InsideCode
        self.mode = {1:self.mode_put_queue,2:self.mode_get_queue}

    def run(self):
        while True:
            message = json.loads(self.socket.recv_json())
            index, value = self.InsideCode(message)
            self.mode[index](value)

    def __get_queue_length(self, mode:int):
        try:
            self.queue[mode]
        except KeyError as e:
            self.queue[mode] = []
        return len(self.queue[mode])

    def mode_put_queue(self, mode:int, li:list):
        length = self.__get_queue_length(mode)
        if length >= MaxQueueLength:
            self.socket.send_json([-1,])
        else:
            list(map(lambda x:self.queue[mode].append(x),li))
            self.socket.send_json([0,])

    def mode_get_queue(self,mode:int):
        length = self.__get_queue_length(mode)
        try:
            self.socket.send_json(json.dumps([0,self.queue[mode].pop(0)]))
        except IndexError as e:
            self.socket.send_json(json.dumps([-1,]))

import json
from queue import Queue

import zmq
from multiprocessing import Process

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
        self.mode = {1:self.mode_append_queue}

    def run(self):
        while True:
            message = json.loads(self.socket.recv_json())
            index, value = self.InsideCode(message)
            self.mode[index](value)

    def mode_append_queue(self,mode:int,li:list):
        try:
            self.queue[mode]
        except KeyError as e:
            self.queue[mode] = []
        length = len(self.queue[mode])
        if length >= MaxQueueLength:
            return -1
        else:
            list(map(lambda x:self.queue[mode].append(x),li))
            return 0



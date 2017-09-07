import json

import zmq
from multiprocessing import Process


class MessageQueue(Process):
    def __init__(self, InsideCode, ServerPort: int = 5555, name: str = "MessageQueue"):
        Process.__init__(self)
        self.__name__ = name
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://0.0.0.0:" + str(ServerPort))
        self.queue = {}
        self.InsideCode = InsideCode

    def run(self):
        while True:
            message = json.loads(self.socket.recv_json())
            self.InsideCode(message)
            
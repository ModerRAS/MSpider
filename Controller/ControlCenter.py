import json

import zmq
from multiprocessing import Process

from Config import *


class ControlCenter(Process):
    def __init__(self):
        Process.__init__(self)
        self.__name__ = "ControlCenter"
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://0.0.0.0:" + str(ServerPort))
        self.queue = {}

    def run(self):
        recv = json.loads(self.socket.recv_json())
        a = 0


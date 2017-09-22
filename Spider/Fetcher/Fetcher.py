import json
from multiprocessing.dummy import Process

import requests
from pika.channel import Channel

from Util import MailBox


class Fetcher(Process):
    def __init__(self):
        super().__init__()
        self.mail_box = MailBox(Exchange="MSpider", Queue="Fetcher")

    def run(self):
        def callback(ch: Channel, method, properties, body):
            """
            body 是一个json文档，然后里面就一个链接的list，list里面就一个链接
            :param ch:
            :param method:
            :param properties:
            :param body:
            :return:
            """
            text = requests.get(json.loads(str(body, encoding="utf-8"))).text
            self.mail_box.send(json.dumps([text, ]))
            ch.basic_ack(delivery_tag=method.delivery_tag)

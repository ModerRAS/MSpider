import pika


class MailBox:
    def __init__(self, Exchange: str, Queue: str, PrefetchCount: int = 1, ServerHost: str = "localhost",
                 ExchangeType: str = "direct", Durable: bool = False):
        self.Exchange = Exchange
        self.Queue = Queue
        self.PrefetchCount = PrefetchCount
        self.ServerHost = ServerHost
        self.ExchangeType = ExchangeType
        self.Durable = Durable
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(ServerHost))
        self.channel = self.conn.channel()
        self.result = self.channel.queue_declare(queue=Queue, durable=Durable)
        self.channel.exchange_declare(durable=Durable,
                                      exchange=Exchange,
                                      exchange_type=ExchangeType)
        self.channel.queue_bind(exchange=Exchange,
                                queue=self.result.method.queue,
                                routing_key="")
        self.channel.basic_qos(PrefetchCount)

    def __del__(self):
        self.conn.close()

    def send(self, message):
        return self.channel.basic_publish(exchange=self.Exchange,
                                          routing_key=self.Queue,
                                          body=message,
                                          properties=pika.BasicProperties(delivery_mode=2))

    def receive(self, callback):
        self.channel.basic_consume(callback, queue=self.Queue, no_ack=False)
        self.channel.start_consuming()

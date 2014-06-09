import kombu
import kombu.mixins


class Worker(kombu.mixins.ConsumerMixin):
    def __init__(self, connection, config):
        self.exchange = kombu.Exchange(config['queue'], type='direct')
        self.queue = kombu.Queue(config['queue'], self.exchange,
                                 routing_key=config['queue'])
        self.connection = connection
        self.config = config
        self.methods = []

    def register_method(self, class_, config_key):
        self.methods.append(class_(self.config[config_key]))

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=[self.queue],
                         callbacks=[self.process_message])]

    def process_message(self, body, message):
        for method in self.methods:
            method.send_message(message.payload)
        message.ack()

    def close(self):
        for method in self.methods:
            method.close()

import twilio.rest
from pagerglue.methods.base import PageMethod


class SMS(PageMethod):
    def __init__(self, config):
        self.config = config
        self.client = twilio.rest.TwilioRestClient(
            self.config['twilio_account_sid'],
            self.config['twilio_auth_token'])

    def send_message(self, message):
        for recipient in self.config['notify']:
            result = self.client.messages.create(
                to=recipient,
                from_=self.config['sender'],
                body=message)

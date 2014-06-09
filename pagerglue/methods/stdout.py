from pagerglue.methods.base import PageMethod


class Stdout(PageMethod):
    def send_message(self, message):
        print(message)

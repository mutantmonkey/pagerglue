import logging
import sleekxmpp
from pagerglue.methods.base import PageMethod

logger = logging.getLogger(__name__)


class XMPPBackend(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password, notify_jids):
        super().__init__(jid, password)

        self.notify_jids = notify_jids

        self.add_event_handler('session_start', self.start, threaded=True)

    def start(self, event):
        self.send_presence()
        self.get_roster()

        # check existing roster for jids we don't want
        for jid in self.roster[self.jid]:
            if jid != self.jid and jid not in self.notify_jids:
                logger.debug("Remove {} from roster".format(jid))
                self.update_roster(jid, subscription='remove')

        # add jids to roster, if needed
        for jid in self.notify_jids:
            if jid not in self.roster[self.jid]:
                logger.debug("Add {} to roster".format(jid))
                self.update_roster(jid, subscription='both')

    def send_message(self, to, body):
        msg = self.Message()
        msg['to'] = to
        msg['body'] = body
        msg.send()


class XMPP(PageMethod):
    xmpp_jid = None
    xmpp_password = None
    notify_jids = None

    def __init__(self, config, *args, **kwargs):
        if set(('jid', 'password', 'notify')) <= set(config):
            self.xmpp_jid = config['jid']
            self.xmpp_password = config['password']
            self.notify_jids = config['notify']
        else:
            logger.warning(
                "Missing XMPP configuration options; XMPP support disabled.")

        self.xmpp = XMPPBackend(self.xmpp_jid, self.xmpp_password,
                                self.notify_jids)

        if self.xmpp.connect():
            logger.debug("Connected to XMPP server")
            self.xmpp.process(block=False)
        else:
            logger.warning(
                "Failed to connect to XMPP server; XMPP will be disabled.")

    def send_message(self, message):
        if not self.xmpp or not self.notify_jids:
            return

        for user in self.notify_jids:
            self.xmpp.send_message(user, message)

    def close(self):
        self.xmpp.disconnect(wait=True)

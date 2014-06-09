import kombu
import yaml
from pagerglue import worker
from pagerglue.methods import xmpp
#from pagerglue.methods import sms


if __name__ == '__main__':
    try:
        import xdg.BaseDirectory
        configpath = xdg.BaseDirectory.load_first_config('pagerglue/config.yml')
    except:
        configpath = os.path.expanduser('~/.config/pagerglue/config.yml')
    config = yaml.safe_load(open(configpath))

    with kombu.Connection(config['broker']) as conn:
        conn.ensure_connection()
        worker = worker.Worker(conn, config)
        worker.register_method(xmpp.XMPP, 'xmpp')
        #worker.register_method(sms.SMS, 'sms')
        try:
            worker.run()
        except KeyboardInterrupt:
            worker.close()

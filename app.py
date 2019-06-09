# coding=UTF-8

# Import modules.
import tornado.ioloop
import tornado.options
import tornado.locale
import tornado.web
import handler
import logging
import gtxclient
import configuration
import pygeoip
import redis
from urlparse import urlparse


# Define command line parameters.
tornado.options.define("port", type=int, default=8888,
                       help="Run this application on the given port, e.g. 80")
tornado.options.define("localhostonly", type=bool, default=False,
                       help="Listen on localhost only")



class GTXApplication(tornado.web.Application):
    """
    Main class for this application holding everything together.
    It defines the URL scheme for the API endpoints, configures application
    settings, initializes a tornado.web.Application instance and establishes
    db connections.
    """
    def __init__(self, username, password, domain, ssl, gtx_port, app_url):
        # Handlers defining the URL scheme.
        handlers = [
            (r"/validate_number/", handler.NumberValidationHandler),
        ] + self.parse_handler_from_config()
        if app_url:
            handlers += [(urlparse(app_url).path + '/dlr/', handler.DLRHandler)]
            dlr_url = app_url + '/dlr/'
        else:
            dlr_url = None
        
        # Setup GTX client.
        self.gtx_client = gtxclient.AsyncGTXClient(username, password,
                                                   domain=domain, ssl=ssl,
                                                   port=gtx_port,
                                                   dlr_url=dlr_url)
        
        # Load GeoIP database.
        self.geo_ip = pygeoip.GeoIP('GeoIP.dat', pygeoip.MEMORY_CACHE)
        self.geo_ipv6 = pygeoip.GeoIP('GeoIPv6.dat', pygeoip.MEMORY_CACHE)
        
        # Create db connection.
        self.redis = redis.StrictRedis(host=configuration.REDIS['host'],
                                       port=configuration.REDIS['port'],
                                       password=configuration.REDIS['password'],
                                       db=configuration.REDIS['selected_db'])
        
        # Configure application settings.
        settings = {'gzip': True}
        
        # Call super constructor to initiate a Tornado Application.
        tornado.web.Application.__init__(self, handlers, **settings)
        
    def parse_handler_from_config(self):
        handlers = []
        conf = configuration.SIMPLE_MESSAGE_HANDLERS
        for (k, v) in conf.iteritems():
            v['type'] = type('SimpleMessageHandler' + k,
                             (handler.SimpleMessageHandler,),
                             {'message': v['message'], 'sender': v['sender']})
            handlers.append((k, v['type']))
        return handlers



def main():
    """
    Main function to start the application. It parses command line arguments,
    initiates application classes, starts the server and Tornado's IOLoop.
    """
    tornado.options.parse_command_line()
    application = GTXApplication(username=configuration.GTX['username'],
                                 password=configuration.GTX['password'],
                                 domain=configuration.GTX['domain'],
                                 ssl=configuration.GTX['ssl'],
                                 gtx_port=configuration.GTX['port'],
                                 app_url=configuration.APP_URL)
    if tornado.options.options.localhostonly:
        address='127.0.0.1'
        logging.info("Listening to localhost only")
    else:
        address = ''
        logging.info("Listening to all addresses on all interfaces")
    application.listen(tornado.options.options.port, address=address,
                       xheaders=True)
    tornado.ioloop.IOLoop.instance().start()


# Run main method if script is run from command line.
if __name__ == "__main__":
    main()

# coding=UTF-8

# Import modules.
import phonenumbers
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
import os
import logging
from tornado.httputil import url_concat
import phonenumbers


class AsyncGTXClient(object):
    
    def __init__(self, username, password, domain='http.gtx-messaging.net',
                 ssl=False , port=13483, dlr_url=None):
        self.http_client = AsyncHTTPClient()
        self.username = username
        self.password = password
        self.domain = domain
        self.ssl = ssl
        self.port = port
        self.dlr_url = dlr_url
        
    
    def assamble_url(self, sender, to, text):
        """
        Assambles the url for sending a message. This will url encode
        all parameters.
        """
        phonenumber = phonenumbers.parse(to)
        to = phonenumbers.format_number(phonenumber, phonenumbers.PhoneNumberFormat.E164)
        params = {'username': self.username,
                  'password': self.password,
                  'from': sender,
                  'to': to,
                  'text': text}

        if self.dlr_url:
            params['dlr-mask'] = 7
            params['dlr-url'] = self.dlr_url
        
        url = 'http'
        if self.ssl: url += 's'
        url += '://' + self.domain + ':' + str(self.port)
        url = url_concat(url, params)

        return url
        
            
    def send_message(self, sender, to, text, callback):
        """
        Sends a message through the GTX Pro HTTP Gateway.
        """
        url = self.assamble_url(sender, to, text)
        logging.debug('Requesting GTX service: ' + url)
        request = HTTPRequest(url=url, method='GET')
        if self.ssl:
            request.ca_certs = os.path.join(os.path.dirname(__file__),
                                            'VenistaRoot.crt')
        
        # Define response callback.
        def handle_request(response):
            if response.error:
                logging.warning("Request failed: " + str(response.error))
                callback(False)
            else: callback(True)
                
        # Start request.
        self.http_client.fetch(request, handle_request)
    


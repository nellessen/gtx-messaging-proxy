GTX Messaging Proxy
===================
A proxy for gtx-messaging.com for implementing custom messaging services.  

Author: David Nellessen (https://github.com/nellessen)  
License: [MIT License](LICENSE)  

[GTX Messaging](http://www.gtx-messaging.com) is a SMS service. This application
provides a very simple, JSON-based web-API for accessing the
[GTX](http://www.gtx-messaging.com) API from public accessible web sites
or web applications. A typical use-case for this Proxy is a website that
provides a *send download link* form.

### Requirements
First of all you need Python and Redis on your machine running this application.
In addition install the following packages (assuming you are using PIP):
```Bash
pip install tornado
pip install pygeoip
pip install redis
pip install phonenumbers
git clone https://github.com/nellessen/gtx-messaging-proxy.git
cd gtx-messaging-proxy
```

### Configuration
Copy **configuration.example.py** to **configuration.py** and change the
configuration parameters accordingly:
- **GTX**: Use the connection Details and account information for your
  GTX Pro HTTP Gateway.
- **APP_URL**: Defines the URL under which the service will be available.
  you can put http://1.2.3.4:80 if your server's IP running this application
  is 1.2.3.4 and the port provided as
  [command line parameter](#running-the-application) is 80. Of course
  you can also use a proxy like nginx. Than you have to provide the URL
  configured in your proxy. This is used for the signal delivery report.
- **REDIS**: You need Redis running on your machine. If you haven't change
  the default Redis configuration you will not have to touch this most likely.
You can leave the rest as is for getting started.

### Running the Application
Run the following command from within the directory where this file is located:
```Bash
python app.py
```
This will start the server on port 8888 and accepting request for all hosts.
Three command line parameters are worth mentioning:
```Bash
python app.py --port=80 --localhostonly=True --logging=debug
```
This will start the server listening on port 80, accepting request from
localhost only (which is useful in a proxy setup e.g. nginx) and set the
log-level to debug (possible levels are debug, info, warning, error). Use 
warning or error log-level for production use. The logs will be printed
to stdout.

Defining Simple Message Handler
-------------------------------
A simple message handler can be defined in the configuration file. You will
find an example there:
```Python
SIMPLE_MESSAGE_HANDLERS['/example/'] = {'message': 'Welcome to GTX',
                                        'sender': 'Awesome Sender'}
```
This will create a message service as follows:

### Example Request
*Request URL*
```
http://1.2.3.4:80/example/
```

*Query String Parameters (URL-encoded)*
```
receiver: 017612345678
```

*Request Headers*
```
Request Method: GET
Accept: application/json
Accept-Language:en-US,en;q=0.8,de;q=0.6
Content-Type:application/json
```

### Example Response

*Response Headers*
```
Status Code: 200
Content-Type: application/json; charset=UTF-8
...
```
**Status Code**:
- 200: Request succeeded. Does not mean sending succeeded (see below).
- 404: You have requested a wrong URL
- 500: Server crashed

*Response Body*
```javascript
{
    "status": "ok",
    "message": "Message sent",
    "number": "+49 176 12345678"
}
```
The above response indicates that the request was successful and that the
GTX API call was successful. It does not garantee message delivery though.
It might take some time, depending on the GTX Pro HTTP Gateway product
your are using. The server log shows signal delivery report though.  

**No receiver phone number**:  
In case the no query string parameter *receiver* is sent you will receive the
following response body:
 ```javascript
{
    "status": "error",
    "error": "receiver_missing"
}
```

**Invalid phone number**:  
In case the phone number provided is invalid you will receive the following
response body:
 ```javascript
{
    "status": "error",
    "error": "receiver_validation"
}
```

**Request limit acceded**:  
In case you have performed to many requests from the same IP you will receive
the following response body:
 ```javascript
{
    "status": "error",
    "error": "limit_acceded"
}
```

**GTX Error**:  
If the GTX service response with an error you will receive the following
response body:
 ```javascript
{
    "status":"error",
    "error":"gtx_error",
    "message": "GTX Service Error",
    "number":"+49 176 49559259"
}
```
This happens in case the GTX Server is down or your account data configured
is wrong or if the remote service response with an error for any other reason.  

If everything is OK a message  *Welcome to GTX* from *Awesome Sender*
will be send to *+49 176 12345678*.


Features
--------
There are a couple of nice feature worth mentioning. First of all you can
regard this package as a framework for building messaging application
using the GTX Pro HTTP Gateway. The
[Simple Message Handler](#defining-simple-message-handler) is just a shortcut
for quickly implementing a standard use-case where you want to define a 
static message and sender ID and get an API end-point that sends this message
to a phone number given as query string parameter. But you can also implement
more complex handlers. Either way you will get several nice features:

### Phone number validation and normalization
The phone numbers will be validated and normalized. If the user does not
provide an international phone number the country of the user will be
guessed by his IP address with fallbacks to the browser locale or a default
country (you can turn this of in *configuration.GUESS_COUNTRY*). The geo-IP
features works in this app without external services needed. In addition
to the handler you configure there is a validation handler that validates
phone numbers the same way. You can use it it if you want to check a number
before sending a message. It is available under the path */validate_number/*.
You must provide the phone number to validate as the query string parameter
*number*.  
TODO: Detailed documentation of the validation service.

### Request limitation
To avoid unwanted costs there is a default limitation of requests on an
IP base for the messaging service (10 requests per hour) and for the validation
service (10 requests per minute).
This limitation uses Redis to count requests. This is very fast with in minimum
of memory needed. Another nice side-effect is that you can run multiple
instances of this application on the same machine and the limits will still
work as intended.

### Cross-Domain Requests
If you want to host the service on a domain separate from where your website
using the service lives, you normally face the same-origin-policy issue.
Therefore this application supports JSONP in addition to JSON. So if you are using
jQuery set `dataType: 'jsonp'` instead of `dataType: 'json'` in Ajax requests
and you won't run into same-origin issues.

### Scalability
Not yet tested. But unless I didn't implement any bugs this will be incredible
fast. This application is based on tornado which uses an event-drive,
non-blocking architecture which handles a lot of requests that don't need
much processing very well. You can even use a setup with nginx as a proxy
and start multiple instance of this application which will multiply the
performance. I hope the guys from GTX Messaging can handle it ;-)

Example
-------
Open the example.html for an example how to use a service.

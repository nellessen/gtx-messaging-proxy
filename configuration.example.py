# coding=UTF-8

# GTX Pro Configuration.
GTX = {}
# The GTX Pro HTTP Gateway domain.
GTX['domain'] = 'http.gtx-messaging.net'
# If true uses HTTPS instead of HTTP for request to the GTX Pro HTTP Gateway.
GTX['ssl'] = True
# The GTX Pro HTTP Gateway port. Use 13483 for Platinum, 13484 for gold and 13485 for silver.
GTX['port'] = 13483
# The GTX Pro HTTP Gateway username or account name.
GTX['username'] = 'YOU_GTX_USERNAME'
# The GTX Pro HTTP Gateway username or account password.
GTX['password'] = 'YOU_GTX_PASSWORT'

# The URL under which this application is available, used for signal delivery report.
APP_URL = 'http://YOUR_SERVERS_IP:8888'

# If True phone numbers will guessed if not given in international notion.
GUESS_COUNTRY = True
# Default locale (used to guess phone numbers)
DEFAULT_COUNTRY = 'DE'

# Configure Redis used to limit calls.
# Database settings for redis.
REDIS = {'host': 'localhost',
         'port': 6379,
         'selected_db': 0, # Database.
         'password': None}

# Configure how many number validations are allowed per IP in the given number of seconds.
VALIDATION_LIMIT = {'amount': 10, # Maximum of 10 number validation requests per IP ...
                    'expires': 60} # .. in 60 seconds allowed.

# Define simple message handlers. Syntax:
# SIMPLE_MESSAGE_HANDLERS['/desired_path/'] = {'message': 'The message that will be sent',
#                                              'sender': 'The sender title or phone number'}
SIMPLE_MESSAGE_HANDLERS = {}
SIMPLE_MESSAGE_HANDLERS['/example/'] = {'message': 'Welcome to GTX',
                                        'sender': 'Awesome Sender'}

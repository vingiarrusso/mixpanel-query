import requests
import time
import hashlib

class MixpanelQuery(object):
    def __init__(self):
        self.api_key = 'your api key'
        self.api_secret = 'your api secret'
        self.base_url = 'http://mixpanel.com/api/2.0/'
        self.expire = str(int(time.time()) + 600)
        self.default_params = {
            "api_key": self.api_key,
            "api_secret": self.api_secret,
            "expire": self.expire
        }

    def makeSignature(self, params):
        string_to_hash = ''.join('='.join(key) for key in sorted(params.items())) + self.api_secret
        return hashlib.md5(string_to_hash).hexdigest()

    def send(self, params):
        endpoint = params["endpoint"]
        del params["endpoint"]
        params.update(self.default_params)
        params.update({"sig": self.makeSignature(params)})
        response = requests.get('{}{}'.format(self.base_url, endpoint), params=params)
        data = response.json()
        return data


#example usage:
mixpanel_query = MixpanelQuery()
mixpanel_result = mixpanel_query.send({
    "endpoint": "events/properties",
    "type": "unique",
    "unit": "day",
    "interval": "2",
    "event": "your event",
    "name": "the property you want to grab from the event"})
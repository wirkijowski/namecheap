#import configparser
import urllib.request


class NamecheapConnection(object):


    def __init__(self, url='https://api.namecheap.com/xml.response',
            ApiUser=None, ApiKey=None, UserName=None, ClientIp=None):
        
        self.url = url
        self.xml_namespace = '{http://api.namecheap.com/xml.response}'

        self.parameters = {
            'ApiUser': ApiUser,
            'ApiKey': ApiKey,
            'UserName': UserName,
            'ClientIp': ClientIp,
        }

        self.headers = { 'User-Agent': 'api' }

    def __makerequest__(self, **kw_params):

        parameters = self.parameters

        for key, value in kw_params.items():
            parameters[key] = value
        data = urllib.parse.urlencode(parameters)
        data = data.encode('utf-8')
        req = urllib.request.Request(self.url, data)
        response = urllib.request.urlopen(req)
        recv = response.read()
        return recv.decode('utf-8')


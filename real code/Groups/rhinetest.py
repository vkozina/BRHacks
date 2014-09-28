from flask import Flask, request
import requests	
from requests import get, post

#self = Rhine(self, sdf0b913e4b07b5243b7f527)
#api_key = 'sdf0b913e4b07b5243b7f527'

class InvalidRequest(Exception):
    pass

class CallError(Exception):
    pass

class Rhine:
    conv = staticmethod(lambda es: ','.join(es) \
        if type(es) is list else es)
    conv_ = staticmethod(lambda es: ',' \
        .join(['(' + ','.join(sub) + ')' for sub in es]))
    
    def __init__(self, api_key):
        self.api_key = api_key

    def _call(self, req):
        response = get('http://api.rhine.io/' + self.api_key + '/' + req)
        try:
            data = response.json()
        except:
            raise InvalidRequest(req + ' is not a valid request.')
        if 'error' in data:
            raise CallError('Error: ' + data['error'])
        return data

    def distance(self, entity1, entity2):
        return float(self._call('distance/{0}/{1}' \
            .format(Rhine.conv(entity1), Rhine.conv(entity2)))['distance'])

    def synonym_check(self, entity1, entity2):
        return self._call('synonym_check/{0}/{1}' \
            .format(entity1, entity2))['synonym'] == 'True'

    def entity_extraction(self, text):
        return self._call('entity_extraction/{0}'.format(text))
            
    def closest_entities(self, entity):
        return self._call('closest_entities/{0}' \
            .format(entity))['closest_entities']

s = Rhine('sdf0b913e4b07b5243b7f527')
d = Rhine.distance(s, 'Pizza', 'Toast')
print(d)
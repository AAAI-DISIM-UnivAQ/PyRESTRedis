#coding:utf-8
'''
    PyRESTRedis A Python REST Interface to Redis key/value storage server
 
 Licensed with Apache Public License
 by AAAI Research Group
 Department of Information Engineering and Computer Science and Mathematics
 University of L'Aquila, ITALY
 http://www.disim.univaq.it

'''

__author__ = 'giodegas'

from flask import Flask
from flask.ext import restful
from flask.ext.restful import Resource

from redis import Redis

SERVICE_PORT = 8379
REDIS_IP = '127.0.0.1'

class ServiceDiscovery(Resource):
    def get(self):
        return {'available services': '/info, /get/.., /set/../.., /publish/../.., /keys/..'}

class SetKey(Resource):
    def get(self, key_id, value):
        global R
        out = R.set(key_id, value)
        return {'set': out}

class GetKey(Resource):
    def get(self, key_id):
        global R
        out = R.get(key_id)
        return {'get': out}

class Info(Resource):
    def get(self):
        global R
        out = R.info()
        return {'info': out}

class Keys(Resource):
    def get(self, keyPattern):
        global R
        out = R.keys(keyPattern)
        return {'keys': out}

class Publish(Resource):
    def get(self, channel_id, message):
        global R
        out = R.publish(channel_id, message)
        return {'publish': out}

# ------------------------------------------------------------

if __name__ == '__main__':
    app = Flask(__name__)
    api = restful.Api(app)

    api.add_resource(ServiceDiscovery, '/')
    api.add_resource(SetKey, '/set/<string:key_id>/<string:value>')
    api.add_resource(GetKey, '/get/<string:key_id>')
    api.add_resource(Publish, '/publish/<string:channel_id>/<string:message>')
    api.add_resource(Info, '/info')
    api.add_resource(Keys, '/keys/<string:keyPattern>')

    R = Redis(REDIS_IP)
    print 'REST Interface from ',REDIS_IP, R.info()

    app.run(debug=True, port=SERVICE_PORT)

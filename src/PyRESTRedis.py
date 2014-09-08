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

app = Flask(__name__)
api = restful.Api(app)

class ServiceDiscovery(Resource):
    def get(self):
        return {'SERVICES': '/INFO, /GET/.., /SET/../.., /EXISTS/.., /PUBLISH/../.., /KEYS/.., /SADD/../.., /SMEMBERS/.., /redis....'}

class SetKey(Resource):
    def get(self, key_id, value):
        global R
        out = R.set(key_id, value)
        return {'SET': out}

class GetKey(Resource):
    def get(self, key_id):
        global R
        out = R.get(key_id)
        return {'GET': out}

class Info(Resource):
    def get(self):
        global R
        out = R.info()
        return {'INFO': out}

class Keys(Resource):
    def get(self, keyPattern):
        global R
        out = R.keys(keyPattern)
        return {'KEYS': out}

class ExistsKey(Resource):
    def get(self, key_id):
        global R
        out = R.exists(key_id)
        return {'EXISTS': out}

class Sadd(Resource):
    def get(self, key_id, member):
        global R
        out = R.sadd(key_id, member)
        return {'SADD': out}

class Smembers(Resource):
    def get(self, key_id):
        global R
        out = list(R.smembers(key_id))
        return {'SMEMBERS': out}

class Publish(Resource):
    def get(self, channel_id, message):
        global R
        out = R.publish(channel_id, message)
        return {'PUBLISH': out}

class LIndex(Resource):
    def get(self, key_id, index):
        global R
        out = R.lindex(key_id, index)
        return {'LINDEX': out}

class Generic(Resource):
    def get(self, cmd, param1=None, param2=None, param3=None):
        global R
        cmdStr = 'R.'+ cmd +'('
        if param1:
            cmdStr += "'"+param1+"'"
            if param2:
                cmdStr += ",'"+param2+"'"
                if param3:
                    cmdStr += ",'"+param3+"'"
        cmdStr += ')'
        print 'executing..', cmdStr
        out = eval(cmdStr)
        return {cmd.upper(): out}

# ------------------------------------------------------------

@app.after_request
def after_request(response):
    # to allow to serve pages from the same server, different  port
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5000'
    response.headers['Access-Control-Allow-Headers'] = "Origin, X-Requested-With,Content-Type, Accept"
    return response

def addCommand(function, command, arguments=None):
    # add a service twice , lower and upper case
    global api
    urlStrUC = command.upper()
    urlStrLC = command.lower()
    if arguments:
        urlStrUC += '/' + arguments
        urlStrLC += '/' + arguments
    api.add_resource(function, urlStrLC, urlStrUC)

if __name__ == '__main__':
    addCommand(ServiceDiscovery, '/')
    addCommand(SetKey, '/set', '<string:key_id>/<string:value>')
    addCommand(GetKey, '/get','<string:key_id>')
    addCommand(Publish, '/publish','<string:channel_id>/<string:message>')
    addCommand(Info, '/info')
    addCommand(Keys, '/keys','<string:keyPattern>')
    addCommand(ExistsKey, '/exists','<string:key_id>')
    addCommand(Sadd, '/sadd','<string:key_id>/<string:member>')
    addCommand(Smembers, '/smembers','<string:key_id>')
    addCommand(LIndex, '/lindex', '<string:key_id>/<string:index>')

    # All other Redis command with up to 3 arguments, all lower case
    api.add_resource(Generic, '/redis/<string:cmd>',
                     '/redis/<string:cmd>/<string:param1>',
                     '/redis/<string:cmd>/<string:param1>/<string:param2>',
                     '/redis/<string:cmd>/<string:param1>/<string:param2>/<string:param3>')

    R = Redis(REDIS_IP)

    app.run(debug=True, port=SERVICE_PORT)

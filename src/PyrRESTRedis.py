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
from json import dumps

from redis import Redis

SERVICE_PORT = 8379
REDIS_IP = 'localhost'
HOST_IP = 'localhost'

app = Flask(__name__)
api = restful.Api(app)

class ServiceDiscovery(Resource):
    def get(self):
        return {'REDIS SERVICES': 'INFO, GET, SET, DEL, EXISTS, PUBLISH, KEYS, SADD, SMEMBERS, SREM, HSET, HGET, HGETALL, LPOP, SELECT, /redis....'}

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

class DelKey(Resource):
    def get(self, key_id):
        global R
        out = R.delete(key_id)
        return {'DEL': out}

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
        return dumps({'PUBLISH': out})

class LIndex(Resource):
    def get(self, key_id, index):
        global R
        out = R.lindex(key_id, index)
        return {'LINDEX': out}

class HSet(Resource):
    def get(self, key_id, field, value):
        global R
        out = R.hset(key_id, field, value)
        return {'HSET': out}

class HGet(Resource):
    def get(self, key_id, field):
        global R
        out = R.hget(key_id, field)
        if out and len(out)>4000000:
            print 'oversized response'
            out = False
        return {'HGET': out}

class HDel(Resource):
    def get(self, key_id, field):
        global R
        out = R.hdel(key_id, field)
        return {'HDEL': out}

class HExists(Resource):
    def get(self, key_id, field):
        global R
        out = R.hexists(key_id, field)
        return {'HEXISTS': out}

class HGetAll(Resource):
    def get(self, key_id):
        global R
        out = R.hgetall(key_id)
        return {'HGETALL': out}

class SetMemberRemove(Resource):
    def get(self, set_name, member):
        global R
        out = R.srem(set_name, member)
        return {'SREM': out}

class LPop(Resource):
    def get(self, listName):
        global R
        out = R.lpop(listName)
        return {'LPOP': out}

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

class DBSelect(Resource):
    def get(self, dbNum):
        global R
        R = None
        R = Redis(db=dbNum)
        out = 'ok'
        return {'SELECT': out}

class FlushDB(Resource):
    def get(self, password):
        global R
        if password=='_password_':
            out = R.flushdb()
            return {'FLUSHDB': out}
        else:
            return {'FLUSHDB': False}

# ------------------------------------------------------------

@app.after_request
def after_request(response):
    # to allow to serve pages from the same server, different  port
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5000'
    response.headers['Access-Control-Allow-Headers'] = "Origin, X-Requested-With,Content-Type, Accept"
    response.headers['Cache-Control'] = 'no-cache'
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
    R = Redis(REDIS_IP)

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
    addCommand(HSet, '/hset', '<string:key_id>/<string:field>/<string:value>')
    addCommand(HGet, '/hget', '<string:key_id>/<string:field>')
    addCommand(HDel, '/hdel', '<string:key_id>/<string:field>')
    addCommand(HGetAll, '/hgetall', '<string:key_id>')
    addCommand(HExists, '/hexists', '<string:key_id>/<string:field>')
    addCommand(DelKey, '/del', '<string:key_id>')
    addCommand(SetMemberRemove, '/srem', '<string:set_name>/<string:member>')
    addCommand(LPop, '/lpop', '<string:listName>')
    addCommand(DBSelect, '/select', '<int:dbNum>')
    addCommand(FlushDB, '/flushdb', '<string:password>')

    # All other Redis command with up to 3 arguments, all lower case
    api.add_resource(Generic, '/redis/<string:cmd>',
                     '/redis/<string:cmd>/<string:param1>',
                     '/redis/<string:cmd>/<string:param1>/<string:param2>',
                     '/redis/<string:cmd>/<string:param1>/<string:param2>/<string:param3>')

    app.run(debug=True, port=SERVICE_PORT, host=HOST_IP)

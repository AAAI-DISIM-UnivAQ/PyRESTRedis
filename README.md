PyRESTRedis
===========

Python Flask REST simplified interface to Redis

To use it, have [Redis](http://redis.io) server running, then run:

    $ python PyRESTRedis.py
    
and try Redis commands on port 8379:

to know which services are available: http://127.0.0.1:8379

    { "services": "/INFO, /GET/.., /SET/../.., /EXISTS/.., /PUBLISH/../.., /KEYS/.., /SADD/../.., /SMEMBERS/.., /redis...." }
to get information about the available Redis server: http://127.0.0.1:8379/info

to set a key with its value: http://127.0.0.1:8379/SET/mykey/1

    { "set": true }
to read a key content: http://127.0.0.1:8379/GET/mykey

    { "get": "1" }
to check if a key exists: http://127.0.0.1:8379/EXISTS/mykey

    { "exists": true }
to publish data to a Redis channel: http://127.0.0.1:8379/PUBLISH/myChannel/myData

    { "publish": 1 }

if the channel exists, otherwise:

    { "publish": 0 }

to get a list of keys from a pattern: http://127.0.0.1:8379/KEYS/_pattern_

other commands: sadd, smembers.

All Redis commands with up to 3 arguments can be used with: http://127.0.0.1:8379/redis/_command_/_arg1_../_arg3_  

## Dependencies
* [redis-py](http://github.com/andymccurdy/redis-py)
* [Flask](http://flask.pocoo.org)
* [FlaskRESTful](http://flask-restful.readthedocs.org)

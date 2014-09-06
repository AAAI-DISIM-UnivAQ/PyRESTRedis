PyRESTRedis
===========

Python Flask REST simplified interface to Redis

To use it, have [Redis](http://redis.io) server running, then run:

    $ python PyRESTRedis.py
    
and try to set, get your keys and publish to your channels on port 8379:

* to know which services are available: http://127.0.0.1:8379
    
you should have:

    {
    "available services": "/info, /get/.., /set/../.., /exists/.., /publish/../.., /keys/.."
    }

* to get information about the available Redis server: http://127.0.0.1:8379/info

* to set a key with its value: http://127.0.0.1:8379/set/mykey/1

you should have:

    {
    "set": true
    }
    
* to read a key content: http://127.0.0.1:8379/get/mykey

you should have:

    {
    "get": "1"
    }

* to check if a key exists: http://127.0.0.1:8379/exists/mykey
you should have:

    {
    "exists": true
    }

* to publish data to a Redis channel: http://127.0.0.1:8379/publish/myChannel/myData
   
you should have:

    {
    "publish": 1
    }

if the channel exists, otherwise:

    {
    "publish": 0
    }

* to get a list of keys from a pattern: http://127.0.0.1:8379/keys/_pattern_

## Dependencies
* [redis-py](http://github.com/andymccurdy/redis-py)
* [Flask](http://flask.pocoo.org)
* [FlaskRESTful](http://flask-restful.readthedocs.org)
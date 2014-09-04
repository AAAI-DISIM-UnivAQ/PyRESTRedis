PyRESTRedis
===========

Python Flask REST simplified interface to Redis

To use it, have [Redis](http://redis.io) server running, then run:

    $ python PyRESTRedis.py
    
and try to set, get your keys and publish to your channels on port 8379:

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

* to publish data to a Redis channel: http://127.0.0.1:8379/publish/myChannel/myData
   
you should have:

    {
    "publish": 1
    }

if the channel exists, otherwise:

    {
    "publish": 0
    }

* to know which services are available: http://127.0.0.1:8379
    
you should have:

    {
    "available services": "/get, /set, /publish"
    }

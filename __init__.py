#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
 Simple RPC using MSGPACK for data serialization over HTTP

 Require python-msgpack
 
 Quick server usage:
 import zrpc
 
 class MyRPCServer(zphprpc.Server):
   def rpc_myfx(a, b):
     return a + b
 MyRPCServer()


 Quick client usage:
 import zrpc
 rpc_client =  zphprpc.Client('http://myserver');
 echo rpc_client->myfx(4, 5);
"""

VERSION = 0.1

#import BaseHTTPServer
import requests
import msgpack

class Server(object): # TODO: server implementation not finished
    def __init__(self, listen_address='', listen_port=8000):
        self._listen_address = listen_address
        self._listen_port = listen_port

    def do_POST(self):
        pass

class Client(object):
    def __init__(self, url='http://localhost:8000', key=None):
        self.__url = url
        self.__key = key

    def __getattr__(self, method):
        def fx(*args, **kwargs):
            params = {'key': self.__key,
                      'type': 'fx_call',
                      'fx_name': method,
                      'arguments': msgpack.packb(args),
                      'kw_arguments': msgpack.packb(kwargs)}
            result = requests.post(self.__url, params)
            #print repr(result.content)
            try:
                r = msgpack.unpackb(result.content)
            except TypeError:
                print repr(result.text)
                raise Exception("zrpc error\nCan not parse answer.")
            if not isinstance(r, dict):
                print repr(result.text)
                raise Exception("zrpc error\nCan not parse answer.")
            del result
            if r['error'] is not False:
                print r['txt']
                raise Exception("zrpc error\n.%s" % r['error'])
            return r['result']
        if method[:2] == '__':
            return super(Client, self).__getattr__(method)
        return fx

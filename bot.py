#!/usr/bin/python
from __future__ import print_function

import sys
import socket
import json

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("test-exch-codebrew", 25000))
    return s.makefile('rw', 1)

def write(exchange, obj):
    json.dump(obj, exchange)
    exchange.write("\n")

def read(exchange):
    return json.loads(exchange.readline())

def main():
    exchange = connect()
    write(exchange, {"type": "hello", "team": "CODEBREW"})
    while True:
        hello_from_exchange = read(exchange)
        if isBond(hello_from_exchange):
            print(hello_from_exchange['symbol'], file=sys.stderr)




if __name__ == "__main__":
    main()
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
    message = read(exchange)
    print(message, file=sys.stderr)
    while True:
        try:
            message = read(exchange)
        except ValueError:
            print("Exception") 
        if 'symbol' in message and message['symbol'] == "BOND" and 'sell' in message:
            if to_buy(message['sell']):
                print(message, file=sys.stderr)


def to_buy(message):
    for t in message:
        print(t)
        if t[0] <= 1000:
            return True
            #Buy message['sell'][i][1] of them


if __name__ == "__main__":
    main()
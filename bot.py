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

    n_bonds = 0
    order_id = 0

    while True:
        try:
            message = read(exchange)
        except ValueError:
            print("Exception")
        if 'symbol' in message and message['symbol'] == "BOND" and 'sell' in message:
            if to_buy(message['sell'])[0] > 0:
                print(message, file=sys.stderr)
                write(exchange, {"type": "add", "order_id": order_id, "symbol": "BOND", "dir": "BUY", 
                                 "price": to_buy(message['sell'])[0], 
                                 "size": to_buy(message['sell'])[1]})
                order_id += 1
                print(n_bonds)
        elif 'type' in message:
            if message['type'] == "ack" or message['type'] == "reject":
                print(message, file=sys.stderr)

        elif 'type' in message and message['type'] == "fill": #filling order
          n_bonds += message["size"]
          print(message, file=sys.stderr)

        else:
            print(n_bonds)


def to_buy(message):
    for t in message:
        if t[0] <= 1000:
            return t
    return [0,0]
            #Buy message['sell'][i][1] of them


if __name__ == "__main__":
    main()
#!/usr/bin/python
from __future__ import print_function

import sys
import socket
import json


buys = [{"type": "add", "order_id": 0, "symbol": "BOND", "dir": "BUY", "price": 1000, "size": 2},
        {"type": "add", "order_id": 0, "symbol": "BOND", "dir": "BUY", "price": 999, "size": 5},
        {"type": "add", "order_id": 0, "symbol": "BOND", "dir": "BUY", "price": 998, "size": 2},
        {"type": "add", "order_id": 0, "symbol": "BOND", "dir": "BUY", "price": 997, "size": 1}]


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

    write(exchange, buy(0, order_id, 2))
    order_id += 1

    while True:
        try:
            message = read(exchange)
        except ValueError:
            print("Exception")
            break

        if 'type' in message and message['type'] == "fill": #filling order
          n_bonds += message["size"]
          print("Bought ", message["size"], " BONDs @ ", message["price"])
          write(exchange, buy(0, order_id, message["size"]))
          #print(message, file=sys.stderr)
        #elif 'symbol' in message and message['symbol'] == "BOND" and 'sell' in message:
        #    if to_buy(message['sell'])[0] > 0:
                #print(message, file=sys.stderr)
                #write(exchange, {"type": "add", "order_id": order_id, "symbol": "BOND", "dir": "BUY", 
                #                 "price": to_buy(message['sell'])[0], 
                #                 "size": to_buy(message['sell'])[1]})
                #order_id += 1
                #print(n_bonds)
        elif 'type' in message:
            if message['type'] == "ack" or message['type'] == "reject":
                print(message, file=sys.stderr)



def to_buy(message):
    for t in message:
        if t[0] <= 1000:
            return t
    return [0,0]
            #Buy message['sell'][i][1] of them

def buy(index, order_id, n):
  tmp = buys[index]
  tmp["order_id"] = order_id; tmp["size"] = n
  return tmp

if __name__ == "__main__":
    main()
#coding: utf-8

import socket
import struct

def main():
    s = socket.socket()
    s.connect(('localhost', 5555))
    s.send(struct.pack('>BHHHH', 32, 3, 1, 2, 3))
    s.close()


if __name__ == "__main__":
    main()
#coding: utf-8

from client import Client
from protocols import Protocol

def main():
    cl = Client(Protocol)
    cl.listen('', 9090)

if __name__ == "__main__":
    main()
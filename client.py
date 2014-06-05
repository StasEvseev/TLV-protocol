#coding: utf-8

from struct import *
import functools
import socket
import errno
from tornado import ioloop

from protocols import CheckDataError


class TLV(object):
    MAX_SIZE_PACKAGE = 2 ** 16 + 3
    FRM_TYPE = ">B"
    FRM_LENGTH = ">H"
    SIZE_HEAD_META = calcsize(FRM_TYPE) + calcsize(FRM_LENGTH)
    @classmethod
    def get_max_size(cls):
        return cls.MAX_SIZE_PACKAGE
    @classmethod
    def parse(cls, data):
        type_code = unpack_from(cls.FRM_TYPE, data)[0]
        size = unpack_from(cls.FRM_LENGTH, data, calcsize(cls.FRM_TYPE))[0]
        content = unpack_from(">%sB" % size, data, cls.SIZE_HEAD_META)
        return type_code, size, content


class Client(object):
    def __init__(self, protocol):
        self.protocol = protocol
        self.tlv = TLV
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def handle_connection(self, connection):
        data = connection.recv(self.tlv.get_max_size())
        type_code, length, data = self.tlv.parse(data)

        command = self.protocol.get_command(hex(type_code))
        try:
            command.do(length, data)
        except CheckDataError:
            print "Problem with data"

    def listen(self, host, port):
        def connection_ready(sock, handler, fd, events):
            while True:
                try:
                    connection, address = sock.accept()
                except socket.error, e:
                    if e.args[0] not in (errno.EWOULDBLOCK, errno.EAGAIN):
                        raise
                    return
                connection.setblocking(0)
                handler(connection)

        self.socket.bind((host, port))
        self.socket.setblocking(0)
        self.socket.listen(128)

        io_loop = ioloop.IOLoop.instance()
        callback = functools.partial(connection_ready, self.socket, self.handle_connection)
        io_loop.add_handler(self.socket.fileno(), callback, io_loop.READ)
        io_loop.start()

"""
Multipurpose RCON library in Python
by Anthony Nguyen
MIT Licensed, see LICENSE
"""

import socket
import time


class RConnection():
    """
    Base class for an RCON "connection", even though RCON is technically
    connectionless (UDP) Initialization takes an address, port, and password
    """
    _long_commands = ["map"]

    def __init__(self, host, port, password):
        self.host = host
        try:
            self.port = int(port)
        except ValueError:
            self.port = 27960
        self.password = password

        self.connect()

    def __enter__(self):
        if self.test():
            return self

    def __exit__(self, type, value, traceback):
        self.close()
        return traceback if traceback else True

    def connect(self):
        """Connect function that sets up the socket
        Meant for internal use"""
        self.close()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.connect((self.host, self.port))

    def close(self):
        try:
            self.socket.close()
            return True
        except AttributeError:
            return False

    def set_host(self, host):
        self.host = host
        self.connect()

    def set_port(self, port):
        try:
            self.port = int(port)
            self.connect()
        except ValueError:
            pass

    def set_password(self, password):
        self.password = password
        self.connect()

    def test(self):
        self.socket.settimeout(4)
        try:
            self.socket.send(b"test")
            self.socket.recv(65535)
            return True
        except:
            return False

    def recvall(self, timeout=0.5):
        self.socket.setblocking(False)
        ret = ""
        data = ""

        start = time.time()
        while True:
            if ret and time.time() - start > timeout:
                break
            elif time.time() - start > timeout * 2:
                break

            try:
                data = self.socket.recv(4096)
                if data:
                    ret += data[4:].decode()
                    start = time.time()
                else:
                    time.sleep(0.1)
            except:
                pass

        return ret

    def send(self, data):
        self.socket.send(b"\xFF\xFF\xFF\xFF" + "rcon {0} {1}".format(
            self.password, data).encode())

        if data.split(" ")[0] in self._long_commands:
            r = self.recvall(timeout=5)
        else:
            r = self.recvall()

        return r

"""
Multipurpose RCON library in Python
by Anthony Nguyen
updated to Python3 by Dustin S (texnofobix)
MIT Licensed, see LICENSE
"""

import threading as thread
import socket
import time


class RconError(Exception):
    """Raised whenever a RCON command cannot be evaluated"""
    pass


class RConnection(object):
    """
    Base class for an RCON "connection", even though RCON is technically
    connectionless (UDP) Initialization takes an address, port, and password
    """
    _host = ''  # host where the server is
    _port = 27960  # virtual port where to forward rcon commands
    _password = ''  # rcon password of the server
    _timeout = 0.5  # default socket timeout
    _rconsendheader = b'\xFF\xFF\xFF\xFF'
    _rconsendstring = 'rcon {0} {1}'  # rcon command pattern
    _rconreplystring = '\xFF\xFF\xFF\xFFprint\n'  # rcon response header
    _badrcon_replies = [
        'Bad rconpassword.',
        'Invalid password.',
        'print\nBad rcon_password.\n'
    ]
    # custom timeouts
    _long_commands_timeout = {'map': 5.0, 'fdir': 5.0, 'dir maps/': 5.0}

    def __init__(self, host, port, password=None):
        """
        :param host: The ip/domain where to send RCON commands
        :param port: The port where to send RCON commands
        :param password: The RCON password
        :raise RconError: If it's not possible to setup the RCON interface
        """
        self.host = host
        self.port = port
        self.password = password
        self.lock = thread.Lock()
        self.socket = socket.socket(type=socket.SOCK_DGRAM)
        self.socket.connect((self.host, self.port))
        self.test_password()

    def _get_host(self):
        return self._host

    def _set_host(self, value):
        try:
            self._host = value.strip()
        except AttributeError:
            raise RconError('expecting hostname')

    """:type : str"""
    host = property(_get_host, _set_host)

    def _get_password(self):
        return self._password

    def _set_password(self, value):
        if value is not None:
            self._password = value.strip()

    """:type : str"""
    password = property(_get_password, _set_password)

    def _get_port(self):
        return self._port

    def _set_port(self, value):
        try:
            self._port = int(value)
        except ValueError:
            raise RconError('bad rcon port supplied')

    """:type : int"""
    port = property(_get_port, _set_port)

    def __enter__(self):
        if self.test():
            return self

    def __exit__(self, type, value, traceback):
        try:
            self.socket.close()
        except (AttributeError, socket.error):
            pass
        finally:
            return traceback or True

    def test_password(self):
        """
        Test the RCON connection
        :raise RconError: When an invalid RCON password is supplied
        """
        response = self.send('status')
        if response in self._badrcon_replies:
            self._password = None
            raise RconError('bad rcon password supplied')
        return True

    def _recvall(self, timeout=0.5):
        """
        Receive the RCON command response
        :param timeout: The timeout between consequent data receive
        :return str: The RCON command response with header stripped out
        """
        response = ''
        self.socket.setblocking(False)
        start = time.time()
        while True:
            if response and time.time() - start > timeout:
                break
            elif time.time() - start > timeout * 2:
                break

            try:
                data = self.socket.recv(4096)[4:]
                if data:
                    response += data.decode('utf-8')
                    start = time.time()
                else:
                    time.sleep(0.1)
            except socket.error:
                pass

        return response

    def send(self, data):
        """
        Send a command over the socket. If password is set use rcon
        :param data: The command to send
        :raise RconError: When it's not possible to evaluate the command
        :return str: The server response to the RCON command
        """
        try:
            if not data:
                raise RconError('no command supplied')
            with self.lock:
                if self.password != '':
                    data = self._rconsendstring.format(self.password, data)
            self.socket.send(self._rconsendheader + bytes(data, 'utf-8'))
        except socket.error as e:
            raise RconError(e.message, e)
        else:
            timeout = self._timeout
            command = data.split(' ')[0]
            if command in self._long_commands_timeout:
                timeout = self._long_commands_timeout[command]
            return self._recvall(timeout=timeout)

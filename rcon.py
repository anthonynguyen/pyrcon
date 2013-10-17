# Multipurpose RCON library in Python
# by Anthony Nguyen
# MIT Licensed, see LICENSE

import socket

# Base class for an RCON "connection", even though RCON is technically connectionless (UDP)
# Initialization takes an address, port, and password
class RConnection():
	def __init__(self, host, port, password):
		self.host = host
		try:
			self.port = int(port)
		except ValueError:
			self.port = 27960
		self.password = password

		self.connect()

	def connect(self):
		"""Connect function that sets up the socket
		Meant for internal use"""
		self.close()

		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.socket.connect((self.host, self.port))
		self.socket.settimeout(2.0)

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
		try:
			self.socket.send(b"test")
			self.socket.recv(65535)
			return True
		except:
			return False

	def send(self, data):
		try:
			self.socket.send(b"\xFF\xFF\xFF\xFF" + "rcon {} {}".format(self.password, data).encode())
			r = self.socket.recv(4096)
			return r[4:].decode()
		except:
			return False
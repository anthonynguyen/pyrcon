import unittest
import pyrcon


host = 'localhost'
port = 27911
password = 'mypass'

# py.test test.py --cov-report xml:cov.xml --cov pyrcon


class RconTestCase(unittest.TestCase):
    def setUp(self):
        self.conn = pyrcon.RConnection(host, port)

    def test__get_host(self):
        self.assertEqual(self.conn._get_host(), host)

    def test__get_port(self):
        self.assertEqual(self.conn._get_port(), port)

    def test__get_password(self):
        self.assertEqual(self.conn._get_port(), port)

    def test_connect_no_password(self):
        self.assertEqual(self.conn.send('status')[0:6], 'print\n')

    def test_connect_with_rcon(self):
        self.conn.password = password
        self.assertEqual(self.conn.send('echo hi'), 'print\nhi\n')

    def test_connect_with_invalid_rcon(self):
        message = 'allowed no command'
        self.conn.password = password
        with self.assertRaises(pyrcon.rcon.RconError, msg=message):
            self.conn.send(None)

    def test_bad_password(self):
        message = 'bad password not caught'
        with self.assertRaises(pyrcon.rcon.RconError, msg=message):
            self.conn = pyrcon.RConnection(host, port, 'bad')

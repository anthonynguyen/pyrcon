import unittest
import pyrcon


TESTHOST = 'localhost'
TESTPORT = 27911
TESTPASS = 'mypass'

# py.test tests --cov-report xml:cov.xml --cov pyrcon


class Q2RconTestCase(unittest.TestCase):
    def setUp(self):
        self.conn = pyrcon.Q2RConnection(TESTHOST, TESTPORT, TESTPASS)
        pass

    def test_get_status(self):
        self.conn.get_status()
        self.assertNotEqual(self.conn.current_map, '', 'unable to get map')

    def test_get_list_maps(self):
        self.conn.get_map_list()
        self.assertTrue(len(self.conn.maplist) > 0, 'no maps found')

    def test_change_invalid_map(self):
        with self.assertRaises(BaseException, msg='invalid map not caught'):
            self.conn.change_map('invalid')

    def test_get_serverinfo(self):
        self.assertTrue(self.conn.get_serverinfo())

    def test_send(self):
        self.assertEqual(self.conn.send('echo hi'), 'hi\n')

    def test_badcommand(self):
        print(self.conn.send('badcommand'))

    def test_current_map(self):
        self.conn.get_status()
        self.assertNotEqual(self.conn.current_map, '')

    def test__parse_serverinfo(self):
        self.assertIs(
            type(self.conn._parse_serverinfo(TEST_SERVER_INFO)), dict
        )


TEST_SERVER_INFO = """Server info settings:
Q2Admin             1.17.52
mapname             dday1
bots                1
dll_version         Dday 5.065b
gamedate            Jan  7 2012
gamename            dday
class_limits        1
death_msg           3
team_kill           1
level_wait          10
RI                  6
website             https://ddaydev.com
maxclients          64
cheats              0
timelimit           0
fraglimit           0
dmflags             16
deathmatch          1
version             R1Q2 b7904 x86-64 Feb 23 2010 Linux
hostname            D-Day ddaydev.com
gamedir             dday
game                dday"""  # noqa: E501

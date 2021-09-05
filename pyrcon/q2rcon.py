""" Quake2 specific RCON library using pyrcon
by texnofobix
MIT license
"""
from pyrcon import RConnection, RconError

REPORT_LINE = '--- ----- ---- --------------- ------- '
REPORT_LINE += '--------------------- -------- ---'


class Q2Exception(RconError):
    """ Class exceptions """


class Q2RConnection(RConnection):
    """ Class to allow connections to Quake 2 Servers """

    def __init__(self, host=None, port=27910, password=None):
        super().__init__(host, port, password)
        self.maplist = []
        self.current_map = ""
        self.players = []
        self.serverinfo = {}

    def send(self, data):
        """
        Send a RCON command over the socket
        :param data: The command to send
        :raise Q2Exception: When it's not possible to evaluate the command
        :return str: The server response to the RCON command
        """
        response = super().send(data)

        if response[0:5] != 'print':
            return Q2Exception('no response from server!')

        return response[6:]

    def get_status(self):
        """
        Send a RCON command over the socket
        :raise Q2Exception: When it's not possible to evaluate the command
        :return str: The server response to the RCON command
        """
        playerinfo = False
        output = self.send('status')
        self.current_map = ''
        self.players = []

        lines = output.splitlines()
        for line in lines:
            #print("line",line)
            if playerinfo and line[0:3].strip(' ') != '':
                self.players.append(
                        {
                            line[0:3].strip():
                            {
                                'score': int(line[5:9]),
                                'ping': line[10:14].strip(),
                                'name': line[15:29].strip(),
                                'lastmsg': int(line[31:38]),
                                'ip_address': line[39:59].strip(),
                                'rate_pps': line[60:69].strip(),
                                'ver': int(line[70:73]),
                            }
                        }
                )

            if line[0:3] == 'map' and self.current_map == '':
                self.current_map = line.split(': ')[1]

            if line == REPORT_LINE:
                playerinfo = True

    def get_map_list(self):
        """
        Get all maps
        :return list: Get all maps
        """
        output = self.send('dir maps/')
        lines = output.splitlines()
        self.maplist = []

        for line in lines:
            sline = line.strip()

            if not (sline == '----' or sline[0:13] == 'Directory of '):
                self.maplist.append(line.split(".")[0])

        self.maplist = list(set(self.maplist))
        self.maplist.sort()
        return self.maplist

    def change_map(self, map_name):
        """
        Request map change by name
        :raise Q2Exception: When it's not possible to evaluate the command
        """
        self.send('map ' + map_name)
        self.get_status()
        if self.current_map != map_name:
            raise Q2Exception('map failed to change')

    def get_serverinfo(self):
        """
        Retrieve serverinfo and parse
        :return dict: serverinfo
        """
        return self._parse_serverinfo(self.send('serverinfo'))

    def _parse_serverinfo(self, data):
        """
        Parse serverinfo response
        :param data: The command to send
        """
        for line in data.splitlines():
            if line[0:21] != 'Server info settings:':
                line = list(filter(lambda x: x != '', line.split(' ')))
                self.serverinfo[line[0]] = line[1]
        return self.serverinfo

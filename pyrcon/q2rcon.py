# Quake2 specific RCON library using pyrcon
# by texnofobix
# MIT license

from pyrcon import RConnection


class Player(object):

    def __init__(self, num, score, ping, name, lastmsg, ip_address, rate_pps, ver):
        self.num = num
        self.score = score
        self.ping = ping
        self.name = name.strip()
        self.lastmsg = lastmsg
        self.ip_address = ip_address
        self.rate_pps = rate_pps
        self.ver = ver
    
    def __repr__(self):
        return str(self.num)+" "+self.name


class Q2RConnection(RConnection):

    def __init__(self, host=None, port=27910, password=None):
        super(Q2RConnection, self).__init__(host, port, password)
        self._maplist = self.maplist()

    def status(self):
        q2map = ''
        status = False
        playerinfo = False
        output = self.send('status')
        players = []
        
        lines = output.splitlines()
        for line in lines:
            if playerinfo and line[0:3].strip(' ') != '':
                players.append(Player(num=line[0:3], score=line[5:9], ping=line[10:14],
                               name=line[15:29], lastmsg=line[31:38], ip_address=line[39:59],
                               rate_pps=line[60:69], ver=line[70:73], ))

            if status and q2map == '':
                q2map = line.split(': ')[1]
                print q2map

            if line == """--- ----- ---- --------------- ------- --------------------- -------- ---""":
                print 'playerinfo start'
                playerinfo = True
                print line[0:2]

            print '>', line
            if line.find('print') >= 0:
                print 'beginning of status'
                status = True
            
        print 'end of status'
        print players

    def maplist(self):
        output = self.send('dir maps/')
        lines = output.splitlines()
        maplist = []

        for line in lines:
            sline = line.strip()
            if not sline:
                break  # seems to duplicate from q2
            if sline != '----' or sline != 'Directory of ' or sline != 'print':
                maplist.append(line.split('.')[0])

        maplist.sort()
        return maplist

    def changemap(self, mapname):
        if mapname in self._maplist:
            print 'yes'
            output = self.send('map ' + mapname)
            print output
            for line in output:
                if line.find('server map: ') >= 0:
                    if line.split(':')[1] != mapname:
                        print "didn't change correctly to " + mapname
        else:
            print 'no'

# Quake2 specific RCON library using pyrcon
# by texnofobix
# MIT license

from pyrcon import RConnection


class q2RConnection(RConnection):
    current_map = ''
    Players = []


    def __init__(self, host=None, port=27910, password=None):
        super(q2RConnection, self).__init__(host, port, password)
        self._maplist = self.maplist()
        self.servervariables()

    def status(self):
        status = False
        playerinfo = False
        output = self.send('status')
        self.current_map = ''
        #print(output)
        #import pdb; pdb.set_trace()    
        self.Players = []
        
        lines =  output.splitlines()
        for line in lines:
            #print("line",line)
            if playerinfo and line[0:3].strip(' ') != '':
                self.Players.append(
                        {
                            line[0:3].strip():
                            {
                                'score':int(line[5:9]),
                                'ping':line[10:14].strip(),
                                'name':line[15:29].strip(),
                                'lastmsg':int(line[31:38]),
                                'ip_address':line[39:59].strip(),
                                'rate_pps':line[60:69].strip(),
                                'ver':int(line[70:73]),
                            }
                        }
                )

            if status and self.current_map == '':
                self.current_map = line.split(': ')[1]

            if line == """--- ----- ---- --------------- ------- --------------------- -------- ---""":
                playerinfo = True

            if line.find('print') >= 0:
                status = True


    def maplist(self):
        output = self.send('dir maps/')
        lines =  output.splitlines()
        maplist = []

        for line in lines:
            sline = line.strip()
            if not sline:
                break # seems to duplicate from q2 
            if sline != '----' or sline != 'Directory of ' or sline != 'print':
                maplist.append(line.split(".")[0])

        maplist.sort()
        return maplist

    def changemap(self, mapname):
        if mapname in self._maplist:
            output = self.send('map ' + mapname)
            for line in output:
                if line.find('server map: ') >= 0:
                    if line.split(':')[1] != mapname:
                        print("didn't change correctly to " + mapname)
            self.current_map = mapname
        else:
            return 'no'

    def servervariables(self):
        self.hostname = self.send('hostname').split('" is "')[1][:-2]
        self.version = self.send('version').split('" is "')[1][:-2]
        self.sv_gravity = self.send('sv_gravity').split('" is "')[1][:-2]


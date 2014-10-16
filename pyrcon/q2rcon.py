# Quake2 specific RCON library using pyrcon
# by texnofobix
# MIT license

from pyrcon import RConnection


class q2RConnection(RConnection):
    current_map = ""
    Players = []


    def __init__(self, host=None, port=27910, password=None):
        RConnection.__init__(self, host, port, password)
        self._maplist = self.maplist()

    def status(self):
        status = False
        playerinfo = False
        output = self.send("status")
        self.Players = []
        
        lines =  output.splitlines()
        for line in lines:
            if playerinfo and line[0:3].strip(" ")<>"":
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

            if status and self.current_map == "":
                self.current_map = line.split(": ")[1]
                #print q2map

            if line == '''--- ----- ---- --------------- ------- --------------------- -------- ---''':
                #print "playerinfo start"
                playerinfo = True
                #print line[0:2]

            #print ">",line
            if line.find("print") >= 0:
                #print "beginning of status"
                status = True
            
        #print "end of status"
        #print Players

    def maplist(self):
        output = self.send("dir maps/")

        lines =  output.splitlines()
        maplist = []

        for line in lines:
            sline = line.strip()
            if sline == "":
                break #seems to duplicate from q2 
            if sline <> "----" or sline <> 'Directory of ' or sline <> 'print':
                maplist.append(line.split(".")[0])

        maplist.sort()
        return maplist

    def changemap(self, mapname):
        if mapname in self._maplist:
            #print "yes"
            output = self.send("map " + mapname)
            #print output
            for line in output:
                if line.find("server map: ") >= 0:
                    if line.split(":")[1] <> mapname:
                        print "didn't change correctly to " + mapname
            self.current_map = mapname
        else:
            return "no"

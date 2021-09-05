"""
Copyright 2015 - texnofobix
"""


import configparser
config = configparser.ConfigParser()
configFilePath = r'q2webapi.conf'
config.read(configFilePath)


# set configuration here
webhost = str(config.get('web', 'host'))
webport = int(config.get('web', 'port'))
q2host = str(config.get('q2', 'host'))
q2port = int(config.get('q2', 'port'))
q2password = str(config.get('q2', 'password'))

import pyrcon
import json
import bottle

app = bottle.Bottle()


class EnableCors(object):
    name = 'enable_cors'
    api = 2

    def apply(self, fn, context):
        def _enable_cors(*args, **kwargs):
            # set CORS headers
            bottle.response.headers['Access-Control-Allow-Origin'] = '*'
            bottle.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
            bottle.response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token,rcon-password'

            if bottle.request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)

        return _enable_cors


@app.route('/')
def index():
        return '''
    <h1>q2webapi</h1>
    <pre>
    <a href="/v1/players">/v1/players</a> - Gets all the players on the server.
    /v1/players/<num> - Gets a specific player info

    <a href="/v1/maps">/v1/maps</a> - Gets all the maps on the server
    <a href="/v1/maps/current">/v1/maps/current</a> - Gets the current map
    /v1/maps/<mapname> [get to test if valid / post to change with rcon-password in header]
    </pre>
    '''


@app.get('/v1/status')
def status():
    conn.status()
    bottle.response.content_type = 'application/json'
    output = {'currentMap': conn.current_map, 'connectedPlayers': len(conn.Players)}
    return json.dumps(output)

@app.route('/v1/players', method=['OPTIONS', 'GET'])
def players():
    conn.status()
    if bottle.request.headers.get('rcon-password') == q2password:
        # print conn.Players
        Players = conn.Players
    else:
        playerCnt = 0
        Players = []

        for player in conn.Players:
            print((list(player.keys())))
            Players.append({str(list(player.keys())):
                            {'name': player[str(playerCnt)]['name']}})

    bottle.response.content_type = 'application/json'
    players = {"players": Players}
    return json.dumps(players, separators=(',', ': '))


@app.route('/v1/players/<num:int>', method=['OPTIONS', 'GET'])
def player(num):
    if bottle.request.headers.get('rcon-password') == q2password:
        bottle.response.content_type = 'application/json'
        conn.status()
        if num <= len(conn.Players) - 1:
            return json.dumps({"players": conn.Players[num]})
        return json.dumps({"players": None})
    return bottle.abort(401, "Sorry, access denied. Missing required rcon-password header with valid password.")


@app.delete('/v1/players/<num:int>')
def kickPlayer(num):
    bottle.response.content_type = 'application/json'
    if bottle.request.headers.get('rcon-password') == q2password:
        return '{"kickPlayerNum": "' + str(num) + \
            '","message": "' + str(conn.send("kick " + str(num))) + '"}'
    return bottle.abort(401, "Sorry, access denied. Missing required rcon-password header with valid password.")


@app.get('/v1/maps')
def allmaps():
    bottle.response.content_type = 'application/json'
    return json.dumps({"maps": conn.maplist()})


@app.get('/v1/maps/current')
def map_current():
    conn.status()
    bottle.response.content_type = 'application/json'
    return json.dumps({"maps": conn.current_map})


@app.get('/v1/maps/<mapname:re:[a-z0-9]+>')
def testmap(mapname):
    if mapname in conn.maplist():
        setreturn = True
    else:
        setreturn = False
    bottle.response.content_type = 'application/json'

    return '{"mapname": "' + str(mapname) + \
        '", "mapExists": "' + str(setreturn).lower() + '"}'


@app.post('/v1/maps/<mapname:re:[a-z0-9]+>')
def changemap(mapname):
    bottle.response.content_type = 'application/json'
    if bottle.request.headers.get('rcon-password') == q2password:
        return '{"requestedMap": "' + str(mapname) + \
            '","changedMap": ' + str(conn.changemap(mapname)).lower() + '}'
    return bottle.abort(401, "Sorry, access denied. Missing required rcon-password header with valid password.")


@app.route('/v1/rawcommand',method=['OPTIONS', 'POST'])
def rawCommand():
    bottle.response.content_type = 'application/json'
    if bottle.request.headers.get('rcon-password') == q2password:
        command = str(bottle.request.forms.get('command')).strip()
        print(command)
        return json.dumps({"command": command, "status": conn.send(command)})
    return bottle.abort(401, "Sorry, access denied. Missing required rcon-password header with valid password.")

app.install(EnableCors())
app.config['autojson'] = True

conn = pyrcon.q2RConnection(host=q2host, port=q2port, password=q2password)
app.run(host=webhost, port=webport, reloader=True, debug=True)

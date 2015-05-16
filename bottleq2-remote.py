"""
Copyright 2015 - texnofobix
"""

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
    conn = pyrcon.q2RConnection(host=bottle.request.query.q2host, port=bottle.request.query.q2port, password=bottle.request.headers.get('rcon-password'))
    conn.status()
    bottle.response.content_type = 'application/json'
    output = {'currentMap': conn.current_map, 'connectedPlayers': len(conn.Players)}
    return json.dumps(output)

@app.route('/v1/players', method=['OPTIONS', 'GET'])
def players():
    conn = pyrcon.q2RConnection(host=bottle.request.query.q2host, port=bottle.request.query.q2port, password=bottle.request.headers.get('rcon-password'))
    conn.status()
    Players = conn.Players
    bottle.response.content_type = 'application/json'
    print Players
    players = {"players": Players}
    return json.dumps(players, separators=(',', ': '))

@app.route('/v1/players/<num:int>', method=['OPTIONS', 'GET'])
def player(num):
    conn = pyrcon.q2RConnection(host=bottle.request.query.q2host, port=bottle.request.query.q2port, password=bottle.request.headers.get('rcon-password'))
    conn.status()
    bottle.response.content_type = 'application/json'
    conn.status()
    if num <= len(conn.Players) - 1:
        return json.dumps({"players": conn.Players[num]})
    return json.dumps({"players": None})

@app.delete('/v1/players/<num:int>')
def kickPlayer(num):
    conn = pyrcon.q2RConnection(host=bottle.request.query.q2host, port=bottle.request.query.q2port, password=bottle.request.headers.get('rcon-password'))
    bottle.response.content_type = 'application/json'
    return '{"kickPlayerNum": "' + str(num) + \
             '","message": "' + str(conn.send("kick " + str(num))) + '"}'

@app.get('/v1/maps')
def allmaps():
    conn = pyrcon.q2RConnection(host=bottle.request.query.q2host, port=bottle.request.query.q2port, password=bottle.request.headers.get('rcon-password'))
    bottle.response.content_type = 'application/json'
    return json.dumps({"maps": conn.maplist()})


#@app.get('/v1/maps/current')
def map_current():
    conn = pyrcon.q2RConnection(host=bottle.request.query.q2host, port=bottle.request.query.q2port, password=bottle.request.headers.get('rcon-password'))
    conn.status()
    bottle.response.content_type = 'application/json'
    return json.dumps({"maps": conn.current_map})


@app.get('/v1/maps/<mapname:re:[a-z0-9]+>')
def testmap(mapname):
    conn = pyrcon.q2RConnection(host=bottle.request.query.q2host, port=bottle.request.query.q2port, password=bottle.request.headers.get('rcon-password'))
    conn.status()
    if mapname in conn.maplist():
        setreturn = True
    else:
        setreturn = False
    bottle.response.content_type = 'application/json'

    return '{"mapname": "' + str(mapname) + \
        '", "mapExists": "' + str(setreturn).lower() + '"}'


@app.post('/v1/maps/<mapname:re:[a-z0-9]+>')
def changemap(mapname):
    conn = pyrcon.q2RConnection(host=bottle.request.query.q2host, port=bottle.request.query.q2port, password=bottle.request.headers.get('rcon-password'))
    bottle.response.content_type = 'application/json'
    return '{"requestedMap": "' + str(mapname) + \
            '","changedMap": ' + str(conn.changemap(mapname)).lower() + '}'


@app.route('/v1/rawcommand',method=['OPTIONS', 'POST'])
def rawCommand():
    conn = pyrcon.q2RConnection(host=bottle.request.query.q2host, port=bottle.request.query.q2port, password=bottle.request.headers.get('rcon-password'))
    bottle.response.content_type = 'application/json'
    command = str(bottle.request.forms.get('command')).strip()
    print command
    return json.dumps({"command": command, "status": conn.send(command)})

app.install(EnableCors())
app.config['autojson'] = True

app.run(host="127.0.0.1", port=8080, reloader=True, debug=True)

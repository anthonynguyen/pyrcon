pyrcon
======

A stupidly simple RCON library

About
-----

Yeah, just use it.

Tested on the following engines:
 * quake2.

Installation
------------

``python setup.py install``

Usage
-----
Generic

.. code:: python

    import pyrcon
    conn = pyrcon.RConnection("example.com", 123, "password")
    conn.send("command")

Quake2

.. code:: python

    import pyrcon
    conn = pyrcon.q2RConnection("example.com", 27910, "password")
    conn.status()

To use the webapi for q2:

    Local
    
    1. Install bottle
    2. Create/update a file called q2webapi.conf

    .. code:: python
        
        [web]
        host = 0.0.0.0
        port = 80
        
        [q2]
        host = 127.0.0.1
        port = 27910
        password = rconpassword

    3. Run python bottleq2-local.py
    
    
    Remote
    1. Install bottle
    2. Run python bottleq2-remote.py

License
-------
MIT licensed. See LICENSE.

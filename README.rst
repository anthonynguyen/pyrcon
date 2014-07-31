pyrcon
======

A stupidly simple RCON library

About
-----

Yeah, just use it.

Installation
------------

``python setup.py install``

Usage
-----

    import pyrcon
    conn = pyrcon.RConnection("example.com", 123, "password")
    conn.send("command")


License
-------
MIT licensed. See LICENSE.

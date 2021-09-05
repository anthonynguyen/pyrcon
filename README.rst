pyrcon
======

A stupidly simple RCON library

About
-----

Yeah, just use it.

Tested on the following engines:
 * Quake 2.

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
    conn = pyrcon.Q2RConnection("example.com", 27910, "password")
    conn.get_status()
    print(conn.current_map)
    
See code / tests for examples



License
-------
MIT licensed. See LICENSE.

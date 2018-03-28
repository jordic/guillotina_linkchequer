Guillotina LinkChecker
==================================

Toy app for learn and try guillotina async server.



Dependencies
------------

Python >= 3.6


Installation
------------

This example will use virtualenv::

  virtualenv .
  ./bin/python setup.py develop


Running
-------

Most simple way to get running::

  ./bin/guillotina


Running Postgresql Server:

    docker run --rm -e POSTGRES_DB=guillotina -e POSTGRES_USER=guillotina -p 127.0.0.1:5432:5432 --name postgres postgres:9.6

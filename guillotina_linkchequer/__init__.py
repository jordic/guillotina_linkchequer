from guillotina import configure
from datetime import timedelta
import logging
import sys

app_settings = {
    # provide custom application settings here...
    'default_schedule': timedelta(0, 300, 0)
}


def includeme(root):
    """
    custom application initialization here
    """
    configure.scan('guillotina_linkchequer.content')
    configure.scan('guillotina_linkchequer.api')
    configure.scan('guillotina_linkchequer.install')
    configure.scan('guillotina_linkchequer.utility')
    configure.scan('guillotina_linkchequer.subscribers')

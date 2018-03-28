from guillotina import configure
from datetime import timedelta
import logging
import sys

app_settings = {
    # provide custom application settings here...
    'default_schedule': timedelta(0, 300, 0)
}


root = logging.getLogger()
root.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)


def includeme(root):
    """
    custom application initialization here
    """
    configure.scan('guillotina_linkchequer.content')
    configure.scan('guillotina_linkchequer.api')
    configure.scan('guillotina_linkchequer.install')
    configure.scan('guillotina_linkchequer.utility')
    configure.scan('guillotina_linkchequer.subscribers')

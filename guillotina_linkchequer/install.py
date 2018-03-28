# -*- coding: utf-8 -*-
from guillotina import configure
from guillotina.addons import Addon




@configure.addon(
    name="guillotina_linkchequer",
    title="Guillotina app to check links")
class ManageAddon(Addon):

    @classmethod
    def install(cls, container, request):
        pass
        #registry = request.container_settings  # noqa
        # install logic here...

    @classmethod
    def uninstall(cls, container, request):
        pass
        #registry = request.container_settings  # noqa
        # uninstall logic here...

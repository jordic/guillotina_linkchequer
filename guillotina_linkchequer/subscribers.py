

from guillotina import configure
from guillotina.component import getUtility
from guillotina.interfaces import IObjectAddedEvent
from guillotina.interfaces import IObjectRemovedEvent
from guillotina.interfaces import IObjectModifiedEvent
from guillotina_linkchequer.content import ILink
from guillotina_linkchequer.interfaces import ILinkChecker


@configure.subscriber(for_=(ILink, IObjectAddedEvent))
async def link_added(link, event):
    util = getUtility(ILinkChecker)
    await util.add(link)


@configure.subscriber(for_=(ILink, IObjectModifiedEvent))
async def link_modified(link, event):
    util = getUtility(ILinkChecker)
    await util.add(link)


@configure.subscriber(for_=(ILink, IObjectRemovedEvent))
async def link_modified(link, event):
    util = getUtility(ILinkChecker)
    await util.remove(link)



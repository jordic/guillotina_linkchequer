

import aiohttp
import time
import logging

from datetime import timedelta
from datetime import datetime
from dateutil.tz import tzutc

from guillotina import configure
from guillotina import content
from guillotina import Interface
from guillotina import schema
from guillotina import app_settings
from guillotina.component import get_utility

from guillotina_linkchequer.interfaces import ILinkChecker

_zone = tzutc()

logger = logging.getLogger('linkchequer')


class ILink(Interface):
    url = schema.URI(required=True)
    last_checked = schema.Datetime()
    every = schema.Int() # seconds
    status = schema.Int()
    response_time = schema.Int()


@configure.contenttype(
    type_name='Link',
    schema=ILink,
    behaviors=[
        'guillotina.behaviors.dublincore.IDublinCore',
    ]
)
class Link(content.Item):

    async def interval(self):
        if self.every:
            return timedelta(0, self.every, 0)
        return app_settings['default_schedule']

    async def next_tick(self):
        inter = await self.interval()
        if not self.last_checked:
            return 1
        if datetime.now(tz=_zone) > (self.last_checked + inter):
            return 1
        return (
            (self.last_checked + inter) - datetime.now(tz=_zone)
        ).total_seconds()


async def check_item(link):
    t = time.time()
    async with aiohttp.ClientSession() as session:
        resp = await session.get(link.url)
        _ = await resp.read()
        ttotal = round((time.time() - t)*1000)

    logger.info(f'{link.url} status {resp.status} request_time {ttotal}')
    link.last_checked = datetime.now(tz=_zone)
    link.response_time = ttotal
    link.status = resp.status
    link._p_register()
    await link.__parent__._get_transaction().commit()
    util = get_utility(ILinkChecker)
    await util.add(link)


class ILinkFolder(Interface):
    pass


@configure.contenttype(
    type_name="Link Folder",
    schema=ILinkFolder,
    allowed_types=['Link'],
    behaviors=["guillotina.behaviors.dublincore.IDublinCore"]
)
class LinkFolder(content.Folder):
    pass
